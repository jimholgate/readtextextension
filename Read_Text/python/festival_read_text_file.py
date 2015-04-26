#!/usr/bin/env python
# -*- coding: UTF-8-*-
'''
Festival
========

Reads a text file using festival and a media player.

The festival engine is a software speech synthesizer.

Install festival using a package manager to install a festivox or festival
voice.  The package manager should automatically select the festival package
and the required support files.

If you are using this extension to create still frame videos you need ffmpeg
or avconv. Webm is the recommended video format.  If you are creating a long
video, be patient.  It can take a long time for the external program to render
it.

Read Selection... Dialog setup:
-------------------------------

External program:

    /usr/bin/python

Command line options (default):

    "(FESTIVAL_READ_TEXT_PY)" "(TMP)"

or (save as a .wav file in the home directory):

    "(FESTIVAL_READ_TEXT_PY)" --output "(HOME)(NOW).wav" "(TMP)"

See the manual page for `text2wave` for more detailed information

[Read Text Extension](http://sites.google.com/site/readtextextension/)

Copyright (c) 2011 - 2015 James Holgate

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
import platform
import sys
import readtexttools


def usage():
    '''
    Command line help
    '''
    sA = ' ' + os.path.split(sys.argv[0])[1]
    sB = '    ' + sA
    print ('\nFestival Read Text\n==================\n')
    print ('Reads a text file using text2wave and a media player.\n')
    print ('Converts format with `avconv`, `lame`, `faac` or `ffmpeg`.\n')
    print ('Usage\n-----\n')
    print(sB + ' "input.txt"')
    print(sB + ' --language [de|en|en-GB|es|fr|it] "input.txt"')
    print(sB + ' --visible "false" "input.txt"')
    print(sB + ' --output "output.wav" "input.txt"')
    print(sB + ' --output "output.[m4a|mp2|mp3|ogg]" "input.txt"')
    print(sB + ' --output "output.[avi|webm]" \ ')
    print('       --image "input.[png|jpg] "input.txt"')
    print(sB + ' --audible "false" --output "output.wav" \ ')
    print('       "input.txt"\n\n')


def festivalread(sFILEPATH,
                 sVISIBLE,
                 sAUDIBLE,
                 sTMP0,
                 sIMG1,
                 sC,
                 sEVAL1,
                 sB,
                 sART,
                 sDIM):
    '''
        sTXTFILE - Text File to speak
        sVISIBLE- Use a graphic media player, or False for invisible player
        sTMP0 - Name of desired output file
        sAUDIBLE - If false, then don't play the sound file
        sIMG1 - a .png or .jpg file if required.
        sC - text
        sEVAL1 - Linux text2wave command prefix, like '(voice_upc_ca_ona_hts)'
        sB - title
        sART - artist or author
        sDIM - Dimensions to scale photo '600x600'
    '''
    # Determine the output file name
    sOUT1 = readtexttools.fsGetSoundFileName(sTMP0, sIMG1, "OUT")
    # Determine the temporary file name
    sTMP1 = readtexttools.fsGetSoundFileName(sTMP0, sIMG1, "TEMP")

    # Delete old versions
    if os.path.isfile(sTMP1):
        os.remove(sTMP1)
    if os.path.isfile(sOUT1):
        os.remove(sOUT1)
    try:
        if "windows" in platform.system().lower():
            if readtexttools.getWinFullPath('festival/text2wave'):
                sBasApp = readtexttools.getWinFullPath('festival/festival.exe')
                sBasScr = readtexttools.getWinFullPath('festival/text2wave')
                sApp = sBasApp + ' --script "' + sBasScr + '"'
                s1 = sApp + ' "' + sFILEPATH + '" -o "' + sTMP1 + '"'
                readtexttools.myossystem(s1)
                readtexttools.ProcessWaveMedia(sB,
                                               sTMP1,
                                               sIMG1,
                                               sOUT1,
                                               sAUDIBLE,
                                               sVISIBLE,
                                               sART,
                                               sDIM)
            else:
                # With Windows, this script only supports reading text aloud.
                sApp = readtexttools.getWinFullPath('festival/festival.exe')
                s1 = sApp + '--tts  "' + sFILEPATH + '"'
            readtexttools.myossystem(s1)
        else:
            sApp = 'text2wave'
            # text2wave is an executable festival script
            if len(sEVAL1) == 0:
                s1 = sApp + ' "' + sFILEPATH + '" -o "' + sTMP1 + '"'
            else:
                s1 = sApp + ' -eval "' + sEVAL1
                s1 = s1 + '" "' + sFILEPATH + '" -o "' + sTMP1 + '"'
            readtexttools.myossystem(s1)
            readtexttools.ProcessWaveMedia(sB,
                                           sTMP1,
                                           sIMG1,
                                           sOUT1,
                                           sAUDIBLE,
                                           sVISIBLE,
                                           sART,
                                           sDIM)
    except IOError as err:
        print ('I was unable to read!')
        usage()
        sys.exit(2)


def main():
    sWAVE = ''
    sVISIBLE = ''
    sAUDIBLE = ''
    sTXTFILE = ''
    sRATE = '100%'
    sPITCH = '100%'
    sIMG1 = ''
    sEVAL1 = ''
    sTIT = ''
    sART = ''
    sDIM = '600x600'
    sFILEPATH = sys.argv[-1]
    if os.path.isfile(sFILEPATH):
        if (sys.argv[-1] == sys.argv[0]):
            usage()
            sys.exit(0)
        elif (os.path.isfile('/usr/bin/text2wave') !=
              os.path.isfile('/usr/bin/python')):
            usage()
            sys.exit(0)
        try:
            opts, args = getopt.getopt(
                sys.argv[1:],
                'hovarpietnd',
                ['help',
                 'output=',
                 'visible=',
                 'audible=',
                 'rate=',
                 'pitch=',
                 'image=',
                 'eval=',
                 'title=',
                 'artist=',
                 'dimensions='])
        except getopt.GetoptError as err:
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
            elif o in ('-r', '--rate'):
                sRATE = a
            elif o in ('-p', '--pitch'):
                sPITCH = a
            elif o in ('-i', '--image'):
                sIMG1 = a
            elif o in ('-e', '--eval'):
                sEVAL1 = a
            elif o in ('-t', '--title'):
                sTIT = a
            elif o in ('-n', '--artist'):
                sART = a
            elif o in ('-d', '--dimensions'):
                sDIM = a
            else:
                assert False, 'unhandled option'
        try:
            # https://docs.python.org/3/library/codecs.html#standard-encodings
            #
            # iso-8859-15 is for western European languages. Should festival
            # include a switch to allow Asian & complex languages to use utf-8?
            # We were using `sys.getfilesystemencoding()`, but letting the
            #  system choose could cause garbled or missing speech utterances.
            oFILE = codecs.open(sFILEPATH, mode='r', encoding='iso8859_15')
        except (IOError):
            print ('I was unable to open the file you specified!')
            usage()
        else:
            sTXT = oFILE.read()
            oFILE.close()
            if len(sTXT) != 0:
                sTXT = readtexttools.cleanstr(sTXT, readtexttools.bFalse())
                sA = '" <speed level = \'' + sRATE + '\'>'
                sA = sA + "<pitch level = '" + sPITCH + '\'>'
                sA = sA + sTXT + '</pitch></speed>"'
                sB = readtexttools.checkmyartist(sART)
                sC = readtexttools.checkmytitle(sTIT, 'festival')
                festivalread(sFILEPATH,
                             sVISIBLE,
                             sAUDIBLE,
                             sWAVE,
                             sIMG1,
                             sA,
                             sEVAL1,
                             sC,
                             sB,
                             sDIM)
    else:
        print ('I was unable to find the file you specified!')
    sys.exit(0)

if __name__ == '__main__':
    main()

