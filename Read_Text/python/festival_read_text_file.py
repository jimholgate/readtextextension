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

or (speak more slowly with a lowered pitch):

    "(FESTIVAL_READ_TEXT_PY)" --rate=75% --pitch=75% "(TMP)"

This python code uses [Sable][1] XML code to change speech rate and pitch.
Not all voices support Sable markup.  For unsupported voices, the rate and
pitch command line arguments do not change the sound rate and pitch.

See the info pages for `festival` for more information.

To change the speed and pitch of **recorded** sound files, use [Audacity][2],
a free multi-track audio editor and recorder.

[Read Text Extension][3]

Copyright (c) 2011 - 2018 James Holgate

  [1]: https://www.cs.cmu.edu/~awb/festival_demos/sable.html
  [2]: http://sourceforge.net/projects/audacity/
  [3]: http://sites.google.com/site/readtextextension/

'''
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals
    )
import codecs
import getopt
import math
import os
import sys
import readtexttools

def usage():
    '''
    Command line help
    '''

    print(r'''
Festival Read Text
==================

Reads a text file using text2wave and a media player.

Converts format with `avconv`, `lame`, `faac` or `ffmpeg`.

Usage
-----

     festival_read_text_file.py "input.txt"
     festival_read_text_file.py --language [de|en|en-GB|es|fr|it] "input.txt"
     festival_read_text_file.py --visible "false" "input.txt"
     festival_read_text_file.py --output "output.wav" "input.txt"
     festival_read_text_file.py --output "output.[m4a|mp2|mp3|ogg]" "input.txt"
     festival_read_text_file.py --output "output.[avi|webm]" \ 
       --image "input.[png|jpg] "input.txt"
     festival_read_text_file.py --audible "false" --output "output.wav" \ 
       "input.txt"
''')


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
Creates a temporary speech-synthesis sound file and optionally
reads the file aloud.

+ `sTXTFILE` - Text File to speak
+ `sVISIBLE`- Use a graphic media player, or False for invisible player
+ `sTMP0` - Name of desired output file
+ `sAUDIBLE` - If false, then don't play the sound file
+ `sIMG1` - a .png or .jpg file if required.
+ `sC` - text
+ `sEVAL1` - Linux text2wave command prefix, like `(voice_upc_ca_ona_hts)`
+ `sB` - title
+ `sART` - artist or author
+ `sDIM` - Dimensions to scale photo '600x600'
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
        if 'nt' in os.name.lower():
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
                s1 = ''.join([
                        sApp, ' "',
                        sFILEPATH,
                        '" -o "',
                        sTMP1,
                        '"'])
            else:
                s1 = ''.join([
                        sApp,
                        ' -eval "',
                        sEVAL1,
                        '" "',
                        sFILEPATH,
                        '" -o "',
                        sTMP1,
                        '"'])
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


def festivalSpeakerNameString(sA):
    '''
    [Sable][4]
    =======
    
    Use name in `<SPEAKER NAME="kal_diphone">` markup
    `(voice_upc_ca_ona_hts)` becomes **upc_ca_ona_hts**
    `(voice_kal_diphone)` becomes **kal_diphone**

    [4]: https://www.cs.cmu.edu/~awb/festival_demos/sable.html
    
    '''
    retVal = 'male1'
    if '(voice_' in sA:
        s1 = sA.replace('(voice_', '')
        s1 = s1.replace(')', '')
        retVal = s1
    return retVal
    

def festivalRateString(sA):
    '''
    Use RATE for value of Sable `<RATE SPEED="50%">` markup.
    Converts w3 Smil style percentage to Sable style percentage
    sA - rate expressed as a percentage.
    Use '100%' for default rate of 0% in Sable.
    Returns Sable rate as string between -99% and 100%.
    
    '''
    i2 = 0
    iMinVal = -99
    iMaxVal = 100
    retVal = 0
    s1 = ''
    
    try:
        if '%' in sA:
            s1 = sA.replace('%', '')
            s1 = s1.replace('-', '')
            i2 = int(s1) - 100
        else:
            i2 = 0
    except(TypeError):
       print ('I was unable to determine festival rate!')
    if i2 <= iMinVal:
        retVal = iMinVal
    elif i2 >= iMaxVal:
        retVal = iMaxVal
    else:
        retVal = i2
    myStr = str(retVal) + '%'
    return myStr


def festivalPitchString(sA):
    '''
    Use PITCH for value of Sable `<PITCH BASE="50%">` markup.
    Converts w3 Smil style percentage to Sable percentage
    sA - Pitch expressed as a percentage.
    Use '100%' for default Pitch of 0% in Sable markup
    Returns pitch value as string between -99% and 100%
    
    '''
    i2 = 0
    iMinVal = -99
    iMaxVal = 100
    retVal = 0
    s1 = ''
    
    try:
        if '%' in sA:
            s1 = sA.replace('%', '')
            s1 = s1.replace('-', '')
            i2 = int(s1) - 100
        else:
            i2 = 0
    except(TypeError):
       print ('I was unable to determine festival pitch!')
    if i2 <= iMinVal:
        retVal = iMinVal
    elif i2 >= iMaxVal:
        retVal = iMaxVal
    else:
        retVal = i2
    myStr = str(retVal) + '%'
    return myStr


def main():
    '''
Creates a temporary speech-synthesis sound file and optionally
reads the file aloud.
    '''
    sWAVE = ''
    sVISIBLE = ''
    sAUDIBLE = ''
    sSABLESPEAKER = ''
    sSABLERATE = ''
    sSABLEPITCH = ''
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
        elif not os.path.isfile('/usr/bin/text2wave'):
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
                sSABLERATE = festivalRateString(sRATE)
            elif o in ('-p', '--pitch'):
                sPITCH = a
                sSABLEPITCH = festivalPitchString(sPITCH)
            elif o in ('-i', '--image'):
                sIMG1 = a
            elif o in ('-e', '--eval'):
                sEVAL1 = a
                sSABLESPEAKER = festivalSpeakerNameString(sEVAL1)
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
            # iso-8859-15 is for western European languages.  Should festival
            # include a switch to allow Asian & complex languages to use utf-8?
            #
            # Festival voices use Sable markup instead of w3 SMIL  
            #
            oFILE = codecs.open(sFILEPATH, mode='r', encoding='iso8859_15')
        except (IOError):
            print ('I was unable to open the file you specified!')
            usage()
        else:
            sTXT = oFILE.read()
            oFILE.close()
            if len(sTXT) != 0:
                sTXT = readtexttools.stripxml(sTXT)
            if len(sTXT) != 0:
                sTXT = readtexttools.stripxml(sTXT)
                if (len(sSABLERATE) == 0 and len(sSABLEPITCH) == 0):
                    # Pass plain text (RECOMMENDED for most users)
                    sTXT = readtexttools.cleanstr(
                            sTXT,
                            readtexttools.bFalse())
                    sA = sTXT
                else:
                    # Prepare Sable XML (To SLOW DOWN speech use --RATE=75%)
                    sTXT = readtexttools.cleanstr(sTXT, readtexttools.bFalse())
                    sTXT = sTXT.replace("&", "&#38;")
                    sTXT = sTXT.replace("<", "&#60;")
                    sTXT = sTXT.replace(">", "&#62;")
                    sA = ''.join([
                            '<SABLE>\n',
                            '<SPEAKER NAME="',
                            sSABLESPEAKER + '">\n',
                            '<RATE SPEED="',
                            sSABLERATE + '">\n',
                            '<PITCH BASE="',
                            sSABLEPITCH,
                            '">\n',
                            sTXT,
                            '\n</PITCH>',
                            '\n</SPEAKER>',
                            '\n</SABLE>'])
                    os.remove(sFILEPATH)
                    sFILEPATH = sFILEPATH + ".sable"
                    oFILE2 = codecs.open(
                        sFILEPATH,
                        mode='w',
                        encoding='iso8859_15')
                    oFILE2.write(sA)
                    oFILE2.close()
                sB = readtexttools.checkmyartist(sART)
                sC = readtexttools.checkmytitle(sTIT, 'festival')
                festivalread(sFILEPATH,
                             sVISIBLE,
                             sAUDIBLE,
                             sWAVE,
                             sIMG1,
                             sTXT,
                             sEVAL1,
                             sC,
                             sB,
                             sDIM)
    else:
        print ('I was unable to find the file you specified!')
    sys.exit(0)

if __name__ == '__main__':
    main()

