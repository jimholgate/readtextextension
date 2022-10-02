#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u'''
Posix Speech Toolkit
====================

This toolkit enables multilingual speech on Posix operating systems like
MacOS and Linux.

Some voice tools might not be able to change the prosody, age or gender of
all voices in all languages.

MacOS
=====

### Enable python 3

For local python scripts to work with MacOS, you need to install XCode and
to agree to the terms of the Xcode/iOS license.

This requires administrator (sudo) privileges.

Once you have installed XCode, open a terminal and run

    sudo xcodebuild -license

and read the license. Finally, type `accept`, and hit the `return` key.

Depending on the release of MacOS, you might need to install additional software
to enable python to run locally.

Run `python3 --version` and if the program shows you further installation prompts,
follow the instructions to install the required software.

### Menu options

External program:

    /usr/bin/python3

Command line options (default voice):

    "(SPD_READ_TEXT_PY)" "(TMP)"

or (specific language):

    "(SPD_READ_TEXT_PY)" --language "(SELECTION_LANGUAGE_CODE)" "(TMP)"

or (specific voice):

    "(SPD_READ_TEXT_PY)" --voice "Fiona" "(TMP)"

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

Copyright (c) 2010 - 2022 James Holgate
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import codecs
import getopt
import os
import platform
import subprocess
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

NET_SERVICE_LIST = ['AUTO', 'NETWORK', 'AWS',
                    'AZURE', 'GOOGLECLOUD', 'GTTS']

def about_script(player='speech-dispatcher'): # -> str
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

[More](%(more_url)s)''' %locals()


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
        a1 = [
            '{',
            '}',
            '(',
            ')',
            ';',
            ':'
            ]
        for i, item in enumerate(a1):
            if (a1[i] in s1) is False:
                bsafe = True
                break

        if bsafe is False:
            a2 = [
                '{',
                '}',
                '(',
                ')'
                ]
            # Escape the problem characters with `\`
            for i, item in enumerate(a2):
                s1 = s1.replace(a2[i], ''.join(['\\', a2[i]]))
    return s1


def hard_reset(sd='speech-dispatcher'):  # -> bool
    '''kill posix process'''
    if not bool(sd):
        return False
    if not readtexttools.have_posix_app('killall'):
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


def net_play(_file_spec='', _language='en-US', i_rate=0,
             _requested_voice=''): # -> bool
    '''Attempt to play a sound from the network.'''
    if network_read_text_file.network_ok(_language):
        if _requested_voice in NET_SERVICE_LIST:
            net_rate = 160
            if i_rate < 0:
                net_rate = 110
            ret_val = network_read_text_file.network_main(
                _file_spec, _language, 'false', 'true', '',
                '', '', '', '600x600', net_rate,
                _requested_voice)
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

        self.all_voices = ['MALE3', 'MALE2', 'MALE1',
                           'FEMALE3', 'FEMALE2', 'FEMALE1',
                           'CHILD_MALE', 'CHILD_FEMALE',
                           'AUTO', 'NETWORK', 'AWS',
                           'AZURE', 'GOOGLECLOUD', 'GTTS']
        self.spd_voices = ['MALE3', 'MALE2', 'MALE1',
                           'FEMALE3', 'FEMALE2', 'FEMALE1',
                           'CHILD_MALE', 'CHILD_FEMALE']
        self.stop_voice = 'TriggerAssertionError'
        # NOTE: speechd might reject a language when length of item > 2
        self.language_list = espeak_read_text_file.espk_languages()
        self.config_dir = '/etc/speech-dispatcher/modules'
        self.local_config = ''
        self.local_json = readtexttools.get_my_lock('json')
        self.json_content = ''
        self.spd_ok = bool(speechd)
        if self.spd_ok:
            self.spd_ok = int(self.py_m) > 2
        try:
            if len(os.getenv('HOME')) != 0:
                local_config = os.path.join(
                    os.getenv('HOME'),
                    '.config/speech-dispatcher/modules')
                if os.path.isdir(local_config):
                    self.local_config = local_config
        except Exception:
            pass

    def is_a_supported_language(self, _lang='en',
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
            elif os.path.isfile('/usr/share/espeak-ng-data/%(_short_lang)s_dict' %locals()):
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
                bug_cleaner = speechd.SSIPClient(
                    self.client_app, self.client_user, None, None)
                bug_cleaner.speak('\t')
                time.sleep(0.2)
                bug_cleaner.close()
            self.client = speechd.SSIPClient(
                self.client_app, self.client_user, None, None)
            return True
        except (AttributeError, ImportError, NameError, speechd.SpawnError,
                speechd.SSIPCommunicationError):
            return False

    def _switch_to_female(self, voice=''):  # -> bool
        '''If voice includes `FEMALE` or a network voice, return `True`'''
        if voice.count('FEMALE') != 0 or voice in NET_SERVICE_LIST:
            return True
        return False

    def speak_spd(self, output_module='', language='',
                  voice='', i_rate=0, _file_spec=''): # -> bool
        '''Set user configuration settings'''
        _lock = readtexttools.get_my_lock("lock")
        _try_voice = voice
        if voice not in self.all_voices:
            if voice not in ['none', 'None', language,
                             language.split('-')[0].split('_')[0]]:
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
                        language, not os.path.isfile(
                            '/usr/bin/spd-say')):
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
                        for _player in ['avplay', 'ffplay', 'vlc',
                                        'gst-launch-1.0']:
                            hard_reset(_player)
                        os.remove(self.local_json)
                    else:
                        self.json_content = self.json_tools.set_json_content(
                            language, voice, i_rate,
                            _file_spec, output_module)
                        readtexttools.write_plain_text_file(self.local_json,
                                                            self.json_content,
                                                            'utf-8')
                        retval = net_play(_file_spec, language, i_rate, voice)
                        if not retval:
                            print(network_read_text_file.network_problem(voice))
                        os.remove(self.local_json)
                        return retval
                    return False
            else:
                pass
            self.client.set_rate(i_rate)
        except (ImportError, NameError, speechd.SpawnError):
            if len(voice) != 0:
                self.json_content = self.json_tools.set_json_content(
                    language, voice, i_rate,
                    _file_spec, output_module)
                readtexttools.write_plain_text_file(self.local_json,
                                                    self.json_content,
                                                    'utf-8')
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
            _txt = self.xml_tool.clean_for_xml(_txt, True)
            _message = '''<?xml version='1.0'?>
<speak version='1.1' xml:lang='%(language)s'>%(_txt)s</speak>''' % locals()
        _time = guess_time(_txt, i_rate, _file_spec, language)
        self.client.set_data_mode(self.xml_tool.use_mode)
        self.client.set_punctuation(speechd.PunctuationMode.SOME)
        _voice_list = None
        # Try to match requested gender and locale for supported synthesizers
        try:
            _client_voices = self.list_synthesis_voices(language.split('-')[0])
        except [AttributeError, TypeError]:
            _client_voices = [""]
        if language in ['en-AS', 'en-PH', 'en-PR', 'en-UM', 'en-US',
                        'en-VI']:
            if self._switch_to_female(voice):
                _voice_list = ['Slt', 'Clb', 'samantha', 'Bdl', 'Alan',
                               'English (America)+female1']
            else:
                _voice_list = ['Bdl', 'Alan', 'Clb', 'Slt', 'samantha',
                               'English (America)+male1']
        elif language[:2] == 'en':
            if self._switch_to_female(voice):
                _voice_list = ['serena', 'Slt', 'Clb', 'Alan', 'Bdl',
                               'English+female1']
            else:
                _voice_list = ['Alan', 'Bdl', 'Clb', 'Slt', 'serena',
                               'English']
        elif language[:2] == 'kg':
            if self._switch_to_female(voice):
                _voice_list = ['Azamat', 'Nazgul', 'Kyrgyz+female1']
            else:
                _voice_list = ['Nazgul', 'Azamat', 'Kyrgyz']
        elif language[:2] == 'pl':
            if self._switch_to_female(voice):
                _voice_list = ['Magda', 'Natan', 'Polish+female1']
            else:
                _voice_list = ['Natan', 'Magda', 'Polish']
        elif language[:2] == 'ru':
            if self._switch_to_female(voice):
                _voice_list = ['Anna', 'Elena', 'Aleksandr', 'Artemiy',
                               'Russian+female1']
            else:
                _voice_list = ['Aleksandr', 'Artemiy', 'Anna', 'Elena',
                               'Russian']
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
                except(AttributeError, SyntaxError, TypeError):
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
        '''List synthesis voices. i. e.: ('Alan', 'Slt',...)'''
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
        of say.
            '''
        s1 = ''
        self._i = ''
        self._f = ''
        self.is_mac = os.path.isfile('/usr/bin/say')
        # On MacOS systems, we specify the complete path`/usr/bin/say`.
        self.app = ''
        self.lock = readtexttools.get_my_lock("lock")
        if self.is_mac:
            self.app = 'say'
            if os.path.isfile('/usr/bin/say'):
                self.app = '/usr/bin/say'
            try:
                s1 = (subprocess.check_output(
                    ''.join([self.app, ' --voice="?"']),
                    shell=True))
                # Python 3 : a bytes-like
                # object is required
                self._i = codecs.decode(s1, 'utf-8')
            except Exception:
                self._i = ''
                # We may need to use sample values, if the local
                # `say -v?` command returns nothing.
                s1 = ''
        if len(self._i) == 0:
            self._i = ('''
Alex                en_US    # [[pbas -6]][[rate -40]] Stop, Dave.[[pbas -6]][[rate -40]My mind is going.
Amelie              fr_CA    # Salut! On m’appelle  Amelie. J’utilise une voix québécoise.
Audrey              fr_FR    # Bonjour, je m’appelle Audrey. J’utilise une voix française.
Felix               fr_CA    # Salut! On m’appelle Felix. J’utilise une voix canadienne.
Fred                en_US    # I'm Fred and I truly enjoy living inside this chic aluminum box.
Samantha            en_US    # Hi, my name is Samantha. I use an American-English voice.
Thomas              fr_FR    # Bonjour, je m’appelle Thomas. J’utilise une voix française.
Victoria            en_US    # Isn't it great to use a computer that can talk to you?
Virginie            fr_FR    # Bonjour, je m’appelle Virginie. J’utilise une voix française.
                ''')
        self._a1 = self._i.split('\n')
        s1 = ''
        self._a2 = []
        for line in self._i.splitlines():
            self._a2.append(tuple(line.split("           ")))

        if self.is_mac:
            try:
                s1 = (subprocess.check_output(
                    ''.join([self.app, " --file-format=? "]),
                    shell=True))
                # Python 3 : a bytes-like
                # object is required
                self._f = codecs.decode(s1, 'utf-8')
            except:
                # We may need to use sample values, if the local
                # `say --file-format=?` command
                # returns nothing.
                s1 = ''
                self._f = ''
        if len(self._f) == 0:
            if os.name == 'nt':
                self._f = (
                    "                           (,) []\n"
                    )
            else:
                self._f = (
                    "WAVE  WAVE                 (.wav) [lpcm,ulaw,alaw]\n"
                    )
        self._a3 = self._f.split('\n')
        self._a4 = []
        for line in self._f.splitlines():
            self._a4.append(tuple(line.split('(')))

    def _getvoicename(self, inti):
        s1 = ''
        try:
            s1 = self._a2[inti][0]
        except:
            s1 = ''
        return s1

    def _getlanguagecountry(self, inti):
        s1 = ''
        try:
            s1 = self._a2[inti][1].split('#')[0].strip().replace('_', '-')
        except:
            s1 = ''
        return s1

    def _getlanguage(self, inti):
        s1 = self._getlanguagecountry(inti)
        return s1.split('-')[0].lower()

    def _getsamplephrase(self, inti):
        s1 = ''
        try:
            s1 = self._a2[inti][1].split('#')[1].strip()
        except:
            s1 = ''
        return s1

    def _getsayfileextensionstr(self, inti):
        s1 = ''
        try:
            s1 = self._a4[inti][1].split(')')[0].lower()
        except:
            s1 = ''
        return s1

    def voicesampletext(self, s0):
        '''
        Returns a voice sample string in the form `Most people
        recognize me by my voice.` when given a voice name like "Alex"

        **Example 1**: `mydata.voicesampletext('Alex')` returns
        "Most people recognize me by my voice."
        because Alex is a MacOS voice.

        **Example 2**: `mydata.languagecountry('Ailani')` returns ""
        because no voice called "Ailani" is supported on any version
        of say.'''
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

    def _i_rate_voice(self, i_rate=0, _voice=''):
        '''Specific to MacOS say -- check rate and voice, and return
        a list with `[m_rate, _voice]`.'''
        m_rate = ''
        if bool(i_rate):
            try:
                if i_rate < 0:
                    m_rate = ' -r 110'
                elif i_rate != 0:
                    m_rate = ' -r 240'
            except:
                pass
        if _voice in ['Agnes', 'Albert']:
            _voice = "Alex"
        return m_rate, _voice

    def say_aloud(self, _file_spec='', _voice='', _requested_voice='',
                  i_rate=0):  # -> bool
        '''Read aloud using a MacOS system voice if the voice
        is not already talking. Returns `True` if there is no
        error.
        '''
        if os.path.isfile(readtexttools.get_my_lock('lock')):
            return True
        _speaker_conf = [self._i_rate_voice(i_rate, _voice)]
        m_rate = _speaker_conf[0][0]
        _voice = _speaker_conf[0][1]
        try:
            # We need to use subprocess here, because we want to test for
            # `CalledProcessError`.
            v_tag = '-v '
            if len(_voice) == 0:
                return False
            readtexttools.lock_my_lock()
            _command = ''.join([
                    self.app,
                    "%(m_rate)s %(v_tag)s%(_voice)s -f '%(_file_spec)s'" %locals()])
            s1 = (subprocess.check_output(
                _command,
                shell=True))
            readtexttools.unlock_my_lock()
            return len(s1) == 0
        except TypeError:
            # fork_exec() takes exactly 21 arguments (17 given)
            try:
                os.system(_command)
                readtexttools.unlock_my_lock()
                return True
            except:
                print('Cannot execute command: `%(_command)s`' %locals())
                return False
        except subprocess.CalledProcessError:
            # You clicked a button to cancel reading aloud, so `killall` stopped
            # the running process, with a `subprocess.CalledProcessError` here.
            # Let's tidy up for the next run.
            readtexttools.unlock_my_lock()
            return False

    def save_audio(self,
                   _file_spec='', _voice='', i_rate=0, _media_out='',
                   _audible=False, _visible=False):  # -> bool
        '''

+ `_file_spec` - Text file to speak
+ `_voice` - Supported voice
+ `i_rate` - Two speeds supported
+ `_visible` - Use a graphic media player, or False for invisible player
+ `_media_out` - Name of desired output media file
+ `_audible` - If false, then don't play the sound file
+ `_visible` - If false, then try playing in the background.
    '''
        if len(_media_out) == 0:
            return False
        m_rate = ''
        v_tag = '-v '

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
        _media_work = readtexttools.get_work_file_path(_media_out, _icon, 'TEMP') + '.aiff'

        # Remove old files.
        if os.path.isfile(_media_work):
            os.remove(_media_work)
        if os.path.isfile(_media_out):
            os.remove(_media_out)
        _app = self.app
        _command = "%(_app)s%(m_rate)s %(v_tag)s%(_voice)s -o '%(_media_work)s' -f '%(_file_spec)s' " %locals()
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
            _info = "Apple MacOS Speech Synthesis Voice: %(_voice)s" %locals()
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
            i1 = (len(s5) * - 1) + 1

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
            elif s5[: i1] == '~':
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

        if s1 in ["Agnes", "Alfred"]:
            s1 = "Alex"
        return s1


def main():
    '''Command line speech-dispatcher tool. Some implimentations of python
    require the long command line switch'''

    _xml_tool = readtexttools.XmlTransform()
    __file_spec = sys.argv[-1]
    _txt = ''
    i_rate = 0
    _language = ''
    _output = ''
    _output_module = ''
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
    if not os.path.isfile(__file_spec):
        print("I was unable to find the text file you specified!")
        usage()
        sys.exit(0)
    elif sys.argv[-1] == sys.argv[0]:
        usage()
        sys.exit(0)
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "hmolvr",
            ["help", "output_module=", "output=", "language=", "voice=",
             "rate="])
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
                i_rate = int(a)
            except ValueError:
                pass
        else:
            assert False, "unhandled option"

    if os.path.isfile('/usr/bin/say'):
        _say_formats = SayFormats()
        mac_reader = _say_formats.voice(_language)
        if bool(_voice):
            for line in _say_formats._a1:
                if line.startswith('%(_voice)s ' %locals()):
                    mac_reader = _voice
                    break
        if len(_output) == 0:
            if not _say_formats.say_aloud(__file_spec, mac_reader, _voice,
                                          i_rate):
                if _voice in NET_SERVICE_LIST:
                    if not net_play(__file_spec, _language, i_rate, _voice):
                        print(network_read_text_file.network_problem(_voice))
        else:
            _say_formats.save_audio(__file_spec, mac_reader, i_rate, _output,
                                    False, False)
        sys.exit(0)
    elif os.name in ['posix']:
        if not USE_SPEECHD:
            readtexttools.web_info_translate(
                '''The `speechd` library is not compatible with your application
or platform.''',
                _language)
            sys.exit(0)
        _spd_formats = SpdFormats()
        if not _spd_formats.spd_ok:
            print("The `speechd` python 3 library is required.")
            usage()
            sys.exit(0)
        if not _spd_formats.set_up():
            print('''The python 3 `speechd` setup failed. Check for a system update and
restart your computer.''')
            usage()
            sys.exit(0)
        _testing = False
        if not _spd_formats.speak_spd(_output_module, _language,
                                      _voice, i_rate, __file_spec):
            # Error - Try resetting `speechd`
            hard_reset('speech-dispatcher')
    sys.exit(0)


if __name__ == "__main__":
    main()
