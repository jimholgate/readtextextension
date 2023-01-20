#!/usr/bin/env python
# -*- coding: UTF-8-*-
'''
Reads a text file using the rhvoice platform and a media player.

Install
-------

To enable rhvoice in Ubuntu 22.04, use:

    sudo apt install libportaudio2 librhvoice-audio2 \\
    librhvoice-core4 librhvoice5 rhvoice-english \\
    speech-dispatcher-rhvoice rhvoice

To add languages, add the appropriate packages

    sudo apt install rhvoice-brazilian-portuguese
    sudo apt install rhvoice-esperanto
    sudo apt install rhvoice-kyrgyz
    sudo apt install rhvoice-russian
    sudo apt install rhvoice-tatar
    sudo apt install rhvoice-ukrainian
    sudo apt install rhvoice-english

The command line interface that this script uses is depreciated, so
it might not continue to work, or it might not work as well as it
does when using `speech-dispatcher`, `docker rhvoice-rest` or `orca`.

If you configure `speech-dispatcher` to use `rhvoice` and enter
`"(SPD_READ_TEXT_PY)" "(TMP)"` in Read Text Extension's main
dialog then your system might have a smaller delay when you click
the *Read Selection* button before the voice starts speaking.

To enable rhvoice for speech-dispatcher in Ubuntu 22.04, use:

    sudo apt install speech-dispatcher-rhvoice

To install rhvoice on other linux platforms, use a docker image
like <https://hub.docker.com/r/aculeasis/rhvoice-rest>.

The available voices might vary according to the specific image. 
'''

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import getopt
import os
import sys
import readtexttools


def usage():  # -> None
    '''
    Command line help
    '''
    print('''
RhVoice Speech Synthesis
========================

Reads a text file using a synthetic voice and a media player
like ffmpeg or avconv.  Voices are available for

* Albanian
* Brazilian-Portuguese
* English
* Esperanto
* Kyrgyz
* Macedonian
* Polish
* Russian
* Tatar
* Ukrainian

Usage
-----

The language flag can be the iso Language or a specific voice.

    rhvoice_read_text_file.py --language=en-US --visible=False "input.txt"
    rhvoice_read_text_file.py --language=natalia --visible=False "input.txt"


To enable rhvoice in Ubuntu 22.04, use:

    sudo apt install libportaudio2 librhvoice-audio2 \\
    librhvoice-core4 librhvoice5 rhvoice-english \\
    speech-dispatcher-rhvoice rhvoice
''')


class RhVoiceClass(object):
    u''' The following notice should be displayed in a dialog when users click
    *About...* or the equivalent in their language when this class is enabled.

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

    The `rhvoice` libraries are enabled by electing to install it on a
    supported platform. Read the documentation for help installing the
    libraries or to help with troubleshooting if the tools do not work
    when using your Linux package manager.

    See:

    * <https://github.com/RHVoice/RHVoice>
    * <https://github.com/RHVoice/RHVoice/issues>
    * <https://rhvoice.org/>

    '''

    def __init__(self):  # -> None
        '''Initialize data'''
        self.ok = True
        self.app = 'RHVoice-test'
        self.domain_table = [
            {
                'package': 'Albanian',
                'sample': 'Përshëndetje. Unë jam një zë i sistemit shqiptar.',
                'iso_code': 'AL',
                'lang1': 'sq',
                'voices': ["hana"]
            },
            {
                'package': 'Brazilian-Portuguese',
                'sample': 'Olá. Eu sou a voz portuguesa do sistema.',
                'iso_code': 'BR',
                'lang1': 'pt',
                'voices': ["Letícia-F123"]  # Western European letters.
            },
            {
                'package':
                'English',
                'sample':
                'Hello. I am an English system voice.',
                'iso_code':
                'CA',
                'lang1':
                'en',
                'voices': [
                    "alan",  # en_GB.scotland Male
                    "bdl",  # en-US Male
                    "clb",  # en-US Female
                    "slt",  # en-US Female
                    "natalia",  # This `ua` voice can talk in English
                    "elena"
                ]  # This `ru` voice can talk in English
            },
            {
                'package': 'English',
                'sample': 'Hello. I am an English system voice.',
                'iso_code': 'KG',
                'lang1': 'en',
                'voices': ["alan", "bdl", "clb", "slt",
                           "nazgul"]  # This `ky-KG` voice can talk in English
            },
            {
                'package':
                'English',
                'sample':
                'Hello. I am an English system voice.',
                'iso_code':
                'GB',
                'lang1':
                'en',
                'voices': [
                    "alan",
                    "slt",
                    "clb",
                    "bdl",
                    "natalia",  # This `uk-UA` voice can talk in English
                    "elena"
                ]  # This `ru-RU` voice can talk in English
            },
            {
                'package': 'English',
                'sample': 'Hello. I am an English system voice.',
                'iso_code': 'RU',
                'lang1': 'en',
                'voices': ["alan", "slt", "clb", "bdl",
                           "elena"]  # This `ru-RU` voice can talk in English
            },
            {
                'package': 'English',
                'sample': 'Hello. I am an English system voice.',
                'iso_code': 'TA',
                'lang1': 'en',
                'voices': ["alan", "slt", "clb", "bdl",
                           "talgat"]  # This `tt-TA` voice can talk in English
            },
            {
                'package': 'English',
                'sample': 'Hello. I am an English system voice.',
                'iso_code': 'UK',
                'lang1': 'en',
                'voices': ["alan", "slt", "clb", "bdl",
                           "natalia"]  # This `uk-UA` voice can talk in English
            },
            {
                'package':
                'English',
                'sample':
                'Hello. I am an English system voice.',
                'iso_code':
                'US',
                'lang1':
                'en',
                'voices': [
                    "bdl",
                    "slt",
                    "clb",
                    "alan",
                    "natalia",  # This `uk-UA` voice can talk in English
                    "elena"
                ]  # This `ru-RU` voice can talk in English
            },
            {
                'package': 'Esperanto',
                'sample': 'Saluton. Mi estas la Esperanta voĉo de la sistemo.',
                'iso_code': 'PL',
                'lang1': 'eo',
                'voices': ["spomenka"]  # Western European letters.
            },
            {
                'package': 'Macedonian',
                'sample': 'Здраво. Јас сум глас на македонскиот систем.',
                'iso_code': 'MK',
                'lang1': 'mk',
                'voices': ["kiko", "suze"]
            },
            {
                'package': 'Kyrgyz',
                'sample': 'Салам. Мен системанын кыргыз үнүмун.',
                'iso_code': 'KG',
                'lang1': 'ky',
                'voices': ["azamat", "nazgul"]
            },
            {
                'package': 'Polish',
                'sample': 'Witam. Jestem polskim głosem systemowym.',
                'iso_code': 'PL',
                'lang1': 'pl',
                'voices': ["magda", "natan"]
            },
            {
                'package': 'Russian',
                'sample': 'Здравствуйте. Я - русский голос системы.',
                'iso_code': 'RU',
                'lang1': 'ru',
                'voices': ["aleksandr", "anna", "artemiy", "elena", "irina"]
            },
            {
                'package': 'Tatar',
                'sample': 'Салам. Мен системанын татар үнүмин.',
                'iso_code': 'TA',
                'lang1': 'tt',
                'voices': ["talgat"]
            },
            {
                'package': 'Ukrainian',
                'sample': 'Привет. Я украинский голос системы.',
                'iso_code': 'UA',
                'lang1': 'uk',
                'voices': ["anatol", "marianna", "natalia", "volodymyr"]
            }
        ]

    def read(self,
             _text="",
             _iso_lang='en-US',
             _visible="false",
             _audible="true",
             _out_path="",
             _icon="",
             _info="",
             _post_process='process_wav_media',
             _writer='',
             _size='600x600',
             _speech_rate='100'):  # -> bool
        '''

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
        _slow = False
        _lang_check = True
        _lang = _iso_lang
        _error_icon = readtexttools.net_error_icon()
        _env_lang = readtexttools.default_lang().split('_')[0].split('-')[0]
        _voice = self.language_to_voice(_iso_lang)
        if not bool(_voice):
            self.ok = False
            return False
        _media_out = ''
        # Determine the output file name
        _media_out = readtexttools.get_work_file_path(_out_path, _icon, 'OUT')
        # Determine the temporary file name
        _media_work = readtexttools.get_work_file_path(_out_path, _icon,
                                                       'TEMP')
        _text_work = ''.join([_media_work, '.txt'])

        # Remove old files.
        if os.path.isfile(_media_work):
            os.remove(_media_work)
        if os.path.isfile(_media_out):
            os.remove(_media_out)
        if os.path.isfile(_text_work):
            os.remove(_text_work)
        readtexttools.write_plain_text_file(_text_work, _text, 'utf-8')
        _app = self.app
        _speech_rate = readtexttools.safechars(_speech_rate, '1234567890')
        _command = '''%(_app)s -i '%(_text_work)s' -r %(_speech_rate)s -p %(_voice)s -o '%(_media_work)s'  
 ''' % locals()
        try:
            readtexttools.my_os_system(_command)
        except:
            self.ok = False
            return False
        if os.path.isfile(_media_work) and _post_process in [
                'process_wav_media', 'process_audio_media'
        ]:
            if os.path.getsize(_media_work) == 0:
                return False
            readtexttools.process_wav_media(_info, _media_work, _icon,
                                            _media_out, _audible, _visible,
                                            _writer, _size)
            return True
        else:
            _msg = "Could not play a rhvoice media file locally."
            if bool(_media_out):
                _msg = "Could not save a rhvoice media file locally."
            readtexttools.pop_message("Python `rhvoice`" % locals(), _msg,
                                      5000, _error_icon, 1)
        self.ok = False
        return False

    def voice_available(self, iso_lang='en-US', _check_list=None):  # -> bool
        '''Check if you have installed a language resource for
        a language or a voice.'''
        _voice = self.language_to_voice(iso_lang)
        if bool(_check_list):
            if _voice in _check_list:
                self.ok = True
                return True
        else:
            if os.path.isdir('/usr/share/RHVoice/voices/%(_voice)s' %
                             locals()):
                self.ok = True
                return True
        self.ok = False
        return False

    def first_good_voice(self, _voices=None, _check_list=None):  # -> string
        '''Check the default Linux installation for the first
        voice available from the `_voices` list. The preferred
        voice in English depends on the region. If English is not
        installed, try reading the text with the native voice.'''
        for test_voice in _voices:
            try:
                _voice = test_voice.strip()
                if bool(_voice):
                    if bool(_check_list):
                        if _voice in _check_list:
                            return _voice
                    else:
                        if os.path.isdir(
                                '/usr/share/RHVoice/voices/%(_voice)s' %
                                locals()):
                            return _voice
            except (AttributeError, SyntaxError):
                pass
        return ''

    def language_to_voice(self, iso_lang='en-US', _check_list=None):  # -> str
        '''Check if the library supports the language or voice.
        If so, return a voice in the language, otherwise return
        `''`.'''
        test_lang = ''
        test_region = ''
        try:
            for sep in ['-', '_']:
                if sep in iso_lang:
                    test_lang = iso_lang.split(sep)[0]
                    test_region = iso_lang.split(sep)[1]
                    break
        except (AttributeError, NameError):
            return ''
        try:
            domain_table = self.domain_table
            _tld = ''
            _lang1 = ''
            _region = ''
            _voices = ['']
            for i in range(len(domain_table)):
                _region = '-'.join(
                    [domain_table[i]['lang1'], domain_table[i]['iso_code']])
                if _region.strip() == iso_lang.strip():
                    return self.first_good_voice(domain_table[i]['voices'])
            for i in range(len(domain_table)):
                if domain_table[i]['lang1'] == test_lang.lower():
                    _tld = domain_table[i]['package']
                    _lang1 = domain_table[i]['lang1']
                    _region = '-'.join([_lang1, domain_table[i]['iso_code']])
                    _voices = domain_table[i]['voices']
                    break
            for _test in [iso_lang, test_lang]:
                if len(_voices[0]) == 0:
                    if len(_test) != 0:
                        if not '-' in _test:
                            return _test
                elif _test.lower() == _region.lower():
                    return self.first_good_voice(_voices, _check_list)
                elif _test.lower() == _lang1:
                    return self.first_good_voice(_voices, _check_list)
                elif _test.lower() == _tld.lower():
                    return self.first_good_voice(_voices, _check_list)
                elif _test in _voices:
                    return _test
                elif _test.lower() in _voices:
                    return self.first_good_voice(_voices, _check_list)
        except NameError:
            pass
        return ''


def main():  # -> NoReturn
    '''Use rhvoice speech synthesis for supported languages while on-line'''
    if not sys.version_info >= (3, 6) or not os.name in ['posix']:
        print('Your system does not support the rhvoice python tool.')
        usage()
        sys.exit(0)
    _imported_meta = readtexttools.ImportedMetaData()
    _speech_rate = 100
    _iso_lang = 'en-US'
    try:
        _iso_lang = readtexttools.default_lang().replace('_', '-')
    except AttributeError:
        pass
    _media_out = ''
    _visible = ''
    _audible = ''
    _text = ''
    _percent_rate = '100'
    _speech_rate = _percent_rate
    _icon = ''
    _title = ''
    _writer = ''
    _size = '600x600'
    _text_file_in = sys.argv[-1]

    if not os.path.isfile(_text_file_in):
        sys.exit(0)
    if sys.argv[-1] == sys.argv[0]:
        usage()
        sys.exit(0)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hovalritnd', [
            'help', 'output=', 'visible=', 'audible=', 'language=', 'rate=',
            'image=', 'title=', 'artist=', 'dimensions='
        ])
    except getopt.GetoptError:
        # print help information and exit
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
            _speech_rate = _percent_rate
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
    _rhvoice_cl = RhVoiceClass()
    _voice = _rhvoice_cl.language_to_voice(_iso_lang)
    if not _rhvoice_cl.voice_available(_voice):
        print('The %(_voice)s voice (%(_iso_lang)s) was not found.' % locals())
        usage()
        sys.exit(0)
    _text = _imported_meta.meta_from_file(_text_file_in)
    if len(_text) != 0:
        _text = readtexttools.clean_str(_text, True).strip()
        _text = readtexttools.strip_mojibake(_iso_lang[:2].lower(), _text)
        _info = readtexttools.check_artist(_writer)
        clip_title = readtexttools.check_title(_title, 'rhvoice')
        # If the library does not require a postprocess, use `0`,
        # otherwise use the item corresponding to the next action.
        _post_processes = [
            None, 'process_mp3_media', 'process_playlist',
            'process_riff_media', 'process_vorbis_media', 'process_wav_media',
            'process_audio_media'
        ]
        _rhvoice_cl.read(_text, _iso_lang, _visible, _audible, _media_out,
                         _icon, clip_title, _post_processes[5], _info, _size,
                         _speech_rate)
    sys.exit(0)


if __name__ == '__main__':
    main()
