#!/usr/bin/env python
# -*- coding: UTF-8-*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals
    )
###############################################################################

# Read Text Extension
#
# Copyright And License
#
# (c) 2015 [James Holgate Vancouver, CANADA](readtextextension(a)outlook.com)
#
# THIS IS FREE SOFTWARE; YOU CAN REDISTRIBUTE IT AND/OR MODIFY IT UNDER THE
# TERMS OF THE GNU GENERAL PUBLIC LICENSE AS PUBLISHED BY THE FREE SOFTWARE
# FOUNDATION; EITHER VERSION 2 OF THE LICENSE, OR(AT YOUR OPTION)ANY LATER
# VERSION.  THIS SCRIPT IS DISTRIBUTED IN THE HOPE THAT IT WILL BE USEFUL, BUT
# WITHOUT ANY WARRANTY; WITHOUT EVEN THE IMPLIED WARRANTY OF MERCHANTABILITY OR
#  FITNESS FOR A PARTICULAR PURPOSE.SEE THE GNU GENERAL PUBLIC LICENSE FOR MORE
# DETAILS.
#
# YOU SHOULD HAVE RECEIVED A COPY OF THE GNU GENERAL PUBLIC LICENSE ALONG WITH
# THIS SOFTWARE; IF NOT, WRITE TO THE FREE SOFTWARE FOUNDATION, INC., 59 TEMPLE
# PLACE, SUITE 330, BOSTON, MA 02111-1307  USA
###############################################################################

'''
Read Text Library
=================

Common tools for Read Text Extension.

Reads a .wav sound file, converts it and/or plays it with a media player.

Usage
-----

Audio:

        python readtexttools.py --sound="xxx.wav" --output="xxx.ogg"
        python readtexttools.py --visible="false" --audible="true" \
        --sound="xxx.wav" --output="xxx.ogg"

Video:

        python readtexttools.py --image="xxx.png" --sound="xxx.wav" \
            --output="xxx.webm"
        python readtexttools.py --visible="true" --audible="true" \
        --image="xxx.png" --sound="xxx.wav" --title="Title" --output="xxx.webm"

If the image in the movie is distorted, then the input image may be corrupt or
unusable.  Images directly exported from the office program may not work.  Fix
the image by opening it with an image editor like `gimp` and trimming the image
so that the proportions match the desired output video proportions.  Export the
trimmed image as a `jpg` or `png` image file.

Experimental issues
-------------------

Experimental codecs might produce bad results.  If the command line includes
`-strict experimental`, check the output file on different devices.

Python version
--------------

Currently, python3 is *required* for `speech-dispatcher`.  Python2 requires the
`future` toolkit.  Unless you are using a library or tool that requires
 python2, use `python3` in the command line.

[Read Text Extension](http://sites.google.com/site/readtextextension/)

Copyright (c) 2011 - 2015 James Holgate
'''
import aifc
import codecs
import getopt
import math
import mimetypes
import os
import platform
import shlex
import subprocess
import sunau
import sys
import time
import wave


def usage():
    '''
    Displays the usage of the included python app "main", which can be used to
    convert wav files to other formats like ogg audio or webm video.
    '''
    sA = ' ' + os.path.split(sys.argv[0])[1]
    print('')
    print('Read text tools')
    print('===============\n')
    print('Reads a .wav sound file, converts it and plays copy with a player.')
    print('Requires a converter like `avconv`, `faac`, `lame` or `ffmpeg`.\n')
    print('Usage')
    print('-----\n')
    print('###Audio:\n')
    print(('    '+sA+u' --sound="xxx.wav" --output="xxx.ogg"'))
    print(('    '+sA+u' --visible="false" --audible="true"  \ '))
    print('       --sound="xxx.wav" --output="xxx.ogg"\n')
    print('###Video:\n')
    print('Makes an audio with a poster image.  Uses `avconv` or `ffmpeg`.\n')
    print(('    '+sA+u' --image="xxx.png" --sound="xxx.wav" \ '))
    print(('      --output="xxx.webm"'))
    print(('    '+sA+u' --visible="true" --audible="true" --image="x.png" \\'))
    print('       --sound="x.wav"--title="Title" --output="x.webm"\n')


def fsAppSignature():
    '''
    App signature can help identify file locations and shared settings.
    '''
    retVal = 'ca.bc.vancouver.holgate.james.readtextextension'

    return retVal


def fsAppName():
    '''
    Application name in English
    '''
    retVal = 'Read Text'

    return retVal


def fsAppRelease():
    '''
    Major, Minor, Version release.  Use to check if this is the required
    version.
    '''
    retVal = '0.9.0'

    return retVal


def fsGetSoundFileName(sTMP1, sIMG1, sType1):
    '''
    Determine the temporary filename or output filename
    Given the filename sTMP1, returns a temporary filename if sType1 is 'TEMP'
    or the output filename if sType1 is anything else.
    Example:
    import readtexttools
    # Determine the temporary file name
    sTMP1 = readtexttools.fsGetSoundFileName(sTMP1, sIMG1, 'TEMP')
    # Determine the output file name
    sOUT1 = readtexttools.fsGetSoundFileName(sTMP1, sIMG1, 'OUT')
    '''
    sOUT1 = ''

    if sTMP1 == '':
        sTMP1 = getTempPrefix() + u'-speech.wav'
    sTMP1EXT = os.path.splitext(sTMP1)[1].lower()
    sIMG1EXT = os.path.splitext(sIMG1)[1].lower()

    mimetypes.init()
    if len(sTMP1EXT) == 0:
        sMIME = "xxz/xxz-do-not-match"
    else:
        sMIME = mimetypes.types_map[sTMP1EXT]
    if sTMP1EXT == '.m4a':
            if (os.path.isfile('/usr/bin/faac') or
                    os.path.isfile(r'C:\opt\neroAacEnc.exe') or
                    os.path.isfile(r'C:\opt\faac.exe')):
                sOUT1 = sTMP1
                sTMP1 = sOUT1 + u'.wav'
            else:
                # Can't make m4a, so make wav
                sOUT1 = sTMP1 + u'.wav'
                sTMP1 = sOUT1
    elif sMIME == mimetypes.types_map['.mp3']:
            if ((ffMpegInstalled() and
                    os.path.isfile('/usr/share/doc/liblame0/copyright')) or
                    os.path.isfile('/usr/bin/lame') or
                    os.path.isfile(r'C:\opt\lame.exe')):
                sOUT1 = sTMP1
                sTMP1 = sOUT1 + u'.wav'
            else:
                # Can't make mp3, so make wav
                sOUT1 = sTMP1 + u'.wav'
                sTMP1 = sOUT1
    if sTMP1EXT == '.mp2':
            if ((ffMpegInstalled() and
                    os.path.isfile('/usr/share/doc/libtwolame0/copyright')) or
                    os.path.isfile(r'C:\opt\twolame.exe')):
                sOUT1 = sTMP1
                sTMP1 = sOUT1 + u'.wav'
            else:
                # Can't make mp3, so make wav
                sOUT1 = sTMP1 + u'.wav'
                sTMP1 = sOUT1
    elif sMIME == mimetypes.types_map['.ogg']:
            if ((ffMpegInstalled() and
                    os.path.isfile('/usr/share/doc/libogg0/copyright')) or
                    os.path.isfile(r'C:\opt\oggenc.exe') or
                    os.path.isfile(r'C:\opt\oggenc2.exe')):
                sOUT1 = sTMP1
                sTMP1 = sOUT1 + u'.wav'
            else:
                # Can't make ogg, so make wav
                sOUT1 = sTMP1 + u'.wav'
                sTMP1 = sOUT1
    elif sMIME == mimetypes.types_map['.aif']:
            if ffMpegInstalled():
                sOUT1 = sTMP1
                sTMP1 = sOUT1 + u'.wav'
            else:
                # Can't make aif, so make wav
                sOUT1 = sTMP1 + u'.wav'
                sTMP1 = sOUT1
    elif sMIME == mimetypes.types_map['.flac']:
            if (ffMpegInstalled() or
                    os.path.isfile(r'C:\opt\flac.exe')):
                sOUT1 = sTMP1
                sTMP1 = sOUT1 + u'.wav'
            else:
                # Can't make flac, so make wav
                sOUT1 = sTMP1 + u'.wav'
                sTMP1 = sOUT1
    elif 'video/' in sMIME:
            if (ffMpegInstalled() and
                    sIMG1EXT in '.bmp;.gif;.jpeg;.jpg;.png;.tif;.tiff;.tga;'):
                sOUT1 = sTMP1
                sTMP1 = sOUT1 + u'.wav'
            else:
                # Can't make video, so make wav
                sOUT1 = sTMP1 + u'.wav'
                sTMP1 = sOUT1
    if sType1 == 'TEMP':
        retVal = sTMP1
    else:
        retVal = sOUT1
    return retVal


def ffMpegInstalled():
    '''
    Can we use ffmpeg or avconv?
    '''
    retVal = not(0)

    if len(ffMpegPath()) == 0:
        retVal = not(1)
    return retVal


def ffMpegPath():
    '''
    ffmpeg may not be in the normal environment PATH, so we look for it, and
    return the location.
    '''
    retVal = ''
    mvc = 'Miro Video Converter'
    pcv = 'Participatory Culture Foundation'

    if os.path.isfile('/usr/bin/avconv'):
        retVal = '/usr/bin/avconv'
    elif os.path.isfile('/usr/bin/ffmpeg'):
        retVal = '/usr/bin/ffmpeg'
    elif os.path.isfile('/usr/local/bin/avconv'):
        retVal = '/usr/local/bin/avconv'
    elif os.path.isfile('/usr/local/bin/ffmpeg'):
        retVal = '/usr/local/bin/ffmpeg'
    elif 'darwin' in platform.system().lower():
        if os.path.isfile('Applications/Miro.app/Contents/Helpers/ffmpeg'):
            retVal = 'Applications/Miro.app/Contents/Helpers/ffmpeg'
        elif os.path.isfile(
                'Applications/' + mvc + '.app/Contents/Helpers/ffmpeg'
                ):
            retVal = 'Applications/' + mvc + '.app/Contents/Helpers/ffmpeg'
        elif os.path.isfile('/opt/Shotcut/Shotcut.app/bin/ffmpeg'):
            retVal = '/opt/Shotcut/Shotcut.app/bin/ffmpeg'
    elif 'windows' in platform.system().lower():
        if len(os.path.isfile(getWinFullPath('opt/ffmpeg.exe'))) != 0:
            retVal = getWinFullPath('opt/ffmpeg.exe')
        elif len(os.path.isfile(getWinFullPath(
                pcv + '/Miro/ffmpeg/ffmpeg.exe'
                ))) != 0:
            retVal = getWinFullPath(
                pcv + '/Miro/ffmpeg/ffmpeg.exe')
        elif len(
                os.path.isfile(
                getWinFullPath(
                pcv + '/' + mvc + '/ffmpeg/ffmpeg.exe'
                )
                )
                ) != 0:
            retVal = getWinFullPath(
                pcv + '/' + mvc + '/ffmpeg/ffmpeg.exe'
                )
        elif len(os.path.isfile(getWinFullPath('opt/avconv.exe'))) != 0:
            retVal = getWinFullPath('opt/avconv.exe')
    return retVal


def ProcessWaveMedia(sB, sTMP1, sIMG1, sOUT1, sAUDIBLE, sVISIBLE, sART, sDIM):
    '''
    Converts audio file, plays copy and deletes original
    sB is brief title
    sTMP is working file name (wav)
    sIMG1 is image to add to video.  Ignored if making audio only
    sOUT1 is output file name.( webm, ogg etc.)
    sAUDIBLE - Do we play the file after conversion?
    sVISIBLE - Do we use a GUI or the console?
    '''
    Wav2Media(sB, sTMP1, sIMG1, sOUT1, sAUDIBLE, sVISIBLE, sART, sDIM)
    try:
        if sOUT1 == '':
            print(u'Saved to: ' + sTMP1)
        else:
            if os.path.isfile(sTMP1):
                if os.path.isfile(sOUT1):
                    os.remove(sTMP1)
                else:
                    print(u'Did not remove "' + sTMP1
                          + u'" because the converter did not write "'
                          + sOUT1
                          + '"'
                          )
    except (OSError):
        print(u'Could not remove "' + sTMP1 + u'"')


def SoundLenInSeconds(sTMP1):
    '''
    Tells approximately how long a sound file is in seconds as an integer
    We round up so that processes that call for sleep have time to finish.
    '''
    sTMP1EXT = os.path.splitext(sTMP1)[1].lower()

    mimetypes.init()
    if len(sTMP1EXT) == 0:
        sMIME = "xxz-xzz-no-match"
    else:
        sMIME = mimetypes.types_map[sTMP1EXT]
    retVal = 0
    if sMIME == mimetypes.types_map['.wav']:
        snd_read = wave.open(sTMP1, 'r')
        retVal = math.ceil(snd_read.getnframes()//snd_read.getframerate()) + 1
        snd_read.close()
    elif sMIME == mimetypes.types_map['.au']:
        snd_read = sunau.open(sTMP1, 'r')
        retVal = math.ceil(snd_read.getnframes()//snd_read.getframerate()) + 1
        snd_read.close()
    elif sMIME == (mimetypes.types_map['.aif'] or
                   sMIME == mimetypes.types_map['.aifc']):
        snd_read = aifc.open(sTMP1, 'r')
        retVal = math.ceil(snd_read.getnframes()//snd_read.getframerate()) + 1
        snd_read.close()
    return retVal


def WavtoSeconds(sTMP1):
    '''
    Tells approximately how long a wav file is in seconds
    '''
    retVal = SoundLenInSeconds(sTMP1)

    return retVal


def Wav2Media(sB, sTMP1, sIMG1, sOUT1, sAUDIBLE, sVISIBLE, sART, sDIM):
    '''
    Wav2Media
    =========

    Converts a wave audio file to another format and plays a copy.

            sB is brief title
            sTMP1 is working file name (wav)
            sIMG1 is image to add to video.  Ignored if making audio only
            sOUT1 is output file name.( webm, ogg etc.)
            sAUDIBLE - Do we play the file after conversion?
            sVISIBLE - Do we use a GUI or the console?
            sART - Artist
            sDIM - Dimensions of poster image '600x600'
    '''

    sTT = sB
    iTIME = WavtoSeconds(sTMP1)
    sTIME = repr(iTIME)
    sOUT1EXT = os.path.splitext(sOUT1)[1].lower()
    sTMP1EXT = os.path.splitext(sTMP1)[1].lower()
    sIMG1EXT = os.path.splitext(sIMG1)[1].lower()

    LockMyLock()
    if len(sDIM) == 0:
        sDIM = '600x600'
    # Check for mimetype extensions like `.aif` and `.aiff.`
    mimetypes.init()
    if len(sOUT1EXT) == 0:
        sOUT1MIME = 'zxx/zxx-does-not-match'
    else:
        sOUT1MIME = mimetypes.types_map[sOUT1EXT]
    sART2 = ""
    sTT = ""
    sTL = ""
    sTG = ""
    sTN = ""
    sTY = time.strftime('%Y')
    # getMySongName() is normally the first few words of the selection.
    try:
        if len(sTT) == 0:
            sTT = cleanstr(getMySongName(), bFalse())
        else:
            sTT = cleanstr(sTT, bFalse())
    except (UnicodeDecodeError):
        sTT = timefortitle()
    try:
        if len(sTN) == 0:
            sTN = getMyTrackNo()
        else:
            sTN = '1'
    except (UnicodeDecodeError):
        sTN = '1'
    try:
        if len(sTG) == 0:
            sTG = getMyGenreName()
        else:
            sTG = 'Speech'
    except (UnicodeDecodeError):
        sTG = 'Speech'
    try:
        s1 = sART
        if len(s1) == 0:
            sART2 = cleanstr(getMyUserName(), bFalse)
        else:
            sART2 = cleanstr(s1, bFalse())
    except (UnicodeDecodeError):
        sART2 = fsAppName()
    try:
        sTL = cleanstr(getMyAlbumName(), bFalse())
        print(u'-----------------------------------------------------')
        print(fsAppName())
        print(u'')
        print((u'Title: ' + sTT))
        print((u'Working File Name: ' + sTMP1))
        print((u'File Name: ' + sOUT1))
        print((u'Duration in seconds: ' + sTIME))
        print((u'Track: ' + sTN))
        if 'video/' in sOUT1MIME:
            print((u'Poster Dimensions: ' + sDIM))
        print(u'-----------------------------------------------------')
    except (UnicodeDecodeError):
        sART2 = " "
        sTT = " "
        sTL = " "
        sTG = " "
        sTY = " "
    try:
        # Double quotes must be cleaned from strings but UTF-8 is okay
        sData1 = u" -metadata album='" + cleanstr(sTL, bTrue())
        sData1 = sData1 + u"' -metadata artist='" + cleanstr(sART2, bTrue())
        sData1 = sData1 + u"' -metadata genre='" + sTG
        sData1 = sData1 + u"' -metadata title='" + cleanstr(sTT, bTrue())
        sData1 = sData1 + u"' -metadata track='" + sTN
        sData1 = sData1 + u"' -metadata Year='" + sTY + u"' "
        print(sData1)
    except(UnicodeDecodeError):
        sData1 = u''
    try:
        sCmdA = u''
        sFFcommand = ffMpegPath()
        if sOUT1MIME == mimetypes.types_map['.ogg']:
            sTY = time.strftime('%Y-%m-%d')
            if 'windows' in platform.system().lower():
                # C:/opt/oggenc2.exe
                # Get oggenc2.exe: http://www.rarewares.org/ogg-oggenc.php
                s0 = getWinFullPath('/opt/oggenc2.exe')
                if len(s0) == 0:
                    s0 = getWinFullPath('/opt/oggenc.exe')
                s1 = s0 + u' -o "' + sOUT1 + u'" "' + sTMP1 + u'"'
                myossystem(s1)
            else:
                sCmdA = sData1
                s1 = u'"' + sFFcommand
                s1 = s1 + u'" -i "' + sTMP1 + u'" ' + sCmdA + u' -y "'
                s1 = s1 + sOUT1 + u'"'
                myossystem(s1)
                print(s1)
        elif sOUT1EXT == '.m4a':
            # .m4a is an 'audio/mpeg' file.
            #
            # Nero
            # ====
            #
            # **Nero** includes console apps for encoding, tagging and
            # decoding aac format files.  Recommended for platform
            # compatibility.
            #
            # Speech synthesizers let you save files in `.wav` format.
            # To convert `.wav` files to `.m4a` files you can share
            # on most mobile phones, players and tablets, download
            # the `NeroAACCodec-1.5.1.zip` archive from
            # [Nero software](http://www.nero.com/), then save
            # neroAacEnc` and `neroAacTag` in `/usr/local/bin`.
            #
            # [HTTP](http://www.nero.com/enu/downloads-nerodigital-nero-aac-codec.php)
            # [FTP](http://ftp6.nero.com/tools/NeroAACCodec-1.5.1.zip)
            #
            # Note: The Linux binary is for 32 bit Intel systems.
            #
            # Faac
            # ====
            #
            # Faac is  an aac muxer.  For cross-platform sound files
            # you may need to compile it with optional plugins.
            #
            if 'windows' in platform.system().lower():
                # C:/opt/neroAacEnc.exe
                s0 = getWinFullPath('/opt/neroAacEnc.exe')
                if len(s0) == 0:
                    s0 = getWinFullPath('/opt/faac.exe')
                    s1 = s0 + u' -o "' + sOUT1 + u'" "' + sTMP1 + u'"'
                else:
                    s1 = s0 + u' -if "' + sTMP1 + u'" -of "' + sOUT1 + u'"'
                myossystem(s1)
            else:
                if (os.path.isfile('/usr/bin/neroAacEnc') or
                        os.path.isfile('/usr/local/bin/neroAacEnc')):
                    s1 = 'neroAacEnc -if "' & sTMP1 & '" -of "' & sOUT1 & '" '
                    print(s1)
                    myossystem(s1)
                    if (os.path.isfile('/usr/bin/neroAacTag') or
                            os.path.isfile('/usr/local/bin/neroAacTag')):
                        s9 = ''
                        s9 = s9 + '" -meta:album="' + cleanstr(sTL, bTrue())
                        s9 = s9 + '" -meta:artist="' + cleanstr(sART2, bTrue())
                        s9 = s9 + '" -meta:genre="' + sTG
                        s9 = s9 + '" -meta:title="' + cleanstr(sTT, bTrue())
                        s9 = s9 + '" -meta:track="' + sTN
                        s9 = s9 + '" -meta:year="' + sTY + u'"'
                        if (len(sIMG1) > 0 and os.path.isfile(sIMG1)):
                            s9 = s9 + ' -add-cover:front:"' + sIMG1 & '" '
                        s1 = 'neroAacTag "' + sOUT1 + '"' + s9
                        print(s1)
                        myossystem(s1)
                elif os.path.isfile('/usr/bin/faac'):
                    s1 = u'faac -o "' + sOUT1 + u'" "' + sTMP1 + '"'
                    print(s1)
                    myossystem(s1)
                else:
                    # ffmpeg or avconv are disabled March, 2015 because
                    # `Unable to find a suitable output format for 'pipe:'`
                    try:
                        sCmdA = sData1
                        sCmdA = sCmdA + ' -strict experimental -acodec aac'
                        sCmdA = sCmdA + ' -ab 96k  -preset slow -f m4a'
                        sCmdA = sCmdA + ' -crf 22 '
                    except(UnicodeDecodeError):
                        sCmdA = ""
                    s1 = u'"' + sFFcommand + u'" - y -i "' + sTMP1 + u'" '
                    s1 = s1 + sCmdA + u' "' + sOUT1 + u'"'
                    print("-----------------------------------")
                    print("m4a output with avconv is disabled.")
                    print("-----------------------------------")
                    print(s1)
                    # myossystem(s1)
        elif sOUT1MIME == mimetypes.types_map['.mp3']:
            # Try lame for mp3 or 'audio/mpeg' files that haven't been
            #  dealt with above.
            if 'windows' in platform.system().lower():
                # The program is supplied in a zip file.  To use it,
                #  you need to extract it to the directory shown.
                # C:/opt/lame.exe
                # See: http://www.rarewares.org/mp3-lame-bundle.php
                s0 = getWinFullPath('/opt/lame.exe')
                s1 = s0 + u' -V 4 --tl "' + sTL
                s1 = s1 + u'" --ta "' + sART2
                s1 = s1 + u'" --tt "' + sTT
                s1 = s1 + u'" --tg "' + sTG
                s1 = s1 + u'" --tn "' + sTN
                s1 = s1 + u'" --ty ' + sTY
                s1 = s1 + u' "' + sTMP1
                s1 = s1 + u'" "' + sOUT1 + u'"'
                myossystem(s1)
            else:
                if len(sIMG1) > 0 and len(sFFcommand) > 0:
                    sOUT2 = sOUT1 + '.mp3'
                else:
                    sOUT2 = sOUT1
                if os.path.isfile('/usr/bin/lame'):
                    try:
                        sCmdA = '--tl "' + sTL
                        sCmdA = sCmdA + u'" --ta "' + sART2
                        sCmdA = sCmdA + u'" --tt "' + sTT
                        sCmdA = sCmdA + u'" --tg "' + sTG
                        sCmdA = sCmdA + u'" --tn "' + sTN
                        sCmdA = sCmdA + u'" --ty ' + sTY
                    except(UnicodeDecodeError, TypeError):
                        sCmdA = ""
                    # lame default setting of `--vbr-new` causes a crash in
                    # avconv, so use `--vbr-old`
                    s1 = 'lame --vbr-old ' + sCmdA + ' "' + sTMP1
                    s1 = s1 + '" "' + sOUT2 + '"'
                    print(s1)
                    myossystem(s1)
                else:
                    try:
                        # We must use these -acodec settings or
                        # avconv crashes when this script runs.
                        sCmdA = sData1
                        sCmdA = sCmdA + u' -acodec libmp3lame -ab 320k'
                        sCmdA = sCmdA + u' -aq 0 '
                    except(UnicodeDecodeError, TypeError):
                        sCmdA = u""
                    s1 = sFFcommand + u' -i "' + sTMP1 + u'" ' + sCmdA
                    s1 = s1 + u' -y "' + sOUT2 + u'"'
                    print(s1)
                    myossystem(s1)
                if len(sIMG1) > 0 and len(sFFcommand) > 0:
                    # Add image.  Make a straight copy of the audio
                    # so the quality remains the same.
                    sCmdA = u' -acodec copy '
                    s1 = sFFcommand + ' -i "' + sOUT2 + '" -i "' + sIMG1
                    s1 = s1 + u'" -map 0:0 -map 1:0 -c copy'
                    s1 = s1 + u' -id3v2_version 3 -metadata:s:v'
                    s1 = s1 + u' title="Album cover"'
                    s1 = s1 + u' -metadata:s:v comment="Cover (Front)" '
                    s1 = s1 + sCmdA + u' -y "'
                    s1 = s1 + sOUT1 + '" '
                    print(s1)
                    myossystem(s1)
                    if os.path.isfile(sOUT1):
                        os.remove(sOUT2)
                    else:
                        os.rename(sOUT2, sOUT1)
        elif sOUT1MIME == mimetypes.types_map['.aif']:
            # .aif converted with avconv doesn't have metadata.
            sCmdA = sData1
            s1 = u'"' + sFFcommand + u'" -i "' + sTMP1 + u'" '
            s1 = s1 + sCmdA + u' -y "'
            s1 = s1 + sOUT1 + u'"'
            myossystem(s1)
        elif sOUT1MIME == mimetypes.types_map['.flac']:
            # flac - free lossless audio codec.
            if 'windows' in platform.system().lower():
                # The programs is supplied in a zip file.  To use it,
                # extract it to the directory shown.
                # C:/opt/flac.exe
                # See: http://flac.sourceforge.net/
                s0 = getWinFullPath('/opt/flac.exe')
                s1 = s0 + u' -f -o "' + sOUT1 + u'" "' + sTMP1 + u'"'
                myossystem(s1)
            else:
                sCmdA = sData1
                s1 = u'"' + sFFcommand + u'" -i "' + sTMP1 + u'" '
                s1 = s1 + sCmdA + u' -y "'
                s1 = s1 + sOUT1 + u'"'
                myossystem(s1)
        elif sOUT1MIME == mimetypes.types_map['.webm']:
            # Chrome, Firefox (Linux) and totem can open webm directly.
            sCmdA = sData1
            s1 = u'"' + sFFcommand + u'" -i "'
            s1 = s1 + sTMP1 + u'" -f image2 -i "' + sIMG1
            s1 = s1 + u'" -s "' + sDIM + '" -t "' + sTIME
            s1 = s1 + u'" -vcodec libvpx -g 120 -lag-in-frames 16'
            s1 = s1 + u' -deadline good -cpu-used 0 -vprofile 0'
            s1 = s1 + u' -qmax 63 -qmin 0 -b:v 768k -acodec libvorbis'
            s1 = s1 + u' -ab 112k -ar 44100 -f webm '
            s1 = s1 + sCmdA + u' -y "' + sOUT1 + u'"'
            myossystem(s1)
        else:
            sOUT1 = sTMP1
        print(sOUT1EXT)
        print(u'-------------------')
        print(u' ')
        print(fsAppName() + ' Wav2Media')
        print(u'=================== ')
        print(u' ')
        print('    ' + s1)
        print(u' ')
        if os.path.isfile(sOUT1):
            if sAUDIBLE.lower() == 'false':
                print('Play is off - file will not play.')
                print(('The file was saved to:  ' + sOUT1))
                if os.path.isfile("/usr/bin/notify-send"):
                    s1 = u'notify-send "' + fsAppName() + '" "' + sOUT1 + u'"'
                    myossystem(s1)
            else:
                # Play the file
                v1 = '.avi;.flv;.webm;.m4v;.mov;.mpg;.mp4;.wmv'
                if (sVISIBLE.lower() == 'false' and
                        sTMP1EXT not in v1):
                    PlayWaveInBackground(sOUT1)
                else:
                    ShowWithApp(sOUT1)
        else:
            print('No output file was created.')
    except (IOError):
        print(fsAppName() + " Tools execution failed")
        sys.exit(2)
        if os.path.isfile('/usr/bin/notify-send'):
            s1 = u'notify-send "' + fsAppName() + '" "python error"'
            myossystem(s1)
    UnlockMyLock()


def bFalse():
    '''
    False boolean for comparison
    '''
    retVal = not(1)
    return retVal


def bTrue():
    '''
    True boolean for comparison
    '''
    retVal = not(0)
    return retVal


def cleanstr(sIN, bBeautifyQuotes):
    '''
    cleanstr
    ========

            sIN - string to clean
            bBeautifyQuotes - use smart quotes

    Removes some characters from strings for use in 'song' titles
    Beautifying also simply deals with problem syntax when handling text
    using quotes in python.  If you aren't using beautiful quotes, then
    check that the voices work with text that includes plain single
    and double quotes.

    For this toolbox, `sA = u'Blah'`  is good, but `sA = u"Blah"` is
    bad.  If your code doesn't match this convention, set the second
    parameter to `not(0)` (true).

    Known conforming code
    ---------------------

            sA = readtexttools.cleanstr(sB, readtexttools.bFalse())

    Unknown if code is okay
    -----------------------

            sA = readtexttools.cleanstr(sB, readtexttools.bTrue())
    '''
    retval = " "

    try:
        retval = sIN
        retval = retval.replace('\n', u' ')
        retval = retval.replace('\f', u'')
        retval = retval.replace('\r', u'')
        retval = retval.replace('\t', u' ')
        if bBeautifyQuotes:
            retval = retval.replace(" '", u" ‘")  # &lsquo;
            retval = retval.replace("'", u"’")  # &rsquo;
            retval = retval.replace(' "', u' “')  # &ldquo;
            retval = retval.replace('"', u"”")  # &rdquo;
        retval = retval.replace('"', u' ')
    except(UnicodeDecodeError):
        print(retval + ' error in readtexttools.cleanstr')
    return retval


def timefortitle():
    '''
    Returns an unambiguous time expression for a title in an
    international format
    '''
    return time.strftime('%Y-%m-%d_%H:%M:%S-%Z')


def dateforalbum():
    '''
    Returns a date expression for an album in an international
    format.
    '''
    return time.strftime('%Y-%m-%d')


def checkmytitle(sTIT, sTOOL):
    '''
    If it is not a working title, replace title.
    '''
    sC = sTIT

    try:
        if len(sC) == 0:
            sC = sTOOL + u' ' + timefortitle()
        else:
            sC = sTIT
    except(UnicodeDecodeError):
        sC = sTOOL + u' ' + timefortitle()
    return sC


def checkmyartist(sART):
    '''
    If not a working artist, replaces artist with user name.
    '''
    sC = sART

    try:
        if len(sC) == 0:
            sC = getMyUserName()
        else:
            sC = sART
    except(UnicodeDecodeError):
        sC = getMyUserName()
    return sC


def LockMyLock():
    '''
    Create a file that informs the world that the application.
    is at work.
    '''
    s1 = getMyLock('lock')

    fileh = open(s1, 'w')
    fileh.write(fsAppSignature())
    fileh.close()


def UnlockMyLock():
    '''
    Create a file that informs the world that the application
    is finished.
    '''
    s1 = getMyLock('lock')

    if os.path.isfile(s1):
        os.remove(s1)


def getMyLock(sLOCK):
    '''
    Returns path to temporary directory plus a lock file name.
    Use an value like 'lock' for sLOCK.  You can use more than
    one lock if you use different values for sLOCK.
    '''
    s1 = '.' + sLOCK
    s2 = fsAppSignature()
    s3 = ''

    if 'windows' in platform.system().lower():
        s3 = os.path.join(os.getenv('TMP'),
                          s2 + u'.' + os.getenv('USERNAME') + s1)
    elif 'darwin' in platform.system().lower():
        s3 = os.path.join(os.getenv('TMPDIR'),
                          s2 + u'.' + os.getenv('USERNAME') + s1)
    else:
        s3 = os.path.join('/tmp',
                          fsAppSignature() + u'.' + os.getenv('USER') + s1)
    return s3


def getMyUserName():
    '''
    Returns the user name.  Optionally, you can provide a
    temporary lock.id file for this function to read the
    artist or author name from and then remove.
    '''
    sOUT1 = ""

    if 'windows' in platform.system().lower():
        sOUT1 = os.getenv('USERNAME')
    elif 'darwin' in platform.system().lower():
        sOUT1 = os.getenv('USERNAME')
    else:
        sOUT1 = os.getenv('USER')
    s1 = getMyLock('lock.id')
    if os.path.isfile(s1):
        f = codecs.open(s1, mode='r', encoding='utf-8')
        sOUT1 = f.read()
        f.close()
        os.remove(s1)
    return sOUT1


def getMySongName():
    '''
    Returns the song name.
    '''
    sOUT1 = timefortitle()

    s1 = getMyLock('lock.title')
    if os.path.isfile(s1):
        f = codecs.open(s1, mode='r', encoding='utf-8')
        sOUT1 = f.read()
        f.close()
        os.remove(s1)
    return sOUT1


def getMyGenreName():
    '''
    Returns the song genre.
    '''
    sOUT1 = 'Speech'

    s1 = getMyLock('lock.genre')
    if os.path.isfile(s1):
        f = codecs.open(s1, mode='r', encoding='utf-8')
        sOUT1 = f.read()
        f.close()
        os.remove(s1)
    return sOUT1


def getMyTrackNo():
    '''
    Returns the song track number.
    '''
    sOUT1 = '1'

    s1 = getMyLock('lock.track')
    if os.path.isfile(s1):
        f = codecs.open(s1, mode='r', encoding='utf-8')
        sOUT1 = f.read()
        f.close()
        os.remove(s1)
    return sOUT1


def getMyAlbumName():
    '''
    Returns the album name.
    '''
    sOUT1 = u"(" + fsAppName() + " " + dateforalbum() + u")"

    s1 = getMyLock('lock.album')
    if os.path.isfile(s1):
        f = codecs.open(s1, mode='r', encoding='utf-8')
        sOUT1 = f.read()
        f.close()
        os.remove(s1)
    return sOUT1


def getTempPrefix():
    '''
    Returns path to temporary directory plus a filename prefix.
    Need to supply an extension to determine the context - i.e:
     -sound.wav for sound
     -image.png for image
    '''
    if 'windows' in platform.system().lower():
        sOUT1 = os.path.join(os.getenv('TMP'), os.getenv('USERNAME'))
    elif 'darwin' in platform.system().lower():
        sOUT1 = os.path.join(os.getenv('TMPDIR'), os.getenv('USER'))
    else:
        sOUT1 = os.path.join('/tmp', os.getenv('USER'))
    return sOUT1


def getWinFullPath(s1):
    '''
    Copy Windows zipped command-line programs (oggenc.exe,
    neroAacEnc.exe, neroAacTag.exe etc.) to "C:/opt".  For
    Windows programs that use an installation program (mbrola,
    espeak etc.), accept the defaults.

    Code checks for path in the 64 and 32 bit program
    directories and in thehome drive.  For example, if s1 is
    "/opt/oggenc.exe" and Windows is the US English locale on
    a single user computer, the code checks:

            "C:/Program Files/opt/oggenc.exe"
            "C:/Program Files(x86)/opt/oggenc.exe"
            "C:/opt/oggenc.exe"
    '''
    sCommand = ''

    if os.path.isfile(os.path.join(os.getenv('ProgramFiles'), s1)):
        sCommand = os.path.join(os.getenv('ProgramFiles'), s1)
    elif os.getenv('ProgramFiles(x86)'):
        if os.path.isfile(os.path.join(os.getenv('ProgramFiles(x86)'), s1)):
            sCommand = os.path.join(os.getenv('ProgramFiles(x86)'), s1)
    elif os.getenv('HOMEDRIVE'):
        if os.path.isfile(os.path.join(os.getenv('HOMEDRIVE'), s1)):
            sCommand = os.path.join(os.getenv('HOMEDRIVE'), s1)
    else:
        sCommand = ''
    if 'windows' in platform.system().lower():
        return sCommand
    else:
        return ''


def ShowWithApp(sOUT1):
    '''
    Same as double clicking the document - opens in default
    application.
    '''
    if 'darwin' in platform.system().lower():
        # MacOS
        s1 = u'open "' + sOUT1 + u'" '
        myossystem(s1)
    elif 'windows' in platform.system().lower():
        # Windows
        os.startfile(sOUT1)
    else:
        if os.path.isfile('/usr/bin/xdg-open'):
            s1 = u'xdg-open "' + sOUT1 + u'" '
        elif os.path.isfile('/usr/bin/gnome-open'):
            s1 = u'gnome-open "' + sOUT1 + u'" '
        elif os.path.isfile('/usr/bin/kde-open'):
            s1 = u'kde-open "' + sOUT1 + u'" '
        myossystem(s1)


def PlayWaveInBackground(sOUT1):
    '''
    Opens using command line shell.
    '''
    if 'darwin' in platform.system().lower():
        # MacOS
        s1 = u'afplay "' + sOUT1 + u'" '
        myossystem(s1)
    elif 'windows' in platform.system().lower():
        # Windows
        import winsound
        winsound.PlaySound(sOUT1, winsound.SND_FILENAME | winsound.SND_NOWAIT)
    else:
        if os.path.isfile('/usr/bin/esdplay'):
            s1 = u'esdplay "' + sOUT1 + u'" '
        elif os.path.isfile('/usr/bin/paplay'):
            s1 = u'paplay "' + sOUT1 + u'" '
        elif os.path.isfile('/usr/bin/aplay'):
            s1 = u'aplay "' + sOUT1 + u'" '
        myossystem(s1)


def myossystem(s1):
    '''
    This is equivalent to os.system(s1)
    Replaced os.system(s1) to avoid Windows path errors.
    '''
    s1 = s1.encode('utf-8')
    if 'windows' in platform.system().lower():
        try:
            retcode = subprocess.call(s1, shell=False)
            if retcode < 0:
                print('Process was terminated by signal')
            else:
                print('Process returned')
        except (OSError, e):
            print('Execution failed')
    else:
        os.system(s1)


def main():
    '''
    Converts the input wav sound to another format.  Ffmpeg
    can include a still frame movie if you include an image.
    '''
    if sys.argv[-1] == sys.argv[0]:
        usage()
        sys.exit(0)
    sLANG = ''
    sWAVE = ''
    sVISIBLE = ''
    sAUDIBLE = ''
    sTXT = ''
    sIMG1 = ''
    sOUT1 = ''
    sART = ''
    sDIM = '600x600'
    sB = 'Video memo'
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            'hovaistad',
            ['help',
             'output=',
             'visible=',
             'audible=',
             'image=',
             'sound=',
             'title=',
             'artist=',
             'dimensions=']
            )
    except (getopt.GetoptError):
        # print help information and exit
        print('An option was not recognized')
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif o in ('-o', '--output'):
            sOUT1 = a
        elif o in ('-v', '--visible'):
            sVISIBLE = a
        elif o in ('-a', '--audible'):
            sAUDIBLE = a
        elif o in ('-i', '--image'):
            sIMG1 = a
        elif o in ('-s', '--sound'):
            sWAVE = a
        elif o in ('-t', '--title'):
            sB = a
        elif o in ('-n', '--artist'):
            sART = a
        elif o in ('-d', '--dimensions'):
            sART = a
        else:
            assert False, 'unhandled option'
            usage()
    if len(sOUT1) == 0 or len(sWAVE) == 0:
        usage()
    else:
        Wav2Media(sB, sWAVE, sIMG1, sOUT1, sAUDIBLE, sVISIBLE, sART, sDIM)
    sys.exit(0)


if __name__ == '__main__':
    main()
