#!/usr/bin/env python
# -*- coding: UTF-8-*-
'''
Pico
====

Reads a text file using pico2wave and a media player.

The SVOX Pico engine is a software speech synthesizer for German, English (GB
and US), Spanish, French and Italian.

SVOX produces a clear and distinct speech output made possible by the use of
Hidden Markov Model (HMM) algorithms.

[SVOX Pico](http://dafpolo.free.fr/telecharger/svoxpico/SVOX_Pico_Manual.pdf)

Install `pico2wave` using a package manager to install the following packages:

        libttspico0
        libttspico-utils
        libttspico-data

Due to license restrictions,the packages are formally part of Debian's
non-free category rather than Debian proper ("main"). The packages are also
available in Ubuntu's multiverse repository.

If you are using this extension to create still frame videos you need ffmpeg
or avconv.  Webm is the recommended video format. If you are creating a long
video, be patient.  It can take a long time for the external program to render
the video.

Read Selection... Dialog setup:
-------------------------------

External program:

        /usr/bin/python

Command line options (default):

        "(PICO_READ_TEXT_PY)" --language=(SELECTION_LANGUAGE_CODE) "(TMP)"

or (save as a .wav file in the home directory):

         "(PICO_READ_TEXT_PY)" --language=(SELECTION_LANGUAGE_CODE) \
           --output "(HOME)(NOW).wav" "(TMP)"

or (speak more slowly with a lowered pitch):

        "(PICO_READ_TEXT_PY)" --language=(SELECTION_LANGUAGE_CODE) \
          --rate=80% --pitch=80% "(TMP)"

See the manual page for `pico2wave` for more detailed information

[Read Text Extension](http://sites.google.com/site/readtextextension/)

Copyright (c) 2011 - 2018 James Holgate

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
import readtexttools

def usage():
    '''
    Command line help
    '''
    print('''Pico Read Text
==============

Reads a text file using pico2wave and a media player.

Converts format with `avconv`, `lame`, `faac` or `ffmpeg`.

Usage
-----

     pico_read_text_file.py "input.txt"
     pico_read_text_file.py --language [de|en|en-GB|es|fr|it] "input.txt"
     pico_read_text_file.py --visible "false" "input.txt"
     pico_read_text_file.py --rate=100% --pitch=100% "input.txt"
     pico_read_text_file.py --output "output.wav" "input.txt"
     pico_read_text_file.py --output "output.[m4a|mp2|mp3|ogg]" "input.txt"
     pico_read_text_file.py --output "output.[avi|webm]"
       --image "input.[png|jpg] "input.txt"
     pico_read_text_file.py --audible "false" --output "output.wav"
       "input.txt" ''')


def picoread(sTXT, sLANG, sVISIBLE, sAUDIBLE, sTMP0, sIMG1, sB, sART, sDIM):
    '''
    sTXT - Actual text to speak. The file must be written as utf-8.
    sLANG - Supported two or four letter language code - defaults to US English
    sVISIBLE- Use a graphic media player, or False for invisible player
    sTMP0 - Name of desired output media file
    sAUDIBLE - If false, then don't play the sound file
    sIMG1 - a .png or .jpg file if required.
    sB - Commentary or title for post processing
    sPOSTPROCESS - Get information, play file, or convert a file
    sART - Artist or Author
    sDIM - Dimensions to scale photo '600x600'
    '''
    sOUT1 = ''
    if sLANG[:2].lower() == 'de':
        s = 'de-DE'
    elif sLANG[:2].lower() == 'en':
        if sLANG[-2:].upper() in 'AU;BD;BS;GB;GH;HK;IE;IN;JM;NZ;PK;SA;TT':
            s = 'en-GB'
        else:
            s = 'en-US'
    elif sLANG[:2].lower() == 'es':
        s = 'es-ES'
    elif sLANG[:2].lower() == 'fr':
        s = 'fr-FR'
    elif sLANG[:2].lower() == 'it':
        s = 'it-IT'
    else:
        s = 'en-US'
    # Determine the output file name
    sOUT1 = readtexttools.fsGetSoundFileName(sTMP0, sIMG1, 'OUT')
    # Determine the temporary file name
    sTMP1 = readtexttools.fsGetSoundFileName(sTMP0, sIMG1, 'TEMP')

    # Delete old versions
    if os.path.isfile(sTMP1):
        os.remove(sTMP1)
    if os.path.isfile(sOUT1):
        os.remove(sOUT1)
    try:
        if 'nt' in os.name.lower():
            sCommand = readtexttools.getWinFullPath('opt/picosh.exe')
            if "de" in s.lower():
                s1 =''.join([
                        sCommand,
                        ' –v de-DE_gl0 "',
                        sTXT,
                        '" "',
                        sTMP1,
                        '"'])
            else:  # Pico for Windows defaults to British English
                s1 = ''.join([
                        sCommand,
                        ' "',
                        sTXT,
                        '" "',
                        sTMP1,
                        '"']) 
        else:
            sCommand = 'pico2wave'
            s1 = ''.join([
                    sCommand,
                    ' -l ',
                    s,
                    ' -w "',
                    sTMP1,
                    '"  ',
                    sTXT])
        readtexttools.myossystem(s1)
        readtexttools.ProcessWaveMedia(sB,
                                       sTMP1,
                                       sIMG1,
                                       sOUT1,
                                       sAUDIBLE,
                                       sVISIBLE,
                                       sART,
                                       sDIM
                                       )
    except (IOError):
        print ('I was unable to read!')
        usage()
        sys.exit(2)


def main():
    sLANG = 'en-US'
    sWAVE = ''
    sVISIBLE = ''
    sAUDIBLE = ''
    sTXT = ''
    sRATE = '100%'
    sPITCH = '100%'
    sIMG1 = ''
    sTIT = ''
    sART = ''
    sDIM = '600x600'
    sFILEPATH = sys.argv[-1]
    if os.path.isfile(sFILEPATH):
        if sys.argv[-1] == sys.argv[0]:
            usage()
            sys.exit(0)
        elif not os.path.isfile('/usr/bin/pico2wave'):
            print('Please install libttspico-utils.')
            usage()
            sys.exit(0)
        try:
            opts, args = getopt.getopt(
                sys.argv[1:],
                'hovalrpitnd',
                ['help',
                 'output=',
                 'visible=',
                 'audible=',
                 'language=',
                 'rate=',
                 'pitch=',
                 'image=',
                 'title=',
                 'artist=',
                 'dimensions='])
        except (getopt.GetoptError):
            # print help information and exit
            print('option -a not recognized')
            usage()
            sys.exit(2)
        for o, a in opts:
            if o in ('-h', '--help'):
                usage()
                sys.exit(0)
            elif o in ('-o', '--output'):
                sWAVE = a
            elif o in ('-v', '--visible'):
                sVISIBLE = a
            elif o in ('-a', '--audible'):
                sAUDIBLE = a
            elif o in ('-l', '--language'):
                sLANG = a
            elif o in ('-r', '--rate'):
                sRATE = a
            elif o in ('-p', '--pitch'):
                sPITCH = a
            elif o in ('-i', '--image'):
                sIMG1 = a
            elif o in ('-t', '--title'):
                sTIT = a
            elif o in ('-n', '--artist'):
                sART = a
            elif o in ('-d', '--dimensions'):
                sDIM = a
            else:
                assert False, 'unhandled option'
        try:
            oFILE = codecs.open(sFILEPATH, mode='r', encoding='utf-8')
        except (IOError):
            print ('I was unable to open the file you specified!')
            usage()
        else:
            sTXT = oFILE.read()
            oFILE.close()
            if len(sTXT) != 0:
                sTXT = readtexttools.stripxml(sTXT)
            if len(sTXT) != 0:
                sTXT = readtexttools.cleanstr(sTXT, readtexttools.bFalse())
                sA = ''.join([
                        '" <speed level = \'',
                        sRATE,
                        '\'>',
                        "<pitch level = '",
                        sPITCH,
                        '\'>',
                        sTXT,
                        '</pitch></speed>"'])
                sB = readtexttools.checkmyartist(sART)
                sC = readtexttools.checkmytitle(sTIT, "pico")
                picoread(sA,
                         sLANG,
                         sVISIBLE,
                         sAUDIBLE,
                         sWAVE,
                         sIMG1,
                         sC,
                         sB,
                         sDIM
                         )
    else:
        print ('I was unable to find the file you specified!')
    sys.exit(0)


if __name__ == "__main__":
    main()
