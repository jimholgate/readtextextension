#!/usr/bin/env python3
# -*- coding: UTF-8-*-
'''

Reads a text file using an web service and a media player.
Online services require a network connection and installation
of an online connection library.

Check the terms and conditions that apply to the on-line service
provider. There may be acceptable use policies, limits or costs.

* Variants like speech rate, pitch, voice and gender might
  not apply to all services or to all languages.
* Online services could be terminated without warning.
* Your content might not be private or secure.
* Your organization or local laws might restrict use of online
  data services provided outside of your country's jurisdiction.
* An online provider could block your access because your use
  is excessive or otherwise violates their terms of service.

It doesn't work?
----------------

The tool relies on external libraries or packages, and python
might not have access to the current required package.

The version of python that LibreOffice includes with Windows,
MacOS and Linux distributions that use application containment
do not normally apply python modifications like user installed
python libraries. This script won't work because it can't use
the required libraries.

If you use python pip to install libraries, you might have to
manually update them from time to time. Packages that are managed
by update utilities like `apt-get`, `yum` and `dnf` are managed
by the distribution.

If you are using a docker service, your docker application might
take a more time to than usual to start up when the package updates
it's files. If you are using a system docker application with a
personal account, then you might need to manually download updated
speech resources if the docker application stops working with
locally installed languages.
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import getopt
import math
import os
import platform
import sys
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
            'child_male', 'male1', 'male2', 'male3', 'aws'
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


class GoogleTranslateClass(object):
    u''' The following notice should be displayed in a dialog when users click
    *About...* or the equivalent in their language when this class is enabled.

    Powered by Google\u2122

    "Google", "Google Cloud" and "Google Translate" are trademarks of Google Inc.

    The contents of this resource are not affiliated with, sponsored by, or endorsed
    by Google nor does the documention represent the views or opinions of Google or
    Google personnel.

    The creators of the `gtts` python library are the originators of the library
    enabling the `GoogleTranslateClass` class.

    The `gtts` library can only be enabled by electing to install it on a supported
    platform. Read the documentation for help installing `gtts`  or to help with
    troubleshooting if `gtts` does not work when using your Linux package manager.

        sudo apt -y install python3-gtts

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
+ Pip Installer: `pip3 install gtts` (*Not* `sudo`!)

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
            readtexttools.get_work_file_path(_out_path, _icon, 'TEMP'), '.mp3'
        ])

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
            _msg = "Could not play a network media file locally. Try `pip3 install gtts`."
            if bool(_media_out):
                _msg = "Could not save a network media file locally. Try `pip3 install gtts`."
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


class LocalClass(object):
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

    [Default larnyx address](http://0.0.0.0:5002)

    [About Larynx...](https://github.com/rhasspy/larynx)'''

    def __init__(self):  # -> None
        '''Initialize data. See
        <https://github.com/rhasspy/larynx#basic-synthesis>'''
        _metadata = readtexttools.ImportedMetaData()
        self.ok = True
        # This is the default. You can set up Larynx to use a different port.
        self.url = 'http://0.0.0.0:5002'  # localhost port 5002
        self.vocoders = None  # ordered fast+normal to slow+high quality
        self.ssmls = [False, True]  # false = TEXT or true = SSML
        self.length_scales = [
            [320, 289, '---------|', '0.50'], [288, 257, '--------|-', '0.55'],
            [256, 225, '-------|--', '0.62'], [224, 193, '------|---', '0.71'],
            [192, 161, '-----|----', '0.83'], [128, 97, '---|-----', '1.25'],
            [96, 66, '--|------', '1.66'], [64, 33, '-|-------', '2.50'],
            [32, 0, '|--------', '5.00']
        ]  # A lower speed corresponds to a longer duration.
        # larynx `glow_tts` voices from larynx version 1.1.
        self.accept_voice = [
            '', 'all', 'auto', 'child_female', 'female1', 'female2', 'female3',
            'child_male', 'male1', 'male2', 'male3', 'larynx', 'localhost',
            'docker', 'local_server'
        ]
        self.spd_fm = ['female1', 'female2', 'female3', 'child_female']
        self.spd_m = ['male1', 'male2', 'male3', 'child_male']

        # The routine uses the default voice as a fallback. The routine
        # prioritizes a voice that you chose to install.
        self.default_lang = readtexttools.default_lang()
        self.default_voice = 'mary_ann'
        self.larynx_v1 = None
        if '_IN' in self.default_lang:
            self.larynx_v1 = ['cmu_aup', 'cmu_ksp', 'cmu_slp']
        elif self.default_lang == 'en_CA':
            self.larynx_v1 = ['cmu_jmk']
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
        if not 'female' in _search:
            for _voice in (_data_list):
                if _voice not in self.larynx_fm:
                    _voices = ''.join([_voices, _voice, '\n'])
            try:
                _resultat = _voices.strip().split('\n')[count_f]
            except IndexError:
                _resultat = ''
        if len(_resultat) != 0:
            return _resultat
        count_f = 0
        for count, _item in enumerate(self.spd_fm):
            if _item == _search:
                count_f = count
                break
        _voices = ''
        for _voice in (_data_list):
            if _voice in self.larynx_fm:
                _voices = ''.join([_voices, _voice, '\n'])
        try:
            _resultat = _voices.strip().split('\n')[count_f]
        except IndexError:
            _resultat = ''
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
                platform.python_version_tuple()[1]) < 9:
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
            print(
                '''Requested [larynx-server](https://github.com/rhasspy/larynx)
            It did not respond correctly.''')
            self.ok = False
            return False
        except AttributeError:
            try:
                response = urllib.urlopen(''.join([self.url, '/api/voices']))
                data_response = response.read()
                data = json.loads(data_response)
            except [AttributeError, urllib.error.URLError]:
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
                if _lang1 in data[_item]['language']:
                    larynx_names = ''.join(
                        [larynx_names, '\n', data[_item]['name']])
                elif _lang2 == data[_item]['language'].split('-')[0]:
                    larynx_names = ''.join(
                        [larynx_names, '\n', data[_item]['name']])
        larynx_names = larynx_names.strip()
        _vox = vox.lower()
        _verified_name = self._spd_voice_to_larynx_voice(_vox, larynx_names)
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
            for _item in data:
                if data[_item]['name'] == _verified_name:
                    self.voice_id = data[_item]['id']
                    self.ok = True
                    return self.ok
        self.ok = False
        for _item in data:
            if data[_item]['downloaded']:
                if _vox in [data[_item]['name'], data[_item]['id']]:
                    _voice_id = data[_item]['id']
                    self.voice_id = _voice_id
                    break
                elif _lang1 in [
                        data[_item]['id'], data[_item]['language'],
                        data[_item]['name']
                ]:
                    _voice_id = data[_item]['id']
                elif _lang2 == data[_item]['language'].split('-')[0]:
                    _voice_id = data[_item]['id']
                if len(_voice_id) != 0:
                    self.voice_id = _voice_id
                    self.ok = True
                    break
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
             _speech_rate=160,
             quality=1,
             ssml=False,
             _denoiserStrength=0.02,
             _noiseScale=0.333,
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
        _media_out = ''
        # Determine the output file name
        _media_out = readtexttools.get_work_file_path(_out_path, _icon, 'OUT')
        # Determine the temporary file name
        _media_work = readtexttools.get_work_file_path(_out_path, _icon,
                                                       'TEMP')
        _voice = self.voice_id
        _lengthScale = '0.85'
        try:
            if not self.is_x86_64:
                # Unknown platform - try the fastest setting.
                _vocoder = self.vocoders[0]
            elif quality in range(0, len(self.vocoders)):
                # Set manually
                _vocoder = self.vocoders[quality]
            elif len(_media_out) > 0:
                # Medium quality when saving file.
                _vocoder = self.vocoders[1]
            elif len(_text.split()) > 30:
                # Word count > 30 so use fastest setting.
                _vocoder = self.vocoders[0]
            else:
                _vocoder = self.vocoders[1]
        except IndexError:
            if bool(self.vocoders):
                _vocoder = self.vocoders[0]
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
                _lengthScale = _item[3]
                break
        if REQUESTS_OK:
            _text = '\n'.join(['', _text, ''])
            response = requests.post(
                _url,
                params={
                    'voice': _voice,
                    'vocoder': _vocoder,
                    'denoiserStrength': _denoiserStrength,
                    'noiseScale': _noiseScale,
                    'lengthScale': _lengthScale,
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
        elif readtexttools.have_posix_app('curl', False):
            if not bool(self.base_curl):
                return False
            _text = str(_text.translate(self.base_curl))
            _curl = '''curl -d "%(_text)s" "%(_url)s?voice=%(_voice)s&vocoder=%(_vocoder)s&denoiserStrength=%(_denoiserStrength)s&noiseScale=%(_noiseScale)s&lengthScale=%(_lengthScale)s&ssml=%(_ssml)s" -o "%(_media_work)s"''' % locals(
            )
            os.system(_curl)
        else:
            print('''The application cannot load a sound file.
Your computer is missing a required library.
Use `pip3 install requests` or `apt-get install python3-requests` to fix it.'''
                  )
            self.ok = False
            return False
        if os.path.getsize(_media_work) == 0:
            time.sleep(2)
        if os.path.isfile(_media_work) and _post_process in [
                'process_audio_media', 'process_wav_media'
        ]:
            if os.path.getsize(_media_work) == 0:
                return False
            # NOTE: Calling process must unlock_my_lock()
            readtexttools.process_wav_media(_info, _media_work, _icon,
                                            _media_out, _audible, _visible,
                                            _writer, _size)
            return True
        return False


def speech_wpm(_percent='100%'):  # -> int
    '''
    _percent - rate expressed as a percentage.
    Use '100%' for default rate of 160 words per minute (wpm).
    Returns rate between 20 and 640.
    '''
    i1 = 0
    i2 = 0
    _minimum = 20
    _maximum = 640
    _normal = 160
    s1 = ''

    try:
        if '%' in _percent:
            s1 = _percent.replace('%', '')
            i1 = (float(s1) if '.' in s1 else int(s1) / 100)
            i2 = math.ceil(i1 * _normal)
        else:
            i1 = (float(_percent) if '.' in _percent else int(_percent))
            i2 = math.ceil(i1)
    except TypeError:
        return _normal
    if i2 <= _minimum:
        return _minimum
    elif i2 >= _maximum:
        return _maximum
    return i2


def network_ok(_iso_lang='en-US', _local_url=''):  # -> bool
    '''Do at least one of the classes support an on-line speech library?'''
    _gtts_class = GoogleTranslateClass()
    _continue = False
    if _gtts_class.check_version(2.2):
        _continue = True
    if not _continue:
        _larynx = LocalClass()
        _continue = _larynx.language_supported(_iso_lang, _local_url, 'AUTO')
    if not _continue:
        _amazon_class = AmazonClass()
        _continue = bool(_amazon_class.language_supported(_iso_lang))
    if not _continue:
        _azure_class = AzureClass()
        _continue = bool(_azure_class.language_supported(_iso_lang))
    if not _continue:
        _google_cloud_class = GoogleCloudClass()
        _continue = bool(_google_cloud_class.language_supported(_iso_lang))
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
                 _local_url=''):  # -> boolean
    '''Read a text file aloud using a network resource.'''
    _imported_meta = readtexttools.ImportedMetaData()
    _larynx = LocalClass()
    _amazon_class = AmazonClass()
    _azure_class = AzureClass()
    _google_cloud_class = GoogleCloudClass()
    _gtts_class = GoogleTranslateClass()
    _continue = False
    _vox = _vox.strip('\'" \t\n').lower()
    _continue = _larynx.language_supported(
        _iso_lang,
        _local_url,
        _vox,
    ) and _vox in _larynx.accept_voice
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
        print(
            'No working network server was found, or the requested voice is unavailable.\n'
        )
        usage()
        return False
    _text = _imported_meta.meta_from_file(_text_file_in)
    if len(_text) != 0:
        _text = readtexttools.clean_str(_text, True).strip()
        _text = readtexttools.strip_mojibake(_iso_lang[:2].lower(), _text)
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
                         _speech_rate, _quality, _ssml)
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
            opts, args = getopt.getopt(sys.argv[1:], 'hovalritndsxu', [
                'help', 'output=', 'visible=', 'audible=', 'language=',
                'rate=', 'image=', 'title=', 'artist=', 'dimensions=',
                'speaker=', 'voice=', 'url='
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
            else:
                assert False, 'unhandled option'
        network_main(_text_file_in, _iso_lang, _visible, _audible, _media_out,
                     _writer, _title, _icon, _size, _speech_rate, _speaker,
                     _local_url)
    sys.exit(0)


if __name__ == '__main__':
    main()
