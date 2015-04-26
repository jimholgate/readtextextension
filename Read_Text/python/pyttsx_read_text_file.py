#!/usr/bin/env python
# -*- coding: UTF-8-*-
'''
To read a plain text file using Python pyttsx speech.
    Designed for reading text aloud with the Windows SAPI5 system.
    For other systems, read documentation for pyttsx for installation help.

For Windows :
    get Python 2.x from
        http://www.python.org/
    get Python Extensions for Windows from
        http://sourceforge.net/projects/pywin32/files/
    get the Speech assistive technology pyTTS module from:
        http://pypi.python.org/pypi/pyttsx/1.0

Read Text Extension for OpenOffice.org (for Windows) :
    See: http://sites.google.com/site/readtextextension/
    Tools > Add-Ons > Read Selection... Dialog setup:
    External program: C:\Program Files\Python\python.exe
    External program alternate: C:\Program Files\Python\pythonw.exe
    Command line options: "(HOME)Downloads\read_text_file.py" "(TMP)"
    or "(HOME)Downloads\read_text_file.py" --voice "Microsoft Sam" "(TMP)"

Copyright (c) 2010 - 2015 James Holgate

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
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


def usage():
    sA = '    ' + os.path.split(sys.argv[0])[1]
    print ('\nPyttsx Read Text\n================\n')
    print ('Reads a text file using the Windows pyttsx library.\n')
    print ('Usage\n-----\n')
    print ("To say the text with a specific voice")
    print (sA + ' --voice "xxxxxx" "TextFile.txt"')
    print ("")
    print ("To say the text with the default voice")
    print (sA + ' "TextFile.txt"')
    print ("")
    print ("To say the text slower")
    print (sA + ' --rate "-20" "TextFile.txt"')
    print ("")
    print ("To say the text faster")
    print (sA + ' --rate "20" "TextFile.txt"')
    print ("")


def ReadTheStringAloud(voiceName, voiceRate, speechString):
    '''
    Says speechString, using the default voice or voiceName voice
    Positive voiceRate is faster; Negative voiceRate is slower
    '''
    try:
        import pyttsx
        engine = pyttsx.init()
    except (ImportError):
        print ('I did not find the pyttsx text to speech resources!')
        usage()
        sys.exit(2)
    try:
        engine.setProperty(
            'rate',
            engine.getProperty('rate') + int(voiceRate))
    except Error:
        print ('I did not understand the rate!')
        usage()
        sys.exit(2)
    voices = engine.getProperty('voices')
    for voice in voices:
        if voice.name == voiceName:
            engine.setProperty('voice', voice.id)
            break
    engine.say(speechString)
    engine.runAndWait()


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hvr",
                                   ["help",
                                    "voice=",
                                    "rate="])
    except (getopt.GetoptError):
        # print help information and exit:
        print ('option -a not recognized')
        usage()
        sys.exit(2)
    voiceName = ""
    voiceRate = 0
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-v", "--voice"):
            voiceName = a
        elif o in ("-r", "--rate"):
            voiceRate = a
        else:
            assert False, "unhandled option"
    try:
        f = codecs.open(
            sys.argv[-1],
            mode='r',
            encoding=sys.getfilesystemencoding())
    except IOError:
        print ('I was unable to open the file you specified!')
        usage()
    else:
        s = f.read()
        f.close()
        ReadTheStringAloud(voiceName, voiceRate, s)
        sys.exit(0)

if __name__ == "__main__":
    main()
