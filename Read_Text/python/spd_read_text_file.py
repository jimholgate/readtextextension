#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
This Posix Speech Toolkit enables multilingual speech on Posix operating
systems like MacOS and Linux. It includes tools to configure Speech Dispatcher
and Python scripts to enable text-to-speech conversion. It is possible to use
an online speech synthesizer in case the built-in speech synthesizer does not
support the requested language.

-----

Posix Speech Toolkit
====================

This toolkit enables multilingual speech on Posix operating systems like
MacOS and Linux.

Some voice tools might not be able to change the prosody, age or gender of
all voices in all languages. If your computer does not have a matching
voice region or style, it will try to find a close substitute.

MacOS
=====

### Check python 3

For local python scripts to work with MacOS, you might need to install
additional software. The specific details depend on the version of
MacOS that you are using.

One way to see if python3 is ready to go on your device is to run 
`python3 --version` in a terminal. If the program shows you a version
number, you are ready to use python3. Otherwise follow the python
website's instructions to install and set up the required software.

+ Getting started? See: [Overview](https://docs.python.org/3/using/mac.html)
+ Recently updated the system or python?  For each local library, run pip3.
  i.e.: `pip3 install --upgrade Pillow qrcode`
+ Still not working? Rename or remove your local python library
  i.e.: `mv ~/Library/Python/3.x/ ~/Library/Python/3.x_old/`. Reinstall any
  required libraries. i.e.: `pip3 install Pillow qrcode`
+ Still not working? See: [venv](https://docs.python.org/3/tutorial/venv.html)

### Optional voices

Apple makes several languages available with "Enhanced" versions of
voices that sound better than the default voices.

*System Settings - Accessibility - Spoken Content - System speech language*

### Menu options

External program:

    /usr/bin/python3

Command line options (default voice):

    "(SPD_READ_TEXT_PY)" "(TMP)"

or (specific language):

    "(SPD_READ_TEXT_PY)" --language "(SELECTION_LANGUAGE_CODE)" "(TMP)"

or (specific voice):

    "(SPD_READ_TEXT_PY)" --voice "Alex" "(TMP)"

Linux
=====

 * `spd-conf` - A tool for configuration of Speech Dispatcher and problem
    diagnostics
 * `spd-say` - send text-to-speech output request to speech-dispatcher
 * `speech-dispatcher` - server process managing speech requests in Speech
    Dispatcher

Read Selection... Dialog setup
------------------------------

External program:

        /usr/bin/python3

Command line options (default voice):

        "(SPD_READ_TEXT_PY)" "(TMP)"

or (specific language):

    "(SPD_READ_TEXT_PY)" --language "(SELECTION_LANGUAGE_CODE)" --voice "MALE1" "(TMP)"

Installation
------------

Many Linux distributions include speech dispatcher by default. If it is not
installed, you can install it using your normal package manager. For Debian
and Ubuntu, use:

    sudo apt-get install speech-dispatcher python3-speechd
    info spd-say
    info spd-conf
    spd-conf

Test the speech-dispatcher using the command:

    spd-say -t female1 -l en-US  "Testing 1 2 3"

For more information, read the documentation at the speech-dispatcher web site.

See also: [Speech
Dispatcher](http://cvs.freebsoft.org/doc/speechd/speech-dispatcher.html)

Resolving Problems
------------------

### You updated LibreOffice and now speech synthesis doesn't work

If you update the version using self-contained "secure" package, the
security settings of the package might prohibit your application from
running extensions that rely on system resources.

If you updated LibreOffice using a simple **snap store** user interface,
then the snap daemon will protect your computer by refusing permission to
run some third party applications. To run this extension, remove the snap
version, then reinstall the system LibreOffice using the following commands:

    sudo snap remove libreoffice
    sudo snap refresh
    sudo apt update
    sudo apt upgrade
    sudo apt install libreoffice

See also: [Classic Confinement : Introduction to
Snap](https://ubuntu.com/blog/how-to-snap-introducing-classic-confinement)

### The speech synthesizer produces distorted sound.

This python script uses a third party python library called `speechd` with
a daemon (background process) called `speech-dispatcher`.

You can test `speech dispatcher` with:

    spd-say -t female1 -l en-US  "Testing 1 2 3"

If your system includes the orca screen reader, you can test the system's
normal speech synthesis quality with:

    orca -s

You can resolve many problems by testing and updating your local
`speech-dispatcher` settings with the following command:

    spd-conf

Some languages might sound better if you change the `speech-dispatcher`
defaults.

Auto
====

If your python setup is configured to enable it, the `AUTO` voice enables
using on-line speech in case your built-in speech synthesizer does not
support the requested language. On MacOS, you need to install system-wide
`python3` developer tools that include `pip3`. On a supported platform,
open a console, type `pip3 list` and the system will prompt you to install
developer resources.

gTTS Library
------------

Powered by Google\u2122

"Google", "Google Cloud" and "Google Translate" are trademarks of Google Inc.

The contents of this resource are not affiliated with, sponsored by, or endorsed
by Google nor does the documention represent the views or opinions of Google or
Google personnel.

See also:

1. [gTTS](https://pypi.org/project/gTTS/)
2. [gTTS-token](https://pypi.org/project/gTTS-token/)

-----

[Read Text Extension](http://sites.google.com/site/readtextextension/)

Copyright (c) 2010 - 2023 James Holgate
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import codecs
import getopt
import os
import platform
import sys
import time
import espeak_read_text_file
import network_read_text_file
import openjtalk_read_text_file
import readtexttools
import rhvoice_read_text_file

USE_SPEECHD = True
try:
    import speechd
except ImportError:
    for test_path in ['/snap/libreoffice', '/var/', '/.var/']:
        if test_path in os.path.realpath(__file__):
            print('''
Using a *container* version of an office application could restrict your
computer's ability to run system python libraries.
''')
            # Run `main()` to show usage alternatives.
            USE_SPEECHD = False
    try:
        if USE_SPEECHD:
            import speechd_py as speechd
    except ImportError:
        USE_SPEECHD = False

NET_SERVICE_LIST = [
    'AUTO', 'NETWORK', 'AWS', 'AZURE', 'GOOGLECLOUD', 'GTTS', 'LARYNX',
    'MARYTTS'
]


def about_script(player='speech-dispatcher'):  # -> str
    '''Information about the python script'''
    if not bool(player):
        return ''
    gtts_data_source = ''
    module_help = '''
Use a specific output module
    spd_read_text_file.py --output_module "espeak-generic" "TextFile.txt" '''
    module_option = '[--output_module="xx"] '
    sample_voices = 'MALE1, FEMALE1, ... CHILD_FEMALE'
    sample_voice = 'MALE1'
    more_url = 'http://htmlpreview.github.io/?https://github.com/brailcom/speechd/blob/master/doc/speech-dispatcher.html'
    if os.path.isfile('/usr/bin/say'):
        player = 'say'
        if not os.path.isfile('/usr/bin/python'):
            # On MacOS the script only supports `gtts`` on `python3``
            gtts_data_source = u'''gtts
----

The optional `gtts` python3 library enables network speech
when a local voice is unavailable.

It isn't needed for most languages. Using network resources
for speech might reduce your privacy in some conditions.
Services might be subject to local laws, fees, policies,
limitations of liability or other terms and conditions.

Read the `gtts`[documentation](https://pypi.org/project/gTTS/),
the license and the [pip](https://pip.pypa.io/en/stable/)
information for installation instructions. 

    pip3 install gTTS

Use "AUTO" as the voice.

    spd_read_text_file.py --voice "AUTO" "TextFile.txt" 

The `gtts` library is powered by Google\u2122

"Google" and "Google Translate" are trademarks of Google Inc.

The contents of this resource are not affiliated with, sponsored by, or endorsed
by Google nor does the documention represent the views or opinions of Google or
Google personnel.
'''
        module_help = ''
        sample_voices = 'Alex, Alice, Alva, AUTO, ... Zosia'
        sample_voice = 'Alex'
        module_option = ''
        more_url = 'https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/SpeakText.html'

    return '''
Posix speech
============

Reads a text file using `%(player)s` -- a Posix system text to speech tool.

%(gtts_data_source)s
Usage
-----

    spd_read_text_file.py %(module_option)s[--language="xx"] \\ 
       [--voice="xx"] [--rate="nn"] input.txt 
%(module_help)s 

Use a specific language - en, fr, es...
    spd_read_text_file.py --language "fr" "TextFile.txt" 

Use a specific voice - %(sample_voices)s
    spd_read_text_file.py --voice "%(sample_voice)s" "TextFile.txt" 

To say the text slower - minimum -100
    spd_read_text_file.py --rate "-20" "TextFile.txt" 

To say the text faster - maximum 100
    spd_read_text_file.py --rate "20" "TextFile.txt"

[More](%(more_url)s)''' % locals()


def get_whoami():  # -> str
    '''Get the current user string'''
    whoami = ''
    for _env_key in ['USER', 'USERNAME', 'LOGNAME', 'PWD', 'HOME']:
        try:
            whoami = os.getenv(_env_key)
            if len(whoami) != 0:
                whoami = whoami.split(os.sep)[-1]
                break
        except TypeError:
            pass
    return whoami


def filterinputs(s0):
    '''
    Escape input for a bash shell.
        '''
    bsafe = False
    s1 = s0
    if os.name == 'nt':
        if '"' in s1:
            # use of "" is supported by Microsoft compiler-based executables
            # and batch files, but other programs might not use a standardized
            # escape sequence.  Using `\"` can have unintended consequences
            # with complex strings.  Single quotes do not signify a string
            # separator.
            s1 = s1.replace('"', '""')
    else:
        if '"' in s1:
            s1 = s1.replace('"', '\\"')
        if "'" in s1:
            s1 = s1.replace("'", "\\'")

        # Check for shellshock
        a1 = ['{', '}', '(', ')', ';', ':']
        for i, item in enumerate(a1):
            if (a1[i] in s1) is False:
                bsafe = True
                break

        if bsafe is False:
            a2 = ['{', '}', '(', ')']
            # Escape the problem characters with `\`
            for i, item in enumerate(a2):
                s1 = s1.replace(a2[i], ''.join(['\\', a2[i]]))
    return s1


def hard_reset(sd='speech-dispatcher'):  # -> bool
    '''kill posix process'''
    if not readtexttools.have_posix_app(sd, False):
        return False
    if not readtexttools.have_posix_app('killall', False):
        return False
    whoami = get_whoami()
    command = '''killall %(sd)s''' % locals()
    if whoami:
        command = '''killall -q -u %(whoami)s %(sd)s''' % locals()
    return readtexttools.my_os_system(command)


def usage():  # -> None
    '''Print information about the script to the console'''
    player = 'speech-dispatcher'
    _reset = USE_SPEECHD
    if os.path.isfile('/usr/bin/say'):
        _reset = True
        player = 'say'
    print(about_script(player))
    if _reset:
        hard_reset(player)


def guess_time(second_string, word_rate, _file_path, _language):  # -> int
    '''
        Estimate time in seconds for speech to finish
    '''
    i_rate = ((int(word_rate) * 0.8) + 100) / 100
    i_seconds = (1 + len(second_string) / 18)
    retval = i_rate * i_seconds
    if i_seconds < 60:
        _command = "/usr/bin/espeak"
        if os.path.isfile('/usr/bin/espeak-ng'):
            _command = '/usr/bin/espeak-ng'
        if 'nt' in os.name.lower():
            win_subdir = "eSpeak/command_line/espeak.exe"
            _command = readtexttools.get_nt_path(win_subdir)
        if os.path.isfile(_command):
            _wave = readtexttools.get_work_file_path("", "", "TEMP")
            try:
                espeak_read_text_file.espkread(_file_path, _language, "", "",
                                               _wave, "", "",
                                               "show_sound_length_seconds", "",
                                               "", 50, 160)
                retval = i_rate * (readtexttools.sound_length_seconds(_wave))
            except (AttributeError, TypeError, ImportError):
                # Library is missing or incorrect version
                print('A local library for guess_time is missing or damaged.')
                retval = i_rate * i_seconds
    return retval


def net_play(_file_spec='',
             _language='en-US',
             i_rate=0,
             _requested_voice=''):  # -> bool
    '''Attempt to play a sound from the network.'''
    if network_read_text_file.network_ok(_language):
        if _requested_voice.upper() in NET_SERVICE_LIST:
            net_rate = 160
            if i_rate < 0:
                net_rate = 110
            ret_val = network_read_text_file.network_main(
                _file_spec, _language, 'false', 'true', '', '', '', '',
                '600x600', net_rate, _requested_voice)
            readtexttools.unlock_my_lock()
            return bool(ret_val)
        else:
            readtexttools.unlock_my_lock()
        return True
    return False


class SpdFormats(object):
    '''
Linux Speech Daemon
===================
This class provides information about popular `speechd`
configurations.
    '''

    def __init__(self):  # -> None
        '''Define common settings'''
        self.open_jtalk = openjtalk_read_text_file.OpenJTalkClass()
        self.client_app = readtexttools.app_signature()
        self.xml_tool = readtexttools.XmlTransform()
        self.json_tools = readtexttools.JsonTools()
        self.imported_meta = readtexttools.ImportedMetaData()
        self.client_user = get_whoami()
        self.client = None
        self.py_m = platform.python_version_tuple()[0]
        # Speech dispatcher and network tools do not have all
        # voices for all languages, so a tool might substitute
        # a missing voice for one that it does have.
        self.rate_scales = [[320, 289, '---------|', 100],
                            [288, 195, '--------|-', 35],
                            [194, 132, '-------|--', 22],
                            [131, 193, '------|---', 15],
                            [192, 130, '-----|----', 10],
                            [129, 103, '----|----', 0],
                            [102, 96, '---|-----', -35],
                            [95, 66, '--|------', -42],
                            [65, 33, '-|-------', -50],
                            [32, 0, '|--------', -100]]
        self.all_voices = [
            'MALE3', 'MALE2', 'MALE1', 'FEMALE3', 'FEMALE2', 'FEMALE1',
            'CHILD_MALE', 'CHILD_FEMALE', 'AUTO', 'NETWORK', 'AWS', 'AZURE',
            'GOOGLECLOUD', 'GTTS'
        ]
        self.spd_voices = [
            'MALE3', 'MALE2', 'MALE1', 'FEMALE3', 'FEMALE2', 'FEMALE1',
            'CHILD_MALE', 'CHILD_FEMALE'
        ]
        self.stop_voice = 'TriggerAssertionError'
        # NOTE: speechd might reject a language when length of item > 2
        self.language_list = espeak_read_text_file.espk_languages()
        self.config_dir = '/etc/speech-dispatcher/modules'
        self.local_config = ''
        self.local_json = readtexttools.get_my_lock('json')
        self.json_content = ''
        try:
            self.spd_ok = bool(speechd)
        except:
            self.spd_ok = False
        if self.spd_ok:
            self.spd_ok = int(self.py_m) > 2
        try:
            if len(os.getenv('HOME')) != 0:
                local_config = os.path.join(
                    os.getenv('HOME'), '.config/speech-dispatcher/modules')
                if os.path.isdir(local_config):
                    self.local_config = local_config
        except Exception:
            pass

    def percent_to_spd(self, _percent_int=100):  # -> int
        '''Given a percent, returns an integer representing a speech
        rate to pass to speech-dispatcher. It is between `-100` and
        `100` but the actual speed will depend on the language, voice,
        settings and the text to speech tool.'''
        try:
            _percent_int = int(_percent_int)
        except AttributeError:
            return 0
        if _percent_int > 320:
            return 100
        for _item in self.rate_scales:
            if _percent_int <= _item[0] and _percent_int >= _item[1]:
                print(''.join(['speech rate : -100 [', _item[2], '] 100']))
                return _item[3]
        return 0

    def is_a_supported_language(self,
                                _lang='en',
                                experimental=False):  # -> Bool
        '''Verify that your installed speech synthesisers are *registered* with
        the selected language. If there's an error and `experimental` is `True`,
        then we return `True` if it is language that `espeak-ng` supports.'''
        _short_lang = _lang.split('-')[0].split('_')[0]
        _list = self.list_synthesis_languages(_lang)
        if not bool(_list):
            _list = self.list_synthesis_languages(_short_lang)
        if bool(_list):
            return True
        if experimental:
            _rhvoice = rhvoice_read_text_file.RhVoiceClass()
            if _short_lang in self.language_list:
                return True
            elif os.path.isfile(
                    '/usr/share/espeak-ng-data/%(_short_lang)s_dict' %
                    locals()):
                return True
            elif _rhvoice.voice_available(_short_lang):
                # rhvoice includes Ukrainian and other languages that might
                # not be included with espeak-ng or espeak
                return True
            elif _short_lang == 'ja':
                if os.path.exists(self.open_jtalk.dictionary):
                    return True
        return False

    def is_named_voice(self, _language, _voice='Bdl'):  # -> Bool
        '''Verify that `spd-say` lists the voice. '''
        _result = self.list_synthesis_voices(_language)
        if not bool(_result):
            return False
        if _voice in _result:
            return True
        return False

    def set_up(self):  # -> bool
        '''Set up the instance of speechd'''
        if not self.spd_ok:
            return False
        try:
            if sys.version_info.major == 3 and sys.version_info.minor < 9:
                # Your computer uses an older version of python3.
                # Sometimes speech-dispatcher sounds distorted and echoes
                # on first run.
                bug_cleaner = speechd.SSIPClient(self.client_app,
                                                 self.client_user, None, None)
                bug_cleaner.speak('\t')
                time.sleep(0.2)
                bug_cleaner.close()
            self.client = speechd.SSIPClient(self.client_app, self.client_user,
                                             None, None)
            return True
        except (AttributeError, ImportError, NameError, speechd.SpawnError,
                speechd.SSIPCommunicationError):
            return False

    def _switch_to_female(self, voice=''):  # -> bool
        '''If voice includes `FEMALE` or a network voice, return `True`'''
        if voice.count('FEMALE') != 0 or voice.upper() in NET_SERVICE_LIST:
            return True
        return False

    def speak_spd(self,
                  output_module='',
                  language='',
                  voice='',
                  i_rate=0,
                  _file_spec=''):  # -> bool
        '''Set user configuration settings'''
        _lock = readtexttools.get_my_lock("lock")
        _audio_players = readtexttools.PosixAudioPlayers()
        _try_voice = voice
        if voice not in self.all_voices:
            if voice not in [
                    'none', 'None', language,
                    language.split('-')[0].split('_')[0]
            ]:
                if self.is_named_voice(language, voice):
                    _try_voice = voice.strip()
                else:
                    _try_voice = "MALE1"
            else:
                _try_voice = "AUTO"  # pass on except: or use alternate
        if os.path.isfile(_lock):
            _try_voice = self.stop_voice
        else:
            readtexttools.lock_my_lock()
        try:
            if bool(output_module):
                try:
                    self.client.set_output_module(output_module)
                except AssertionError:
                    pass
            if bool(language):
                # speechd `client.py` : Len(Language) == 2
                try:
                    self.client.set_language(language)
                except AssertionError:
                    try:
                        self.client.set_language(language[:2])
                    except AssertionError:
                        pass
            try:
                if bool(_try_voice):
                    self.client.set_voice(_try_voice)
            except AssertionError:
                if _try_voice == self.stop_voice:
                    self.client.close()
                    time.sleep(0.2)
                    hard_reset('speech-dispatcher')
                    readtexttools.unlock_my_lock()
                    return True
                elif not self.is_a_supported_language(
                        language, not os.path.isfile('/usr/bin/spd-say')):
                    self.client.close()
                    hard_reset('speech-dispatcher')
                    time.sleep(0.2)
                    readtexttools.unlock_my_lock()
                    if os.path.isfile(self.local_json):
                        # Using the json file as a lock file. The lock
                        # lock file works if and only if the network
                        # media creator returns an audio file that is
                        # normally playable with your computer's media
                        # player.
                        for _application in _audio_players.player_applications(
                        ):
                            hard_reset(_application)
                        os.remove(self.local_json)
                    else:
                        self.json_content = self.json_tools.set_json_content(
                            language, voice, i_rate, _file_spec, output_module)
                        readtexttools.write_plain_text_file(
                            self.local_json, self.json_content, 'utf-8')
                        retval = net_play(_file_spec, language, i_rate, voice)
                        if not retval:
                            print(
                                network_read_text_file.network_problem(voice))
                        os.remove(self.local_json)
                        return retval
                    return False
            else:
                pass
            try:
                self.client.set_rate(i_rate)
            except AssertionError:
                pass
        except (ImportError, NameError, speechd.SpawnError):
            if len(voice) != 0:
                self.json_content = self.json_tools.set_json_content(
                    language, voice, i_rate, _file_spec, output_module)
                readtexttools.write_plain_text_file(self.local_json,
                                                    self.json_content, 'utf-8')
                retval = net_play(_file_spec, language, i_rate, voice)
                os.remove(self.local_json)
                readtexttools.unlock_my_lock()
                return retval
            else:
                readtexttools.unlock_my_lock()
            return False
        try:
            f = codecs.open(_file_spec,
                            mode='r',
                            encoding=sys.getfilesystemencoding())
        except IOError:
            print("I was unable to open the file you specified!")
            usage()
            return False
        _txt = f.read()
        f.close()
        if len(_txt) == 0:
            self.client.close()
            readtexttools.unlock_my_lock()
            return False
        concise_lang = ''.join([language.lower(),
                                '-']).split('-')[0].split('_')[0]
        _txt = readtexttools.strip_xml(_txt)
        _txt = readtexttools.strip_mojibake(concise_lang, _txt)
        try:
            if os.uname()[1] in ['centos', 'fedora', 'rhel']:
                # `espeak-ng` for `speechd` on fedora 5.18.18-200.fc36.x86_64
                # changes the pitch of capitalized words. This could make the
                # synthesized speech hard to understand.
                _txt = _txt.lower()
        except [AttributeError, TypeError]:
            pass
        if self.xml_tool.use_mode in ['text']:
            _message = ' " %(_txt)s"' % locals()
        else:
            # This tool uses standard XML; no need to modify text beyond cleanup.
            _txt = self.xml_tool.clean_for_xml(_txt, False).replace('\\"', '"')
            _message = '''<?xml version='1.0'?>
<speak version='1.1' xml:lang='%(language)s'>%(_txt)s</speak>''' % locals()
        _time = guess_time(_txt, i_rate, _file_spec, language)
        self.client.set_data_mode(self.xml_tool.use_mode)
        self.client.set_punctuation(speechd.PunctuationMode.SOME)
        _voice_list = None
        # Try to match requested gender and locale for supported synthesizers
        try:
            _client_voices = self.list_synthesis_voices(language.split('-')[0])
            # Bare `except` because when using a Linux appimage, we get a
            # TypeError: catching classes that do not inherit from
            # BaseException is not allowed if we include specific exceptions.
        except:
            _client_voices = [""]
        if language[:2] == 'de':
            if self._switch_to_female(voice):
                _voice_list = [
                    'eva_k', 'hokuspokus', 'kerstin',
                    'rebecca_braunert_plunkett', 'karlsson', 'pavoque',
                    'thorsten', 'German+female1'
                ]
            else:
                _voice_list = [
                    'karlsson', 'pavoque', 'thorsten', 'eva_k', 'hokuspokus',
                    'kerstin', 'rebecca_braunert_plunkett', 'German'
                ]
        elif language in [
                'en-AS', 'en-PH', 'en-PR', 'en-UM', 'en-US', 'en-VI'
        ]:
            if self._switch_to_female(voice):
                _voice_list = [
                    'Slt', 'cmu_slt', 'Clb', 'cmu_clb', 'ek', 'harvard',
                    'judy_bieber', 'kathleen', 'ljspeech', 'cmu_eey',
                    'cmu_ljm', 'cmu_lnh', 'blizzard_lessac', 'mary_ann',
                    'samantha', 'blizzard_fls', 'southern_english_female',
                    'cmu_slp', 'Bdl', 'cmu_bdl', 'Alan',
                    'southern_english_male', 'northern_english_male',
                    'cmu_ahw', 'cmu_aup', 'cmu_fem', 'cmu_jmk', 'cmu_ksp',
                    'cmu_rms', 'cmu_rxr', 'scottish_english_male',
                    'English (America)+female1'
                ]
            else:
                _voice_list = [
                    'Bdl', 'cmu_bdl', 'Alan', 'southern_english_male',
                    'northern_english_male', 'cmu_ahw', 'cmu_aup', 'cmu_fem',
                    'cmu_jmk', 'cmu_ksp', 'cmu_rms', 'cmu_rxr',
                    'scottish_english_male', 'Clb', 'cmu_clb', 'ek', 'harvard',
                    'judy_bieber', 'kathleen', 'ljspeech', 'cmu_eey',
                    'cmu_ljm', 'cmu_lnh', 'Slt', 'cmu_slt', 'blizzard_lessac',
                    'mary_ann', 'samantha', 'blizzard_fls',
                    'southern_english_female', 'cmu_slp',
                    'English (America)+male1'
                ]
        elif language == 'en-IN':
            if self._switch_to_female(voice):
                _voice_list = [
                    'cmu_slp', 'serena', 'blizzard_fls',
                    'southern_english_female', 'blizzard_lessac', 'mary_ann',
                    'Slt', 'cmu_slt', 'Clb', 'cmu_clb', 'ek', 'harvard',
                    'judy_bieber', 'kathleen', 'ljspeech', 'cmu_eey',
                    'cmu_ljm', 'cmu_lnh', 'cmu_ahw', 'Alan',
                    'southern_english_male', 'northern_english_male',
                    'cmu_aew', 'cmu_aup', 'cmu_fem', 'cmu_jmk', 'cmu_ksp',
                    'cmu_rms', 'cmu_rxr', 'scottish_english_male', 'Bdl',
                    'cmu_bdl', 'English+female1'
                ]
            else:
                _voice_list = [
                    'cmu_ahw', 'Alan', 'southern_english_male',
                    'northern_english_male', 'cmu_aew', 'cmu_aup', 'cmu_fem',
                    'cmu_jmk', 'cmu_ksp', 'cmu_rms', 'cmu_rxr',
                    'scottish_english_male', 'Bdl', 'cmu_bdl',
                    'blizzard_lessac', 'mary_ann', 'cmu_slp', 'Clb', 'cmu_clb',
                    'ek', 'harvard', 'judy_bieber', 'kathleen', 'ljspeech',
                    'cmu_eey', 'cmu_ljm', 'cmu_lnh', 'Slt', 'cmu_slt',
                    'serena', 'blizzard_fls', 'southern_english_female',
                    'English'
                ]
        elif language[:2] == 'en':
            if self._switch_to_female(voice):
                _voice_list = [
                    'serena', 'blizzard_fls', 'southern_english_female',
                    'blizzard_lessac', 'mary_ann', 'cmu_slp', 'Slt', 'cmu_slt',
                    'Clb', 'cmu_clb', 'ek', 'harvard', 'judy_bieber',
                    'kathleen', 'ljspeech', 'cmu_eey', 'cmu_ljm', 'cmu_lnh',
                    'Alan', 'southern_english_male', 'northern_english_male',
                    'cmu_aew', 'cmu_ahw', 'cmu_aup', 'cmu_fem', 'cmu_jmk',
                    'cmu_ksp', 'cmu_rms', 'cmu_rxr', 'scottish_english_male',
                    'Bdl', 'cmu_bdl', 'English+female1'
                ]
            else:
                _voice_list = [
                    'Alan', 'southern_english_male', 'northern_english_male',
                    'cmu_aew', 'cmu_ahw', 'cmu_aup', 'cmu_fem', 'cmu_jmk',
                    'cmu_ksp', 'cmu_rms', 'cmu_rxr', 'scottish_english_male',
                    'Bdl', 'cmu_bdl', 'blizzard_lessac', 'mary_ann', 'Clb',
                    'cmu_clb', 'ek', 'harvard', 'judy_bieber', 'kathleen',
                    'ljspeech', 'cmu_eey', 'cmu_ljm', 'cmu_lnh', 'Slt',
                    'cmu_slt', 'serena', 'blizzard_fls',
                    'southern_english_female', 'cmu_slp', 'English'
                ]
        elif language[:2] == 'es':
            if self._switch_to_female(voice):
                _voice_list = ['karen_savage', 'carlfm', 'Spanish+female1']
            else:
                _voice_list = ['carlfm', 'karen_savage', 'Spanish']
        elif language == 'fr-CA':
            if self._switch_to_female(voice):
                _voice_list = [
                    'siwis', 'tom', 'gilles_le_blanc', 'French+female1'
                ]
            else:
                _voice_list = ['tom', 'gilles_le_blanc', 'siwis', 'French']
        elif language[:2] == 'fr':
            if self._switch_to_female(voice):
                _voice_list = [
                    'siwis', 'gilles_le_blanc', 'tom'
                    'French+female1'
                ]
            else:
                _voice_list = ['gilles_le_blanc', 'tom', 'siwis', 'French']
        elif language[:2] == 'it':
            if self._switch_to_female(voice):
                _voice_list = ['lisa', 'riccardo_fasol', 'Italian+female1']
            else:
                _voice_list = ['riccardo_fasol', 'lisa', 'Italian']
        elif language[:2] == 'kg':
            if self._switch_to_female(voice):
                _voice_list = ['Azamat', 'Nazgul', 'Kyrgyz+female1']
            else:
                _voice_list = ['Nazgul', 'Azamat', 'Kyrgyz']
        elif language[:2] == 'nl':
            if self._switch_to_female(voice):
                _voice_list = [
                    'nathalie', 'bart_de_leeuw', 'flemishguy', 'rdh',
                    'Dutch+female1'
                ]
            else:
                _voice_list = [
                    'bart_de_leeuw', 'flemishguy', 'rdh', 'nathalie', 'Dutch'
                ]
        elif language[:2] == 'pl':
            if self._switch_to_female(voice):
                _voice_list = ['Magda', 'Natan', 'Polish+female1']
            else:
                _voice_list = ['Natan', 'Magda', 'Polish']
        elif language[:2] == 'ru':
            if self._switch_to_female(voice):
                _voice_list = [
                    'Anna', 'Elena', 'Aleksandr', 'Artemiy', 'hajdurova',
                    'minaev', 'nikolaev', 'Russian+female1'
                ]
            else:
                _voice_list = [
                    'Aleksandr', 'Artemiy', 'hajdurova', 'minaev', 'nikolaev',
                    'Anna', 'Elena', 'Russian'
                ]
        elif language[:2] == 'sv':
            if self._switch_to_female(voice):
                _voice_list = ['talesyntese', 'Swedish+female1']
            else:
                _voice_list = ['talesyntese', 'Swedish']
        elif language[:2] == 'sw':
            if self._switch_to_female(voice):
                _voice_list = ['biblia_takatifu', 'Swahili+female1']
            else:
                _voice_list = ['biblia_takatifu', 'Swahili']
        elif language[:2] == 'uk':
            if self._switch_to_female(voice):
                _voice_list = ['Natalia', 'Anatol', 'Ukrainian+female1']
            else:
                _voice_list = ['Anatol', 'Natalia', 'Ukrainian']
        else:
            _voice_list = [voice]
        for test_voice in _voice_list:
            if test_voice in _client_voices:
                try:
                    self.client.set_synthesis_voice(test_voice)
                    break
                except (AttributeError, SyntaxError, TypeError):
                    pass
        self.client.speak(_message)
        time.sleep(_time)
        self.client.close()
        readtexttools.unlock_my_lock()
        return True

    def list_synthesis_languages(self, _language=''):  # -> (tuple | None)
        '''if `language == `''` then list all synthesis languages.
        if the language is a string, then return a one item list if the
        language is supported.'''
        string_list = ''
        _lang = _language.split('-')[0]
        _iso = ''
        if bool(self.client):
            for _item in self.client.list_synthesis_voices():
                _iso = _item[1].split('-')[0]
                if string_list.count(_lang) == 0:
                    if bool(_language):
                        if _lang in [_item[1]] or _language in [_item[1]]:
                            string_list = string_list + _item[1] + ':'
                            break
                        elif _lang == _iso:
                            string_list = string_list + _iso + ':'
                            break
                    else:
                        string_list = string_list + _item[1] + ':'
            if len(string_list) > 1:
                return string_list[:-1].split(':')
        return None

    def list_synthesis_voices(self, _language=''):  # -> (tuple | None)
        '''List synthesis voices. i. e.: ('Alan', 'southern_english_male', 'northern_english_male', 'Slt',...)'''
        string_list = ''
        if bool(self.client):
            for _item in self.client.list_synthesis_voices():
                if bool(_language):
                    if _language in [_item[1], _item[2]]:
                        string_list = string_list + _item[0] + ':'
                else:
                    string_list = string_list + _item[0] + ':'
            return string_list[:-1].split(':')
        return None

    def list_output_modules(self):  # -> (tuple | None)
        '''List available output modules. i. e.: (espeak-ng-mbrola, espeak-ng,
        rhvoice, pico, festival, festvox ...)'''
        if bool(self.client):
            return self.client.list_output_modules()
        return None


def app_info_extract(app='say',
                     tmp_file_name='say.txt',
                     ask='voice',
                     grep_filter='',
                     check_for_string='',
                     _remove=False):  # -> str
    '''* `say --voice="?"`
    * `say --voice="?" | grep "en_"`

    Return app information with `?` wildcard.

    * `grep_filter` is ignored if it doesn't start with `| grep `.
    * Use `| grep "en_"` not `"en_"`'''
    if not ask.startswith('-'):
        ask = "--%(ask)s='?'" % locals()
    _fmd = readtexttools.ImportedMetaData()
    _grep = ''
    if grep_filter.startswith('| grep '):
        _grep = ' %(grep_filter)s' % locals()
    _app_out = readtexttools.get_my_lock(tmp_file_name)
    s1 = ""
    try:
        if not os.path.isfile(_app_out):
            os.system("%(app)s %(ask)s%(_grep)s > %(_app_out)s" % locals())
        if os.path.isfile(_app_out):
            if os.path.getsize(_app_out) == 0:
                os.remove(_app_out)
            else:
                s1 = _fmd.meta_from_file(_app_out, _remove)
    except:
        return ''
    if len(check_for_string) == 0:
        return s1
    elif check_for_string in s1:
        return s1
    return ''


class SayFormats(object):
    '''
    MacOS voices
    ============

    This class provides information about MacOS platform's voice
    options.

    If your system has say and say's path is in your system paths,
    then

    + `SayFormats.voice('xxx')` returns (string) like `Alex` if
         supported.
    + `SayFormats.languagecountry('xxx')')` returns (string) like
      `en_US` if supported.
    + `SayFormats.voicesampletext('xxx')')` returns (string) like
        `Hallo, mijn naam is Xander. Ik ben een Nederlandse stem.`
        if `say` supports the language.

    or else the function returns "".  See the help for each public
    `def` for more information.
    '''

    def __init__(self):
        '''
        Def that initializes characteristics of the installed version
        of say.'''
        no_debug = 0
        debug_inspect_output = 1
        self.debug = [no_debug, debug_inspect_output][0]
        # First item must be `''` for `grep` command to work.
        self.block_list = ['Agnes', 'Albert']
        self.grep_block_list = ['', 'Agnes', 'Albert', 'Enhanced', 'Premium']
        s1 = ''
        self._i = ''
        self._f = ''
        self.is_mac = os.path.isfile('/usr/bin/say')
        # On MacOS systems, we specify the complete path`/usr/bin/say`.
        # Modify default word rate for a voice using last column in
        # the spd_table
        self.json_string = ''
        try:
            self.uname_major_ver = int(os.uname().release.split('.')[0])
        except [AttributeError, IndexError, ValueError]:
            self.uname_major_ver = 0
        self.word_rate = 0
        self.app = ''
        self.lock = readtexttools.get_my_lock("lock")
        self.always = -1
        self.premium = 4
        self.osx_11_13 = 3
        self.osx_13 = 2
        self.old = 1
        self.voice_found = ''
        if self.uname_major_ver > 21:
            self.editions = [self.osx_13, self.osx_11_13, self.always]
        else:
            self.editions = [self.old, self.osx_11_13, self.always]
        self.wpm = 0
        # For a first occurance of a locale, use a rate suitable for learners.
        # Subsequent occurances of the locale (MALE2 etc.) can use different
        # rates. Local users can adjust the rates in the main menu.
        self.spd_table = [
            ['Alex', 'en_US', self.always, 'MALE1', 161],
            ['Daniel', 'en_GB', self.osx_11_13, 'MALE1', 181],
            ['Juan', 'es_MX', self.old, 'MALE1', 181],
            ['Jorge', 'es_ES', self.old, 'MALE1', 181],
            ['Diego', 'es_AR', self.old, 'MALE1', 181],
            ['Luca', 'it_IT', self.old, 'MALE1', 181],
            ['Maged', 'ar_SA', self.old, 'MALE1', 181],
            ['Rishi', 'en_IN', self.osx_13, 'MALE1', 181],
            ['Samantha', 'en_US', self.osx_11_13, 'FEMALE1', 161],
            ['Serena', 'en_GB', self.osx_13, 'FEMALE1', 181],
            ['Thomas', 'fr_FR', self.osx_11_13, 'MALE1', 161],
            ['Xander', 'nl_NL', self.osx_11_13, 'MALE1', 145],
            ['Yelda', 'tr_TR', self.osx_11_13, 'MALE1', 145],
            ['Yuri', 'ru_RU', self.old, 'MALE1', 145],
            ['Eddy (Finnish (Finland))', 'fi_FI', self.osx_13, 'MALE1', 145],
            ['Eddy (French (Canada))', 'fr_CA', self.osx_13, 'MALE1', 145],
            ['Eddy (German (Germany))', 'de_DE', self.osx_13, 'MALE1', 145],
            ['Eddy (Italian (Italy))', 'it_IT', self.osx_13, 'MALE1', 145],
            ['Eddy (Spanish (Mexico))', 'es_MX', self.osx_13, 'MALE1', 145],
            ['Eddy (Spanish (Spain))', 'es_ES', self.osx_13, 'MALE1', 145],
            ['Alice', 'it_IT', self.osx_11_13, 'FEMALE1', 145],
            ['Alva', 'sv_SE', self.osx_11_13, 'FEMALE1', 145],
            ['Amelie', 'fr_CA', self.old, 'FEMALE1', 145],
            ['Amélie', 'fr_CA', self.osx_13, 'FEMALE1', 181],
            ['Anna', 'de_DE', self.osx_11_13, 'FEMALE1', 145],
            ['Carmit', 'he_IL', self.osx_11_13, 'FEMALE1', 145],
            ['Ellen', 'nl_BE', self.osx_11_13, 'FEMALE1', 145],
            ['Ioana', 'ro_RO', self.osx_11_13, 'FEMALE1', 145],
            ['Kanya', 'th_TH', self.osx_11_13, 'FEMALE1', 145],
            ['Karen', 'en_AU', self.osx_11_13, 'FEMALE1', 181],
            ['Kyoko', 'ja_JP', self.osx_11_13, 'FEMALE1', 145],
            ['Laura', 'sk_SK', self.osx_11_13, 'FEMALE1', 145],
            ['Lekha', 'hi_IN', self.osx_11_13, 'FEMALE1', 145],
            ['Luciana', 'pt_BR', self.osx_11_13, 'FEMALE1', 145],
            ['Mariska', 'hu_HU', self.old, 'FEMALE1', 145],
            ['Mei-Jia', 'zh_TW', self.old, 'FEMALE1', 145],
            ['Melina', 'el_GR', self.osx_11_13, 'FEMALE1', 145],
            ['Milena', 'ru_RU', self.osx_11_13, 'FEMALE1', 145],
            ['Moira', 'en_IE', self.osx_11_13, 'FEMALE1', 181],
            ['Monica', 'es_ES', self.old, 'FEMALE1', 146],
            ['Mónica', 'es_ES', self.osx_13, 'FEMALE1', 146],
            ['Nora', 'nb_NO', self.osx_11_13, 'FEMALE1', 145],
            ['Paulina', 'es_MX', self.osx_11_13, 'FEMALE1', 181],
            ['Sara', 'da_DK', self.osx_11_13, 'FEMALE1', 145],
            ['Satu', 'fi_FI', self.osx_11_13, 'FEMALE1', 145],
            ['Sin-ji', 'zh_HK', self.old, 'FEMALE1', 145],
            ['Tessa', 'en_ZA', self.osx_11_13, 'FEMALE1', 181],
            ['Ting-Ting', 'zh_CN', self.old, 'FEMALE1', 145],
            ['Veena', 'en_IN', self.osx_11_13, 'FEMALE1', 181],
            ['Yuna', 'ko_KR', self.osx_11_13, 'FEMALE1', 145],
            ['Zosia', 'pl_PL', self.osx_11_13, 'FEMALE1', 145],
            ['Zuzana', 'cs_CZ', self.osx_11_13, 'FEMALE1', 145],
            [
                'Flo (French (France))', 'fr_FR', self.osx_13, 'CHILD_FEMALE2',
                131
            ],
            [
                'Flo (Spanish (Mexico))', 'es_MX', self.osx_13,
                'CHILD_FEMALE2', 131
            ], ['Eddy (English (U.S.))', 'en_US', self.osx_13, 'MALE2', 145],
            ['Grandpa (English (U.S.))', 'en_US', self.osx_13, 'MALE3', 145],
            ['Reed (English (U.S.))', 'en_US', self.osx_13, 'MALE4', 146],
            ['Rocko (English (U.S.))', 'en_US', self.osx_13, 'MALE5', 145],
            ['Bruce', 'en_US', self.osx_13, 'MALE6', 145],
            ['Fred', 'en_US', self.osx_11_13, 'MALE7', 146],
            ['Ralph', 'en_US', self.osx_13, 'MALE8', 145],
            ['Junior', 'en_US', self.osx_13, 'CHILD_MALE1', 145],
            ['Superstar', 'en_US', self.osx_13, 'CHILD_FEMALE2', 145],
            [
                'Flo (English (U.S.))', 'en_US', self.osx_13, 'CHILD_FEMALE2',
                131
            ],
            ['Grandma (English (U.S.))', 'en_US', self.osx_13, 'FEMALE3', 146],
            ['Shelley (English (U.S.))', 'en_US', self.osx_13, 'FEMALE4', 146],
            [
                'Sandy (English (U.S.))', 'en_US', self.osx_13,
                'CHILD_FEMALE1', 145
            ], ['Oliver', 'en_GB', self.osx_11_13, 'MALE2', 181],
            ['Flo (German (Germany))', 'de_DE', self.osx_13, 'FEMALE2', 131],
            [
                'Grandma (German (Germany))', 'de_DE', self.osx_13, 'FEMALE3',
                146
            ],
            [
                'Shelley (German (Germany))', 'de_DE', self.osx_13, 'FEMALE4',
                146
            ],
            [
                'Sandy (German (Germany))', 'de_DE', self.osx_13,
                'CHILD_FEMALE1', 145
            ],
            ['Grandpa (German (Germany))', 'de_DE', self.osx_13, 'MALE2', 145],
            ['Reed (German (Germany))', 'de_DE', self.osx_13, 'MALE3', 145],
            ['Rocko (German (Germany))', 'de_DE', self.osx_13, 'MALE4', 145],
            [
                'Flo (English (U.K.))', 'en_GB', self.osx_13, 'CHILD_FEMALE2',
                131
            ],
            ['Grandma (English (U.K.))', 'en_GB', self.osx_13, 'FEMALE3', 146],
            ['Kate', 'en_GB', self.osx_13, 'FEMALE4', 181],
            [
                'Sandy (English (U.K.))', 'en_GB', self.osx_13,
                'CHILD_FEMALE1', 180
            ], ['Albert', 'en_US', self.osx_13, 'NOVELTY1', 145],
            ['Bad News', 'en_US', self.osx_13, 'NOVELTY2', 145],
            ['Bahh', 'en_US', self.osx_13, 'NOVELTY3', 145],
            ['Bells', 'en_US', self.osx_13, 'NOVELTY4', 145],
            ['Boing', 'en_US', self.osx_13, 'NOVELTY5', 145],
            ['Bubbles', 'en_US', self.osx_13, 'NOVELTY6', 145],
            ['Cellos', 'en_US', self.osx_13, 'NOVELTY7', 145],
            ['Good News', 'en_US', self.osx_13, 'NOVELTY8', 145],
            ['Jester', 'en_US', self.osx_13, 'NOVELTY9', 145],
            ['Kathy', 'en_US', self.osx_13, 'NOVELTY10', 145],
            ['Organ', 'en_US', self.osx_13, 'NOVELTY12', 145],
            ['Trinoids', 'en_US', self.osx_13, 'NOVELTY13', 145],
            ['Whisper', 'en_US', self.osx_13, 'NOVELTY14', 145],
            ['Wobble', 'en_US', self.osx_13, 'NOVELTY15', 145],
            ['Zarvox', 'en_US', self.osx_13, 'NOVELTY16', 145],
            [
                'Flo (Spanish (Spain))', 'es_ES', self.osx_13, 'CHILD_FEMALE2',
                131
            ],
            [
                'Grandma (Spanish (Spain))', 'es_ES', self.osx_13, 'FEMALE3',
                146
            ],
            [
                'Shelley (Spanish (Spain))', 'es_ES', self.osx_13, 'FEMALE4',
                146
            ],
            [
                'Sandy (Spanish (Spain))', 'es_ES', self.osx_13,
                'CHILD_FEMALE', 145
            ],
            ['Grandpa (Spanish (Spain))', 'es_ES', self.osx_13, 'MALE2', 145],
            ['Reed (Spanish (Spain))', 'es_ES', self.osx_13, 'MALE3', 145],
            ['Rocko (Spanish (Spain))', 'es_ES', self.osx_13, 'MALE4', 145],
            [
                'Grandma (Spanish (Mexico))', 'es_MX', self.osx_13, 'FEMALE2',
                146
            ],
            [
                'Shelley (Spanish (Mexico))', 'es_MX', self.osx_13, 'FEMALE3',
                146
            ],
            [
                'Sandy (Spanish (Mexico))', 'es_MX', self.osx_13,
                'CHILD_FEMALE', 180
            ],
            ['Grandpa (Spanish (Mexico))', 'es_MX', self.osx_13, 'MALE2', 180],
            ['Reed (Spanish (Mexico))', 'es_MX', self.osx_13, 'MALE3', 180],
            ['Rocko (Spanish (Mexico))', 'es_MX', self.osx_13, 'MALE4', 180],
            [
                'Grandma (French (France))', 'fr_FR', self.osx_13, 'FEMALE2',
                146
            ],
            [
                'Shelley (French (France))', 'fr_FR', self.osx_13, 'FEMALE3',
                146
            ],
            [
                'Sandy (French (France))', 'fr_FR', self.osx_13,
                'CHILD_FEMALE', 145
            ], ['Jacques', 'fr_FR', self.osx_13, 'MALE2', 145],
            ['Eddy (French (France))', 'fr_FR', self.osx_13, 'MALE3', 145],
            ['Grandpa (French (France))', 'fr_FR', self.osx_13, 'MALE4', 145],
            ['Rocko (French (France))', 'fr_FR', self.osx_13, 'MALE5', 145],
            [
                'Flo (French (Canada))', 'fr_CA', self.osx_13, 'CHILD_FEMALE2',
                131
            ],
            [
                'Grandma (French (Canada))', 'fr_CA', self.osx_13, 'FEMALE3',
                146
            ],
            [
                'Shelley (French (Canada))', 'fr_CA', self.osx_13, 'FEMALE4',
                146
            ],
            [
                'Sandy (French (Canada))', 'fr_CA', self.osx_13,
                'CHILD_FEMALE', 160
            ],
            ['Grandpa (French (Canada))', 'fr_CA', self.osx_13, 'MALE2', 160],
            ['Reed (French (Canada))', 'fr_CA', self.osx_13, 'MALE3', 160],
            ['Rocko (French (Canada))', 'fr_CA', self.osx_13, 'MALE4', 160],
            [
                'Flo (Finnish (Finland))', 'fi_FI', self.osx_13,
                'CHILD_FEMALE2', 131
            ],
            [
                'Grandma (Finnish (Finland))', 'fi_FI', self.osx_13, 'FEMALE3',
                146
            ],
            [
                'Sandy (Finnish (Finland))', 'fi_FI', self.osx_13,
                'CHILD_FEMALE', 145
            ],
            [
                'Shelley (Finnish (Finland))', 'fi_FI', self.osx_13, 'FEMALE2',
                146
            ],
            [
                'Grandpa (Finnish (Finland))', 'fi_FI', self.osx_13, 'MALE2',
                145
            ],
            ['Reed (Finnish (Finland))', 'fi_FI', self.osx_13, 'MALE3', 145],
            ['Rocko (Finnish (Finland))', 'fi_FI', self.osx_13, 'MALE4', 145],
            [
                'Flo (Italian (Italy))', 'it_IT', self.osx_13, 'CHILD_FEMALE2',
                131
            ],
            [
                'Grandma (Italian (Italy))', 'it_IT', self.osx_13, 'FEMALE3',
                146
            ],
            [
                'Shelley (Italian (Italy))', 'it_IT', self.osx_13, 'FEMALE4',
                146
            ],
            [
                'Sandy (Italian (Italy))', 'it_IT', self.osx_13,
                'CHILD_FEMALE', 145
            ],
            ['Grandpa (Italian (Italy))', 'it_IT', self.osx_13, 'MALE2', 145],
            ['Reed (Italian (Italy))', 'it_IT', self.osx_13, 'MALE3', 145],
            ['Rocko (Italian (Italy))', 'it_IT', self.osx_13, 'MALE4', 145],
            [
                'Flo (Portuguese (Brazil))', 'pt_BR', self.osx_13,
                'CHILD_FEMALE2', 131
            ],
            [
                'Grandma (Portuguese (Brazil))', 'pt_BR', self.osx_13,
                'FEMALE3', 146
            ],
            [
                'Shelley (Portuguese (Brazil))', 'pt_BR', self.osx_13,
                'FEMALE4', 146
            ],
            [
                'Sandy (Portuguese (Brazil))', 'pt_BR', self.osx_13,
                'CHILD_FEMALE', 145
            ],
            ['Eddy (Portuguese (Brazil))', 'pt_BR', self.osx_13, 'MALE2', 145],
            [
                'Grandpa (Portuguese (Brazil))', 'pt_BR', self.osx_13, 'MALE3',
                145
            ],
            ['Reed (Portuguese (Brazil))', 'pt_BR', self.osx_13, 'MALE4', 145],
            [
                'Rocko (Portuguese (Brazil))', 'pt_BR', self.osx_13, 'MALE5',
                145
            ], ['Fiona', 'en-GB', self.old, 'FEMALE2', 145],
            ['Lee', 'en_AU', self.premium, 'MALE1', 181],
            ['Fiona', 'en_GB', self.premium, 'FEMALE1', 181]
        ]
        # You could parse a list of currently available premium voice settings:
        #
        #     plutil -convert json ~/Library/Preferences/com.apple.speech.voice.prefs.plist -o ~/Desktop/voices.json
        #
        # + Is the added latency acceptable?
        # + Are errors possible when using a dynamically updated file?
        # + Is the data private to MacOS? (i. e. The format changes over time)
        #
        # See <https://github.com/mklement0/voices/blob/master/bin/voices>
        if self.is_mac:
            self.app = 'say'
            if os.path.isfile('/usr/bin/say'):
                self.app = '/usr/bin/say'
            _app = self.app
            self._i = app_info_extract(self.app, 'say.txt', 'voice', '', ' # ')
        if len(self._i.strip()) == 0:
            self._i = ''
            for _item in self.spd_table:
                _name = _item[0]
                _locale = _item[1]
                _edition_check = _item[2]
                _spd_voice = _item[3]
                if _edition_check in self.editions:
                    self._i = '\n'.join([
                        self._i,
                        '%(_name)s           %(_locale)s     # %(_spd_voice)s'
                        % locals()
                    ])
                if self.debug and 1:
                    if _edition_check in [self.premium]:
                        _edition = str(_edition_check)
                        print(
                            "'['%(_name)s', '%(_locale)s', %(_edition)s, '%(_spd_voice)s'],  # testing"
                            % locals())
            self._i = self._i.strip()
        self._a1 = self._i.strip().split('\n')
        s1 = ''
        self.history_json_str = ''
        self._a2 = []
        _div = 11 * " "
        # Handle long voice names like `Shelley (Portuguese (Brazil))`
        self._i = self._i.strip().replace(') ',
                                          ')%(_div)s' % locals()).replace(
                                              '# ', '%(_div)s' % locals())
        for line in self._i.splitlines():
            _item1 = tuple(line.split(_div))
            if len(_item1) == 3:
                self._a2.append(_item1)
            else:
                _line = line
                print('''INFO: `say` said `%(_line)s`''' % locals())
        if self.is_mac:
            self._f = app_info_extract(self.app, 'say_f.txt', 'file-format',
                                       '', ') [')
        if len(self._f) == 0:
            if os.name == 'nt':
                self._f = "                           (,) []\n"
            else:
                self._f = (
                    "WAVE  WAVE                 (.wav) [lpcm,ulaw,alaw]\n")
        self._a3 = self._f.split('\n')
        self._a4 = []
        for line in self._f.splitlines():
            self._a4.append(tuple(line.split('(')))

    def parse_prefs(self):  # -> str
        '''Return the installation and use log of the system speech setup
        preferences as a json formatted string'''
        if len(self.history_json_str) != 0:
            return self.history_json_str
        _app = '/usr/bin/plutil'
        if os.path.isfile(_app):
            _app = 'plutil'
        else:
            return ''
        _fmd = readtexttools.ImportedMetaData()
        _remove = False
        __json_f = 'say-i.json'
        _app_out = readtexttools.get_my_lock(__json_f)
        _say_prefs = os.path.expanduser(
            '~/Library/Preferences/com.apple.speech.voice.prefs.plist')
        _command = 'plutil -convert json %(_say_prefs)s -o %(_app_out)s' % locals(
        )
        if not os.path.isfile(_app_out):
            os.system(_command)
        self.history_json_str = _fmd.meta_from_file(_app_out, _remove)
        return self.history_json_str

    def check_grep_filter(self, name='Lee'):  # -> str
        '''Uses `self.parse_prefs()` to generate a `grep` string. It returns
        a filter string that allows the `name` if it is in the log file
        used by *System Settings - Accessibility - Spoken Content*, otherwise
        the routine returns `''`.
        '''
        _lcase_name = name.lower().strip()
        _parse_prefs = self.parse_prefs()
        if 'com.apple.speech.synthesis.voice.%(_lcase_name)s)' % locals(
        ) in _parse_prefs:
            return ''
        elif 'com.apple.speech.synthesis.voice.%(name)s)' % locals(
        ) in _parse_prefs:
            return ''
        else:
            if ' ' in _lcase_name:
                name = "'%(name)s'" % locals()
            return ' | grep -v %(name)s ' % locals()

    def _getvoicename(self, inti=0):  # -> str
        '''i.e. `Alex'''
        s1 = ''
        try:
            s1 = self._a2[inti][0]
        except:
            s1 = ''
        return s1

    def _getlanguagecountry(self, inti=0):  # -> str
        '''i.e. `US`'''
        s1 = ''
        try:
            s1 = self._a2[inti][1].split('#')[0].strip().replace('_', '-')
        except:
            s1 = ''
        return s1

    def _getlanguage(self, inti=0):  # -> str
        '''i.e. `en`'''
        s1 = self._getlanguagecountry(inti)
        return s1.split('-')[0].lower()

    def spd_voice_to_say_voice(self,
                               _use_voice='FEMALE1',
                               _lang='en-US'):  # -> str
        '''Given a voice in speechd request format, tries to return a
        matching MacOS voice.  i.e. `Alex`'''
        _count = [1, 1, 1, 1, 1, 1]
        _count_label = [
            'MALE', 'FEMALE', 'CHILD_MALE', 'CHILD_FEMALE', 'NOVELTY',
            'TESTING'
        ]
        word_rate = self.word_rate
        _ubound_count_label = len(_count_label) - 1
        _continue = False
        _spd_voice = _use_voice.upper().strip(' \'"\t')
        for _counter in range(0, _ubound_count_label):
            if _spd_voice.startswith(_count_label[_counter]):
                _continue = True
                break
        if not bool(_continue):
            return _use_voice.strip(' \'"\t')
        _a4 = []

        _lang = _lang.replace('-', '_').split('.')[0]
        _display_lang = _lang.replace('_', '-')
        _alt_lang = ''.join([_lang.split('_')[0], '_']).lower()
        _country = _lang.replace(_alt_lang, '')
        if len(_country) == 0:
            _country = 'ZA'
        _i_say = 0
        _i_spd = 3
        _i_word_rate = 4
        _voice_filters = ' | grep -v '.join(self.grep_block_list)
        if _alt_lang in ['en_', 'en']:
            for opt_vox in ['Lee', 'Fiona']:
                _test_vox = self.check_grep_filter(opt_vox)
                if len(_test_vox) != 0:
                    _voice_filters = ''.join([_voice_filters, _test_vox])
        if self.debug and 1:
            print(_voice_filters)
        _remove = True
        _voice_lines = '\n'.join([
            app_info_extract(
                self.app, 'say_spd1.txt', 'voice',
                '''| grep -v '))' | grep %(_lang)s %(_voice_filters)s''' %
                locals(), ' # ', _remove),
            app_info_extract(
                self.app, 'say_spd1.txt', 'voice',
                '''| grep -v '))' | grep -v _%(_country)s | grep  %(_alt_lang)s %(_voice_filters)s'''
                % locals(), ' # ', _remove),
            app_info_extract(
                self.app, 'say_spd1.txt', 'voice',
                '''| grep '))' | grep %(_lang)s %(_voice_filters)s''' %
                locals(), ' # ', _remove),
            app_info_extract(
                self.app, 'say_spd1.txt', 'voice',
                '''| grep '))' | grep -v _%(_country)s | grep %(_alt_lang)s %(_voice_filters)s'''
                % locals(), ' # ', _remove)
        ]).strip()
        if self.debug and 1:
            print(_voice_lines)
        if len(_voice_lines) == 0:
            return _spd_voice
        elif ' %(_lang)s ' % locals() in _voice_lines:
            _lang = _lang.strip(' \'"\t')
        elif ' %(_alt_lang)s' % locals() in _voice_lines:
            _lang = _alt_lang
        else:
            return _spd_voice

        for _line in _voice_lines.splitlines():
            for _item in self.spd_table:
                if _line.startswith(_item[_i_say]):
                    found_g = ''
                    for _xyxx in range(0, _ubound_count_label):
                        if _item[_i_spd].startswith(_count_label[_xyxx]):
                            found_g = ''.join([
                                _count_label[_xyxx],
                                str(_count[_xyxx]).strip()
                            ])
                            _count[_xyxx] = _count[_xyxx] + 1
                    if len(found_g) != 0:
                        if len(self.voice_found) == 0:
                            self.voice_found = found_g
                        _country = _line.split('_')[1].split(' ')[0]
                        _display_lang = ''.join([_alt_lang,
                                                 _country]).replace('_', '-')
                        word_rate = _item[_i_word_rate]
                        _say_voice = _line.split(_alt_lang)[0].strip()
                        _a4.append(
                            [found_g, _display_lang, _say_voice, word_rate])
        if self.debug and 1:
            print(_a4)
        _tts_system = ''.join([os.uname().sysname, '_tts']).lower()
        for _voice in _a4:
            if _spd_voice == _voice[0]:
                self.word_rate = _voice[3]
                _gender = 'male'
                if 'FEMALE' in _spd_voice:
                    _gender = 'female'
                    self.voice_found = _voice[0]
                _lcase_lang = _voice[1].lower()
                _vox = _voice[2]
                _vox_id = _vox.replace(' ', '_').lower()
                _key = """%(_lcase_lang)s/%(_vox_id)s-%(_tts_system)s""" % locals(
                )
                _sample_url = 'https://google.com/search?q=MacOS+say+%(_vox)s' % locals(
                )
                _found = _voice[0]
                # Report on found voice.
                self.json_string = ('''
{"%(_key)s" : {
 "downloaded" : false,
 "gender" : "%(_gender)s",
 "id" : "%(_key)s",
 "language" : "%(_lcase_lang)s",
 "mimetype : "audio/aiff",
 "name" : "%(_vox)s",
 "request" : "%(_spd_voice)s",
 "sample_url" : "%(_sample_url)s",
 "tts_system" : "%(_tts_system)s"
 }
}''' % locals())
                if self.debug and 1:
                    print(self.json_string)
                else:
                    print(_voice)
                return _voice[2]
        if len(self.voice_found) != 0:
            return self.voice_found
        elif 'FEMALE' in _spd_voice.upper():
            return 'Samantha'
        return 'Alex'

    def _getsamplephrase(self, inti=0):  # -> str
        '''i.e. `Most people recognize me by my voice.`'''
        s1 = ''
        try:
            s1 = self._a2[inti][2].strip()
        except:
            s1 = ''
        return s1

    def _getsayfileextensionstr(self, inti=0):  # -> str
        '''i.e. `aiff`'''
        s1 = ''
        try:
            s1 = self._a4[inti][1].split(')')[0].lower()
        except:
            s1 = ''
        return s1

    def voicesampletext(self, s0=''):  # -> str
        '''
        Returns a voice sample string in the form `Most people
        recognize me by my voice.` when given a voice name like "Alex"

        **Example 1**: `mydata.voicesampletext('Alex')` returns
        "Most people recognize me by my voice."
        because Alex is a MacOS voice.

        **Example 2**: `mydata.languagecountry('Ailani')` returns ""
        because no voice called "Ailani" is supported on any version
        of say.

        Note: If this python cannot read `say` output, then this tool
        returns a generated string like `MALE1` or `FEMALE3`.
        '''
        s1 = filterinputs(s0).upper()
        s2 = ''
        s3 = ''

        try:
            for i, item in enumerate(self._a1):
                if s1 == self._getvoicename(i).upper():
                    s2 = self._getsamplephrase(i)
                    break
        except:
            s2 = ''
        return s2

    def languagecountry(self, s0):
        '''
        Returns language and country string in the form `en-US`
        when given a voice in the form 'Alex', 'alex' or 'ALEX' or
        a comma separated list of installed language-COUNTRY pairs
        when given a '' string or a '~' string.

        **Example 1**: `mydata.languagecountry('Alex')` returns "en-US"
        because Alex is a US English voice.

        **Example 2**: `mydata.languagecountry('Ailani')` returns ""
        because no voice called "Ailani" is supported on any version of
        say.

        **Example 3**: `mydata.languagecountry('') and
        `mydata.languagecountry('~')
        return a comma separated list of all the installed
        language-COUNTRY pairs in the form `en-US,it-IT,sv-SE,fr-CA,
        es-MX,...`
        '''
        s1 = filterinputs(s0).upper()
        s2 = ''
        s3 = ''
        try:
            if len(s1) == 0 or s1 == '~':
                for i, item in enumerate(self._a1):
                    s3 = self._getlanguagecountry(i)
                    if not s3 in ''.join([s2, ' ']):
                        s2 = ''.join([s2, ',', s3])
                s2 = s2[1:]
            else:
                for i, item in enumerate(self._a1):
                    if s1 == self._getvoicename(i).upper():
                        s2 = self._getlanguagecountry(i)
                        break
        except:
            s2 = ''
        return s2

    def _i_rate_voice(self, i_rate=0, _voice=''):  # -> tuple [str, str]
        '''Specific to MacOS say -- check rate and voice, and return
        a list with `[m_rate, _voice]`.'''
        m_rate = ''
        if bool(i_rate):
            try:
                if i_rate < .25:
                    m_rate = ' -r 32'  # 110
                elif i_rate > 3:
                    m_rate = ' -r 350'
                else:
                    self.wpm = int(i_rate * self.word_rate)
                    _wpm = str(self.wpm)
                    if self.debug and 1:
                        print([
                            'Speech rate: `_wpm`', _wpm,
                            'Multiplier: `i_rate`', i_rate
                        ])
                    m_rate = ' -r %(_wpm)s' % locals()
            except:
                pass
        return m_rate, _voice

    def say_aloud(self,
                  _file_spec='',
                  _voice='',
                  _requested_voice='',
                  i_rate=0):  # -> bool
        '''Read aloud using a MacOS system voice if the voice
        is not already talking. Returns `True` if there is no
        error.
        '''
        # get_my_lock('lock') uses the values for lock my lock
        # and unlock my lock
        if os.path.isfile(readtexttools.get_my_lock('lock')):
            return False
        if _requested_voice.upper() in NET_SERVICE_LIST:
            # Accept if you literally ask for these voices, but replace a
            # requested "AUTO" or "NETWORK" request with the default system
            # voice instead.
            if _voice in self.block_list:
                _voice = "Alex"
        readtexttools.lock_my_lock()
        if i_rate == 0 and self._i_rate_voice != 0:
            i_rate = self._i_rate_voice
        _speaker_conf = [self._i_rate_voice(i_rate, _voice)]
        m_rate = _speaker_conf[0][0]
        _voice = _speaker_conf[0][1]
        v_tag = '-v '
        if len(_voice) == 0:
            v_tag = ''
        if 'm4af  Apple MPEG-4 Audio' in self._f:
            _media_test = readtexttools.get_my_lock('say.m4a')
        else:
            _media_test = readtexttools.get_my_lock('say.aiff')

        _app = self.app
        _command = "%(_app)s %(m_rate)s %(v_tag)s'%(_voice)s' -f '%(_file_spec)s'" % locals(
        )
        _base_command = "%(_app)s -f '%(_file_spec)s'" % locals()
        _test_command = "%(_app)s %(m_rate)s -v '%(_requested_voice)s' -o '%(_media_test)s' '1 2 3'" % locals(
        )
        if len(_voice) == 0:
            os.system(_test_command)
            if os.path.isfile(_media_test):
                os.remove(_media_test)
                _command = "%(_app)s %(m_rate)s -v '%(_requested_voice)s' -f '%(_file_spec)s'" % locals(
                )
            else:
                # readtexttools.unlock_my_lock()
                return False
        if self.debug and 1:
            print('=' * 75, '\n', _command, '\n', '=' * 75)
        try:
            if not os.path.isfile(_file_spec):
                return False
            readtexttools.lock_my_lock()
            _result = os.system(_command)
            # `time.sleep(1)` is blocking the thread to avoid a duplicate
            # system `say` execution process:
            time.sleep(1)
            if bool(_result):
                _result = os.system(_base_command)
                time.sleep(1)
            readtexttools.unlock_my_lock()
            return not bool(_result)
        except:
            print('Cannot execute command: `%(_command)s`' % locals())
        return False

    def save_audio(self,
                   _file_spec='',
                   _voice='',
                   i_rate=0,
                   _media_out='',
                   _audible=False,
                   _visible=False):  # -> bool
        '''

+ `_file_spec` - Text file to speak
+ `_voice` - Supported voice
+ `i_rate` - Speech speed if supported
+ `_media_out` - Name of desired output media file
+ `_audible` - If false, then don't play the sound file
+ `_visible` - Use a graphic media player, or False for invisible player
    '''
        m_rate = ''
        v_tag = '-v '
        if len(_voice) == 0:
            v_tag = ''
        _error_icon = readtexttools.net_error_icon()
        _speech_rate = readtexttools.safechars(i_rate, '1234567890')
        _speaker_conf = [self._i_rate_voice(_speech_rate, _voice)]
        m_rate = _speaker_conf[0][0]
        _voice = _speaker_conf[0][1]
        if not bool(_voice):
            self.ok = False
            return False
        _icon = readtexttools.app_icon_image('poster-001.png')
        # Determine the output file name
        _media_out = readtexttools.get_work_file_path(_media_out, _icon, 'OUT')
        # Determine the temporary file name
        _media_work = readtexttools.get_work_file_path(_media_out, _icon,
                                                       'TEMP') + '.aiff'
        # Remove old files.
        if os.path.isfile(_media_work):
            os.remove(_media_work)
        if os.path.isfile(_media_out):
            os.remove(_media_out)
        _app = self.app
        _command = "%(_app)s %(m_rate)s %(v_tag)s'%(_voice)s' -o '%(_media_work)s' -f '%(_file_spec)s' " % locals(
        )
        try:
            readtexttools.my_os_system(_command)
        except:
            self.ok = False
            return False
        if os.path.isfile(_media_work):
            if os.path.getsize(_media_work) == 0:
                return False
            _writer = ''
            _size = '600x600'
            _info = "Apple MacOS Speech Synthesis Voice: %(_voice)s" % locals()
            readtexttools.process_wav_media(_info, _media_work, _icon,
                                            _media_out, _audible, _visible,
                                            _writer, _size)
            return True
        else:
            _msg = "Could not play a say media file locally."
            if bool(_media_out):
                _msg = "Could not save a say media file locally."
            readtexttools.pop_message("Python `say`" % locals(), _msg, 5000,
                                      _error_icon, 1)
        self.ok = False
        return False

    def voice(self, s0=''):
        '''
        Returns voice name string in the form `Alex` when
        given the language and COUNTRY. The language and country
        are case sensitive.

        **Example 1**: `mydata.voice('en-US')` returns "Alex"
        because Alex is the first matching US English voice.

        **Example 2**: `mydata.voice('')` or mydata.voice('~') returns
        a comma separated list of all supported voices.

         **Example 3**: `mydata.voice('hw-US')` returns ""
        because say does not support the Hawaiian language.

         **Example 4**: `mydata.voice('~fr-CA')` returns "Amelie,Felix"
        because the tilde (`~`) character makes the function return a
        comma separated string containing of all the matching languages.
        '''
        s5 = filterinputs(s0)
        try:
            s5 = s5.replace('_', '-').lower()
            s4 = ''
            s3 = ''
            s2 = ''
            s1 = ''
            i1 = (len(s5) * -1) + 1

            for i, item in enumerate(self._a1):
                s2 = self._getlanguagecountry(i).lower()
                if len(s5) == 0 or s5 == '~':
                    s1 = ''.join([s1, ',', self._getvoicename(i)])
                elif s5[:i1] == '~':
                    if ''.join(['~', s2]) == s5:
                        # Make a comma separated list of matching voices
                        s1 = ''.join([s1, ',', self._getvoicename(i)])
                elif s2 == s5:
                    s1 = self._getvoicename(i)
                    break
            if len(s5) == 0 or s5 == '~':
                s1 = s1[1:-1]
            elif s5[:i1] == '~':
                s1 = s1[1:]
            elif len(s1) == 0:
                # No exact match; trying language match
                s3 = s5.split('-')[0].lower()
                if s3 == 'de':
                    s4 = 'de-de'
                elif s3 == 'fr':
                    s4 = 'fr-fr'
                elif s3 == 'es':
                    s4 = 'es-mx'
                elif s3 == 'nl':
                    s4 = 'nl-nl'
                elif s3 == 'pt':
                    s4 = 'pt-br'
                for i, item in enumerate(self._a1):
                    if s4 == self._getlanguagecountry(i).lower():
                        # Country with highest population of native
                        # speakers
                        s1 = self._getvoicename(i)
                        break
                if len(s1) == 0:
                    for i, item in enumerate(self._a1):
                        if s3 == self._getlanguage(i).lower():
                            # Using first available international match
                            s1 = self._getvoicename(i)
                            break
        except:
            s1 = ''
        return s1


def main():
    '''Command line speech-dispatcher tool. Some implimentations of python
    require the long command line switch'''
    _is_dev = False
    _imported_metadata = readtexttools.ImportedMetaData()
    _spd_formats = SpdFormats()
    _file_spec = sys.argv[-1]
    _txt = ''
    i_rate = 0
    sd_rate = 0
    _word_rate = 160
    _language = ''
    _output = ''
    _output_module = ''
    _visible = False
    _voice = 'MALE1'
    verbose_language = readtexttools.default_lang()
    py_m = platform.python_version_tuple()[0]
    py_m_verbose = '.'.join(platform.python_version_tuple())
    if verbose_language:
        for splitter in ['_', ':']:
            if splitter in verbose_language:
                _language = verbose_language.split(splitter)[0]
                break
    if not _language:
        _language = 'en'
    concise_lang = _language[:2].lower()

    if not os.path.isfile(_file_spec):
        print("I was unable to find the text file you specified!")
        usage()
        sys.exit(0)
    elif sys.argv[-1] == sys.argv[0]:
        usage()
        sys.exit(0)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hmolvri", [
            "help", "output_module=", "output=", "language=", "voice=",
            "rate=", "visible="
        ])
    except getopt.GetoptError:
        print('option was not recognized')
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-m", "--output_module"):
            _output_module = a
        elif o in ('-o', '--output'):
            _output = a
        elif o in ("-l", "--language"):
            # 2 letters lowercase - fr Français, de Deutsch...
            concise_lang = ''.join([a.lower(), '-']).split('-')[0]
            _language = a
        elif o in ("-v", "--voice"):
            # MALE1, MALE2 ...
            _voice = a
        elif o in ("-r", "--rate"):
            try:
                if a.endswith('%'):
                    _rate = (int(readtexttools.remove_unsafe_chars(a)))
                    i_rate = _rate * 0.01
                    sd_rate = _spd_formats.percent_to_spd(_rate)
                    _word_rate = network_read_text_file.speech_wpm(a)
                else:
                    i_rate = int(readtexttools.remove_unsafe_chars(a))
            except ValueError:
                i_rate = 0
        elif o in ("-i", "--visible"):
            if a.lower() in ['true']:
                _visible = True
        else:
            assert False, "unhandled option"
    if os.path.isfile('/usr/bin/say'):
        if os.path.isfile(readtexttools.get_my_lock('lock')):
            hard_reset('say')
            readtexttools.unlock_my_lock()
            exit()
        if not bool(i_rate) and bool(_voice):
            # Enable a custom rate for each voice
            i_rate = 1
        _say_formats = SayFormats()
        mac_reader = _say_formats.voice(_language)
        _voice = _say_formats.spd_voice_to_say_voice(_voice, _language)
        if not _voice.lower() == mac_reader.lower():
            for line in _say_formats._a1:
                if line.startswith('%(_voice)s ' % locals()):
                    mac_reader = _voice
                    break
        _message_old = _imported_metadata.meta_from_file(_file_spec).strip()
        _message = readtexttools.local_pronunciation(
            _language, _message_old, 'macos_say', 'MACOS_SAY_USER_DIRECTORY',
            _is_dev)[0].strip()
        if len(_message) != 0:
            # Found misspoken words or phrases. MacOS does not support all phonetic
            # codes, so you need to approximate the correct sound using similar words
            # in the json document. See:
            # * <https://www.internationalphoneticalphabet.org/ipa-chart-audio/index.html>
            # * <https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-ssml-phonetic-sets>
            if not _message == _message_old:
                os.remove(_file_spec)
                readtexttools.write_plain_text_file(_file_spec, _message,
                                                    'utf-8')
        if len(_output) == 0 and not (_visible):
            resultat = _say_formats.say_aloud(_file_spec, mac_reader, _voice,
                                              i_rate)

            if not resultat:
                readtexttools.unlock_my_lock()
                if _voice.upper() in NET_SERVICE_LIST:
                    if not net_play(_file_spec, _language, i_rate, _voice):
                        print(network_read_text_file.network_problem(_voice))
        else:
            _audible = _visible
            if not _say_formats.save_audio(_file_spec, mac_reader, i_rate,
                                           _output, _audible, _visible):

                if len(_language) != 0:
                    try:
                        _ext = os.path.splitext(_output)[1]
                    except IndexError:
                        _ext = ''
                    if _voice.upper() in NET_SERVICE_LIST:
                        if not network_read_text_file.network_main(
                                _file_spec, _language, _visible, _audible,
                                _output, '', '', '', '600x600', i_rate, _voice,
                                ''):
                            readtexttools.pop_message(
                                'Network : Spoken content',
                                'No `%(_language)s` voice\n%(_voice)s: No `%(_ext)s` audio exported.'
                                % locals())
                    else:
                        readtexttools.pop_message(
                            'Accessibility : Spoken content',
                            'No `%(_language)s` voice\nNo `%(_ext)s` audio exported.'
                            % locals())
        sys.exit(0)
    elif os.name in ['posix']:
        if not USE_SPEECHD:
            print(
                '''The `speechd` library is not compatible with your application
or platform. Try a networked speech tool like `larynx-server` or `docker-marytts`.''')
            if i_rate == 0:
                _word_rate = 160
            if not network_read_text_file.network_main(
                    _file_spec, _language, 'false', 'false', _output, '', '',
                    '', '600x600', _word_rate, _voice, ''):

                _web_message = _imported_metadata.meta_from_file(
                    _file_spec).strip()
                _max_message_len = 4999
                if len(_web_message) > _max_message_len:
                    for punct in [
                            '\n', '\t', '?', '!', '.', ',', ';', ':', ' '
                    ]:
                        if punct in _web_message:
                            _web_message = _web_message.split(punct)[0]
                            if not len(_web_message) > _max_message_len:
                                break
                if len(_web_message) > _max_message_len:
                    exit(0)
                readtexttools.web_info_translate(_web_message, _language)
            sys.exit(0)

        if not _spd_formats.spd_ok:
            print("The `speechd` python 3 library is required.")
            usage()
            sys.exit(0)
        if not _spd_formats.set_up():
            print(
                '''The python 3 `speechd` setup failed. Check for a system update and
restart your computer.''')
            usage()
            sys.exit(0)
        _testing = False
        if not _spd_formats.speak_spd(_output_module, _language, _voice,
                                      sd_rate, _file_spec):
            # Error - Try resetting `speechd`
            hard_reset('speech-dispatcher')
    sys.exit(0)


if __name__ == "__main__":
    main()
