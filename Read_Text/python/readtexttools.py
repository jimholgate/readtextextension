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
# (c) 2018 [James Holgate Vancouver, CANADA](readtextextension(a)outlook.com)
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

Copyright (c) 2011 - 2020 James Holgate
'''
import aifc
import codecs
import getopt
import math
import mimetypes
import os
import shlex
import sunau
import sys
import time

try:
    import subprocess
except ImportError:
    pass
try:
    import wave
except ImportError:
    pass

try:
    import urllib.parse as urlparse
    import urllib.request as urllib
except ImportError:
    try:
        import urlparse
        import urllib
    except ImportError:
        pass

try:
    import gi
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst
except:
    pass

try:
    from HTMLParser import HTMLParser
except ImportError:
    # python 3
    from html.parser import HTMLParser


class ClassRemoveXML(HTMLParser):
    ''' Remove XML using python HTML parsing. '''
    def __init__(self):
        self.reset()
        self.fed = []
        self.convert_charrefs = []
    def handle_data(self, d):
        ''' Handle string data. '''
        self.fed.append(d)
    def get_fed_data(self):
        ''' Return fed data. '''
        return ''.join(self.fed)


def stripxml(str1):
    '''
    `stripxml(str1)`

    Plain text output
    =================

    When `stripxml` is applied to a string, python converts the
    xml input into plain text with no special codes.  This is
    for speech synthesis and other applications that require a
    sanitized string.

    Application note
    ----------------

    With python 3, the function fails if this file is placed in a
    directory that contains a file called `html.py`. This is
    because the python tries to find the `HTMLParser` library
    from the local `html.py` file.
    '''
    try:
        mydata = ClassRemoveXML()
        mydata.feed(str1)
        retval = mydata.get_fed_data()
    except Exception:
        # unexpected error
        retval = str1
    return retval


def usage():
    '''
    Displays the usage of the included python app "main", which can be used to
    convert wav files to other formats like ogg audio or webm video.
    '''
    sA = ' ' + os.path.split(sys.argv[0])[1]
    print('''
Read text tools
===============

Reads a .wav sound file, converts it and plays copy with a player.
Requires a converter like `avconv`, `faac`, `lame` or `ffmpeg`.

## Usage

### Audio:

     readtexttools.py --sound="xxx.wav" --output="xxx.ogg"
     readtexttools.py --visible="false" --audible="true"  \\ 
       --sound="xxx.wav" --output="xxx.ogg"

### Video:

Makes an audio with a poster image.  Uses `avconv` or `ffmpeg`.

     readtexttools.py --image="xxx.png" --sound="xxx.wav" \\ 
      --output="xxx.webm"
     readtexttools.py --visible="true" --audible="true" --image="x.png" \\
       --sound="x.wav"--title="Title" --output="x.webm"
''')


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
    sMIME = "xxz/xxz-do-not-match"
    if len(sTMP1EXT) != 0:
        try:
            sMIME = mimetypes.types_map[sTMP1EXT]
        except IndexError:
            pass
    if sTMP1EXT in ['.m4a']:
            if (os.path.isfile('/usr/bin/faac') or
                    os.path.isfile('C:\\opt\\neroAacEnc.exe') or
                    os.path.isfile('C:\\opt\\faac.exe')):
                sOUT1 = sTMP1
                sTMP1 = sOUT1 + u'.wav'
            else:
                # Can't make m4a, so make wav
                sOUT1 = sTMP1 + u'.wav'
                sTMP1 = sOUT1
    elif sMIME == mimetypes.types_map['.mp3']:
        if MediaConverterInstalled() != False:
            if (os.path.isfile('/usr/share/doc/liblame0/copyright') or
                    os.path.isfile('/usr/share/doc/libmp3lame0/copyright') or
                    os.path.isfile('/usr/bin/lame') or
                    os.path.isfile('C:\\opt\\lame.exe') or
                    os.path.isfile('/usr/lib/x86_64-linux-gnu/libmp3lame.so.0')):
                sOUT1 = sTMP1
                sTMP1 = sOUT1 + u'.wav'
            else:
                # Can't make mp3, so make wav
                sOUT1 = sTMP1 + u'.wav'
                sTMP1 = sOUT1
        else:
            # Can't make mp3, so make wav
            sOUT1 = sTMP1 + u'.wav'
            sTMP1 = sOUT1
    elif sTMP1EXT in ['.mp2']:
        if MediaConverterInstalled() != False:
            if (os.path.isfile('/usr/share/doc/libtwolame0/copyright') or
                    os.path.isfile('C:\\opt\\twolame.exe')):
                sOUT1 = sTMP1
                sTMP1 = sOUT1 + u'.wav'
            else:
                sOUT1 = sTMP1 + u'.wav'
                sTMP1 = sOUT1
        else:
            # Can't make mp2, so make wav
            sOUT1 = sTMP1 + u'.wav'
            sTMP1 = sOUT1
    elif sTMP1EXT in ['.oga','.ogg']:
        if MediaConverterInstalled() != False:
            if (os.path.isfile('/usr/share/doc/libogg0/copyright') or
                    os.path.isfile('C:\\opt\\oggenc.exe') or
                    os.path.isfile('C:\\opt\\oggenc2.exe')):
                sOUT1 = sTMP1
                sTMP1 = sOUT1 + u'.wav'
            else:
                sOUT1 = sTMP1 + u'.wav'
                sTMP1 = sOUT1
        else:
            # Can't make ogg, so make wav
            sOUT1 = sTMP1 + u'.wav'
            sTMP1 = sOUT1
    elif sMIME == mimetypes.types_map['.aif']:
            if MediaConverterInstalled() != False:
                sOUT1 = sTMP1
                sTMP1 = sOUT1 + u'.wav'
            else:
                # Can't make aif, so make wav
                sOUT1 = sTMP1 + u'.wav'
                sTMP1 = sOUT1
    elif sTMP1EXT in ['.flac']:
            if (MediaConverterInstalled() != False or
                    os.path.isfile('C:\\opt\\flac.exe')):
                sOUT1 = sTMP1
                sTMP1 = sOUT1 + u'.wav'
            else:
                # Can't make flac, so make wav
                sOUT1 = sTMP1 + u'.wav'
                sTMP1 = sOUT1
    elif sTMP1EXT in ['.webm']:
            if (MediaConverterInstalled() != False):
                sOUT1 = sTMP1
                sTMP1 = sOUT1 + u'.wav'
            else:
                # Can't make webm, so make wav
                sOUT1 = sTMP1 + u'.wav'
                sTMP1 = sOUT1
    elif 'video/' in sMIME:
            if (len(ffMpegPath()) > 4 and
                    sIMG1EXT in ['.bmp','.gif','.jpeg','.jpg','.png','.tif','.tiff','.tga']):
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
    if retVal:
        MakeOutputDirectory(sOUT1)
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
    elif os.path.isfile('/usr/bin/osascript'):
        if os.path.isfile('Applications/Miro.app/Contents/Helpers/ffmpeg'):
            retVal = 'Applications/Miro.app/Contents/Helpers/ffmpeg'
        elif os.path.isfile(
                'Applications/' + mvc + '.app/Contents/Helpers/ffmpeg'
                ):
            retVal = 'Applications/' + mvc + '.app/Contents/Helpers/ffmpeg'
        elif os.path.isfile('/opt/Shotcut/Shotcut.app/bin/ffmpeg'):
            retVal = '/opt/Shotcut/Shotcut.app/bin/ffmpeg'
    elif 'nt' in os.name.lower():
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


def fGstLaunchPath():
    '''
    gst-launch is primarily a debugging tool for developers and users.
    gst-launch-x.x may not be in the normal environment PATH,
    so we look for it, and return the location.
    '''
    retVal = ''

    if os.path.isfile('/usr/bin/gst-launch-1.0'):
        retVal = '/usr/bin/gst-launch-1.0'
    elif os.path.isfile('/usr/bin/gst-launch-1.0'):
        retVal = '/usr/bin/gst-launch-1.0'
    elif os.path.isfile('/usr/local/bin/gst-launch-0.10'):
        retVal = '/usr/local/bin/gst-launch-0.10'
    elif os.path.isfile('/usr/local/bin/gst-launch-0.10'):
        retVal = '/usr/local/bin/gst-launch-0.10'
    return retVal


def MediaConverterInstalled():
    retVal = False
    if len(ffMpegPath()) > 4:
        retVal = True
    elif len(fGstLaunchPath()) > 4:
        retVal = True
    return retVal


def MakeOutputDirectory(sOUT1):
    ''' Make sure that the destination directory exists'''
    DestDir = os.path.dirname(sOUT1)
    if os.path.exists(DestDir) != True:
        try:
            os.makedirs(DestDir)
        except:
            DestDir = ''
    return DestDir


def ProcessWaveMedia(sB, sTMP1, sIMG1, sOUT1, sAUDIBLE, sVISIBLE, sART, sDIM):
    '''
    Converts audio file, plays copy and deletes original
    + sB is brief title
    + sTMP is working file name (wav)
    + sIMG1 is image to add to video.  Ignored if making audio only
    + sOUT1 is output file name.( webm, ogg etc.)
    + sAUDIBLE - Do we play the file after conversion?
    + sVISIBLE - Do we use a GUI or the console?
    '''
    # Handle simply with Gstreamer
    if ((os.path.splitext(sOUT1)[1].lower() == ".spx") and
       (CheckForGSTPlugIn("libgstvorbis") != '')):
        GstWav2Media(sB, sTMP1, sIMG1, sOUT1, sAUDIBLE, sVISIBLE, sART, sDIM)
    elif ((os.path.splitext(sOUT1)[1].lower() == ".opus") and
          (CheckForGSTPlugIn("libgstopus") != '')):
        GstWav2Media(sB, sTMP1, sIMG1, sOUT1, sAUDIBLE, sVISIBLE, sART, sDIM)
    # Handle with avconv, ffmpeg or a specific program
    elif len(ffMpegPath()) > 4:
        Wav2Media(sB, sTMP1, sIMG1, sOUT1, sAUDIBLE, sVISIBLE, sART, sDIM)
    elif os.path.splitext(sOUT1)[1].lower() == ".mp3":
        if os.path.isfile('/usr/bin/lame'):
            Wav2Media(sB, sTMP1, sIMG1, sOUT1, sAUDIBLE, sVISIBLE, sART, sDIM)
        else:
            GstWav2Media(sB,
                         sTMP1, sIMG1, sOUT1, sAUDIBLE, sVISIBLE, sART, sDIM)
    elif (os.path.splitext(sOUT1)[1].lower() == ".m4a"):
        Wav2Media(sB, sTMP1, sIMG1, sOUT1, sAUDIBLE, sVISIBLE, sART, sDIM)
    else:
        # Use Gstreamer if you are missing `ffmpeg`, `avconv` etc.
        GstWav2Media(sB, sTMP1, sIMG1, sOUT1, sAUDIBLE, sVISIBLE, sART, sDIM)
    try:
        if sOUT1 == '':
            print(u'Saved to: ' + sTMP1)
        else:
            if os.path.isfile(sTMP1):
                if os.path.isfile(sOUT1):
                    os.remove(sTMP1)
                else:
                    print(u'Did not remove "' + sTMP1 +
                          u'" because the converter did not write "' +
                          sOUT1 +
                          '"'
                          )
    except (OSError):
        print(u'Could not remove "' + sTMP1 + u'"')


def CheckForGSTPlugIn(sA):
    '''
    Check directories for a named GST plugin (i. e.: `libgstvorbis`)
    '''
    # This does not check for plugin by pad name, mime type or extension
    s1 = ''
    s2 = '/usr/local/lib/x86_64-linux-gnu/'
    s3 = '/usr/local/lib/'
    s4 = '/usr/lib/x86_64-linux-gnu/'
    s5 = '/usr/lib/'
    s6 = '.so'
    if os.path.isfile('/usr/bin/osascript'):
        s2 = os.path.join(
                          os.getenv(
                           'HOME'),
                           '/.gstreamer-0.10/plugins/')
        s4 = os.getenv('GST_PLUGIN_PATH')
        s6 = '.dylib'
    elif 'nt' in os.name.lower():
        s2 = os.path.join(
                          os.getenv(
                           'HOME'),
                           '/.gstreamer-0.10/plugins/')
        s3 = os.path.join(
                          os.getenv(
                           'HOMEDRIVE'),
                           '/gstreamer-sdk/0.10/x86/lib/gstreamer-0.10/')
        s4 = os.getenv('GST_PLUGIN_PATH')
        s5 = os.path.join(
                          os.getenv(
                          'HOMEDRIVE'),
                          '/opt/gstreamer-0.10/')
        s6 = '.dll'

    if os.path.isfile(os.path.join(s2 + 'gstreamer-1.0/', sA + s6)):
        s1 = os.path.join(s2 + 'gstreamer-1.0/', sA + s6)
    elif os.path.isfile(os.path.join(s2 + 'gstreamer-0.10/', sA + s6)):
        s1 = os.path.join(s2 + 'gstreamer-0.10/', sA + s6)
    elif os.path.isfile(os.path.join(s3 + 'gstreamer-1.0/', sA + s6)):
        s1 = os.path.join(s3 + 'gstreamer-1.0/', sA + s6)
    elif os.path.isfile(os.path.join(s3 + 'gstreamer-0.10/', sA + s6)):
        s1 = os.path.join(s3 + 'gstreamer-0.10/', sA + s6)
    elif os.path.isfile(os.path.join(s4 + 'gstreamer-1.0/', sA + s6)):
        s1 = os.path.join(s4 + 'gstreamer-1.0/', sA + s6)
    elif os.path.isfile(os.path.join(s4 + 'gstreamer-0.10/', sA + s6)):
        s1 = os.path.join(s4 + 'gstreamer-0.10/', sA + s6)
    elif os.path.isfile(os.path.join(s5 + 'gstreamer-1.0/', sA + s6)):
        s1 = os.path.join(s5 + 'gstreamer-1.0/', sA + s6)
    elif os.path.isfile(os.path.join(s5 + 'gstreamer-0.10/', sA + s6)):
        s1 = os.path.join(s5 + 'gstreamer-0.10/', sA + s6)
    print ('\n# Discovered GStreamer library # \n\n`' + s1 + "`")
    return s1


def ExecuteGSTCommand(sA):
    '''
    Execute a GStreamer command. This usually includes a source,
    a series of pads, and a destination.

    Example 1
    ---------

    Convert a wav file to an mp3 file.
    ```
    filesrc name='xx.wav' ! lamemp3enc ! filesink location='xx.mp3'
    ```

    Example 2
    ---------

    Play a sound file.
    ```
    playbin uri='file:///pathto/xx.mp3'
    ```

    Find examples of commands on the [Gstreamer cheat sheet
    wiki](http://wiki.oz9aec.net/index.php/Gstreamer_cheat_sheet).
    '''
    i1 = 0
    try:
        Gst.init(None)
        pl = Gst.parse_launch(sA)
        pl.set_state(gst.STATE_NULL)
        pl.set_state(gst.STATE_PLAYING)
        i1 = 1
    except:
        i1 = 0
    if i1 == 0:
        try:
            s1 = "gst-launch-1.0 " + sA
            myossystem(s1)
            i1 = 1
        except:
            i1 = 0
    if i1 == 0:
        try:
            s1 = "gst-launch-0.10 " + sA
            myossystem(s1)
            i1 = 1
        except:
            i1 = 0
    return i1


def NullGSTCommand():
    i1 = 0
    try:
        Gst.init(None)
        pl = Gst.parse_launch("audiotestsrc ! audioconvert ! testsink")
        pl.set_state(gst.STATE_NULL)
        UnlockMyLock()
        i1 = 1
    except:
        i1 = 0
    return i1


def GstWav2Media(sB, sTMP1, sIMG1, sOUT1, sAUDIBLE, sVISIBLE, sART, sDIM):
    '''
    If `avconv` is not installed and `ffmpeg` is not installed, use
    gst-launch for a **basic** media conversion.  Note: wav format
    files do not contain metadata tags.  Some forms of metadata tagging
    may be incompatible with legacy players.
    '''
    sTMP1EXT = os.path.splitext(sOUT1)[1].lower()
    sPIPE = u'" ! decodebin ! audioconvert ! '
    sFileView = sOUT1

    print('\n# Using GStreamer #\n\nGStreamer writes common media formats.\n')
    print (sTMP1EXT)

    if sTMP1EXT == ".m4a":
        # libgstisomp4 - Basic ISO MP4 container
        if '' == CheckForGSTPlugIn('libgstisomp4'):
            print('## gst-launch ##\n\nM4A is not supported. Using WAV.')
            sPIPE = u''
        else:
            print('## libgstisomp4 ##\n\nQuickTime Muxer\n' +
                  'Mono : Raw 16-bit PCM audio')
            #sPIPE = sPIPE + u'qtmux !'
            sPIPE = sPIPE + u'qtmux !'
    elif sTMP1EXT == ".mp3":
        # libgstlame - MP3 compatible compressed file.
        if '' == CheckForGSTPlugIn('libgstlame'):
            print('## gst-launch ##\n\nMP3 is not supported. Using WAV.')
            sPIPE = u''
        else:
            print('## libgstlame ##\n\nL.A.M.E. mp3 encoder\n' +
                  'GStreamer Ugly Plugins')
            sPIPE = sPIPE + u'lamemp3enc !'
    elif sTMP1EXT == ".flac":
        sPIPE = sPIPE + u'flacenc !'
    elif sTMP1EXT == ".oga":
        sPIPE = sPIPE + u'vorbisenc ! oggmux !'
    elif sTMP1EXT == ".ogg":
        sPIPE = sPIPE + u'vorbisenc ! oggmux !'
    elif sTMP1EXT == ".opus":
        if '' == CheckForGSTPlugIn('libgstopus'):
            print('## gst-launch ##\n\nOPUS is not supported.  Using WAV.')
            sPIPE = u''
        else:
            print('## OPUS plugin library ##\n\nGStreamer Bad Plugins.')
            sPIPE = sPIPE + u'opusenc ! oggmux !'
    elif sTMP1EXT == ".spx":
        sPIPE =  sPIPE + u'speexenc ! oggmux !'
    elif sTMP1EXT == ".webm":
        sPIPE = (sPIPE + u'vorbisenc ! webmmux !')
    else:
        sPIPE = ""
    # Convert
    if (sOUT1 != "") and (sPIPE != ""):
        s1 = (u'filesrc location="' +
                   sTMP1 +
                   sPIPE +
                  ' filesink location="' +
                   sOUT1 +
                   u'"')
        print('\n## Using GStreamer command ##\n\n```\n' + s1 + '\n```\n')
        sFileView = writeXspfPlayList(sOUT1, sART, sIMG1)
        print(s1)
        ExecuteGSTCommand(s1)
    else:
        # Play the file
        print ("Play the file")
        v1 = ['.avi','.flv','.webm','.m4v','.mov','.mpg','.mp4','.wmv']
        if sTMP1EXT == '':
            sTMP1EXT = ".wav"
        if (sVISIBLE.lower() == 'false' and
                sTMP1EXT not in v1):
            LockMyLock()
            PlayWaveInBackground(sTMP1)
        else:
            ShowWithApp(sTMP1)
        exit()
    # Playback with or without GUI
    try:
        if os.path.isfile(sFileView):
            if sAUDIBLE.lower() == 'false':
                print('Play is off - file will not play.')
                print(('The file was saved to:  ' + sOUT1))
                if os.path.isfile("/usr/bin/notify-send"):
                    s1 = u'notify-send "' + fsAppName() + '" "' + sOUT1 + u'"'
                    myossystem(s1)
            else:
                # Play the file
                v1 = '.avi;.flv;.webm;.m4v;.mov;.mpg;.mp4;.wmv'
                if sTMP1EXT == '':
                    sTMP1EXT = ".wav"
                if (sVISIBLE.lower() == 'false' and
                        sTMP1EXT not in v1):
                    LockMyLock()
                    PlayWaveInBackground(sOUT1)
                else:
                    ShowWithApp(sFileView)
        elif os.path.isfile(sOUT1):
            if sAUDIBLE.lower() == 'false':
                print('Play is off - file will not play.')
                print(('The file was saved to:  ' + sOUT1))
                if os.path.isfile("/usr/bin/notify-send"):
                    s1 = u'notify-send "' + fsAppName() + '" "' + sOUT1 + u'"'
                    myossystem(s1)
            else:
                # Play the file
                v1 = '.avi;.flv;.webm;.m4v;.mov;.mpg;.mp4;.wmv'
                if sTMP1EXT == '':
                    sTMP1EXT = ".wav"
                if (sVISIBLE.lower() == 'false' and
                        sTMP1EXT not in v1):
                    LockMyLock()
                    PlayWaveInBackground(sOUT1)
                else:
                    ShowWithApp(sOUT1)
        else:
            print('`GstWav2Media` finished with no errors.')
    except:
        print('Error in `GstWav2Media`.')
        sys.exit(2)
    UnlockMyLock()


def SoundLenInSeconds(sTMP1):
    '''
    Tells approximately how long a sound file is in seconds as an integer
    We round up so that processes that call for sleep have time to finish.
    '''
    sTMP1EXT = os.path.splitext(sTMP1)[1].lower()
    retVal = 0
    mimetypes.init()
    sMIME = "xxz-xzz-no-match"
    if len(sTMP1EXT) != 0:
        try:
            sMIME = mimetypes.types_map[sTMP1EXT]
        except IndexError:
            retVal = 0
    if sMIME == mimetypes.types_map['.wav']:
        try:
            snd_read = wave.open(sTMP1, 'r')
            retVal = math.ceil(snd_read.getnframes()//snd_read.getframerate()) + 1
            snd_read.close()
        except NameError:
            pass
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


def GetAMetaDataStr(i1, sART2):
    # Set defaults
    sTT = ""
    sTL = ""
    sTG = ""
    sTN = ""
    sTY = time.strftime('%Y')
    iNone = 0
    iAvconv = 1
    iOggEnc2 = 2
    iNeroMp4 = 3
    iWinLame = 4
    iUnixLame = 5
    iVLCxspfTrack = 6
    iVLCxspfTitle = 7
    iVLCxspfAuthor = 8
    iVLCxspfAlbum = 9
    iVLCxspfGenre = 10
    iXSPF = 11
    iM3U = 12

    # Look up data
    try:
        if len(sTT) == 0:
            sTT = cleanstr(getMySongName(), False)
        else:
            sTT = cleanstr(sTT, False)
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
        s1 = sART2
        print ("ART2", s1)
        if len(s1) == 0:
            sART2 = cleanstr(getMyUserName(), False)
        else:
            sART2 = cleanstr(s1, False)
        print(sART2)
    except (UnicodeDecodeError):
        sART2 = fsAppName()
        print ("Error finding ART2")
    try:
        sTL = cleanstr(getMyAlbumName(), False)
    except:
        sTL = "Untitled album"
    # Format the string with tags
    try:
        if i1 == iNone:
            # Print data, but do not return a string.
            s1 = ''
        elif i1 == iAvconv:
            # Vorbis - flac, ogg, opus, spx
            # avconv, ffmpeg
            # Double quotes must be cleaned from strings but UTF-8 is okay
            s1 = (u" -metadata album='" + cleanstr(sTL, True) +
                  u"' -metadata artist='" + cleanstr(sART2, True) +
                  u"' -metadata genre='" + sTG +
                  u"' -metadata title='" + cleanstr(sTT, True) +
                  u"' -metadata track='" + sTN +
                  u"' -metadata Year='" + sTY + u"' ")
        elif i1 == iOggEnc2:
            # oggenc2 and oggenc2.exe command line sequence
            # Double quotes must be cleaned from strings but UTF-8 is okay
            s1 = (u" -metadata album='" + cleanstr(sTL, True) +
                  u"' -metadata artist='" + cleanstr(sART2, True) +
                  u"' -metadata genre='" + sTG +
                  u"' -metadata title='" + cleanstr(sTT, True) +
                  u"' -metadata track='" + sTN +
                  u"' -metadata Year='" + sTY + u"' ")
        elif i1 == iNeroMp4:
            s1 = (u' -meta:album="' + cleanstr(sTL, True) +
                  u'" -meta:artist="' + cleanstr(sART2, True) +
                  u'" -meta:genre="' + sTG +
                  u'" -meta:title="' + cleanstr(sTT, True) +
                  u'" -meta:track="' + sTN +
                  u'" -meta:year="' + sTY + u'" ')
        elif i1 == iWinLame:
            s1 = (u' --tl "' + sTL +
                  u'" --ta "' + sART2 +
                  u'" --tt "' + sTT +
                  u'" --tg "' + sTG +
                  u'" --tn "' + sTN +
                  u'" --ty ' + sTY)
        elif i1 == iUnixLame:
            s1 = (u' --tl "' + sTL +
                  u'" --ta "' + sART2 +
                  u'" --tt "' + sTT +
                  u'" --tg "' + sTG +
                  u'" --tn "' + sTN +
                  u'" --ty ' + sTY)
        elif i1 == iVLCxspfTrack:
            s1 = cleanstr(sTT, True)
        elif i1 == iVLCxspfTitle:
            s1 = cleanstr(sTL, True)
        elif i1 == iVLCxspfAuthor:
            s1 = cleanstr(sART2, True)
        elif i1 == iVLCxspfAlbum:
            s1 = cleanstr(sTL, True)
        elif i1 == iVLCxspfGenre:
            s1 = cleanstr(sTG, True)
        elif i1 == iXSPF:
            s1 = ('<?xml version="1.0" encoding="UTF-8"?>\n' +
                  '<playlist version="1" xmlns="http://xspf.org/ns/0/">\n' +
                  '<!-- xspf.org playlist for videolan.org player -->\n' +
                  '<trackList>\n' +
                  '<track>\n' +
                  '<location>' + '[%%LOCATION%%]' +
                  '</location>\n' +
                  '<creator>' + (sART2) +
                  '</creator>\n' +
                  '<album>' + (sTL) +
                  '</album>\n' +
                  '<title>' + (sTT) +
                  '</title>\n' +
                  '<annotation>' + (sTG) +
                  '</annotation>\n' +
                  '<image>' + '[%%IMAGE%%]' +
                  '</image>\n' +
                  '</track>\n' +
                  '</trackList>\n' +
                  '</playlist>')

        elif i1 == iM3U:
            s1 = ('#EXTM3U\n' +
                  'EXTINF:[%%SECONDS%%],' +
                  sART2 +
                  ' - ' +
                  sTT +
                  '\n' +
                  '[%%LOCATION%%]' +
                  '\n')
        else:
            # Print data, but do not return a string.
            s1 = ''
    except:
        s1 = ''
        print("Error in `GetAMetaDataStr(n, sART2)`")
    if s1 != '':
        print('\n## Metadata ##\n```')
        print(s1)
        print(u'```\n')
    return s1


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

    iTIME = WavtoSeconds(sTMP1)
    sTIME = repr(iTIME)
    sOUT1EXT = os.path.splitext(sOUT1)[1].lower()
    sTMP1EXT = os.path.splitext(sTMP1)[1].lower()
    # GetAMetaDataStr(iUnixLame, sART)
    iAvconv = 1
    iOggEnc2 = 2
    iNeroMp4 = 3
    iWinLame = 4
    iUnixLame = 5

    LockMyLock()
    if len(sDIM) == 0:
        sDIM = '600x600'
    # Check for mimetype extensions like `.aif` and `.aiff.`
    mimetypes.init()
    if len(sOUT1EXT) == 0:
        sOUT1MIME = 'zxx/zxx-does-not-match'
    else:
        sOUT1MIME = mimetypes.types_map[sOUT1EXT]
    # getMySongName() is normally the first few words of the selection.
    try:
        # Double quotes must be cleaned from strings but UTF-8 is okay
        sData1 = GetAMetaDataStr(iAvconv, sART)
    except(UnicodeDecodeError):
        sData1 = u''
    try:
        sCmdA = u''
        sFFcommand = ffMpegPath()
        if sOUT1EXT in ['.ogg', 'oga']:
            if 'nt' in os.name.lower():
                # C:/opt/oggenc2.exe
                # Get oggenc2.exe: http://www.rarewares.org/ogg-oggenc.php
                s0 = getWinFullPath('/opt/oggenc2.exe')
                if len(s0) == 0:
                    s0 = getWinFullPath('/opt/oggenc.exe')
                s1 = ''.join([s0,
                      ' -o "',
                      sOUT1,
                      '" "',
                      sTMP1,
                      '"'])
                myossystem(s1)
            else:
                sCmdA = sData1
                s1 = ''.join(['"',
                      sFFcommand,
                      '" -i "',
                      sTMP1,
                      '" ',
                      sCmdA,
                      ' -y "',
                      sOUT1, '"'])
                myossystem(s1)
        elif sOUT1EXT in ['.m4a']:
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
            # GStreamer
            # =========
            #
            # GStreamer includes a basic m4a muxer, but the file is not
            # compressed or optimized.
            #
            if 'nt' in os.name.lower():
                # C:/opt/neroAacEnc.exe
                s0 = getWinFullPath('/opt/neroAacEnc.exe')
                if len(s0) == 0:
                    s0 = getWinFullPath('/opt/faac.exe')
                    s1 = ''.join([s0,
                          ' -o "',
                          sOUT1,
                          '" "',
                          sTMP1,
                          '"'])
                else:
                    s1 = ''.join([s0,
                          ' -if "',
                          sTMP1,
                          '" -of "',
                          sOUT1,
                          '"'])
                myossystem(s1)
            else:
                if (os.path.isfile('/usr/bin/neroAacEnc') or
                        os.path.isfile('/usr/local/bin/neroAacEnc')):
                    s1 = ''.join(['neroAacEnc -if "',
                            sTMP1,
                            '" -of "',
                            sOUT1,
                            '" '])
                    myossystem(s1)
                    if (os.path.isfile('/usr/bin/neroAacTag') or
                            os.path.isfile('/usr/local/bin/neroAacTag')):
                        s9 = GetAMetaDataStr(iNeroMp4, sART)
                        if (len(sIMG1) > 0 and os.path.isfile(sIMG1)):
                            s9 = ''.join([s9,
                                  ' -add-cover:front:"',
                                  sIMG1,
                                  '" '])
                        s1 = ''.join(['neroAacTag "',
                              sOUT1,
                              '"',
                              s9])
                        myossystem(s1)
                else:
                    # Freeware Advanced Audio Coder
                    # FAAC 1.28
                    # faac is disabled March, 2016 because
                    # WARNING: MP4 support unavailable!
                    #
                    # ffmpeg or avconv are disabled March, 2015 because
                    # `Unable to find a suitable output format for 'pipe:'`
                    #
                    # Create a mono Raw 16-bit PCM audio ISO M4A file in
                    # a QuickTime container. (Not optimal...)
                    print('# WARNING #\n\n Could not locate Nero AAC encoder')
                    GstWav2Media(sB,
                                 sTMP1,
                                 sIMG1,
                                 sOUT1,
                                 sAUDIBLE,
                                 sVISIBLE,
                                 sART,
                                 sDIM)

        elif sOUT1MIME == mimetypes.types_map['.mp3']:
            # Try lame for mp3 or 'audio/mpeg' files that haven't been
            #  dealt with above.
            if 'nt' in os.name.lower():
                # The program is supplied in a zip file.  To use it,
                #  you need to extract it to the directory shown.
                # C:/opt/lame.exe
                # See: http://www.rarewares.org/mp3-lame-bundle.php
                s0 = getWinFullPath('/opt/lame.exe')
                s1 = ''.join([s0,
                        ' -V 4 ',
                        GetAMetaDataStr(iWinLame, sART),
                        ' "',
                        sTMP1,
                        '" "',
                        sOUT1,
                        '"'])
                myossystem(s1)
            else:
                if len(sIMG1) > 0 and len(sFFcommand) > 0:
                    sOUT2 = sOUT1 + '.mp3'
                else:
                    sOUT2 = sOUT1
                if os.path.isfile('/usr/bin/lame'):
                    try:
                        sCmdA = GetAMetaDataStr(iUnixLame, sART)
                    except(UnicodeDecodeError, TypeError):
                        sCmdA = ""
                    # lame default setting of `--vbr-new` causes a crash in
                    # avconv, so use `--vbr-old`
                    s1 = ''.join(['lame --vbr-old ',
                          sCmdA,
                          ' "',
                          sTMP1,
                          '" "', 
                          sOUT2, 
                          '"'])
                    myossystem(s1)
                else:
                    try:
                        # We must use these -acodec settings or
                        # avconv crashes when this script runs.
                        sCmdA = (sData1 +
                                 u' -acodec libmp3lame -ab 320k' +
                                 u' -aq 0 ')
                    except(UnicodeDecodeError, TypeError):
                        sCmdA = u""
                    s1 = ''.join([sFFcommand,
                         ' -i "',
                         sTMP1,
                         '" ',
                         sCmdA,
                         ' -y "',
                         sOUT2,
                         '"'])
                    myossystem(s1)
                if len(sIMG1) > 0 and len(sFFcommand) > 0:
                    # Add image.  Make a straight copy of the audio
                    # so the quality remains the same.
                    sCmdA = u' -acodec copy '
                    s1 = ''.join([sFFcommand,
                          ' -i "',
                          sOUT2,
                          '" -i "',
                          sIMG1,
                          '" -map 0:0 -map 1:0 -c copy',
                          ' -id3v2_version 3 -metadata:s:v',
                          ' title="Album cover"',
                          ' -metadata:s:v comment="Cover (Front)" ',
                          sCmdA, ' -y "',
                          sOUT1, '" '])
                    myossystem(s1)
                    if os.path.isfile(sOUT1):
                        os.remove(sOUT2)
                    else:
                        os.rename(sOUT2, sOUT1)
        elif sOUT1MIME == mimetypes.types_map['.aif']:
            # .aif converted with avconv doesn't have metadata.
            sCmdA = sData1
            s1 = ''.join(['"',
                  sFFcommand,
                  '" -i "',
                  sTMP1,
                  '" ',
                  sCmdA,
                  ' -y "',
                  sOUT1,
                  '"'])
            myossystem(s1)
        elif sOUT1EXT in ['.flac']:
            # flac - free lossless audio codec.
            if 'nt' in os.name.lower():
                # The programs is supplied in a zip file.  To use it,
                # extract it to the directory shown.
                # C:/opt/flac.exe
                # See: http://flac.sourceforge.net/
                s0 = getWinFullPath('/opt/flac.exe')
                s1 = ''.join([s0,
                      ' -f -o "',
                      sOUT1,
                      '" "',
                      sTMP1,
                      '"'])
                myossystem(s1)
            else:
                sCmdA = sData1
                s1 = ''.join(['"',
                      sFFcommand,
                      '" -i "',
                      sTMP1,
                      '" ',
                      sCmdA,
                      ' -y "',
                      sOUT1,
                      '"'])
                myossystem(s1)
        elif sOUT1EXT in ['.webm']:
            # Chrome, Firefox (Linux) and totem can open webm directly.
            sCmdA = sData1
            s1 = ''.join(['"',
                  sFFcommand,
                  '" -i "',
                  sTMP1,
                  '" -f image2 -i "',
                  sIMG1,
                  '" -s "',
                  sDIM,
                  '" -t "',
                  sTIME,
                  '" -vcodec libvpx -g 120 -lag-in-frames 16',
                  ' -deadline good -cpu-used 0 -vprofile 0',
                  ' -qmax 63 -qmin 0 -b:v 768k -acodec libvorbis',
                  ' -ab 112k -ar 44100 -f webm',
                  ' -auto-alt-ref 0 ',
                  sCmdA,
                  ' -y "',
                  sOUT1,
                  '"'])
            myossystem(s1)
        else:
            sOUT1 = sTMP1
        print(sOUT1EXT)
        print(u'-------------------')
        print(u' ')
        print(fsAppName() + ' Wav2Media')
        print(u'=================== ')
        print(u' ')
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
                v1 = ['.avi','.flv','.webm','.m4v','.mov','.mpg','.mp4','.wmv']
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
    s1 = " "

    try:
        s1 = sIN
        s1 = s1.replace('\n', u' ')
        s1 = s1.replace('\f', u'')
        s1 = s1.replace('\r', u'')
        s1 = s1.replace('\t', u' ')
        if bBeautifyQuotes:
            s1 = s1.replace(" '", u" ‘")  # &lsquo;
            s1 = s1.replace("'", u"’")  # &rsquo;
            s1 = s1.replace(' "', u' “')  # &ldquo;
            s1 = s1.replace('"', u"”")  # &rdquo;
        s1 = s1.replace('"', u' ')
    except(UnicodeDecodeError):
        print(s1 + ' error in readtexttools.cleanstr')
    return s1


def cleanstrforXml(sA):
    s1 = sA
    s1 = s1.replace("&", "&#38;")
    s1 = s1.replace(">", "&#62;")
    s1 = s1.replace("<", "&#60;")
    return s1


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


def WriteAnUTF8TextFile(sPath, sText):
    '''
    Create a simple 'utf-8' plain text file.
    `WriteAnUTF8TextFile("/path/file.txt", "Hello world")`
    '''
    sCodeco = 'utf-8'
    try:
        if os.path.isfile(sPath):
            os.remove(sPath)
        
        f2 = codecs.open(sPath, mode='w', encoding=sCodeco, errors='replace')
        f2.write(sText)
        f2.close
    except:
        print('`WriteAnUTF8TextFile` error in readtexttools.py')
    return os.path.isfile(sPath)


def writeXspfPlayList(sA, sART, sIMG):
    '''
    Write a [XSPF.ORG](http://xspf.org/) playlist.  Let a media player 
    read metadata information for a sound file that has no metadata.
    Optimized for [VLC media player](https://videolan.org).
    '''

    iXSPF = 11
    sFile = sA + '.xspf'
    sURI = sA
    sIMGURI = sIMG
    # Look in system icons to generate a URI if available. 
    sIMGERRLOC = ('/usr/share/icons/HighContrast/scalable/' +
                  'mimetypes/audio-x-generic.svg')
    sPLAYLOC = ('/usr/share/icons/HighContrast/scalable/' +
                'places-extra/playlist.svg')
    sBALLOONLOC = ('/usr/share/icons/HighContrast/scalable/' +
                   'apps-extra/pidgin.svg')


    if os.path.isfile(sIMGERRLOC):
        sIMGERR = path2url(sIMGERRLOC)
    elif os.path.isfile(sPLAYLOC):
        sIMGERR = path2url(sPLAYLOC)
    elif os.path.isfile(sBALLOONLOC):
        sIMGERR = path2url(sBALLOONLOC)
    else:
        sIMGERR = ''

    if os.path.isfile(sA + '.wav'):
        # Temporary file `/path/name.ogg.wav`
        sURI = path2url(sA)
    elif os.path.isfile(sA):
        sURI = path2url(sA)
    else:
        sFile = getMyLock('lock.xspf')

    if urllib.pathname2url(sIMG) == '':
        # This should **not** normally happen - choose a default graphic!
        sIMGURI = sIMGERR
    elif os.path.isfile(sIMG):
        # Offline URI - Convert local file name
        if sIMG[:7] == 'file://':
            sIMGURI = sIMG
        else:
            sIMGURI = path2url(sIMG)
    elif sIMG[:4] == 'http':
        sIMGURI = sIMG
    else:
        sIMGURI = sIMGERR
    s1 = GetAMetaDataStr(iXSPF, sART)
    s1 = s1.replace('[%%LOCATION%%]', sURI, 1)
    s1 = s1.replace('[%%IMAGE%%]', sIMGURI, 1)
    
    WriteAnUTF8TextFile(sFile, s1)
    if os.path.isfile(sFile):
        return sFile
    else:
        return sA


def LockMyLock():
    '''
    Create a file that informs the world that the application.
    is at work.
    '''
    s1 = getMyLock('lock')
    WriteAnUTF8TextFile(s1, fsAppSignature())


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
    Returns path to a temporary directory plus a lock file name.
    Use an value like 'lock' for sLOCK.  You can use more than
    one lock if you use different values for sLOCK.
    '''
    s1 = '.' + sLOCK
    s2 = fsAppSignature()
    s3 = ''
    s4 = os.getenv('READTEXTTEMP')

    if s4 is not None and os.path.isdir(s4) and os.access(s4, os.W_OK):
        if 'nt' in os.name.lower():
            s3 = os.path.join(s4,
                              s2 + u'.' + os.getenv('USERNAME') + s1)
        elif os.path.isfile('/usr/bin/osascript'):
            s3 = os.path.join(s4,
                              s2 + u'.' + os.getenv('USERNAME') + s1)
        else:
            s3 = os.path.join(s4,
                              s2 + u'.' + os.getenv('USER') + s1)
    elif 'nt' in os.name.lower():
        s3 = os.path.join(os.getenv('TMP'),
                          s2 + u'.' + os.getenv('USERNAME') + s1)
    elif os.path.isfile('/usr/bin/osascript'):
        s3 = os.path.join(os.getenv('TMPDIR'),
                          s2 + u'.' + os.getenv('USERNAME') + s1)
    else:
        if os.path.isdir('/tmp') and os.access('/tmp', os.W_OK):
            s3 = os.path.join('/tmp',
                              s2 + u'.' + os.getenv('USER') + s1)
        elif os.path.isdir(
            os.path.join(
                os.getenv(
                    'HOME'), '.config/')) and os.access(
                        os.path.join(
                            os.getenv(
                                'HOME'), '.config/'), os.W_OK):
            s3 = os.path.join(os.getenv('HOME'),
                              '.config/' + s2 + u'.' + os.getenv('USER') + s1)
        else:
            s3 = os.path.join(os.getenv('HOME'),
                              s2 + u'.' + os.getenv('USER') + s1)
    return s3


def getMyUserName():
    '''
    Returns the user name.  Optionally, you can provide a
    temporary lock.id file for this function to read the
    artist or author name from and then remove.
    '''
    sOUT1 = ""

    if 'nt' in os.name.lower():
        sOUT1 = os.getenv('USERNAME')
    elif os.path.isfile('/usr/bin/osascript'):
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
    if 'nt' in os.name.lower():
        sOUT1 = os.path.join(os.getenv('TMP'), os.getenv('USERNAME'))
    elif os.path.isfile('/usr/bin/osascript'):
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
    if 'nt' in os.name.lower():
        return sCommand
    else:
        return ''


def ShowWithApp(sOUT1):
    '''
    Same as double clicking the document - opens in default
    application.
    '''
    if os.path.isfile('/usr/bin/osascript'):
        # MacOS
        s1 = u'open "' + sOUT1 + u'" '
        myossystem(s1)
    elif 'nt' in os.name.lower():
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


def path2url(s1):
    '''Convert a file path to a file URL'''
    try:
        return urlparse.urljoin('file:',
                                urllib.pathname2url(s1))
    except NameError:
        # Fall back works on Posix
        return ''.join(['file://', s1.replace(' ', '%20')])


def PlayWaveInBackground(sOUT1):
    '''
    Opens using command line shell.
    '''
    if os.path.isfile('/usr/bin/osascript'):
        # MacOS
        s1 = u'afplay "' + sOUT1 + u'" '
        myossystem(s1)
    elif 'nt' in os.name.lower():
        # Windows
        try:
            import winsound
            winsound.PlaySound(sOUT1, 
                               winsound.SND_FILENAME
                               | 
                               winsound.SND_NOWAIT)
        except:
            os.startfile(sOUT1)
    else:
        if os.path.isfile('/usr/bin/aplay'):
            s1 = u'aplay "' + sOUT1 + u'" '
        elif os.path.isfile('/usr/bin/esdplay'):
            s1 = u'esdplay "' + sOUT1 + u'" '
        elif os.path.isfile('/usr/bin/paplay'):
            s1 = u'paplay "' + sOUT1 + u'" '
        elif os.path.isfile('/usr/bin/ossplay'):
            s1 = u'ossplay "' + sOUT1 + u'" '
        elif os.path.isfile('/usr/bin/artsplay'):
            s1 = u'artsplay "' + sOUT1 + u'" '
        elif os.path.isfile('/usr/bin/roarcatplay'):
            s1 = u'roarcatplay "' + sOUT1 + u'" '
        elif os.path.isfile('/usr/bin/roarcat'):
            s1 = u'roarcat "' + sOUT1 + u'" '
        elif os.path.isfile('/usr/bin/gst-launch-1.0'):
            s1 = (u'gst-launch-1.0 filesrc location="' +
                   path2url(sOUT1) + 
                   '" ! wavparse ! audioconvert ! audioresample ! osssink')
        elif os.path.isfile('/usr/bin/gst-launch-0.10'):
            s1 = (u'gst-launch-0.10 playbin uri="' +
                   path2url(sOUT1) + u'"')
        myossystem(s1)


def myossystem(s1):
    '''
    This is equivalent to os.system(s1)
    Replaced os.system(s1) to avoid Windows path errors.
    '''
    s1 = s1.encode('utf-8')
    if 'nt' in os.name.lower():
        try:
            retcode = subprocess.call(s1, shell=False)
            if retcode < 0:
                print('Process was terminated by signal')
            else:
                print('Process returned')
        except (NameError, OSError, e):
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

