#!/usr/bin/env python
# -*- coding: UTF-8-*-
r'''
Espeak
======

Reads a text file using espeak, mbrola and a media player.

The espeak program is a software speech synthesizer.
The mbrola synthesiser can improve the naturalness of speech.  However, it
has licensing restrictions, and is not part of Debian's main repository.
Ubuntu makes mbrola and mbrola voices available in the multiverse repository.

Install mbrola by installing mbrola using your package manager or downloading
the mbrola binary and installing it.  Download mbrola voices and copy or link
the voice files into the appropriate directory. For example:

        /usr/share/mbrola/voices (Linux, OSX)
        C:\Program Files (x86)\eSpeak\espeak-data (Windows 64 bit)
        C:\Program Files\eSpeak\espeak-data (Windows 32 bit)

You only need to copy or link to the voices files themselves.
In April 2011, compatible mbrola voices were:

        af1, br1, br3, br4, cr1, cz2, de2, de4, de5, de6, de7, en1,
        es1, es2, fr1, fr4, gr2, hu1, id1, it3, it4, la1, nl2, pl1,
        pt1, ro1, sw1, sw2, tr1, tr2, us1, us2, us3

See also: [espeak - mbrola](http://espeak.sourceforge.net/mbrola.html) and
[mbrola](http://tcts.fpms.ac.be/synthesis/)

About mbrola
------------

    T. DUTOIT, V. PAGEL, N. PIERRET, F.  BATAILLE,
    O. VAN DER VRECKEN
    "The MBROLA Project: Towards a Set of High-Quality
    Speech Synthesizers Free of Use for
    Non-Commercial Purposes"
    Proc. ICSLP'96, Philadelphia, vol. 3, pp. 1393-1396.

or, for a more general reference to Text-To-Speech synthesis, the book :

    *An Introduction to Text-To-Speech Synthesis*,
    forthcoming textbook, T. DUTOIT, Kluwer Academic
    Publishers, 1997.

If you are using this extension to create still frame videos you need ffmpeg
or avconv.  Webm is the recommended video format. If you are creating a long
video, be patient.  It can take a long time for the external program to render
the video.

Read Selection... Dialog setup:
-------------------------------

External program:

        /usr/bin/python

Command line options (default):

        "(ESPEAK_READ_TEXT_PY)" --language=(SELECTION_LANGUAGE_CODE) "(TMP)"

or (save as a .wav file in the home directory):

        "(ESPEAK_READ_TEXT_PY)" --language=(SELECTION_LANGUAGE_CODE) \
          --output="(HOME)(NOW).wav" "(TMP)"

or (speak more slowly with a lowered pitch):

        "(ESPEAK_READ_TEXT_PY)" --language=(SELECTION_LANGUAGE_CODE) \
          --rate=80% --pitch=80% "(TMP)"

See the manual page for `espeak` for more detailed information

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
import math
import os
import sys
import readtexttools

def usage():
    '''
    Command line help
    '''
    print ('''
Espeak Read Text
===============

Reads a text file using espeak and a media player.

Converts format with `avconv`, `lame`, `faac` or `ffmpeg`.

Usage
-----

     espeak_read_text_file.py "input.txt"
     espeak_read_text_file.py --language [de|en|en-GB|es|fr|it] "input.txt"
     espeak_read_text_file.py --visible="false" "input.txt"
     espeak_read_text_file.py --rate=100% --pitch=100% "input.txt"
     espeak_read_text_file.py --output="output.wav" "input.txt"
     espeak_read_text_file.py --output="output.[m4a|mp2|mp3|ogg]" "input.txt"
     espeak_read_text_file.py --output="output.[avi|webm]" \\ 
       --image="input.[png|jpg] "input.txt"
     espeak_read_text_file.py --audible="false" --output="output.wav" \\ 
       "input.txt"
''')


def espkread(sTXTFILE,
             sLANG,
             sVISIBLE,
             sAUDIBLE,
             sTMP0,
             sIMG1,
             sB,
             sPOSTPROCESS,
             sART,
             sDIM,
             iPITCH,
             iRATE):
    '''
Creates a temporary speech-synthesis sound file and optionally
reads the file aloud.

+ `sTXTFILE` - Name of text file to speak
+ `sLANG` - Supported two or four letter language code - defaults to US English
+ `sVISIBLE` - Use a graphic media player, or False for invisible player
+ `sTMP0` - Name of desired output media file
+ `sAUDIBLE` - If false, then don't play the sound file
+ `sIMG1` - a .png or .jpg file if required.
+ `sB` - Commentary or title for post processing
+ `sPOSTPROCESS` - Get information, play file, or convert a file
+ `sART` - Artist or Author
+ `sDIM` - Dimensions to scale photo '600x600'
+ `iPITCH` - pitch value from 5 to 100, default 50
+ `iRATE` - rate value from 20 to 640, default 160
    '''
    sOUT1 = ''

    if sLANG[:2].lower() in ['de']:
        s = 'de'
    elif sLANG[:2].lower() in ['en']:
        if sLANG[-2:].upper() in [
                'AU', 
                'BD', 
                'BS', 
                'CA', 
                'GB', 
                'GH', 
                'HK', 
                'IE', 
                'IN', 
                'JM', 
                'NZ', 
                'PK', 
                'SA', 
                'TT']:
            s = 'en'
        else:
            s = 'en-us'
    elif sLANG[:2].lower() in ['es']:
        if sLANG[-2:].upper() in ['ES']:
            s = 'es'
        elif sLANG[-2:].upper() in ['MX']:
            s = 'es-mx'
        else:
            s = 'es-la'
    elif sLANG[:2].lower() in ['nb']:
        # *Office uses language code for Norwegian Bokmal - nb
        #  NO is the country code for Norway, not an official language code.
        s = 'no'
    elif sLANG[:2].lower() in ['pt']:
        if sLANG[-2:].upper() in ['PT']:
            s = 'pt-pt'
        else:
            s = 'pt'
    elif sLANG[:2].lower() in ['zh']:
        if sLANG[-2:].upper() in ['HK','MO']:
            # Yue is official language in Hong Kong & Macau
            s = 'zh-yue'
        else:
            s = 'zh'
    elif sLANG[:2].lower() in [
            'af', 
            'bs', 
            'ca', 
            'cs', 
            'cy', 
            'da', 
            'de', 
            'el', 
            'eo', 
            'fi', 
            'fr', 
            'hi', 
            'hr', 
            'hu', 
            'hy', 
            'id', 
            'is', 
            'it', 
            'ku', 
            'la', 
            'lv', 
            'mk', 
            'nl', 
            'pl', 
            'ro', 
            'ru', 
            'sk', 
            'sq', 
            'sr', 
            'sv', 
            'sw', 
            'ta', 
            'tr', 
            'vi']:
        s = sLANG[:2].lower()
    else:
        s = 'en'
    sVoice = s  # standard espeak voice
    if sPOSTPROCESS == 'ProcessWaveMedia':
        # Check if an mbrola voice is available for the language, otherwise use
        # the default espeak voice.  If there are several compatible mbrola
        # voices, this python script will choose the first one - for example:
        # de2 instead of de7.
        #
        # Dictionary : `a2` is the locally installed language abbreviation;
        # `a1` is the equivalent ISO 639-1 standard for languages, except in
        # the cases of pt-PT and en-US, which include a regional ISO code.
        a0 = [
            {'a2': 'af1', 'a1': 'af'},
            {'a2': 'br1', 'a1': 'pt'},
            {'a2': 'br3', 'a1': 'pt'},
            {'a2': 'br4', 'a1': 'pt'},
            {'a2': 'cr1', 'a1': 'hr'},
            {'a2': 'cz2', 'a1': 'cs'},
            {'a2': 'de2', 'a1': 'de'},
            {'a2': 'de4', 'a1': 'de'},
            {'a2': 'de5', 'a1': 'de'},
            {'a2': 'de6', 'a1': 'de'},
            {'a2': 'de7', 'a1': 'de'},
            {'a2': 'en1', 'a1': 'en'},
            {'a2': 'es1', 'a1': 'es'},
            {'a2': 'es2', 'a1': 'es'},
            {'a2': 'fr1', 'a1': 'fr'},
            {'a2': 'fr4', 'a1': 'fr'},
            {'a2': 'gr2', 'a1': 'el'},
            {'a2': 'hu1', 'a1': 'hu'},
            {'a2': 'id1', 'a1': 'id'},
            {'a2': 'it3', 'a1': 'it'},
            {'a2': 'it4', 'a1': 'it'},
            {'a2': 'la2', 'a1': 'la'},
            {'a2': 'nl2', 'a1': 'nl'},
            {'a2': 'pl1', 'a1': 'pl'},
            {'a2': 'pt1', 'a1': 'pt-pt'},
            {'a2': 'ro1', 'a1': 'ro'},
            {'a2': 'sw1', 'a1': 'sv'},
            {'a2': 'sw2', 'a1': 'sv'},
            {'a2': 'tr1', 'a1': 'tr'},
            {'a2': 'tr2', 'a1': 'tr'},
            {'a2': 'us1', 'a1': 'en-us'},
            {'a2': 'us2', 'a1': 'en-us'},
            {'a2': 'us3', 'a1': 'en-us'},
            {'a2': 'en1', 'a1': 'en-us'}]

        for i in range(len(a0)):
            # Identify an mbrola voice if it is installed
            
            if a0[i]['a1'] == s:
                if 'nt' in os.name.lower():
                    if os.path.isfile(os.path.join(os.getenv('ProgramFiles'),
                                                   'eSpeak/espeak-data/mbrola',
                                                   a0[i]['a2'])):
                        sVoice = 'mb-' + a0[i]['a2']
                        break
                    elif os.getenv('ProgramFiles(x86)'):
                        sPFX86 = os.getenv('ProgramFiles(x86)')
                        sEEDM = 'eSpeak/espeak-data/mbrola'
                        if (
                           os.path.isfile(os.path.join(sPFX86,
                                                       sEEDM,
                                                       a0[i]['a2']))):
                            sVoice = 'mb-' + a0[i]['a2']
                            break
                else:
                    print(os.path.join('/usr/share/mbrola/voices',
                                                   a0[i]['a2']))
                    if os.path.isfile(os.path.join('/usr/share/mbrola/voices',
                                                   a0[i]['a2'])):
                        sVoice = 'mb-' + a0[i]['a2']
                        break
                    elif os.path.isfile(os.path.join('/usr/share/mbrola/',
                                                     a0[i]['a2'],
                                                     a0[i]['a2'])):
                        sVoice = 'mb-' + a0[i]['a2']
                        break
    # Determine the output file name
    sOUT1 = readtexttools.fsGetSoundFileName(sTMP0, sIMG1, 'OUT')
    # Determine the temporary file name
    sTMP1 = readtexttools.fsGetSoundFileName(sTMP0, sIMG1, 'TEMP')

    # Remove old files.
    if os.path.isfile(sTMP1):
        os.remove(sTMP1)
    if os.path.isfile(sOUT1):
        os.remove(sOUT1)
    try:
        # espeak must be in your system's path
        # for example: /usr/bin/ or /usr/local/bin/
        sApp = 'espeak'
        sSub = 'eSpeak/command_line/espeak.exe'
        if 'nt' in os.name.lower():
            sApp = readtexttools.getWinFullPath(sSub)
        s1 = ''.join([
                '"',
                sApp,
                '" -b 1 -p ',
                str(iPITCH),
                ' -s ',
                str(iRATE),
                ' -v ',
                sVoice,
                ' -w "',
                sTMP1,
                '" -f "',
                sTXTFILE,
                '"'])
        readtexttools.myossystem(s1)
        print ("-----------------------------------------------------")
        print (s1)
        if sPOSTPROCESS == "ProcessWaveMedia":
            print ("ProcessWaveMedia")
            readtexttools.ProcessWaveMedia(sB,
                                           sTMP1,
                                           sIMG1,
                                           sOUT1,
                                           sAUDIBLE,
                                           sVISIBLE,
                                           sART,
                                           sDIM
                                           )
        elif sPOSTPROCESS == "ShowWavtoSeconds":
            print ("ShowWavtoSeconds")
            print (readtexttools.WavtoSeconds(sTMP1))
            print ("-----------------------------------------------------")
    except (IOError):
        print ('I was unable to use espeak and read text tools!')
        usage()


def eSpeakRate(sA):
    '''
    sA - rate expressed as a percentage.
    Use '100%' for default rate of 160 words per minute (wpm).
    Returns rate between 20 and 640.
    '''
    i1 = 0
    i2 = 0
    iMinVal = 20
    iMaxVal = 640
    retVal = 160
    s1 = ''
    
    try:
        if '%' in sA:
            s1 = sA.replace('%', '')
            i1 = (float(s1) if '.' in s1 else int(s1) / 100)
            i2 = math.ceil(i1 * retVal)
        else:
            i1 = (float(sA) if '.' in sA else int(sA))
            i2 = math.ceil(i1)
    except(TypeError):
        print ('I was unable to determine espeak rate!')
    if i2 <= iMinVal:
        retVal = iMinVal
    elif i2 >= iMaxVal:
        retVal = iMaxVal
    else:
        retVal = i2
    return retVal


def eSpeakPitch(sA):
    '''
    sA - Pitch expressed as a percentage.
    Use '100%' for default Pitch of 50.
    "aah" pitch: 0% = a1, 50% = b1, 100% = e2, 200% = d3#
    Returns pitch value between 0 and 100.
    '''
    i1 = 0
    i2 = 0
    iMinVal = 0
    iMaxVal = 100
    retVal = 50
    s1 = ''
    
    try:
        if '%' in sA:
            s1 = sA.replace('%', '')
            i1 = (float(s1) if '.' in s1 else int(s1) / 100)
            i2 = math.ceil(i1 * retVal)
        else:
            i1 = (float(sA) if '.' in sA else int(sA))
            i2 = math.ceil(i1)
    except TypeError:
        print ('I was unable to determine espeak pitch!')
    if i2 <= iMinVal:
        retVal = iMinVal
    elif i2 >= iMaxVal:
        retVal = iMaxVal
    else:
        retVal = i2
    return retVal


def main():
    iEspeechPitch = 50
    iEspeechRate = 160
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
        elif not os.path.isfile('/usr/bin/espeak'):
            print('Please install espeak.  Use `sudo apt-get install espeak`')
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
                sWAVE = a
            elif o in ('-v', '--visible'):
                sVISIBLE = a
            elif o in ('-a', '--audible'):
                sAUDIBLE = a
            elif o in ('-l', '--language'):
                sLANG = a
            elif o in ('-r', '--rate'):
                sRATE = a
                iEspeechRate = eSpeakRate(sRATE)
            elif o in ('-p', '--pitch'):
                sPITCH = a
                iEspeechPitch = eSpeakPitch(sPITCH)
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
        except IOError:
            print ('I was unable to open the file you specified!')
            usage()
        else:
            sTXT = oFILE.read()
            oFILE.close()
            if len(sTXT) != 0:
                sTXT = readtexttools.stripxml(sTXT)
            if len(sTXT) != 0:
                sTXT = readtexttools.cleanstr(sTXT, readtexttools.bFalse())
                sA = '" <speed level = \'' + sRATE + '\'>'
                sA = sA + "<pitch level = '" + sPITCH + '\'>'
                sA = sA + sTXT + '</pitch></speed>"'
                sB = readtexttools.checkmyartist(sART)
                sC = readtexttools.checkmytitle(sTIT, 'espeak')
                sPOSTPROCESS = 'ProcessWaveMedia'
                espkread(sFILEPATH,
                         sLANG,
                         sVISIBLE,
                         sAUDIBLE,
                         sWAVE,
                         sIMG1,
                         sC,
                         sPOSTPROCESS,
                         sB,
                         sDIM,
                         iEspeechPitch,
                         iEspeechRate
                        )
    sys.exit(0)


if __name__ == '__main__':
    main()
