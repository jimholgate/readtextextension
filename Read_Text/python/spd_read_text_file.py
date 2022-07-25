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

See also: [Classic
Confinement](https://ubuntu.com/blog/how-to-snap-introducing-classic-confinement)

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
import readtexttools
import network_read_text_file
try:
    import webbrowser
except:
    pass
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


def net_play(_file_spec='', _language='en-US', i_rate=0, _requested_voice=''): # -> bool
    '''Attempt to play a sound from the network.'''
    if network_read_text_file.network_ok(_language):
        if _requested_voice in ['AUTO', 'NETWORK', 'AWS',
                                'AZURE', 'GOOGLECLOUD', 'GTTS']:
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
        self.client_app = readtexttools.app_signature()
        self.xml_tool = readtexttools.XmlTransform()
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


    def spdsay_supports_language(self, _lang='en', experimental=False):  # -> Bool
        '''Verify spd-say supports language. If spd-say is not installled
        and `experimental is `True` then return languages nominally
        supported by `espeak`.'''
        _imported_meta = readtexttools.ImportedMetaData()
        _short_lang = _lang.split('-')[0].split('_')[0]
        _result = _imported_meta.execute_command(
                        'spd-say -L ')
        if len(_result) == 0:
            print('''NOTICE:
A python script could not use `spd-say`, so it could not determine all
of the available languages. Install package `speech-dispatcher-utils`.''')
            if experimental:
                return _short_lang in ['en', 'af', 'de', 'eo', 'es', 'fi',
                                       'fr', 'it', 'pt', 'ro', 'cs', 'cy',
                                       'el', 'nl', 'no', 'hi', 'pl', 'ru',
                                       'sv', 'vi']
            _result = ' '
        return _result.count(''.join([' ', _short_lang, ' '])) != 0


    def set_up(self):  # -> bool
        '''Set up the instance of speechd'''
        if not self.spd_ok:
            return False
        try:
            # Sometimes speech-dispatcher sounds distorted and echoes
            # on first run. You can fix it with a `hard_reset` --help            
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

    def sanitize_json(self, content= ''):  # -> str
        '''Escape json characters in content'''
        return content.strip().replace(
            '{', '\\u007B').replace(
                '}', '\\u0070').replace(
                    '"', '\\u0022').replace(
                        '@', '\\u0040')

    def set_json_content(self, output_module='', language='en',
                         voice='MALE1', i_rate=0, 
                         _file_spec=''): # -> str
        '''Sanitize content and return json string'''
        s_rate = str(i_rate)
        output_module= self.sanitize_json(output_module)
        language = self.sanitize_json(language)
        voice = self.sanitize_json(voice)
        s_rate = self.sanitize_json(s_rate)
        _file_spec = self.sanitize_json(_file_spec)

        return '''{
  "output_module": "%(output_module)s",
  "language": "%(language)s",
  "voice": "%(voice)s",
  "i_rate": %(s_rate)s,
  "file_spec": "%(_file_spec)s"
}''' %locals()

    def speak_spd(self, output_module='', language='',
                      voice='', i_rate=0, _file_spec=''): # -> bool
        '''Set user configuration settings'''
        _lock = readtexttools.get_my_lock("lock")
        _try_voice = voice
        if voice not in self.all_voices:
            _try_voice = "MALE1"
        if os.path.isfile(_lock):
            self.client.close()
            time.sleep(0.2)
            hard_reset('speech-dispatcher')
            readtexttools.unlock_my_lock()
            return True
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
                    self.client.set_voice(_try_voice.upper())
            except AssertionError:
                if not self.spdsay_supports_language(
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
                        self.json_content = self.set_json_content(
                                output_module, language, voice, i_rate,
                                _file_spec)
                        readtexttools.write_plain_text_file(self.local_json,
                                                            self.json_content,
                                                            'utf-8')
                        retval = net_play(_file_spec, language, i_rate, voice)
                        os.remove(self.local_json)
                        return retval
                    return False
            else:
                readtexttools.unlock_my_lock()
                pass
            self.client.set_rate(i_rate)
        except (ImportError, NameError, speechd.SpawnError):
            if len(voice) != 0:
                readtexttools.unlock_my_lock()
                return bool(net_play(_file_spec, language, i_rate, voice))
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
        concise_lang = ''.join([language.lower(), '-']).split('-')[0].split('_')[0]
        _txt = readtexttools.strip_xml(_txt)
        _txt = readtexttools.strip_mojibake(concise_lang, _txt)
        if self.xml_tool.use_mode in ['text']:
            _message = ' " %(_txt)s"' % locals()   
        else:
            _txt = self.xml_tool.clean_for_xml(_txt)
            _message = '''<?xml version='1.0'?>
<speak version='1.1' xml:lang='%(language)s'>%(_txt)s</speak>''' % locals()            
        _time = guess_time(_txt, i_rate, _file_spec, language)
        self.client.set_data_mode(self.xml_tool.use_mode)
        self.client.set_punctuation(speechd.PunctuationMode.SOME)
        if language in ['en-US', 'en-AS', 'en-PH', 'en-PR', 'en-UM', 'en-VI']:
            _client_voices = self.client.list_synthesis_voices()
            if bool(voice):
                # Don't alter user's choice.
                pass
            elif ('Bdl', 'en', 'none') in _client_voices:
                try:
                    self.client.set_synthesis_voice('Bdl')
                except(AttributeError, SyntaxError, TypeError):
                    pass
            elif ('English (America)+male1', 'en-US',
                  'male1') in _client_voices:
                try:
                    self.client.set_synthesis_voice('English (America)+male1')
                except (AttributeError, SyntaxError, TypeError):
                    pass
        self.client.speak(_message)
        time.sleep(_time)
        self.client.close()
        readtexttools.unlock_my_lock()
        return True

    def list_synthesis_voices(self):  # -> (tuple | None)
        '''List synthesis voices. i. e.: ('Alan', 'en', 'none', ...)'''
        if bool(self.client):
            return self.client.list_synthesis_voices()
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
        self.say = ''
        self.lock = readtexttools.get_my_lock("lock")
        if self.is_mac:
            self.say = 'say'
            if os.path.isfile('/usr/bin/say'):
                self.say = '/usr/bin/say'
            try:
                s1 = (subprocess.check_output(
                    ''.join([self.say, ' --voice="?"']),
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
                    ''.join([self.say, " --file-format=? "]),
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

    def say_aloud(self, _file_spec='', _voice='', _requested_voice='',
                  _language='', i_rate=0):  # -> bool
        '''Read aloud using a MacOS system voice if the voice
        is not already talking. Returns `True` if there is no
        error. '''
        if os.path.isfile(readtexttools.get_my_lock('lock')):
            return True
        m_rate = ''
        if bool(i_rate):
            try:
                if i_rate < 0:
                    m_rate = ' -r 110'
                elif not i_rate == 0:
                    m_rate = ' -r 240'
            except:
                pass
        if _voice in ['Agnes', 'Albert']:
            _voice = "Alex"
        try:
            # We need to use subprocess here, because we want to test for
            # `CalledProcessError`.
            v_tag = '-v '
            if len(_voice) == 0:
                return net_play(_file_spec, _language, i_rate, _requested_voice)
            readtexttools.lock_my_lock()
            s1 = (subprocess.check_output(
                ''.join([
                    self.say,
                    "%(m_rate)s %(v_tag)s%(_voice)s -f '%(_file_spec)s'" %locals()]),
                shell=True))
            readtexttools.unlock_my_lock()
            return len(s1) == 0
        except subprocess.CalledProcessError:
            # You clicked a button to cancel reading aloud, so `killall` stopped
            # the running process, raising a `subprocess.CalledProcessError` here.
            # Let's tidy up for the next run.
            readtexttools.unlock_my_lock()
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
            sys.argv[1:], "holvr",
            ["help", "output_module=", "language=", "voice=", "rate="])
    except (getopt.GetoptError):
        print('option was not recognized')
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output_module"):
            _output_module = a
            
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
        _say_formats.say_aloud(__file_spec, mac_reader, _voice, _language, i_rate)
        sys.exit(0)
    elif os.name in ['posix']:
        if not USE_SPEECHD:
            print('''The `speechd` library is not compatible with your application or platform.''')
            try:
                if _language[:2] in ['en']:
                    _language = 'es'
                webbrowser.open_new(
                    'https://translate.google.com/?sl=auto&tl=%(_language)s&text=The+python+`speechd`+library+is+not+compatible+with+your+application+or+platform&op=translate' %locals()
                    )
            except NameError:
                pass
            exit()
        _spd_formats = SpdFormats()
        if not _spd_formats.spd_ok:
            print("The `speechd` python 3 library is required.")
            usage()
            exit()
        if not _spd_formats.set_up():
            print('''The python 3 `speechd` setup failed. Check for a system update and
restart your computer.''')
            usage()
            exit()
        _testing = False
        if not _spd_formats.speak_spd(_output_module, _language,
                                      _voice, i_rate, __file_spec):
            # Error - Try resetting `speechd`
            hard_reset('speech-dispatcher')
    sys.exit(0)


if __name__ == "__main__": 
    main()
