#!/usr/bin/env python3
# -*- coding: UTF-8-*-
'''
Speech-Dispatcher
=================

 * `spd-conf` - A tool for configuration of Speech Dispatcher and problem
    diagnostics
 * `spd-say` - send text-to-speech output request to speech-dispatcher
 * `speech-dispatcher` - server process managing speech requests in Speech
    Dispatcher

This script helps read text extension toggle the `speech-dispatcher` daemon
on and off. Read text extension uses a lock file to determine if speech
synthesis is running.  The extension invokes the speech-dispatcher python 3
SSIPClient` if there is not a lock file or cancels speech-dispatcher if there
is a lock file.

 * Read text extension does not normally require speech-dispatcher to read text
   aloud.
 * You can edit speech-dispatcher settings to manage speech synthesis
   preferences.
 * Unless you use this script, read text extension doesn't use the
   speech-dispatcher daemon or the `spd-conf` speech-dispatcher settings.

Installation
------------

    sudo apt-get install speech-dispatcher
    info spd-say
    info spd-conf
    spd-conf

Test the speech-dispatcher using the command:

        spd-say "Text to say"

For more information, read the documentation at the speech-dispatcher web site.

[Link](http://cvs.freebsoft.org/doc/speechd/speech-dispatcher.html)

Read Selection... Dialog setup:
-------------------------------

External program:

        /usr/bin/python3

Command line options (default voice):

        "(SPD_READ_TEXT_PY)" "(TMP)"

or (specific language):

        "(SPD_READ_TEXT_PY)" --language "(SELECTION_LANGUAGE_CODE)" \
          --voice "MALE1" "(TMP)"

[Read Text Extension](http://sites.google.com/site/readtextextension/)

Copyright (c) 2010 - 2015 James Holgate

'''
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals
    )
import codecs
import getopt
import os
import sys
import espeak_read_text_file
import readtexttools


def usage():
    '''Show the usage options'''
    print('''Speech-dispatcher Read Text
===========================

Reads a text file using the speech-dispatcher.

Usage
-----

`spd_read_text_file.py [--output_module="xx"] [--language="xx"]
[--voice="xx"] [--rate="nn"] input.txt`

Use a specific output module: 
`spd_read_text_file.py --output_module "espeak-generic" "TextFile.txt"`

Use a specific language - en, fr, es...
`spd_read_text_file.py --language "fr" "TextFile.txt"`

Use a specific voice - MALE1, FEMALE1, ... CHILD_FEMALE:
`spd_read_text_file.py --voice "MALE1" "TextFile.txt"`

To say the text slower - minimum -100:
`spd_read_text_file.py --rate "-20" "TextFile.txt"`

To say the text faster - maximum 100:
`spd_read_text_file.py --rate "20" "TextFile.txt"`''')


def guessTime(sSTR, sRATE, sFILEPATH, sLANG):
    '''
        Estimate time in seconds for speech to finish
    '''
    iRATE = ((int(sRATE) * 0.8) + 100) / 100
    iSecs = (1 + len(sSTR) / 18)
    retval = iRATE * iSecs
    if iSecs < 60:
        sCommand = "/usr/bin/espeak"
        if 'nt' in os.name.lower():
            sECE = "eSpeak/command_line/espeak.exe"
            sCommand = readtexttools.getWinFullPath(sECE)
        if os.path.isfile(sCommand):
            sWAVE = readtexttools.fsGetSoundFileName("", "", "TEMP")
            try:
                espeak_read_text_file.espkread(sFILEPATH, sLANG,
                                               "",
                                               "",
                                               sWAVE,
                                               "",
                                               "",
                                               "ShowWavtoSeconds",
                                               "",
                                               "",
                                               50,
                                               160)
                retval = iRATE * (readtexttools.WavtoSeconds(sWAVE))
            except(AttributeError, TypeError, ImportError):
                # Library is missing or incorrect version
                print('A local library for guessTime is missing or damaged.')
                retval = iRATE * iSecs
    print (retval)
    return retval


def main():
    s1 = sys.argv[-1]
    i1 = 0
    if os.path.isfile(s1):
        if sys.argv[-1] == sys.argv[0]:
            usage()
            sys.exit(0)
        try:
            import speechd
            import time
            client = speechd.SSIPClient(readtexttools.fsAppSignature())
        except (ImportError):
            print ("I did not find the speechd voice synthesis resources!")
            usage()
            sys.exit(2)
        try:
            opts, args = getopt.getopt(sys.argv[1:],
                                       "holvr",
                                       ["help",
                                        "output_module=",
                                        "language=",
                                        "voice=",
                                        "rate="])
        except (getopt.GetoptError):
            # print help information and exit:
            print('option was not recognized')
            usage()
            sys.exit(2)
        for o, a in opts:
            if o in ("-h", "--help"):
                usage()
                sys.exit()
            elif o in ("-o", "--output_module"):
                client.set_output_module(a)
            elif o in ("-l", "--language"):
                # 2 letters lowercase - fr Français, de Deutsch...
                client.set_language(a[:2].lower())
                sLang = a
            elif o in ("-v", "--voice"):
                # MALE1, MALE2 ...
                client.set_voice(a.upper())
            elif o in ("-r", "--rate"):
                client.set_rate(int(a))
                i1 = a
            else:
                assert False, "unhandled option"
        try:
            f = codecs.open(s1, mode='r', encoding=sys.getfilesystemencoding())
        except (IOError):
            client.close()
            print ("I was unable to open the file you specified!")
            usage()
        else:
            sTXT = f.read()
            f.close()
            sA = ' " ' + sTXT + '"'
            sLock = readtexttools.getMyLock("lock")
            if os.path.isfile(sLock):
                client.close()
                readtexttools.myossystem("spd-say --cancel")
                readtexttools.UnlockMyLock()
            else:
                readtexttools.LockMyLock()
                sTime = guessTime(sA, i1, s1, sLang)
                client.set_punctuation(speechd.PunctuationMode.SOME)
                client.speak(sA)
                client.close()
                time.sleep(sTime)
                readtexttools.UnlockMyLock()
            sys.exit(0)
    else:
        print ("I was unable to find the text file you specified!")
        usage()


if __name__ == "__main__":
    main()
