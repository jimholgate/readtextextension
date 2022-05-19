#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Speech-Dispatcher
=================

 * `spd-conf` - A tool for configuration of Speech Dispatcher and problem
    diagnostics
 * `spd-say` - send text-to-speech output request to speech-dispatcher
 * `speech-dispatcher` - server process managing speech requests in Speech
    Dispatcher

Resolving Problems
------------------

### You updated LibreOffice and now speech synthesis doesn't work

If you updated LibreOffice using a simple **snap store** user interface,
then the snap daemon will protect your computer by refusing permission to
run some third party applications. To run this extension using the snap
version of LibreOffice, you can reinstall LibreOffice snap from the
command line using the following commands:

    sudo snap remove libreoffice
    sudo snap refresh
    sudo snap install libreoffice --classic

[More](https://ubuntu.com/blog/how-to-snap-introducing-classic-confinement)

If you update the version using self-contained "secure" package, the
security settings of the package might prohibit your application from
running extensions that rely on system resources.

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

Some languages sound better if you change the `speech-dispatcher` defaults.

[More](http://cvs.freebsoft.org/doc/speechd/speech-dispatcher.html)

Installation
------------

    sudo apt-get install speech-dispatcher python3-speechd
    info spd-say
    info spd-conf
    spd-conf

Test the speech-dispatcher using the command:

    spd-say -t female1 -l en-US  "Testing 1 2 3"

For more information, read the documentation at the speech-dispatcher web site.

[More](http://cvs.freebsoft.org/doc/speechd/speech-dispatcher.html)

Read Selection... Dialog setup
------------------------------

External program:

        /usr/bin/python3

Command line options (default voice):

        "(SPD_READ_TEXT_PY)" "(TMP)"

or (specific language):

        "(SPD_READ_TEXT_PY)" --language "(SELECTION_LANGUAGE_CODE)" \
          --voice "MALE1" "(TMP)"

[Read Text Extension](http://sites.google.com/site/readtextextension/)

Copyright (c) 2010 - 2022 James Holgate

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
import readtexttools


def hard_reset(sd='speech-dispatcher'):  # -> bool
    '''kill posix process'''
    if not readtexttools.have_posix_app('killall'):
        return False
    whoami = get_whoami()
    command = '''killall %(sd)s''' % locals()
    if whoami:
        command = '''killall -q -u %(whoami)s %(sd)s''' % locals()
    return readtexttools.my_os_system(command)


def usage():  # -> None
    _message = '    ' + os.path.split(sys.argv[0])[1]
    sB = '      '

    print('''Speech-dispatcher
=================

Reads a text file using the speech-dispatcher.

Usage
-----

    spd_read_text_file.py [--output_module="xx"] [--language="xx"] \ 
       [--voice="xx"] [--rate="nn"] input.txt 

Use a specific output module
    spd_read_text_file.py --output_module "espeak-generic" "TextFile.txt" 

Use a specific language - en, fr, es...
    spd_read_text_file.py --language "fr" "TextFile.txt" 

Use a specific voice - MALE1, FEMALE1, ... CHILD_FEMALE
    spd_read_text_file.py --voice "MALE1" "TextFile.txt" 

To say the text slower - minimum -100
    spd_read_text_file.py --rate "-20" "TextFile.txt" 

To say the text faster - maximum 100
    spd_read_text_file.py --rate "20" "TextFile.txt"

[More](http://htmlpreview.github.io/?https://github.com/brailcom/speechd/blob/master/doc/speech-dispatcher.html)    
''')
    hard_reset('speech-dispatcher')


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


def guess_time(sSTR, sRATE, sFILEPATH, _language):  # -> int
    '''
        Estimate time in seconds for speech to finish
    '''
    i_rate = ((int(sRATE) * 0.8) + 100) / 100
    i_seconds = (1 + len(sSTR) / 18)
    retval = i_rate * i_seconds
    if i_seconds < 60:
        _command = "/usr/bin/espeak"
        if os.path.isfile('/usr/bin/espeak-ng'):
            _command = '/usr/bin/espeak-ng'
        if 'nt' in os.name.lower():
            sECE = "eSpeak/command_line/espeak.exe"
            _command = readtexttools.get_nt_path(sECE)
        if os.path.isfile(_command):
            sWAVE = readtexttools.get_work_file_path("", "", "TEMP")
            try:
                espeak_read_text_file.espkread(sFILEPATH, _language, "", "",
                                               sWAVE, "", "",
                                               "show_sound_length_seconds", "",
                                               "", 50, 160)
                retval = i_rate * (readtexttools.sound_length_seconds(sWAVE))
            except (AttributeError, TypeError, ImportError):
                # Library is missing or incorrect version
                print('A local library for guess_time is missing or damaged.')
                retval = i_rate * i_seconds
    print(retval, i_rate * i_seconds)
    return retval


def main():  # -> None
    '''Command line speech-dispatcher tool. Some implimentations of python
    require the long command line switch'''
    _xml_tool = readtexttools.XmlTransform()
    _in_file = sys.argv[-1]
    _txt = ''
    i_rate = 0
    _language = ''
    _voice = ''
    verbose_language = os.getenv('LANGUAGE')
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
    if not os.path.isfile(_in_file):
        print("I was unable to find the text file you specified!")
        usage()
        sys.exit(0)
    elif sys.argv[-1] == sys.argv[0]:
        usage()
        sys.exit(0)

    elif not os.path.isfile('/usr/bin/speech-dispatcher'):
        print('''FAIL: The python %(py_m_verbose)s `speechd` library needs
`/usr/bin/speech-dispatcher` to run, but the program
is not available. If you are using an application with
no execution permission, you need to grant permission to
read and execute `speech-dispatcher`.
''' % locals())
    try:
        import speechd
    except (ImportError):
        if int(py_m) < 3:
            print("You are using python %(py_m)s, but python 3 is required." %
                  locals())
            sys.exit(2)
        try:
            for test_path in ['/snap/libreoffice', '/var/', '/.var/']:
                if test_path in os.path.realpath(__file__):
                    usage()
                    sys.exit(2)
            import speechd_py as speechd
            print('''NOTE: Couldn't import the system python %(py_m)s
`speechd` library. Using python %(py_m_verbose)s''' % locals())
        except (ImportError):
            readtexttools.pop_message(
                "Read Text",
                '''This LibreOffice package cannot use <b>speech-dispatcher</b>.
Install `python3-speechd` using your package manager.''')
            print('''Could not import python %(py_m)s speechd_py resources.

    sudo apt install python3-speechd

See also: [pip install](https://pip.pypa.io/en/stable/cli/pip_install/)''' %
                  locals())
            sys.exit(2)
    try:
        _client_app = readtexttools.app_signature()
        _client_user = get_whoami()
        bug_cleaner = speechd.SSIPClient(_client_app, _client_user, None, None)
        bug_cleaner.speak('\t')
        bug_cleaner.close()
        # Bug? speech-dispatcher sounds distorted and echoes on first run.
        # You can fix it with a `hard_reset` --help
        client = speechd.SSIPClient(_client_app, _client_user, None, None)
    except (ImportError, NameError, speechd.SpawnError):
        print("FAIL: Missing needed `speechd` voice synthesis resources!\n\n")
        usage()
        sys.exit(2)
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "holvr",
            ["help", "output_module=", "language=", "voice=", "rate="])
    except (getopt.GetoptError):
        # print help information and exit:
        print('option was not recognized')
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            client.close
            sys.exit()
        elif o in ("-o", "--output_module"):
            client.set_output_module(a)
        elif o in ("-l", "--language"):
            # 2 letters lowercase - fr Français, de Deutsch...
            concise_lang = ''.join([a.lower(), '-']).split('-')[0]
            client.set_language(concise_lang)
            _language = a
        elif o in ("-v", "--voice"):
            # MALE1, MALE2 ...
            _voice = a.upper()
            client.set_voice(_voice)
        elif o in ("-r", "--rate"):
            client.set_rate(int(a))
            i_rate = a
        else:
            assert False, "unhandled option"
    try:
        f = codecs.open(_in_file,
                        mode='r',
                        encoding=sys.getfilesystemencoding())
    except (IOError):
        client.close()
        print("I was unable to open the file you specified!")
        usage()
        sys.exit(0)
    _txt = f.read()
    f.close()
    if len(_txt) != 0:
        _txt = readtexttools.strip_xml(_txt)
        _coding = 'utf-8'
        _txt = readtexttools.strip_mojibake(concise_lang, _txt)
    if _xml_tool.use_mode in ['text']:
        _message = ' " %(_txt)s"' % locals()
        sys.exit(0)
    _txt = _xml_tool.clean_for_xml(_txt)
    _message = '''<?xml version='1.0'?>
<speak version='1.1' xml:lang='%(_language)s'>%(_txt)s</speak>''' % locals()
    _lock = readtexttools.get_my_lock("lock")
    if os.path.isfile(_lock):
        client.close()
        readtexttools.my_os_system("spd-say --cancel")
        time.sleep(0.2)
        hard_reset('speech-dispatcher')
        readtexttools.unlock_my_lock()
    else:
        readtexttools.lock_my_lock()
        _time = guess_time(_txt, i_rate, _in_file, _language)
        client.set_data_mode(_xml_tool.use_mode)
        client.set_punctuation(speechd.PunctuationMode.SOME)
        # print(client.list_synthesis_voices())
        # print(client.list_output_modules()) #  - i. e.: (espeak-ng-mbrola, espeak-ng, ...)
        # client.list_synthesis_voices() - i. e.: ('Alan', 'en', 'none', ...)
        if _language in ['en-US', 'en-AS', 'en-PH', 'en-PR', 'en-UM', 'en-VI']:
            _client_voices = client.list_synthesis_voices()
            if bool(_voice):
                # Don't alter user's choice.
                pass
            elif ('Bdl', 'en', 'none') in _client_voices:
                try:
                    client.set_synthesis_voice('Bdl')
                except (AttributeError, SyntaxError, TypeError):
                    pass
            elif ('English (America)+male1', 'en-US', 'male1') in _client_voices:
                try:
                    client.set_synthesis_voice('English (America)+male1')
                except (AttributeError, SyntaxError, TypeError):
                    pass
        client.speak(_message)
        time.sleep(_time)
        client.close()
        readtexttools.unlock_my_lock()
    sys.exit(0)


if __name__ == "__main__":
    main()
