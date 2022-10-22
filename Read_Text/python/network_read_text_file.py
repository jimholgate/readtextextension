﻿#!/usr/bin/env python
# -*- coding: UTF-8-*-
'''

Reads a text file using an online service and a media player.
Requires a network connection and installation of an online
connection library.

Check the terms and conditions that apply to the on-line service
provider. There may be acceptable use policies, limits or costs.

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
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import getopt
import math
import os
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
''')


def network_problem(voice='default'):  # -> str
    '''Return suggestions to make an on-line voice work.'''
    return '''Is the network connected?
=========================
    
+ The `%(voice)s` on-line voice is currently unavailable.
+ It might help to restart your device, refresh the network
  or check your on-line account status.''' %locals()


class AmazonClass(object):
    u''' The following notice should be displayed in a dialog when users click
    *About...* or the equivalent in their language when this class is enabled.

    Powered by Amazon\u2122 LLC

    "Amazon" is a trademark of Amazon LLC. '''

    # * <https://docs.aws.amazon.com/polly/latest/dg/examples-for-using-polly.html>
    def __init__(self):  # -> None
        '''Initialize data'''
        self.ok = True

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

    def read(self, _text="", _iso_lang='en-US', _visible="false",
             _audible="true", _out_path="", _icon="", _info="",
             _post_process=None, _writer='', _size='600x600',
             _speech_rate=160):  # -> bool
        '''stub'''
        if not self.ok:
            return False
        try:
            return awsserver.read(_text="", _iso_lang='en-US',
                                  _visible="false", _audible="true",
                                  _out_path="", _icon="", _info="", 
                                  _post_process=None, _writer='',
                                  _size='600x600', _speech_rate=160)
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

    def language_supported(self, iso_lang='ca-ES'):  # -> bool
        '''Is the language supported?'''
        try:
            self.ok = azureserver.language_supported(iso_lang)
        except (AttributeError, NameError):
            self.ok = False
        return self.ok

    def read(self, _text="", _iso_lang='en-US', _visible="false",
             _audible="true", _out_path="", _icon="", _info="",
             _post_process=None, _writer='', _size='600x600',
             _speech_rate=160):  # -> bool
        '''stub'''
        if not self.ok:
            return False
        try:
            return azureserver.read(_text="", _iso_lang='en-US',
                                    _visible="false", _audible="true",
                                    _out_path="", _icon="", _info="", 
                                    _post_process=None, _writer='',
                                    _size='600x600', _speech_rate=160)
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

    def language_supported(self, iso_lang='ca-ES'):  # -> bool
        '''Is the language supported?'''
        try:
            self.ok = gcloudserver.language_supported(iso_lang)
        except (AttributeError, NameError):
            self.ok = False
        return self.ok

    def read(self, _text="", _iso_lang='en-US', _visible="false",
             _audible="true", _out_path="", _icon="", _info="",
             _post_process=None, _writer='', _size='600x600',
             _speech_rate=160):  # -> bool
        '''stub'''
        if not self.ok:
            return False
        try:
            return  gcloudserver.read(_text="", _iso_lang='en-US',
                                      _visible="false", _audible="true",
                                      _out_path="", _icon="", _info="",
                                      _post_process=None, _writer='',
                                      _size='600x600', _speech_rate=160)
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
             _text="", _iso_lang='en-US', _visible="false", _audible="true",
             _out_path="", _icon="", _info="",
             _post_process=None, _writer='', _size='600x600',
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
        _provider_logo = '/usr/share/icons/hicolor/scalable/apps/goa-account-%(_domain)s.svg' %locals()

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
            _msg = 'https://translate.%(_domain)s.%(_tld)s' %locals()
        else:
            _msg = '`<https://translate.%(_domain)s.%(_tld)s?&langpair=auto|%(_lang2)s&tbb=1&ie=&hl=%(_env_lang)s&text=%(_short_text)s>' %locals()
        if not self.language_supported(_iso_lang):
            # Fallback: display a link to translate using Google Translate.
            readtexttools.pop_message(
                u"%(_provider)s Translate\u2122" %locals(), _msg, 5000,
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
                "`gtts-%(_version)s` failed to connect." % locals(), _msg, 5000,
                _error_icon, 2)
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


class LarynxClass(object):
    u'''Local voice server using Larynx'''
    def __init__(self):  # -> None
        '''Initialize data. See
        <https://github.com/rhasspy/larynx#basic-synthesis>'''
        _metadata = readtexttools.ImportedMetaData()
        self.ok = True
        self.url = 'http://0.0.0.0:5002'  # localhost port 5002
        self.vocoders = None  # ordered fast+normal to slow+high quality
        self.ssmls = [False, True]  # false = TEXT or true = SSML
        self.length_scales = [1.25, 1.00, 0.85]  # higher number is slower
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
        self.is_x86_64 = False
        if 'x86_64' in _metadata.execute_command('uname -a'):
            self.is_x86_64 = True
        else:
            try:
                if bool(os.getenv('ProgramFiles(x86)')):
                    self.is_x86_64 = True
            except:
                pass

    def _set_vocoders(self, alt_larynx_url=''):  # -> bool
        '''If the server is running, then get the list of voice coders.
        + `alt_larynx_url` If you are connecting to a local network's
           larynx server using a different computer, you might need to use
           a different url.'''
        if len(alt_larynx_url) != 0:
            self.url = alt_larynx_url
        data = {}
        if bool(self.vocoders):
            return True
        try:
            response = urllib.request.urlopen(''.join([self.url, '/api/vocoders']))
            data_response = response.read()
            data = json.loads(data_response)
        except urllib.error.URLError:
            print('''urllib.error.URLError
To use the larynx speech synthesis client, you need to initiate `larynx-server`.
[More...](https://github.com/rhasspy/larynx)''')
            self.ok = False
            return False
        except AttributeError:
            try:
                response = urllib.urlopen(''.join([self.url, 'api/vocoders']))
                data_response = response.read()
                data = json.loads(data_response)
            except [AttributeError, urllib.error.URLError]:
                self.ok = False
                return False
        if len(data) == 0:
            return False
        _nsv = ''
        for _jint in range(0, len(data)):
            _nsv = ''.join([_nsv, data[_jint]['id'], '\n'])
        self.vocoders = _nsv[:-1].split('\n')
        return True

    def language_supported(self, iso_lang='en-US', alt_larynx_url=''):  # -> bool
        '''Is the language or voice supported?
        + `iso_lang` can be in the form `en-US` or a voice like `eva_k`
        + `alt_larynx_url` If you are connecting to a local network's
           larynx server using a different computer, you might need to use
           a different url.'''
        if len(alt_larynx_url) != 0:
            self.url = alt_larynx_url
        if not REQUESTS_OK:
            if not readtexttools.have_posix_app('curl', False):
                self.ok = False
                return False
        self._set_vocoders(self.url)
        if len(self.voice_id) != 0:
            return True
        # format of json dictionary item: 'de-de/eva_k-glow_tts'
        # "voice" or "language and region"
        _lang1 = iso_lang.lower()
        # concise language
        _lang2 = iso_lang.lower()[:2]
        data = {}
        try:
            response = urllib.request.urlopen(''.join([self.url, '/api/voices']))
            data_response = response.read()
            data = json.loads(data_response)
        except urllib.error.URLError:
            print('''urllib.error.URLError
To use the larynx speech synthesis client, you need to initiate `larynx-server`.
[More...](https://github.com/rhasspy/larynx)''')
            self.ok = False
            return False
        except AttributeError:
            try:
                response = urllib.urlopen(''.join([self.url, 'api/voices']))
                data_response = response.read()
                data = json.loads(data_response)
            except [AttributeError, urllib.error.URLError]:
                self.ok = False
                return False
        if len(data) == 0:
            return False
        # Get each json data `dict`, then check each json
        # `string` against the supplied voice or language
        for _item in data:
            if data[_item]['downloaded']:
                for _query in [_lang1, _lang2]:
                    if _query in [data[_item]['id'],
                                  data[_item]['language'], data[_item]['name'],
                                  data[_item]['language'].split('-')[0]]:
                        self.ok = True
                        self.voice_id = data[_item]['id']
                        return True
        self.ok = False
        return False

    def read(self, _text="", _iso_lang='en-US', _visible="false",
             _audible="true", _out_path="", _icon="", _info="",
             _post_process=None, _writer='', _size='600x600',
             _speech_rate=160, quality=1, ssml=False):  # -> bool
        '''
        First, check larynx language support using `def language_supported`.
        Speak text aloud using a running instance of the
        [larynx-server](https://github.com/rhasspy/larynx)
        For most computers "highest" is too slow for
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
        _media_work = readtexttools.get_work_file_path(_out_path, _icon, 'TEMP')
        _voice = self.voice_id
        _length_scale = self.length_scales[2]
        if _speech_rate < 160:
            _length_scale = self.length_scales[1]
        elif _speech_rate > 160:
            _length_scale = self.length_scales[3]
        if not self.is_x86_64:
            # Unknown platform - try the fastest setting.
            _vocoder = self.vocoders[0]
        elif quality in range(0, len(self.vocoders)):
            # Set manually
            _vocoder = self.vocoders[quality]
        elif len(_media_out) > 0:
            # Medium quality when saving file.
            _vocoder = self.vocoders[1]
        elif len(_text.split()) > 20:
            # Word count > 20 so use fastest setting.
            _vocoder = self.vocoders[0]
        else:
            _vocoder = self.vocoders[1]
        _ssml = 'false'
        if ssml:
            _ssml = 'true'
        _url = ''.join([self.url, '/api/tts'])
        if not bool(self.base_curl):
            return False
        if REQUESTS_OK:
            _text = ''.join([_text, ' \n.'])
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            response = requests.post(
                '%(_url)s?voice=%(_voice)s&vocoder=%(_vocoder)s&denoiserStrength=0.005&noiseScale=0.667&lengthScale=%(_length_scale)s&ssml=%(_ssml)s' %locals(),
                headers=headers,
                data=_text.encode('utf-8'))
            with open(_media_work, 'wb') as f:
                f.write(response.content)
        else:
            _text = str(_text.translate(self.base_curl)).encode('utf-8')
            _curl = '''curl -d "%(_text)s" "%(_url)s?voice=%(_voice)s&vocoder=%(_vocoder)s&denoiserStrength=0.005&noiseScale=0.667&lengthScale=%(_length_scale)s&ssml=%(_ssml)s" -o "%(_media_work)s"''' %locals()
            os.system(_curl)
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


def network_ok(_iso_lang='en-US'):  # -> bool
    '''Do at least one of the classes support an on-line speech library?'''
    _gtts_class = GoogleTranslateClass()
    _continue = False
    if _gtts_class.check_version(2.2):
        _continue = True
    if not _continue:
        _larynx = LarynxClass()
        _continue = _larynx.language_supported(_iso_lang)
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


def network_main(_text_file_in='', _iso_lang='ca-ES', _visible='false',
                 _audible='true', _media_out='', _writer='', _title='',
                 _icon='', _size='600x600', _speech_rate=160, vox=''):  # -> boolean
    '''Read a text file aloud using a network resource.'''
    _imported_meta = readtexttools.ImportedMetaData()
    _larynx = LarynxClass()
    _amazon_class = AmazonClass()
    _azure_class = AzureClass()
    _google_cloud_class = GoogleCloudClass()
    _gtts_class = GoogleTranslateClass()
    _continue = False
    _continue = _larynx.language_supported(_iso_lang) and vox in ['', 'AUTO', 'LARYNX']
    if not _continue:
        _continue = _gtts_class.check_version(2.2) and vox in ['', 'AUTO', 'GTTS']
    if not _continue:
        _continue = bool(_amazon_class.language_supported(_iso_lang)) and vox in ['', 'AUTO', 'AWS']
    if not _continue:
        _continue = bool(_azure_class.language_supported(_iso_lang))  and vox in ['', 'AUTO', 'AZURE']
    if not _continue:
        _continue = bool(_google_cloud_class.language_supported(_iso_lang)) and vox in ['', 'AUTO', 'GOOGLECLOUD']
    if not _continue:
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
            'process_riff_media', 'process_vorbis_media',
            'process_wav_media', 'process_audio_media'
        ]
        if _larynx.language_supported(_iso_lang):
            _quality = -1  # Auto; Manual is 0 (lowest) to 2 (highest)
            _ssml = False
            _larynx.read(_text, _iso_lang, _visible, _audible,
                         _media_out, _icon, clip_title,
                         _post_processes[5], _info, _size,
                         _speech_rate, _quality, _ssml)
        elif _amazon_class.language_supported(_iso_lang):
            _amazon_class.read(_text, _iso_lang, _visible, _audible,
                               _media_out, _icon, clip_title,
                               _post_processes[1], _info, _size,
                               _speech_rate)
        elif _azure_class.language_supported(_iso_lang):
            _azure_class.read(_text, _iso_lang, _visible, _audible,
                              _media_out, _icon, clip_title,
                              _post_processes[1], _info, _size,
                              _speech_rate)
        elif _google_cloud_class.language_supported(_iso_lang):
            _google_cloud_class.read(_text, _iso_lang, _visible, _audible,
                                     _media_out, _icon, clip_title,
                                     _post_processes[1], _info, _size,
                                     _speech_rate)
        elif _gtts_class.language_supported(_iso_lang):

            _gtts_class.read(_text, _iso_lang, _visible, _audible,
                             _media_out, _icon, clip_title,
                             _post_processes[1], _info, _size, _speech_rate)
        else:
            # Just display a translation link.
            _gtts_class.read(_text, _iso_lang, _visible, _audible,
                             _media_out, _icon, clip_title,
                             _post_processes[0], _info, _size, _speech_rate)
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
        _iso_lang = readtexttools.default_lang().replace(
            '_', '-')
    except AttributeError:
        pass
    _media_out = ''
    _visible = ''
    _audible = ''
    _text = ''
    _percent_rate = '100%'
    _icon = ''
    _title = ''
    _writer = ''
    _size = '600x600'
    _text_file_in = sys.argv[-1]

    if os.path.isfile(_text_file_in):
        if sys.argv[-1] == sys.argv[0]:
            usage()
            sys.exit(0)
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hovalritnd', [
                'help', 'output=', 'visible=', 'audible=', 'language=', 'rate=',
                'image=', 'title=', 'artist=', 'dimensions='
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
                _speech_rate = speech_wpm(_percent_rate)
            elif o in ('-i', '--image'):
                _icon = a
            elif o in ('-t', '--title'):
                _title = a
            elif o in ('-n', '--artist'):
                _writer = a
            elif o in ('-d', '--dimensions'):
                _size = a
            else:
                assert False, 'unhandled option'
        network_main(_text_file_in, _iso_lang, _visible, _audible,
                     _media_out, _writer, _title, _icon, _size,
                     _speech_rate, 'AUTO')
    sys.exit(0)


if __name__ == '__main__':
    main()
