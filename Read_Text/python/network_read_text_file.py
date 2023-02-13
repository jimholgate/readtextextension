#!/usr/bin/env python3
# -*- coding: UTF-8-*-
'''
This text explains how to use a web service and media player to read a text
file. It outlines the terms and conditions associated with using the on-line
service, as well as the potential privacy and security risks. It introduces
text-to-speech tools, Larynx, Rhvoice and MaryTTS, and how to use them. It
mentions the need to check if the network is available and to set permissions
when using these tools. Lastly, it provides advice on how to update local
libraries and packages when using these tools.

-----

This python tool reads a text file using an web service and a media player.
Online services require a network connection and installation of an online
connection library.

Check the terms and conditions that apply to the on-line service provider.
There may be acceptable use policies, limits or costs.

* Variants like speech rate, pitch, voice and gender might
  not apply to all services or to all languages.
* Online services could be terminated without warning.
* Your content might not be private or secure.
* Your organization or local laws might restrict use of online
  data services. For example, they might restrict services
  provided outside of your country's jurisdiction.
* An online provider could block your access because your use
  is excessive or otherwise violates their terms of service.
* If you run the application in a prsotected container like a flatpak
  or snap, some functions might not work because the application
  does not have permission to execute them.
* On some systems, you might need to install additional software
  like `curl` and `ffmpeg` to ensure that libraries are available to
  download and process files.

Larynx
------

You can configure Read Text Extension to use Larynx. Larynx
works with most Linux distributions, even if provides your
office application using a container distribution platform
like `flatpak` or `snap`.

Using Larynx does not require an on-line connection. The
`larynx-server` application provides speech on a `localhost`
web service similarly to how [`cups`](https://www.cups.org/)
provides printing services using a `localhost` server on many
Posix computers like MacOS and desktop Linux distributions.

> Offline end-to-end text to speech system using gruut and
> onnx (architecture). There are 50 voices available across
> 9 languages.

-- [Rhasspy Larynx
Website](https://github.com/rhasspy/larynx)

<https://hub.docker.com/r/rhasspy/larynx>

+ Is the larynx server running? Consider setting up `larynx-server`
  to automatically start up when you log in.
+ Is the language of the selected text supported and installed?

If you are using a Docker network service, it might take a little
more time to than usual to start up when the package updates
it's files. If you are using a system docker application with a
personal account, then you might need to manually download updated
speech resources if the docker application stops working with
locally installed languages. A system administrator can change your
account's ability to access a docker service or for the docker
package to access locally installed resources.

Rhvoice
-------

[Rhvoice-rest](https://hub.docker.com/r/aculeasis/rhvoice-rest) is
a docker image container that can read English, Esperanto, Georgian,
Kyrgyz, Macedonian, Portuguese, Russian, Tatar and Ukrainian.

MaryTTS
-------

[MaryTTS](http://mary.dfki.de/) (Modular Architecture for Research in Synthesis)
is an open-source, multilingual Text-to-Speech Synthesis platform written in Java.
It can turn text into speech in many different languages. It runs on a `localhost`
web resource on your computer using a Docker container. Using MaryTTS does not
require an on-line connection.

You can make it sound like you by recording your voice and using MaryTTS [Import
Tools](https://github.com/marytts/marytts-wiki/blob/master/VoiceImportToolsTutorial.md)
to create a personalized voice.

The Rhsspy MaryTTS docker image is an easy-to install web application that
includes voices in several languages by default, including,

* English
* French
* German
* Italian
* Swedish
* Russian
* Telugu
* Turkish

See also:

[Adding-voices](https://rhasspy.readthedocs.io/en/v2.4.20/text-to-speech/#adding-voices)

[Docker image](https://hub.docker.com/r/synesthesiam/marytts)

[Rhasspy community](https://community.rhasspy.org/)

It doesn't work?
----------------

The first step is to check if the network is available. The
network service might offer an account status report page or
a help document to assist you.

The tool relies on external libraries or packages, and python
might not have access to the current required packages.

Some ways of installing your office application restrict the
application's ability to run third party extensions. You or
your system administrator might need to set permissions for
this extension to run or for the extension to access a
network resource.

Some of the network tools require specific versions of python
or a specific system platform like `amd64`, `arm64` or `v7`.
This script might not work with those tools because it can't use
the required libraries on an unsupported version of python.

If you use python pip to install local libraries, you might have to
manually update them from time to time. Packages that are managed
by update utilities like `apt-get`, `yum` and `dnf` are upgraded
by the distribution.

If your docker image is not specifically supported here, check if
it has a `maryTTS` compatibility mode. The compatibility mode
allows the speech synthesis image to use the maryTTS address and 
port and the maryTTS Application Program Interface (API) to list
installed voices and to produce spoken audio files over a local
web service.
 
See also:
[Docker docs](https://docs.docker.com/desktop/install/linux-install/)
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import getopt
import math
import os
import platform
import sys
import tempfile
import time
import readtexttools
try:
    import urllib
    import json
except ImportError:
    pass
try:
    import requests
    REQUESTS_OK = True
except:
    REQUESTS_OK = False
try:
    import gtts
except ImportError:
    try:
        if len(readtexttools.find_local_pip('gtts')) != 0:
            sys.path.append(readtexttools.find_local_pip('gtts'))
            try:
                import gtts
            except:
                pass
    except:
        pass
try:
    import awsserver
except ImportError:
    pass
try:
    import azureserver
except ImportError:
    pass
try:
    import gcloudserver
except ImportError:
    pass
try:
    import watsonserver
except ImportError:
    pass

NET_SERVICE_LIST = [
    'AUTO', 'NETWORK', 'AWS', 'AZURE', 'GOOGLECLOUD', 'WATSON', 'GTTS',
    'LARYNX', 'MARYTTS', 'RHVOICE'
]


def usage():  # -> None
    '''
    Command line help
    '''

    print('''
Network Speech Synthesis
========================

Reads a text file using an on-line voice and a media player
like ffmpeg or avconv.

Usage
-----

    network_read_text_file.py --language=ca-ES --visible=False "input.txt"
    network_read_text_file.py --language=ca-ES --rate=70% "input.txt"

Relies on optional external libraries and an on-line connection. With long
strings, or using a slow network, the latency might be longer than two
seconds, or retrieving the online resource might fail.

Local Server
------------

The extension can use a local server that is compatible with the applcation
programming interface (API) of a `rhasspy/larynx` speech server daemon.

The default larnyx address is <http://0.0.0.0:5002>.

You can use a different local address and port in the command options:

    network_read_text_file.py --language=en-US --url="http://localhost:5002" "input.txt"

It is normal for `larynx` to take a moment to start speaking the first time
that you use it.

[About Larynx...](https://github.com/rhasspy/larynx)
''')


def network_problem(voice='default'):  # -> str
    '''Return suggestions to make an on-line voice work.'''
    return '''Is the network connected?
=========================

+ The `%(voice)s` on-line voice is currently unavailable.
+ It might help to restart your device, refresh the network
  or check your on-line account status.
+ If you are using a `localhost` server, it might help to
  enter the local speech server command in a terminal and
  read what it prints out. (i. e.: `larynx-server`)
  ''' % locals()


class LocalCommons(object):
    '''Shared items for local speech servers'''

    def __init__(self):  # -> None
        self.debug = [0, 1, 2, 3][0]

        self.default_lang = readtexttools.default_lang()
        self.default_extension = '.wav'
        self.help_icon = '/usr/share/icons/HighContrast/32x32/apps/web-browser.png'
        self.spd_fm = [
            'female1', 'female2', 'female3', 'female4', 'female5', 'female6',
            'female7', 'female8', 'female9', 'child_female', 'child_female1'
        ]
        self.spd_m = [
            'male1', 'male2', 'male3', 'male4', 'male5', 'male6', 'male7',
            'male8', 'male9', 'child_male', 'child_male1'
        ]
        self.pause_list = [
            '(', '\n', '\r', u"\u2026", u'\u201C', u"\u2014", u"\u2013",
            u'\u00A0'
        ]
        try:
            self.add_pause = str.maketrans({
                '\n': ';\n',
                '\r': ';\r',
                '(': ' ( ',
                u'\u201C': u'\u201C;',
                u'\u2026': u'\u2026;',
                u'\u2014': u'\u2014;',
                u'\u2013': u'\u2013;',
                u'\u00A0': ' '
            })
        except AttributeError:
            self.add_pause = None
        try:
            self.base_curl = str.maketrans({
                '\\': ' ',
                '"': '\\"',
                '''
''': '''\
''',
                '\r': ' '
            })
        except AttributeError:
            self.base_curl = None
        self.is_x86_64 = sys.maxsize > 2**32

    def big_play_list(self, _text=''):  # -> list[str] | None
        '''Split a long string of plain text into a list'''
        if len(_text.strip()) == 0:
            return None
        elif _text.lower().count('<speak') != 0:
            _text = readtexttools.strip_xml(_text)
        return _text.splitlines()

    def do_net_sound(self,
                     _info='',
                     _media_work='',
                     _icon='',
                     _media_out='',
                     _audible='true',
                     _visible='false',
                     _writer='',
                     _size='600x600',
                     _post_process=''):  # -> bool
        '''Play `_media_work` or export it to `_media_out` format.'''
        # use `getsize` to ensure that python waits for file to finish download
        if not os.path.isfile(_media_work):
            return False
        if os.path.getsize(_media_work) == 0:
            time.sleep(2)
        if os.path.isfile(_media_work) and _post_process in [
                'process_audio_media', 'process_wav_media'
        ]:
            if os.path.getsize(_media_work) == 0:
                print('Unable to write media work file.')
                return False
            # NOTE: Calling process must unlock_my_lock()
            readtexttools.unlock_my_lock()
            readtexttools.process_wav_media(_info, _media_work, _icon,
                                            _media_out, _audible, _visible,
                                            _writer, _size)
            return True
        return False

    def do_posix_os_download(
            self,
            _url='',
            _media_work='',
            _body_data='AUDIO=WAVE_FILE&OUTPUT_TYPE=AUDIO&INPUT_TYPE=TEXT&LOCALE=en-US&VOICE=cmu-rms-hsmm&INPUT_TEXT=',
            _text='Testing 123',
            _method='POST',
            _iso_lang='en-US',
            _ok_wait=4,
            _end_wait=30):  # -> bool
        '''Use `curl` or `wget` to download a file.'''
        for _item in [
                _url, _media_work, _body_data, _text, _method, _iso_lang
        ]:
            if len(_item) == 0:
                return False
        for _item in [_ok_wait, _end_wait, self.base_curl]:
            if bool(_item) == False:
                return False
        if os.path.isfile(_media_work):
            os.remove(_media_work)
        _text = readtexttools.strip_mojibake(_iso_lang[:2].lower(), _text)
        _text = str(_text.translate(self.base_curl))
        _text = urllib.parse.quote(_text)
        if _method in ['POST']:
            if readtexttools.have_posix_app('wget', False):
                _verbose = '-q'  # quiet
                if bool(self.debug):
                    _verbose = ''
                _command = '''wget --no-http-keep-alive %(_verbose)s --header='Content-Type: application/x-www-form-urlencoded' -O '%(_media_work)s' --method %(_method)s  --body-data '%(_body_data)s"%(_text)s"' %(_url)s''' % locals(
                )
            elif readtexttools.have_posix_app('curl', False):
                _verbose = '-s'  # silent
                if bool(self.debug):
                    _verbose = '-v'  # verbose
                _command = '''curl %(_verbose)s -o "%(_media_work)s" --max-time %(_end_wait)s --connect-timeout %(_ok_wait)s -X %(_method)s -d '%(_body_data)s %(_text)s' %(_url)s''' % locals(
                )
        elif _method in ['GET']:
            if readtexttools.have_posix_app('wget', False):
                _verbose = '-q'  # quiet
                if bool(self.debug):
                    _verbose = '-v'
                _command = '''wget --no-http-keep-alive %(_verbose)s -O '%(_media_work)s' '%(_url)s?%(_body_data)s"%(_text)s"' ''' % locals()
            elif readtexttools.have_posix_app('curl', False):
                _verbose = '-s'  # silent
                if bool(self.debug):
                    _verbose = '-v'
                _command = '''curl "%(_url)s?%(_body_data)s%(_text)s" %(_verbose)s -o "%(_media_work)s" --max-time %(_end_wait)s --connect-timeout %(_ok_wait)s ''' % locals(
                )
        else:  # Only allow GET and POST
            return False
        if bool(self.debug):
            print(_command)
        return os.system(_command) == 0


class AmazonClass(object):
    u''' The following notice should be displayed in a dialog when users click
    *About...* or the equivalent in their language when this class is enabled.

    Powered by Amazon\u2122 LLC

    "Amazon" is a trademark of Amazon LLC. '''

    # * <https://docs.aws.amazon.com/polly/latest/dg/examples-for-using-polly.html>
    def __init__(self):  # -> None
        '''Initialize data'''
        self.ok = True
        self.accept_voice = [
            '', 'all', 'auto', 'child_female', 'female1', 'female2', 'female3',
            'female4', 'female5', 'female6', 'child_male', 'male1', 'male2',
            'male3', 'male4', 'male5', 'male6', 'aws'
        ]

    def version(self):  # -> string
        '''Returns the version in the form `nn.nn.nn`.'''
        try:
            return awsserver.version()
        except (AttributeError, NameError):
            self.ok = False
        return ''

    def language_supported(self, iso_lang='ca-ES'):  # -> bool
        '''Is the language supported?'''
        try:
            self.ok = awsserver.language_supported(iso_lang)
        except (AttributeError, NameError):
            self.ok = False
        return self.ok

    def read(self,
             _text="",
             _iso_lang='en-US',
             _visible="false",
             _audible="true",
             _out_path="",
             _icon="",
             _info="",
             _post_process=None,
             _writer='',
             _size='600x600',
             _speech_rate=160):  # -> bool
        '''stub'''
        if not self.ok:
            return False
        try:
            return awsserver.read(_text="",
                                  _iso_lang='en-US',
                                  _visible="false",
                                  _audible="true",
                                  _out_path="",
                                  _icon="",
                                  _info="",
                                  _post_process=None,
                                  _writer='',
                                  _size='600x600',
                                  _speech_rate=160)
        except (AttributeError, NameError):
            pass
        return False


class AzureClass(object):
    u''' The following notice should be displayed in a dialog when users click
    *About...* or the equivalent in their language when this class is enabled.

    Powered by Microsoft\u2122

    "Microsoft" and "Azure" are trademarks of Microsoft.'''

    # * <https://azure.microsoft.com/en-us/services/cognitive-services/text-to-speech/>
    def __init__(self):  # -> None
        '''Initialize data'''
        self.ok = True
        self.accept_voice = [
            '', 'all', 'auto', 'child_female', 'female1', 'female2', 'female3',
            'child_male', 'male1', 'male2', 'male3', 'azure'
        ]

    def language_supported(self, iso_lang='ca-ES'):  # -> bool
        '''Is the language supported?'''
        try:
            self.ok = azureserver.language_supported(iso_lang)
        except (AttributeError, NameError):
            self.ok = False
        return self.ok

    def read(self,
             _text="",
             _iso_lang='en-US',
             _visible="false",
             _audible="true",
             _out_path="",
             _icon="",
             _info="",
             _post_process=None,
             _writer='',
             _size='600x600',
             _speech_rate=160):  # -> bool
        '''stub'''
        if not self.ok:
            return False
        try:
            return azureserver.read(_text="",
                                    _iso_lang='en-US',
                                    _visible="false",
                                    _audible="true",
                                    _out_path="",
                                    _icon="",
                                    _info="",
                                    _post_process=None,
                                    _writer='',
                                    _size='600x600',
                                    _speech_rate=160)
        except (AttributeError, NameError):
            pass
        return False


class GoogleCloudClass(object):
    u''' The following notice should be displayed in a dialog when users click
    *About...* or the equivalent in their language when this class is enabled.

    Powered by Google\u2122

    "Google" and "Google Cloud" are trademarks of Google Inc. '''

    # * <https://cloud.google.com/text-to-speech/docs/create-audio-text-command-line>
    # * <https://cloud.google.com/text-to-speech/>
    def __init__(self):  # -> None
        '''Initialize data'''
        self.ok = True
        self.accept_voice = [
            '', 'all', 'auto', 'child_female', 'female1', 'female2', 'female3',
            'child_male', 'male1', 'male2', 'male3', 'googlecloud'
        ]

    def language_supported(self, iso_lang='ca-ES'):  # -> bool
        '''Is the language supported?'''
        try:
            self.ok = gcloudserver.language_supported(iso_lang)
        except (AttributeError, NameError):
            self.ok = False
        return self.ok

    def read(self,
             _text="",
             _iso_lang='en-US',
             _visible="false",
             _audible="true",
             _out_path="",
             _icon="",
             _info="",
             _post_process=None,
             _writer='',
             _size='600x600',
             _speech_rate=160):  # -> bool
        '''stub'''
        if not self.ok:
            return False
        try:
            return gcloudserver.read(_text="",
                                     _iso_lang='en-US',
                                     _visible="false",
                                     _audible="true",
                                     _out_path="",
                                     _icon="",
                                     _info="",
                                     _post_process=None,
                                     _writer='',
                                     _size='600x600',
                                     _speech_rate=160)
        except (AttributeError, NameError):
            pass
        return False


class WatsonClass(object):
    u''' The following notice should be displayed in a dialog when users click
    *About...* or the equivalent in their language when this class is enabled.

    Powered by IBM\u2122

    "IBM" and "Ask Watson" are trademarks of International Business Machines
    Corporation ("IBM").'''

    # * <https://www.ibm.com/docs/en/watson-explorer/11.0.0?topic=modules-installing-watson-explorer-from-command-line>
    # * <https://www.ibm.com/docs/en/watson-explorer/11.0.0?topic=components-requirements>
    def __init__(self):  # -> None
        '''Initialize data'''
        self.ok = True
        self.accept_voice = [
            '', 'all', 'auto', 'child_female', 'female1', 'female2', 'female3',
            'child_male', 'male1', 'male2', 'male3', 'watson'
        ]

    def language_supported(self, iso_lang='ca-ES'):  # -> bool
        '''Is the language supported?'''
        try:
            self.ok = watsonserver.language_supported(iso_lang)
        except (AttributeError, NameError):
            self.ok = False
        return self.ok

    def read(self,
             _text="",
             _iso_lang='en-US',
             _visible="false",
             _audible="true",
             _out_path="",
             _icon="",
             _info="",
             _post_process=None,
             _writer='',
             _size='600x600',
             _speech_rate=160):  # -> bool
        '''stub'''
        if not self.ok:
            return False
        try:
            return watsonserver.read(_text="",
                                     _iso_lang='en-US',
                                     _visible="false",
                                     _audible="true",
                                     _out_path="",
                                     _icon="",
                                     _info="",
                                     _post_process=None,
                                     _writer='',
                                     _size='600x600',
                                     _speech_rate=160)
        except (AttributeError, NameError):
            pass
        return False


class GoogleTranslateClass(object):
    u''' The following notice should be displayed in a dialog when users click
    *About...* or the equivalent in their language when this class is enabled.

    Powered by Google\u2122

    "Google", "Google Cloud" and "Google Translate" are trademarks of Google Inc.

    The contents of this resource are not affiliated with, sponsored by, or endorsed
    by Google nor does the documention represent the views or opinions of Google or
    Google personnel.

    The creators of the `gTTS` python library are the originators of the library
    enabling the `GoogleTranslateClass` class.

    The `gTTS` library can only be enabled by electing to install it on a supported
    platform. Read the documentation for help installing `gTTS` or to get help with
    troubleshooting if `gTTS` does not work when using your Linux package manager.

        sudo apt -y install python3-gtts


    or

        pip3 install gTTS gTTS-token

    See:

    * <https://github.com/pndurette/gTTS>
    * <https://gtts.readthedocs.io/en/latest/>
    '''

    def __init__(self):  # -> None
        '''Initialize data'''
        self.ok = True
        self.accept_voice = [
            '', 'all', 'auto', 'child_female', 'female1', 'female2', 'female3',
            'child_male', 'male1', 'male2', 'male3', 'gtts'
        ]
        self.translator = 'Google'
        self.translator_domain = self.translator.lower()
        self.default_extension = '.mp3'

    def version(self):  # -> string
        '''Returns the version in the form `nn.nn.nn`.'''
        try:
            return gtts.version.__version__
        except (AttributeError, NameError):
            self.ok = False
            return ''

    def check_version(self, minimum_version=2.2):  # -> bool
        '''Check for minimum version.'''
        if os.name == 'nt':
            # The library is not available in the LibreOffice
            # and OpenOffice for Windows python environments.
            # winsound.PlaySound does not play mp3 content.
            self.ok = False
            return self.ok
        _test_version = self.version()
        try:
            self.ok = float('.'.join(
                _test_version.split('.')[:2])) >= minimum_version
        except (AttributeError, IndexError, ValueError):
            self.ok = False
        return self.ok

    def read(self,
             _text="",
             _iso_lang='en-US',
             _visible="false",
             _audible="true",
             _out_path="",
             _icon="",
             _info="",
             _post_process=None,
             _writer='',
             _size='600x600',
             _speech_rate=160):  # -> bool
        '''
Setup
-----

+ See: <https://gtts.readthedocs.io/en/latest/>
+ Package Manager: `sudo dnf install python3-pip` or `sudo apt install python3-pip`
+ Pip Installer: `pip3 install gTTS gTTS-token` (*Not* `sudo`!)

+ `_text` - Text to speak
+ `_iso_lang` - Supported letter language code - defaults to English
+ `_visible` - Use a graphic media player, or False for invisible player
+ `_out_path` - Name of desired output media file
+ `_audible` - If false, then don't play the sound file
+ `_icon` - a .png or .jpg file if required.
+ `_info` - Commentary or title for post processing
+ `_post_process` - Get information, play file, or convert a file
+ `_writer` - Artist or Author
+ `_size` - Dimensions to scale photo '600x600'
+ `_speech_rate` - Two speeds supported: 100% or above is Normal;
   Any value less is Slow.
    '''
        if len(_text) == 0:
            return False
        _tld = "com"
        _region = "US"
        _lang1 = 'en'
        _lang2 = "es"
        _slow = False
        _lang_check = True
        _lang = _iso_lang
        _error_icon = readtexttools.net_error_icon()
        _version = self.version()
        _env_lang = readtexttools.default_lang()
        _domain = self.translator_domain
        _provider = self.translator
        _provider_logo = '/usr/share/icons/hicolor/scalable/apps/goa-account-%(_domain)s.svg' % locals(
        )
        if not os.path.isfile(_provider_logo):
            _provider_logo = '/usr/share/icons/HighContrast/scalable/actions/system-run.svg'

        if '-' in _iso_lang:
            _lang = _iso_lang.split('-')[0]
            _region = _iso_lang.split('-')[1]
        elif '_' in _iso_lang:
            _lang = _iso_lang.split('_')[0]
            _region = _iso_lang.split('_')[1]
        try:
            if _speech_rate < 160:
                _slow = True
        except (NameError, TypeError):
            self.ok = False
        domain_table = [{
            'domain': 'com.au',
            'iso_code': 'AU',
            'lang1': 'en',
            'lang2': 'zh-CN'
        }, {
            'domain': 'co.uk',
            'iso_code': 'GB',
            'lang1': 'en',
            'lang2': 'pl'
        }, {
            'domain': 'ca',
            'iso_code': 'CA',
            'lang1': 'en',
            'lang2': 'fr'
        }, {
            'domain': 'co.nz',
            'iso_code': 'NZ',
            'lang1': 'en',
            'lang2': 'zh-CN'
        }, {
            'domain': 'com.hk',
            'iso_code': 'CN',
            'lang1': 'zh',
            'lang2': 'en'
        }, {
            'domain': 'com.hk',
            'iso_code': 'HK',
            'lang1': 'zh',
            'lang2': 'en'
        }, {
            'domain': 'com.hk',
            'iso_code': 'MO',
            'lang1': 'zh',
            'lang2': 'pt'
        }, {
            'domain': 'com.tw',
            'iso_code': 'TW',
            'lang1': 'zh-TW',
            'lang2': 'en'
        }, {
            'domain': 'co.in',
            'iso_code': 'IN',
            'lang1': 'hi',
            'lang2': 'en'
        }, {
            'domain': 'ie',
            'iso_code': 'IE',
            'lang1': 'en',
            'lang2': 'pl'
        }, {
            'domain': 'co.za',
            'iso_code': 'ZA',
            'lang1': 'af',
            'lang2': 'en'
        }, {
            'domain': 'fr',
            'iso_code': 'FR',
            'lang1': 'fr',
            'lang2': 'ar'
        }, {
            'domain': 'com.br',
            'iso_code': 'BR',
            'lang1': 'pt',
            'lang2': 'de'
        }, {
            'domain': 'pt',
            'iso_code': 'PT',
            'lang1': 'pt',
            'lang2': 'en'
        }, {
            'domain': 'com.mx',
            'iso_code': 'MX',
            'lang1': 'es',
            'lang2': 'en'
        }, {
            'domain': 'es',
            'iso_code': 'ES',
            'lang1': 'es',
            'lang2': 'ca'
        }, {
            'domain': 'ar',
            'iso_code': 'AR',
            'lang1': 'es',
            'lang2': 'en'
        }, {
            'domain': 'ci',
            'iso_code': 'CI',
            'lang1': 'es',
            'lang2': 'en'
        }, {
            'domain': 'ru',
            'iso_code': 'RU',
            'lang1': 'ru',
            'lang2': 'uk'
        }, {
            'domain': 'com.ua',
            'iso_code': 'UA',
            'lang1': 'uk',
            'lang2': 'ru'
        }]
        for i in range(len(domain_table)):
            if domain_table[i]['iso_code'] == _region.upper():
                _tld = domain_table[i]['domain']
                _lang1 = domain_table[i]['lang1']
                _lang2 = domain_table[i]['lang2']
                break

        _media_out = ''
        # Determine the output file name
        _media_out = readtexttools.get_work_file_path(_out_path, _icon, 'OUT')
        # Determine the temporary file name
        _media_work = ''.join([
            readtexttools.get_work_file_path(_out_path, _icon, 'TEMP'),
            self.default_extension
        ])
        if len(_out_path) == 0 and bool(_post_process):
            if readtexttools.handle_sound_playing(_media_work):
                return True
        # Remove old files.
        if os.path.isfile(_media_work):
            os.remove(_media_work)
        if os.path.isfile(_media_out):
            os.remove(_media_out)
        _max_words = 20
        _short_text = '%20'.join(
            _text.replace('+', '%2B').split(' ')[:_max_words])

        for _punctuation in '\n.?!':
            if _punctuation in _short_text:
                _short_text = _short_text.split(_punctuation)[0]
                break
        if _lang != _lang1:
            # Translate **to** default language
            _lang2 = _lang1
        if readtexttools.have_posix_app('osascript', False):
            _msg = 'https://translate.%(_domain)s.%(_tld)s' % locals()
        else:
            _msg = '`<https://translate.%(_domain)s.%(_tld)s?&langpair=auto|%(_lang2)s&tbb=1&ie=&hl=%(_env_lang)s&text=%(_short_text)s>' % locals(
            )
        if not self.language_supported(_iso_lang):
            # Fallback: display a link to translate using Google Translate.
            readtexttools.pop_message(
                u"%(_provider)s Translate\u2122" % locals(), _msg, 5000,
                _provider_logo, 0)
            return True
        try:
            tts = gtts.gTTS(_text, _tld, _lang, _slow, _lang_check)
            tts.save(_media_work)
            if os.path.isfile(_media_work):
                readtexttools.pop_message("`gtts-%(_version)s`" % locals(),
                                          _msg, 5000, _provider_logo, 0)
        except gtts.tts.gTTSError:
            readtexttools.pop_message(
                "`gtts-%(_version)s` failed to connect." % locals(), _msg,
                5000, _error_icon, 2)
            self.ok = False
            return False
        except (AssertionError, NameError, ValueError, RuntimeError):
            # gtts error. Consider using pip3 to check for an update.
            readtexttools.pop_message(
                u"%(_provider)s Translate\u2122" % locals(), _msg, 5000,
                _provider_logo, 0)
            self.ok = False
            return False
        if os.path.isfile(_media_work) and _post_process in [
                'process_mp3_media', 'process_audio_media'
        ]:
            if os.path.getsize(_media_work) == 0:
                return False
            # NOTE: Calling process must unlock_my_lock()
            readtexttools.process_wav_media(_info, _media_work, _icon,
                                            _media_out, _audible, _visible,
                                            _writer, _size)
            return True
        else:
            _msg = "Could not play a network media file locally. Try `pip3 install gTTS gTTS-token`."
            if bool(_media_out):
                _msg = "Could not save a network media file locally. Try `pip3 install gTTS gTTS-token`."
            readtexttools.pop_message("Python `gtts-%(_version)s`" % locals(),
                                      _msg, 5000, _error_icon, 1)
        self.ok = False
        return False

    def language_supported(self, iso_lang='ca-ES'):  # -> bool
        '''Check if the library supports the language.'''
        test_lang = ''
        if not self.check_version(2.2):
            return False
        try:
            for sep in ['-', '_']:
                if sep in iso_lang:
                    test_lang = iso_lang.split(sep)[0]
                    break
        except (AttributeError, NameError):
            return False
        try:
            for _test in [iso_lang, test_lang]:
                if _test in gtts.tts.tts_langs():
                    return True
        except NameError:
            pass
        return False


class LarynxClass(object):
    '''Larynx is a text to speech local http voice server that a
    Raspberry Pi computer can use with automated devices. Larynx
    can support SSML and codes in plain text strings to suggest
    how to say words and phrases. Check the larynx website shown
    at the end to see what processor platforms that larynx
    officially supports.

    To use the larynx speech synthesis client with this python class,
    you need to initiate `larynx-server`. Depending on how larnyx
    is configured, you might need administrator (`sudo`) access to
    start the server or to let local users start the server.

    This python program uses the larynx web api to read text aloud.

    Before putting larynx into daily use, you should test Layrnx speech
    synthesis using a desktop web browser at a `localhost` url. You
    can test different quality settings to determine the best combination
    of fidelity and low latency on your system.  The recommended setting for
    supported Raspberry Pi computers is currently `0` or `Low Quality`.
    For most consumer computers, the recommended setting is `1` or
    `Medium Quality`.

    If the implementation of dbus allows it, this class displays a
    pop-up menu if you have not created a directory in
    `~/.local/share/larynx/`. If your `larynx-server` is set up to
    allow it, this is the directory where the server stores and reads
    downloaded voices.

    [Default larnyx address](http://0.0.0.0:5002)

    [About Larynx...](https://github.com/rhasspy/larynx)'''

    def __init__(self):  # -> None
        '''Initialize data. See
        <https://github.com/rhasspy/larynx#basic-synthesis>'''
        _common = LocalCommons()
        self.common = _common
        self.debug = _common.debug
        self.default_extension = _common.default_extension
        self.ok = True
        # This is the default. You can set up Larynx to use a different port.
        self.url = 'http://0.0.0.0:5002'  # localhost port 5002
        self.help_icon = _common.help_icon
        self.help_heading = 'Rhasspy Larynx'
        self.help_url = 'https://github.com/rhasspy/larynx#larynx'
        self.local_dir = os.path.expanduser('~/.local/share/larynx/')
        self.vocoders = None  # ordered fast+normal to slow+high quality
        self.ssmls = [False, True]  # false = TEXT or true = SSML
        self.rate_denominator = 1
        self.length_scales = [
            [320, 289, '---------|', 0.50], [288, 257, '--------|-', 0.55],
            [256, 225, '-------|--', 0.62], [224, 193, '------|---', 0.71],
            [192, 161, '-----|----', 0.83], [128, 97, '---|-----', 1.25],
            [96, 66, '--|------', 1.66], [64, 33, '-|-------', 2.50],
            [32, 0, '|--------', 5.00]
        ]  # A lower speed corresponds to a longer duration.
        # larynx `glow_tts` voices from larynx version 1.1.
        self.accept_voice = [
            '', 'all', 'auto', 'child_female', 'female1', 'female2', 'female3',
            'female4', 'female5', 'female6', 'female7', 'female8', 'female9',
            'child_female1', 'child_male', 'male1', 'male2', 'male3', 'male4',
            'male5', 'male6', 'male7', 'male8', 'male9', 'child_male1',
            'larynx', 'localhost', 'docker', 'local_server'
        ]
        self.spd_fm = _common.spd_fm
        self.spd_m = _common.spd_m

        # The routine uses the default voice as a fallback. The routine
        # prioritizes a voice that you chose to install.
        self.default_lang = _common.default_lang
        self.default_voice = 'mary_ann'
        self.default_extension = _common.default_extension
        # `mary_ann` is the default voice, and it is always installed. It
        # will not appear in a downloaded voices directory. It will always
        # be included in the server's json request response.
        self.larynx_v1 = ['mary_ann']
        if '_IN' in self.default_lang:
            self.larynx_v1 = ['cmu_aup', 'cmu_ksp', 'cmu_slp']
        elif self.default_lang == 'en_CA':
            self.larynx_v1 = ['mary_ann', 'cmu_jmk']
        elif self.default_lang == 'es_ES':
            self.larynx_v1 = ['carlfm', 'karen_savage']
        elif self.default_lang == 'fr_FR':
            self.larynx_v1 = ['gilles_le_blanc', 'siwis']
        elif self.default_lang == 'it_IT':
            self.larynx_v1 = ['lisa', 'riccardo_fasol']
        elif self.default_lang not in ['en_PH', 'en_US', 'es_MX']:
            self.larnx_v1 = [
                'blizzard_fls', 'ek', 'harvard', 'northern_english_male',
                'scottish_english_male', 'southern_english_female',
                'southern_english_male'
            ]
        # https://community.rhasspy.org/t/preview-of-new-tts-voices/2556

        self.larynx_fm = [
            'eva_k', 'hokuspokus', 'kerstin', 'rebecca_braunert_plunkett',
            'blizzard_fls', 'blizzard_lessac', 'cmu_clb', 'cmu_eey', 'cmu_ljm',
            'cmu_lnh', 'cmu_rms', 'cmu_slp', 'cmu_slt', 'ek', 'harvard',
            'judy_bieber', 'kathleen', 'ljspeech', 'southern_english_female',
            'karen_savage', 'siwis', 'lisa', 'nathalie', 'hajdurova',
            self.default_voice
        ]
        self.voice_id = ''
        self.voice_name = ''
        self.pause_list = _common.pause_list
        self.add_pause = _common.add_pause
        self.base_curl = _common.base_curl
        self.is_x86_64 = _common.is_x86_64

    def _set_vocoders(self, alt_local_url=''):  # -> bool
        '''If the server is running, then get the list of voice coders.
        + `alt_local_url` If you are connecting to a local network's
           larynx server using a different computer, you might need to use
           a different url.'''
        if alt_local_url.startswith("http"):
            self.url = alt_local_url
        data = {}
        if bool(self.vocoders):
            return True
        try:
            response = urllib.request.urlopen(''.join(
                [self.url, '/api/vocoders']))
            data_response = response.read()
            data = json.loads(data_response)
        except urllib.error.URLError:
            self.ok = False
            return False
        except AttributeError:
            try:
                response = urllib.urlopen(''.join([self.url, '/api/vocoders']))
                data_response = response.read()
                data = json.loads(data_response)
            except [AttributeError, urllib.error.URLError]:
                self.ok = False
                return False
        except:
            print('''Unknown error while looking up larynx voice encoders.
Try restarting `larynx-server`.''')
            return False
        if len(data) == 0:
            return False
        _nsv = ''
        for _jint in range(0, len(data)):
            _nsv = ''.join([_nsv, data[_jint]['id'], '\n'])
        self.vocoders = _nsv[:-1].split('\n')
        return True

    def _spd_voice_to_larynx_voice(self,
                                   _search='female1',
                                   larynx_names='mary_ann'):  # -> str
        '''Assign a larynx name like `scottish_english_male` to a spd_voice
        like `male1` '''
        if self.debug and 1:
            print([
                '`LarynxClass` > `_spd_voice_to_larynx_voice`', _search,
                larynx_names
            ])
        _search = _search.lower().strip('\'" \n')
        if len(_search) == 0:
            return ''
        elif len(larynx_names.strip()) == 0:
            return ''
        # data_list has a minimum of four items.
        # Not using Modulo Operator (`%`)
        _data = 5 * '''%(larynx_names)s\n''' % locals()
        _data_list = _data.strip().split('\n')
        _resultat = ''
        count_f = 0
        for count, _item in enumerate(self.spd_m):
            if _item == _search:
                count_f = count
                break
        _voices = ''
        if 'female' not in _search:
            for _voice in _data_list:
                if _voice not in self.larynx_fm:
                    _voices = ''.join([_voices, _voice, '\n'])
            try:
                _resultat = _voices.strip().split('\n')[count_f]
            except IndexError:
                _resultat = self.voice_name
        if len(_resultat) != 0:
            return _resultat
        count_f = 0
        for count, _item in enumerate(self.spd_fm):
            if _item == _search:
                count_f = count
                break
        _voices = ''
        for _voice in _data_list:
            if _voice in self.larynx_fm:
                _voices = ''.join([_voices, _voice, '\n'])
        try:
            _resultat = _voices.strip().split('\n')[count_f]
        except IndexError:
            _resultat = self.voice_name
        return _resultat

    def language_supported(self,
                           iso_lang='en-US',
                           alt_local_url='',
                           vox='auto'):  # -> bool
        '''Is the language or voice supported?
        + `iso_lang` can be in the form `en-US` or a voice like `eva_k`
        + `alt_local_url` If you are connecting to a local network's
           speech server using a different computer, you might need to use
           a different url.'''
        if alt_local_url.startswith("http"):
            self.url = alt_local_url
        if int(platform.python_version_tuple()[0]) < 3 or int(
                platform.python_version_tuple()[1]) < 8:
            self.ok = False
            return self.ok
        if not REQUESTS_OK:
            if not readtexttools.have_posix_app('curl', False):
                self.ok = False
                return False
            if not bool(self.base_curl):
                self.ok = False
                return False
        if not self._set_vocoders(self.url):
            self.ok = False
            return False
        if len(self.voice_id) != 0:
            self.help_url = self.url
            self.help_icon = '/usr/share/icons/HighContrast/scalable/actions/system-run.svg'
            return True
        # format of json dictionary item: 'de-de/eva_k-glow_tts'
        # "voice" or "language and region"
        _lang1 = iso_lang.lower()
        # concise language
        _lang2 = iso_lang.lower().split('-')[0].split('_')[0]
        data = {}
        try:
            response = urllib.request.urlopen(''.join(
                [self.url, '/api/voices']))
            data_response = response.read()
            data = json.loads(data_response)
        except urllib.error.URLError:
            _eurl = self.url
            if self.is_x86_64:
                print('''
[larynx-server](https://github.com/rhasspy/larynx)
can synthesize speech privately using %(_eurl)s.''' % locals())
            self.ok = False
            return False
        except AttributeError:
            try:
                # catching classes that do not inherit from BaseExceptions
                # is not allowed.
                response = urllib.urlopen(''.join([self.url, '/api/voices']))
                data_response = response.read()
                data = json.loads(data_response)
            except Exception:
                try:
                    os.system('larynx-server')
                except OSError:
                    pass
                self.ok = False
                return False
        if len(data) == 0:
            return False
        # Find the first voice that meets the criteria. If found, then
        # return `True`, otherwise return `False`.
        _voice_id = ''
        larynx_names = ''
        for _item in data:
            if data[_item]['downloaded']:
                self.accept_voice.append(data[_item]['name'])
                if _lang1 in data[_item]['language']:
                    larynx_names = ''.join(
                        [larynx_names, '\n', data[_item]['name']])
                elif _lang2 == data[_item]['language'].split('-')[0].split(
                        '_')[0]:
                    larynx_names = ''.join(
                        [larynx_names, '\n', data[_item]['name']])
        larynx_names = larynx_names.strip()
        _vox = vox.lower()
        if _vox in larynx_names.split('\n'):
            _verified_name = _vox
        else:
            _verified_name = self._spd_voice_to_larynx_voice(
                _vox, larynx_names)
        if _verified_name in self.larynx_v1:
            _logo = ''.join([u' \u263B  (', self.default_lang, ')'])
        else:
            _logo = ''.join([u' \u263A  (', _lang2, ')'])
        if len(_verified_name) != 0:
            if len(larynx_names) != 0:
                display_names = larynx_names.replace(
                    _verified_name,
                    u'%(_verified_name)s %(_logo)s  %(_vox)s' % locals())
                print('''
Loading larynx voices for `%(_lang2)s`
==============================

%(display_names)s
''' % locals())
            # Check for a specific matching SPD name
            # Search examples - `FEMALE2`, `MALE1`
            for _item in data:
                if data[_item]['name'] == _verified_name:
                    if self.debug and 1:
                        print([
                            '`LarynxClass` > `language_supported` found: ',
                            data[_item]['name'], 'Setting `id` to: ',
                            data[_item]['id']
                        ])
                    self.voice_id = data[_item]['id']
                    self.voice_name = data[_item]['name']
                    self.ok = True
                    return self.ok
        self.ok = False
        iso_lower = iso_lang.replace('_', '-').lower()
        # Find a voice id that matches Larynx name, id or language
        # Search examples: ``, `AUTO`, `LARYNX`
        for _item in data:
            if data[_item]['downloaded']:
                for try_lang in [
                        data[_item]['language'],
                        data[_item]['language'].split('-')[0]
                ]:
                    for argument in [_vox, iso_lower, _lang1]:
                        if argument in [
                                try_lang, data[_item]['name'],
                                data[_item]['id']
                        ]:
                            self.voice_id = data[_item]['id']
                            self.voice_name = data[_item]['name']
                            self.ok = True
                            return self.ok
        return self.ok

    def get_voc_type(self, _type='small'):  # -> str
        '''Try to get the appropriate voc type for the platform.'''
        if not _type in ['small', 'medium', 'large']:
            return ''
        for coder in self.vocoders:
            if coder.endswith(_type):
                return coder
        return ''

    def read(self,
             _text="",
             _iso_lang='en-US',
             _visible="false",
             _audible="true",
             _out_path="",
             _icon="",
             _info="",
             _post_process=None,
             _writer='',
             _size='600x600',
             _speech_rate=160,
             quality=1,
             ssml=False,
             _denoiser_strength=0.005,
             _noise_scale=0.667,
             _ok_wait=4,
             _end_wait=30):  # -> bool
        '''
        First, check larynx language support using `def language_supported`.
        Speak text aloud using a running instance of the
        [larynx-server](https://github.com/rhasspy/larynx)
        For most personal computers "highest" quality is too slow for
        real time speech synthesis. Use "standard" or "higher".
        '''
        if not self.ok:
            return False
        if len(self.voice_id) == 0:
            self.voice_id = 'en-us/mary_ann-glow_tts'
            self.voice_name = 'mary_ann'
        _done = False
        if not os.path.isdir(self.local_dir):
            if not readtexttools.is_container_instance():
                readtexttools.pop_message(self.help_heading,
                                          ''.join(['<', self.help_url, '>']),
                                          8000, self.help_icon, 1)
        _media_out = ''
        # Determine the output file name
        _media_out = readtexttools.get_work_file_path(_out_path, _icon, 'OUT')
        # Determine the temporary file name
        _media_work = os.path.join(tempfile.gettempdir(), 'larynx.wav')
        if os.path.isfile(_media_work):
            os.remove(_media_work)
        if len(_out_path) == 0 and bool(_post_process):
            if readtexttools.handle_sound_playing(_media_work):
                return True
        _voice = self.voice_name
        if self.debug and 1:
            print(['`LarynxClass` > ` `read`', 'Request `_voice`: ', _voice])
        _length_scale = 0.85
        if bool(self.add_pause) and not ssml:
            for _symbol in self.pause_list:
                if _symbol in _text:
                    _text = _text.translate(self.add_pause).replace('.;', '.')
                    break
        try:
            if not self.is_x86_64:
                # Unknown platform - try the fastest setting.
                _vocoder = self.get_voc_type('small')
            elif quality in range(0, len(self.vocoders) - 1):
                # Set manually - I don't know which order the
                # voices are on your platform, so if it does
                # not work as expected, try a different number.
                _vocoder = self.vocoders[quality]
            elif len(_text.split()) < 3:
                # A single word
                self.rate_denominator = 0.85  # speak slower
                _vocoder = self.get_voc_type('large')
            else:
                _vocoder = self.get_voc_type('medium')
            if len(_vocoder) == 0:
                _vocoder = self.vocoders[len(self.vocoders) - 1]
        except IndexError:
            if bool(self.vocoders):
                _vocoder = self.vocoders[len(self.vocoders) - 1]
            else:
                return False
        _ssml = 'false'
        if ssml:
            _ssml = 'true'
        _url = ''.join([self.url, '/api/tts'])
        for _item in self.length_scales:
            if not _speech_rate > _item[0] and not _speech_rate < _item[1]:
                print(
                    '\nLarynx\n======\n+ tts rate: ', _speech_rate, ''.join([
                        'wpm   20%[', _item[2], ']200%\n+ url: ', self.url,
                        '\n+ voice encoder: ', _vocoder, '\n+ voice id: ',
                        _voice, '\n'
                    ]))
                _length_scale = _item[3]
                break
        _length_scale = str(_length_scale / self.rate_denominator)
        _text = readtexttools.local_pronunciation(_iso_lang, _text, 'larynx',
                                                  'LARYNX_USER_DIRECTORY',
                                                  False)[0]
        if REQUESTS_OK:
            _strips = '\n .;'
            _text = '\n'.join(['', _text.strip(_strips), ''])
            response = requests.post(
                _url,
                params={
                    'voice': _voice,
                    'vocoder': _vocoder,
                    'denoiserStrength': _denoiser_strength,
                    'noiseScale': _noise_scale,
                    'lengthScale': _length_scale,
                    'ssml': _ssml
                },
                headers={
                    'Content-Type':
                    'application/x-www-form-urlencoded',
                    'User-Agent':
                    'Mozilla/5.0 (X11; Debian; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'
                },
                data=_text.encode('utf-8', 'ignore'),
                timeout=(_ok_wait, _end_wait))
            with open(_media_work, 'wb') as f:
                f.write(response.content)
                _done = True
        if not _done:
            if not bool(self.base_curl):
                return False
            _text = readtexttools.strip_mojibake(_iso_lang[:2].lower(), _text)
            _text = str(_text.translate(self.base_curl))                
            app_list = [
                ['curl', '''curl --max-time %(_end_wait)s --connect-timeout %(_ok_wait)s -s -d "%(_text)s" "%(_url)s?voice=%(_voice)s&vocoder=%(_vocoder)s&denoiserStrength=%(_denoiser_strength)s&noiseScale=%(_noise_scale)s&lengthScale=%(_length_scale)s&ssml=%(_ssml)s" -o "%(_media_work)s"''' % locals()], 
                ['wget', '''wget --no-http-keep-alive -q --post-data="%(_text)s" "%(_url)s?voice=%(_voice)s&vocoder=%(_vocoder)s&denoiserStrength=%(_denoiser_strength)s&noiseScale=%(_noise_scale)s&lengthScale=%(_length_scale)s&ssml=%(_ssml)s" -O "%(_media_work)s"''' % locals()],
                ]
            for _app in app_list:
                if readtexttools.have_posix_app(_app[0], False):
                    if bool(self.debug):
                        print(_app[1])
                    os.system(_app[1])
                    if not os.path.isfile(_media_work):
                        continue
                    if os.path.getsize(_media_work) == 0:
                        time.sleep(2)
                    if os.path.isfile(_media_work):
                        _done = True
                        break
        if not _done:
            print('''The application cannot load a sound file.
Your computer is missing a required library.
Use `pip3 install requests` or `apt-get install python3-requests` to fix it.'''
                  )
            self.ok = False
            return False
        return self.common.do_net_sound(_info, _media_work, _icon, _media_out,
                                        _audible, _visible, _writer, _size,
                                        _post_process)


class MaryTtsClass(object):
    '''You can use `synesthesiam/docker-marytts` text to speech localhost
http server for 8 languages. You can find other docker containers that can
use the same application program interface with a different selection of
voices, speech technology, and language options. For example,
[Larynx MaryTTS Compatible API](https://github.com/rhasspy/larynx#marytts-compatible-api)

    docker run \
        -it \
        -p 59125:5002 \
        -e "HOME=${HOME}" \
        -v "$HOME:${HOME}" \
        -v /usr/share/ca-certificates:/usr/share/ca-certificates \
        -v /etc/ssl/certs:/etc/ssl/certs \
        -w "${PWD}" \
        --user "$(id -u):$(id -g)" \
        rhasspy/larynx

Default MaryTts server: <http://0.0.0.0:59125>

[About MaryTts...](https://github.com/synesthesiam/docker-marytts)'''

    def __init__(self):  # -> None
        '''Initialize data. See
        <https://github.com/synesthesiam/docker-marytts>'''
        _common = LocalCommons()
        self.common = _common
        self.debug = _common.debug
        self.ok = True
        self.response = ''
        # This is the default. You can set up MaryTts to use a different port.
        self.url = 'http://0.0.0.0:59125'  # localhost port 59125
        self.help_icon = _common.help_icon
        self.help_heading = 'Rhasspy MaryTTS'
        self.help_url = 'https://github.com/synesthesiam/docker-marytts'
        self.audio_format = 'WAVE_FILE'
        self.input_types = [
            'TEXT', 'SIMPLEPHONEMES', 'SABLE', 'SSML', 'APML', 'EMOTIONML',
            'RAWMARYXML'
        ]
        self.accept_voice = [
            '', 'all', 'auto', 'child_female', 'female1', 'female2', 'female3',
            'female4', 'female5', 'female6', 'female7', 'female8', 'female9',
            'child_female1', 'child_male', 'male1', 'male2', 'male3', 'male4',
            'male5', 'male6', 'male7', 'male8', 'male9', 'child_male1',
            'marytts', 'localhost', 'docker', 'local_server'
        ]
        self.voice_locale = ''
        self.pause_list = _common.pause_list
        self.add_pause = _common.add_pause
        self.base_curl = _common.base_curl
        self.is_x86_64 = _common.is_x86_64

    def marytts_xml(self, _text='', _speech_rate=160):  # -> str
        '''Change the speed that MaryTTS reads plain text aloud using
        `RAWMARYXML`. `maryxml` correctly uses standard XML conventions like
        `&amp;`, `&gt;` and `&lt;`, so the charactrs that they represent use
        corrected XML.'''
        _xmltransform = readtexttools.XmlTransform()
        _text = _xmltransform.clean_for_xml(_text, False)
        try:
            # 160 wpm (Words per minute) yields 100% prosody rate
            _rate = ''.join([str(int(_speech_rate / 1.6)), '%'])
        except [AttributeError, TypeError]:
            _rate = '100%'
        return '''<?xml version="1.0" encoding="UTF-8"?>
<maryxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns="http://mary.dfki.de/2002/MaryXML" version="0.4" xml:lang="en-US"><p>
<prosody rate="%(_rate)s">%(_text)s</prosody></p></maryxml>''' % locals()

    def language_supported(self,
                           iso_lang='en-US',
                           alt_local_url=''):  # -> bool
        '''Is the language or voice supported?
        + `iso_lang` can be in the form `en-US` or `en`.
        + `alt_local_url` If you are connecting to a local network's
           speech server using a different computer, you might need to use
           a different url.'''
        if alt_local_url.startswith("http"):
            self.url = alt_local_url
        if int(platform.python_version_tuple()[0]) < 3 or int(
                platform.python_version_tuple()[1]) < 8:
            self.ok = False
            return self.ok
        if not REQUESTS_OK:
            if not readtexttools.have_posix_app('curl', False):
                if not readtexttools.have_posix_app('wget', False):
                    self.ok = False
                    return False
            if not bool(self.base_curl):
                self.ok = False
                return False
        if len(self.voice_locale) != 0:
            self.help_url = self.url
            self.help_icon = '/usr/share/icons/HighContrast/scalable/actions/system-run.svg'
            return True
        _lang1 = iso_lang.replace('-', '_')
        # concise language
        _lang2 = _lang1.split('_')[0]
        try:
            response = urllib.request.urlopen(''.join([self.url, '/locales']))
            _locales = str(response.read(), 'utf-8')
        except urllib.error.URLError:
            self.ok = False
            return False
        except AttributeError:
            try:
                # catching classes that do not inherit from BaseExceptions
                # is not allowed.
                response = urllib.urlopen(''.join([self.url, '/locales']))
                _locales = str(response.read(), 'utf-8')
            except AttributeError:
                self.ok = False
                return False
        if len(_locales) == 0:
            return False
        # Find the first voice that meets the criteria. If found, then
        # return `True`, otherwise return `False`.
        self.ok = False
        if _lang1 in _locales.split('\n'):
            self.ok = True
            self.voice_locale = _lang1
        elif _lang2 in _locales.split() or _lang2 == 'en':
            self.ok = True
            if _lang2 == 'en':
                if _lang1[-2:].lower() in [
                        'au', 'bd', 'bs', 'gb', 'gh', 'hk', 'ie', 'in', 'jm',
                        'nz', 'pk', 'sa', 'tt'
                ]:
                    self.voice_locale = 'en_GB'
                else:
                    self.voice_locale = 'en_US'
            else:
                self.voice_locale = _lang2.lower()
        return self.ok

    def marytts_voice(self,
                      _voice='female1',
                      _iso_lang='en-US',
                      _prefer_gendered_fallback=True):  # -> str
        '''If the MaryTTS API includes the voice description, return a
        marytts voice description like `cmu-bdl-hsmm`, otherwise return
        `''`.'''
        if len(_voice) == 0:
            return ''
        try:
            response = urllib.request.urlopen(''.join([self.url, '/voices']))
            _voices = str(response.read(), 'utf-8')
        except urllib.error.URLError:
            print(
                '''Requested [docker-marytts](https://github.com/synesthesiam/docker-marytts)
            It did not respond correctly.''')
            return ''
        except AttributeError:
            try:
                # catching classes that do not inherit from BaseExceptions
                # is not allowed.
                response = urllib.urlopen(''.join([self.url, '/voices']))
                _voices = str(response.read(), 'utf-8')
            except AttributeError:
                return ''
        if len(_voices) == 0:
            return ''
        _locale = _iso_lang.replace('-', '_')
        _voice = _voice.lower()
        if _voices.count(_locale) == 0:
            # i. e.: en_AU, en_CA ... en_ZA etc.
            # Disregard the region code and use all voices for the language.
            _locale = _locale.split('_')[0]
        _voice_list = _voices.split('\n')
        for _tester in _voice_list:
            _row = _tester.split(' ')
            if _row[0].count(_voice) != 0:
                self.voice_locale = _row[1]
                return _row[0]
        matches = []
        last_match = ''
        gendered_fallback = ''

        if _voice not in self.accept_voice:
            return last_match
        for _tester in _voice_list:
            _row = _tester.split(' ')
            _add_name = ''
            try:
                if _row[1].startswith(_locale):
                    last_match = _row[0]
                    for _standard in [_row[2], ''.join(['child_', _row[2]])]:
                        if _voice.startswith(_standard):
                            _add_name = last_match
                            break
                if len(_add_name) != 0:
                    matches.append(_add_name)
                    if len(gendered_fallback) == 0:
                        gendered_fallback = last_match
            except IndexError:
                continue
        for i in reversed(range(0, len(matches))):
            if _voice.endswith(str(len(matches) - i)):
                return matches[i]
        if _prefer_gendered_fallback:
            if len(gendered_fallback) != 0:
                return gendered_fallback
        return last_match

    def read(self,
             _text="",
             _iso_lang='en-US',
             _visible="false",
             _audible="true",
             _out_path="",
             _icon="",
             _info="",
             _post_process=None,
             _writer='',
             _size='600x600',
             _speech_rate=160,
             ssml=False,
             _vox='male1',
             _ok_wait=4,
             _end_wait=30):  # -> bool
        '''
        The read tool supports a subset of MaryTTS functions because not
        all voices, languages and synthesisers support all of the features
        of the server.
        '''
        if not self.ok:
            return False
        _media_out = ''

        # Determine the output file name
        _media_out = readtexttools.get_work_file_path(_out_path, _icon, 'OUT')
        # Determine the temporary file name
        _media_work = os.path.join(tempfile.gettempdir(), 'MaryTTS.wav')
        if len(_out_path) == 0 and bool(_post_process):
            if readtexttools.handle_sound_playing(_media_work):
                return True
        if bool(self.add_pause) and not ssml:
            for _symbol in self.pause_list:
                if _symbol in _text:
                    _text = _text.translate(self.add_pause).replace('.;', '.')
                    break
        _view_json = self.debug and 1
        response = readtexttools.local_pronunciation(
            _iso_lang, _text, 'mary_tts', 'MARY_TTS_USER_DIRECTORY',
            _view_json)
        _text = response[0]
        if _view_json:
            print(response[1])
        if ssml:
            _input_type = self.input_types[3]
        elif _speech_rate == 160:
            _input_type = self.input_types[0]
        else:
            _input_type = self.input_types[6]
            _text = self.marytts_xml(_text, _speech_rate)
        _url1 = self.url
        _url = ''.join([_url1, '/process'])
        _locale = _iso_lang.replace('-', '_')
        _found_locale = 'en_US'
        if len(self.voice_locale) != 0:
            _found_locale = self.voice_locale
        _audio_format = self.audio_format
        _output_type = 'AUDIO'
        _mary_vox = self.marytts_voice(_vox, _iso_lang)
        print('''
Docker MaryTTS
==============

* Audio: `%(_audio_format)s`
* Input Type: `%(_input_type)s`
* Locale: `%(_found_locale)s`
* Mapped Voice : `%(_vox)s`
* Output Type: `%(_output_type)s`
* Server URL: `%(_url1)s`
* Voice : `%(_mary_vox)s`

[Docker MaryTTS](https://github.com/synesthesiam/docker-marytts)
''' % locals())
        if REQUESTS_OK:
            if len(_mary_vox) == 0:
                request_params = {
                    'AUDIO': _audio_format,
                    'OUTPUT_TYPE': _output_type,
                    'INPUT_TYPE': _input_type,
                    'LOCALE': _found_locale,
                    'INPUT_TEXT': _text,
                }
            else:
                request_params = {
                    'AUDIO': _audio_format,
                    'OUTPUT_TYPE': _output_type,
                    'INPUT_TYPE': _input_type,
                    'LOCALE': _found_locale,
                    'VOICE': _mary_vox,
                    'INPUT_TEXT': _text,
                }
            _strips = ';\n .;'
            _text = _text.strip(_strips)
            response = requests.post(
                _url,
                params=request_params,
                headers={
                    'Content-Type':
                    'application/x-www-form-urlencoded',
                    'User-Agent':
                    'Mozilla/5.0 (X11; Debian; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'
                },
                data=_text.encode('utf-8', 'ignore'),
                timeout=(_ok_wait, _end_wait))
            with open(_media_work, 'wb') as f:
                f.write(response.content)
            _done = os.path.isfile(_media_work)
        else:
            vcommand = '&VOICE=%(_mary_vox)s' % locals()
            if len(_mary_vox) == 0:
                vcommand = ''
            _method = "POST"
            _body_data = "AUDIO=%(_audio_format)s&OUTPUT_TYPE=%(_output_type)s&INPUT_TYPE=%(_input_type)s&LOCALE=%(_found_locale)s%(vcommand)s&INPUT_TEXT=" % locals(
            )
            _done = self.common.do_posix_os_download(_url, _media_work,
                                                     _body_data, _text,
                                                     _method, _found_locale,
                                                     _ok_wait, _end_wait)
        if not _done:
            print('''The application cannot load a sound file.
Your computer is missing a required library.
Use `pip3 install requests` or `apt-get install python3-requests` to fix it.'''
                  )
            self.ok = False
            return False
        return self.common.do_net_sound(_info, _media_work, _icon, _media_out,
                                        _audible, _visible, _writer, _size,
                                        _post_process)


class RhvoiceLocalHost(object):
    '''[Rhvoice-rest](https://hub.docker.com/r/aculeasis/rhvoice-rest) is
    a docker image that allows Linux users to use speech synthesis (text
    to speech) while running Read Text Extension in a protected container like
    a snap or a flatpak. It provides a `localhost` http server to convert text
    that you select to speech. Docker images come with all the necessary files
    and settings packaged in a tamper-resistant container. 

    This Rhvoice docker container can read English, Esperanto, Georgian, Kyrgyz,
    Macedonian, Portuguese, Russian, Tatar and Ukrainian.

    The `rhvoice` libraries are enabled by electing to install it on a
    supported platform. Read the documentation for help installing the
    libraries or to help with troubleshooting if the tools do not work
    when using your Linux package manager.

    The following notice should be displayed in a dialog when users click
    `About...` or the equivalent in their language when this class is enabled.

    The main library is distributed under LGPL v2.1 or later. But it relies on
    MAGE for better responsiveness. MAGE is distributed under GPL v3 or later,
    so the combination is under GPL v3 or later. If you want to use the library
    in your program under GPL v2 or LGPL, compile the library without MAGE.

    The following restrictions apply to some of the voices:    

    All voices from RHVoice Lab's site are distributed under the Creative 
    Commons Attribution-NonCommercial-NoDerivatives 4.0 International Public
    License.

    The licenses for other optional third party voices are available at GitHub:

    <https://github.com/RHVoice/RHVoice/blob/master/doc/en/License.md>

    The contents of this resource are not affiliated with, sponsored by, or
    endorsed by RHVoice Lab nor does the documention represent the views or
    opinions of RHVoice Lab or RHVoice Lab personnel.

    The creators of the rhvoice libraries are the originators of the libraries
    enabling the `RhVoiceClass` class.

    See:

    * <https://github.com/RHVoice/RHVoice>
    * <https://github.com/RHVoice/RHVoice/issues>
    * <https://rhvoice.org/>'''

    def __init__(self):  # -> None
        '''The docker image doesn't expose details of the directory structure
        to the localhost API, so functions in the parent that rely on a specific
        file path do not work.'''
        _common = LocalCommons()
        self.common = _common
        self.add_pause = _common.add_pause
        self.pause_list = _common.pause_list
        self.base_curl = _common.base_curl
        self.debug = _common.debug
        self.url = 'http://0.0.0.0:8080'  # localhost port 8080
        self.help_icon = _common.help_icon
        self.help_heading = 'Rhvoice Rest'
        self.help_url = 'https://github.com/Aculeasis/rhvoice-rest/'
        self.audio_format = ['wav', 'mp3', 'opus', 'flac'][0]
        self.input_types = ['TEXT']
        self.accept_voice = [
            '', 'all', 'auto', 'child_female', 'female1', 'female2', 'female3',
            'female4', 'female5', 'female6', 'female7', 'female8', 'female9',
            'child_female1', 'child_male', 'male1', 'male2', 'male3', 'male4',
            'male5', 'male6', 'male7', 'male8', 'male9', 'child_male1',
            'rhvoice', 'localhost', 'docker', 'local_server'
        ]
        self.ok = False
        self.voice = ''
        self.female = 2
        self.male = 1
        self.checked_lang = ''
        # This is a list for testing if the API fails. Normally, using
        # the json data at <http://0.0.0.0:8080/info> enables updates
        # and forks of the original docker image to use current data.
        # As of 2023.01,18 the API `country` field might not reflect
        # the accent of the named speaker.
        # [lang | lang-region], ['male' | 'female'], name
        self.checklist = [['zzy', 'male', '_no_name']]

        self.verified_voices = []
        self.length_scales = [[320, 289, '---------|', 100],
                              [288, 257, '--------|-', 95],
                              [256, 225, '-------|--', 85],
                              [224, 193, '------|---', 75],
                              [192, 161, '-----|----', 65],
                              [160, 127, '----|----', 50],
                              [128, 97, '---|-----', 35],
                              [96, 66, '--|------', 20],
                              [64, 33, '-|-------', 10],
                              [32, 0, '|--------', 0]]

    def update_rhvoice_checklist(self):  # -> list
        '''Create a list table in the same format as `self.checklist`
        using a json data adapted from the rhvoice-rest API.

        See: <https://www.iso.org/obp/ui/#iso:code:3166:UA>'''
        _url = ''.join([self.url, '/info'])
        _default_list = self.checklist
        try:
            response = urllib.request.urlopen(_url)
            data_response = response.read()
            data = json.loads(data_response)
        except urllib.error.URLError:
            self.ok = False
            return _default_list
        except AttributeError:
            try:
                response = urllib.urlopen(_url)
                data_response = response.read()
                data = json.loads(data_response)
            except [AttributeError, urllib.error.URLError]:
                self.ok = False
                return _default_list
        except:
            return _default_list
        voice_lib = data['rhvoice_wrapper_voices_info']
        key_list = []
        return_list = []
        for _item in voice_lib:
            key_list.append(_item)
            self.accept_voice.append(_item)
            self.verified_voices = key_list
        try:
            for _key in key_list:
                _iso = ''.join(
                    [voice_lib[_key]['lang'], '-', voice_lib[_key]['country']])
                for iso_c in [['-NaN', ''], ['-UK', '-UA']]:
                    _iso = _iso.replace(iso_c[0], iso_c[1])
                return_list.append([
                    _iso, voice_lib[_key]['gender'],
                    voice_lib[_key]['name'].lower()
                ])
        except KeyError:
            return _default_list
        self.checklist = return_list
        self.ok = True
        return self.checklist

    def language_supported(self,
                           _iso_lang='en-US',
                           alt_local_url=''):  # -> bool
        '''Is the language or voice supported in rhvoice rest?
        + `iso_lang` can be in the form `en-US` or `en`.'''
        if alt_local_url.startswith("http"):
            self.url = alt_local_url
        if self.ok:
            return self.ok
        if not bool(self.verified_voices):
            self.update_rhvoice_checklist()
            if not bool(self.verified_voices):
                self.ok = False
                return False
        self.ok = False
        for _search in [_iso_lang.lower(), _iso_lang.split('-')[0].lower()]:
            for item in self.checklist:
                if item[0].lower().startswith(_search):
                    self.checked_lang = item[0]
                    self.ok = True
                    break
            if len(self.checked_lang) != 0:
                break
        if len(self.checked_lang) != 0:
            for item in self.checklist:
                if item[2] == _iso_lang.lower():
                    self.checked_lang = item[0]
                    self.ok = True
                    break
        if self.ok:
            help_heading = self.help_heading
            help_url = self.help_url
            print('''
Checking %(help_heading)s voices for `%(_iso_lang)s`
========================================

<%(help_url)s>
''' % locals())
            if not REQUESTS_OK:
                if not readtexttools.have_posix_app('curl', False):
                    self.ok = False
                if not bool(self.base_curl):
                    self.ok = False
        return self.ok

    def rhvoice_voice(self,
                      _voice='female1',
                      _iso_lang='en-US',
                      _prefer_gendered_fallback=True):  # -> str
        '''If the Rhvoice API includes the voice description, return a
        rhvoice voice description like `cmu-bdl-hsmm`, otherwise return
        `''`.'''
        if len(_voice) == 0:
            return ''
        if not bool(self.verified_voices):
            self.update_rhvoice_checklist()
            if not bool(self.verified_voices):
                self.ok = False
                return ''
        _voice = _voice.lower()
        if _voice in self.verified_voices:
            return _voice
        _found_locale = self.checked_lang
        if len(_found_locale) == 0:
            _found_locale = readtexttools.default_lang().replace('_', '-')
        _found_locale = _found_locale.split('-')[0].split('_')[0]
        matches = []
        _add_name = ''
        gendered_fallback = ''
        last_match = ''
        i_lang = 0
        i_gender = 1
        i_name = 2
        for _row in self.checklist:
            try:
                if _row[i_lang].startswith(_found_locale):
                    last_match = _row[i_name]
                    for _standard in [
                            _row[i_gender], ''.join(['child_', _row[i_gender]])
                    ]:
                        _add_name = ''
                        if _voice.startswith(_standard):
                            _add_name = last_match
                            break
                if len(_add_name) != 0 and _add_name not in matches:
                    matches.append(_add_name)
                    if len(gendered_fallback) == 0:
                        gendered_fallback = last_match
            except IndexError:
                break
        for i in range(0, len(matches)):
            if _voice.endswith(str(i + 1)):
                return matches[i]
        if _prefer_gendered_fallback:
            if len(gendered_fallback) != 0:
                return gendered_fallback
        return last_match

    def read(self,
             _text="",
             _iso_lang='en-US',
             _visible="false",
             _audible="true",
             _out_path="",
             _icon="",
             _info="",
             _post_process=None,
             _writer='',
             _size='600x600',
             _speech_rate=160,
             _vox='female1',
             _ok_wait=4,
             _end_wait=30):  # -> bool
        '''Read text using <https://hub.docker.com/r/aculeasis/rhvoice-rest>'''
        if not self.ok:
            return False
        _media_out = ''
        _done = False
        # Determine the output file name
        _media_out = readtexttools.get_work_file_path(_out_path, _icon, 'OUT')
        # Determine the temporary file name
        _media_work = os.path.join(tempfile.gettempdir(), 'Rhvoice-rest.wav')
        if len(_out_path) == 0 and bool(_post_process):
            if readtexttools.handle_sound_playing(_media_work):
                return True
        if bool(self.add_pause):
            for _symbol in self.pause_list:
                if _symbol in _text:
                    _text = _text.translate(self.add_pause).replace('.;', '.')
                    break
        _view_json = self.debug and 1
        response = readtexttools.local_pronunciation(_iso_lang, _text,
                                                     'rhvoice',
                                                     'RHVOICE_USER_DIRECTORY',
                                                     _view_json)
        _text = response[0]
        if _view_json:
            print(response[1])
        _length_scale = 50
        for _item in self.length_scales:
            if not _speech_rate > _item[0] and not _speech_rate < _item[1]:
                _length_scale = _item[3]
                break
        _length_scale = str(_length_scale)
        _url1 = self.url
        _url = '%(_url1)s/say' % locals()
        _audio_format = self.audio_format
        _voice = self.rhvoice_voice(_vox, _iso_lang, True)
        if REQUESTS_OK:
            try:
                _strips = '\n .;'
                _text = '\n'.join(['', _text.strip(_strips), ''])
                response = requests.get(_url,
                                        params={
                                            'format': _audio_format,
                                            'rate': _length_scale,
                                            'pitch': '50',
                                            'volume': '50',
                                            'voice': _voice,
                                            'text':
                                            _text.encode('utf-8', 'ignore')
                                        },
                                        timeout=(_ok_wait))
                with open(_media_work, 'wb') as f:
                    f.write(response.content)
                    _done = True
            except requests.exceptions.ConnectionError:
                self.ok = False
                return self.ok
        else:
            _body_data = 'format=%(_audio_format)s&rate=%(_length_scale)s&pitch=50&volume=50&voice=%(_voice)s&text=' % locals()
            _method = "GET"
            _done = self.common.do_posix_os_download(_url, _media_work, _body_data, _text, _method, _iso_lang, _ok_wait, _end_wait)
        if not _done:
            return False
        return self.common.do_net_sound(_info, _media_work, _icon, _media_out,
                                        _audible, _visible, _writer, _size,
                                        _post_process)


def speech_wpm(_percent='100%'):  # -> int
    '''
    _percent - rate expressed as a percentage.
    Use '100%' for default rate of 160 words per minute (wpm).
    Returns rate between 20 and 640.
    '''
    _calc_product = 0
    _result = 0
    _minimum = 20
    _maximum = 640
    _normal = 160
    _p_cent = ''

    try:
        if '%' in _percent:
            _p_cent = _percent.replace('%', '')
            _calc_product = (float(_p_cent)
                             if '.' in _p_cent else int(_p_cent) / 100)
            _result = math.ceil(_calc_product * _normal)
        else:
            _calc_product = (float(_percent)
                             if '.' in _percent else int(_percent))
            _result = math.ceil(_calc_product)
    except TypeError:
        return _normal
    if _result == 0:
        return _normal
    elif _result <= _minimum:
        return _minimum
    elif _result >= _maximum:
        return _maximum
    return _result


def network_ok(_iso_lang='en-US', _local_url=''):  # -> bool
    '''Do at least one of the classes support an on-line speech library?'''
    _gtts_class = GoogleTranslateClass()
    _continue = False
    if _gtts_class.check_version(2.2):
        _continue = True
    if not _continue:
        _larynx = LarynxClass()
        _continue = _larynx.language_supported(_iso_lang, _local_url, 'AUTO')
    if not _continue:
        _mary_tts = MaryTtsClass()
        _continue = _mary_tts.language_supported(_iso_lang, _local_url)
    if not _continue:
        _rhvoice_rest = RhvoiceLocalHost()
        _continue = _rhvoice_rest.language_supported(_iso_lang, _local_url)
    if not _continue:
        _amazon_class = AmazonClass()
        _continue = bool(_amazon_class.language_supported(_iso_lang))
    if not _continue:
        _azure_class = AzureClass()
        _continue = bool(_azure_class.language_supported(_iso_lang))
    if not _continue:
        _google_cloud_class = GoogleCloudClass()
        _continue = bool(_google_cloud_class.language_supported(_iso_lang))
    if not _continue:
        _watson_class = WatsonClass()
        _continue = bool(_watson_class.language_supported(_iso_lang))
    return _continue


def network_main(_text_file_in='',
                 _iso_lang='ca-ES',
                 _visible='false',
                 _audible='true',
                 _media_out='',
                 _writer='',
                 _title='',
                 _icon='',
                 _size='600x600',
                 _speech_rate=160,
                 _vox='',
                 _local_url='',
                 _denoiser_strength=0.005,
                 _noise_scale=0.667):  # -> boolean
    '''Read a text file aloud using a network resource.'''
    _imported_meta = readtexttools.ImportedMetaData()
    _larynx = LarynxClass()
    _marytts = MaryTtsClass()
    _amazon_class = AmazonClass()
    _azure_class = AzureClass()
    _google_cloud_class = GoogleCloudClass()
    _watson_class = WatsonClass()
    _gtts_class = GoogleTranslateClass()
    _rhvoice_rest = RhvoiceLocalHost()
    _continue = False
    _vox = _vox.strip('\'" \t\n').lower()
    _continue = _larynx.language_supported(
        _iso_lang,
        _local_url,
        _vox,
    ) and _vox in _larynx.accept_voice
    if not _continue:
        _continue = _marytts.language_supported(_iso_lang, _local_url)
    if not _continue:
        _continue = _gtts_class.check_version(
            2.2) and _vox in _gtts_class.accept_voice
    if not _continue:
        _continue = bool(_amazon_class.language_supported(
            _iso_lang)) and _vox in _amazon_class.accept_voice
    if not _continue:
        _continue = bool(_azure_class.language_supported(
            _iso_lang)) and _vox in _azure_class.accept_voice
    if not _continue:
        _continue = bool(_google_cloud_class.language_supported(
            _iso_lang)) and _vox in _google_cloud_class.accept_voice
    if not _continue:
        _continue = bool(_watson_class.language_supported(
            _iso_lang)) and _vox in _watson_class.accept_voice
    if not _continue:
        _continue = _rhvoice_rest.language_supported(_iso_lang, _local_url)
    if not _continue:
        print(
            'No working network server was found, or the requested voice is unavailable.\n'
        )
        usage()
        return False
    _text = _imported_meta.meta_from_file(_text_file_in)
    if len(_text) != 0:
        _info = readtexttools.check_artist(_writer)
        clip_title = readtexttools.check_title(_title, 'espeak')
        # If the library does not require a postprocess, use `0`,
        # otherwise use the item corresponding to the next action.
        _post_processes = [
            None, 'process_mp3_media', 'process_playlist',
            'process_riff_media', 'process_vorbis_media', 'process_wav_media',
            'process_audio_media'
        ]
        if _amazon_class.language_supported(_iso_lang):
            _amazon_class.read(_text, _iso_lang, _visible, _audible,
                               _media_out, _icon, clip_title,
                               _post_processes[1], _info, _size, _speech_rate)
        elif _azure_class.language_supported(_iso_lang):
            _azure_class.read(_text, _iso_lang, _visible, _audible, _media_out,
                              _icon, clip_title, _post_processes[1], _info,
                              _size, _speech_rate)
        elif _google_cloud_class.language_supported(_iso_lang):
            _google_cloud_class.read(_text, _iso_lang, _visible, _audible,
                                     _media_out, _icon, clip_title,
                                     _post_processes[1], _info, _size,
                                     _speech_rate)
        elif _larynx.language_supported(_iso_lang):
            _quality = -1  # Auto; Manual is 0 (lowest) to 2 (highest)
            _ssml = '</speak>' in _text and '<speak' in _text
            if _ssml:
                # Check if `_text` is valid XML
                if readtexttools.strip_xml(_text) == _text:
                    _ssml = False
            _larynx.read(_text, _iso_lang, _visible, _audible, _media_out,
                         _icon, clip_title, _post_processes[5], _info, _size,
                         _speech_rate, _quality, _ssml, _denoiser_strength,
                         _noise_scale)
        elif _marytts.language_supported(_iso_lang):
            _ssml = '</speak>' in _text and '<speak' in _text
            _marytts.read(_text, _iso_lang, _visible, _audible, _media_out,
                          _icon, clip_title, _post_processes[5], _info, _size,
                          _speech_rate, _ssml, _vox, 4, 15)
        elif _rhvoice_rest.language_supported(_iso_lang, _local_url):
            _rhvoice_rest.read(_text, _iso_lang, _visible, _audible,
                               _media_out, _icon, clip_title,
                               _post_processes[5], _info, _size, _speech_rate,
                               _vox, 4, 30)
        elif _gtts_class.language_supported(_iso_lang):

            _gtts_class.read(_text, _iso_lang, _visible, _audible, _media_out,
                             _icon, clip_title, _post_processes[1], _info,
                             _size, _speech_rate)
        else:
            # Just display a translation link.
            _gtts_class.read(_text, _iso_lang, _visible, _audible, _media_out,
                             _icon, clip_title, _post_processes[0], _info,
                             _size, _speech_rate)
    return True


def main():  # -> NoReturn
    '''Use network speech synthesis for supported languages while on-line'''
    if not sys.version_info >= (3, 6) or not os.name in ['posix', 'nt']:
        print('Your system does not support the network python tool.')
        usage()
        sys.exit(0)
    _speech_rate = 160
    _iso_lang = 'ca-ES'
    try:
        _iso_lang = readtexttools.default_lang().replace('_', '-')
    except AttributeError:
        pass
    _media_out = ''
    _visible = ''
    _audible = ''
    _text = ''
    _percent_rate = '100%'
    _speech_rate = speech_wpm(_percent_rate)
    _denoiser_strength = 0.005
    _noise_scale = 0.667
    _icon = ''
    _title = ''
    _writer = ''
    _size = '600x600'
    _speaker = 'AUTO'
    _local_url = ''
    _text_file_in = sys.argv[-1]

    if os.path.isfile(_text_file_in):
        if sys.argv[-1] == sys.argv[0]:
            usage()
            sys.exit(0)
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hovalritndsxuec', [
                'help', 'output=', 'visible=', 'audible=', 'language=',
                'rate=', 'image=', 'title=', 'artist=', 'dimensions=',
                'speaker=', 'voice=', 'url=', 'denoiser_strength=',
                'noise_scale='
            ])
        except getopt.GetoptError:
            print('option -a not recognized')
            usage()
            sys.exit(2)
        for o, a in opts:
            if o in ('-h', '--help'):
                usage()
                sys.exit(0)
            elif o in ('-o', '--output'):
                _media_out = a
            elif o in ('-v', '--visible'):
                _visible = a
            elif o in ('-a', '--audible'):
                _audible = a
            elif o in ('-l', '--language'):
                _iso_lang = a
            elif o in ('-r', '--rate'):
                _percent_rate = a
                if len(_percent_rate) != 0:
                    _speech_rate = speech_wpm(_percent_rate)
            elif o in ('-i', '--image'):
                _icon = a
            elif o in ('-t', '--title'):
                _title = a
            elif o in ('-n', '--artist'):
                _writer = a
            elif o in ('-d', '--dimensions'):
                _size = a
            elif o in ('-s', '--speaker'):
                # depreciated
                _speaker = a
            elif o in ('-x', '--voice'):
                _speaker = a
            elif o in ('-u', '--url'):
                _local_url = a
            elif o in ('-e', '--denoiser_strength'):
                try:
                    _denoiser_strength = float(o)
                except (AttributeError, TypeError, ValueError):
                    pass
                if not bool(_denoiser_strength):
                    _denoiser_strength = 0.005
            elif o in ('-c', '--noise_scale'):
                try:
                    _noise_scale = float(o)
                except (AttributeError, TypeError, ValueError):
                    pass
                if not bool(_noise_scale):
                    _noise_scale = 0.667
            else:
                assert False, 'unhandled option'
        network_main(_text_file_in, _iso_lang, _visible, _audible, _media_out,
                     _writer, _title, _icon, _size, _speech_rate, _speaker,
                     _local_url, _denoiser_strength, _noise_scale)
    sys.exit(0)


if __name__ == '__main__':
    main()
