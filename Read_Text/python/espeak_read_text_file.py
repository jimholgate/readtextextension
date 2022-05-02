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

Copyright (c) 2011 - 2022 James Holgate

'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
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
    print('''
Espeak Read Text
===============

Reads a text file using espeak and a media player.

Converts format with `avconv`, `lame`, `faac` or `ffmpeg`.

Usage
-----

     espeak_read_text_file.py "input.txt"
     espeak_read_text_file.py --language [de|en-US|en|es|fr|it...] "input.txt"
     espeak_read_text_file.py --visible="false" "input.txt"
     espeak_read_text_file.py --rate=100% --pitch=100% "input.txt"
     espeak_read_text_file.py --output="output.wav" "input.txt"
     espeak_read_text_file.py --output="output.[flac|mp2|mp3|ogg|opus]" "input.txt"
     espeak_read_text_file.py --output="output.webm" \\ 
       --image="input.[png|jpg] "input.txt"
     espeak_read_text_file.py --audible="false" --output="output.wav" \\ 
       "input.txt"
''')


def espkread(_text_path, _lang, _visible, _audible, sTMP0, _image, _title,
             _post_process, _author, _dimensions, _ipitch, _irate):
    '''
Creates a temporary speech-synthesis sound file and optionally
reads the file aloud.

+ `_text_path` - Name of text file to speak
+ `_lang` - Supported two or four letter language code - defaults to US English
+ `_visible` - Use a graphic media player, or False for invisible player
+ `sTMP0` - Name of desired output media file
+ `_audible` - If false, then don't play the sound file
+ `_image` - a .png or .jpg file if required.
+ `_title` - Commentary or title for post processing
+ `_post_process` - Get information, play file, or convert a file
+ `_author` - Artist or Author
+ `_dimensions` - Dimensions to scale photo '600x600'
+ `_ipitch` - pitch value from 5 to 100, default 50
+ `_irate` - rate value from 20 to 640, default 160
    '''
    _imported_meta = readtexttools.ImportedMetaData()
    _out_file = ''
    _pitch = str(_ipitch)
    _rate = str(_irate)
    _rate = '100'
    if _lang[:2].lower() in ['de']:
        s = 'de'
    elif _lang[:2].lower() in ['en']:
        if _lang[-2:].upper() in [
                'AU', 'BD', 'BS', 'CA', 'GB', 'GH', 'HK', 'IE', 'IN', 'JM',
                'NZ', 'PK', 'SA', 'TT'
        ]:
            s = 'en'
        else:
            s = 'en-us'
    elif _lang[:2].lower() in ['es']:
        if _lang[-2:].upper() in ['ES']:
            s = 'es'
        elif _lang[-2:].upper() in ['MX']:
            s = 'es-mx'
        else:
            s = 'es-la'
    elif _lang[:2].lower() in ['nb']:
        # *Office uses language code for Norwegian Bokmal - nb
        #  NO is the country code for Norway, not an official language code.
        s = 'no'
    elif _lang[:2].lower() in ['pt']:
        if _lang[-2:].upper() in ['PT']:
            s = 'pt-pt'
        else:
            s = 'pt'
    elif _lang[:2].lower() in ['zh']:
        if _lang[-2:].upper() in ['HK', 'MO']:
            # Yue is official language in Hong Kong & Macau
            s = 'zh-yue'
        else:
            s = 'zh'
    elif _lang[:2].lower() in [
            'af', 'bs', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'eo', 'fi', 'fr',
            'hi', 'hr', 'hu', 'hy', 'id', 'is', 'it', 'ku', 'la', 'lv', 'mk',
            'nl', 'pl', 'ro', 'ru', 'sk', 'sq', 'sr', 'sv', 'sw', 'ta', 'tr',
            'vi'
    ]:
        s = _lang[:2].lower()
    else:
        s = 'en'
    _voice = s  # standard espeak voice
    if _post_process == 'process_wav_media':
        # Check if an mbrola voice is available for the language, otherwise use
        # the default espeak voice.  If there are several compatible mbrola
        # voices, this python script will choose the first one - for example:
        # de2 instead of de7.
        #
        # Dictionary : `a2` is the locally installed language abbreviation;
        # `a1` is the equivalent ISO 639-1 standard for languages, except in
        # the cases of pt-PT and en-US, which include a regional ISO code.
        a0 = [{
            'a2': 'af1',
            'a1': 'af'
        }, {
            'a2': 'br1',
            'a1': 'pt'
        }, {
            'a2': 'br3',
            'a1': 'pt'
        }, {
            'a2': 'br4',
            'a1': 'pt'
        }, {
            'a2': 'cr1',
            'a1': 'hr'
        }, {
            'a2': 'cz2',
            'a1': 'cs'
        }, {
            'a2': 'de2',
            'a1': 'de'
        }, {
            'a2': 'de4',
            'a1': 'de'
        }, {
            'a2': 'de5',
            'a1': 'de'
        }, {
            'a2': 'de6',
            'a1': 'de'
        }, {
            'a2': 'de7',
            'a1': 'de'
        }, {
            'a2': 'en1',
            'a1': 'en'
        }, {
            'a2': 'es1',
            'a1': 'es'
        }, {
            'a2': 'es2',
            'a1': 'es'
        }, {
            'a2': 'fr1',
            'a1': 'fr'
        }, {
            'a2': 'fr4',
            'a1': 'fr'
        }, {
            'a2': 'gr2',
            'a1': 'el'
        }, {
            'a2': 'hu1',
            'a1': 'hu'
        }, {
            'a2': 'id1',
            'a1': 'id'
        }, {
            'a2': 'it3',
            'a1': 'it'
        }, {
            'a2': 'it4',
            'a1': 'it'
        }, {
            'a2': 'la2',
            'a1': 'la'
        }, {
            'a2': 'nl2',
            'a1': 'nl'
        }, {
            'a2': 'pl1',
            'a1': 'pl'
        }, {
            'a2': 'pt1',
            'a1': 'pt-pt'
        }, {
            'a2': 'ro1',
            'a1': 'ro'
        }, {
            'a2': 'sw1',
            'a1': 'sv'
        }, {
            'a2': 'sw2',
            'a1': 'sv'
        }, {
            'a2': 'tr1',
            'a1': 'tr'
        }, {
            'a2': 'tr2',
            'a1': 'tr'
        }, {
            'a2': 'us1',
            'a1': 'en-us'
        }, {
            'a2': 'us2',
            'a1': 'en-us'
        }, {
            'a2': 'us3',
            'a1': 'en-us'
        }, {
            'a2': 'en1',
            'a1': 'en-us'
        }]

        for i in range(len(a0)):
            # Identify an mbrola voice if it is installed

            if a0[i]['a1'] == s:
                if 'nt' in os.name.lower():
                    if os.path.isfile(
                            os.path.join(os.getenv('ProgramFiles'),
                                         'eSpeak/espeak-data/mbrola',
                                         a0[i]['a2'])):
                        _voice = 'mb-' + a0[i]['a2']
                        break
                    elif os.getenv('ProgramFiles(x86)'):
                        sPFX86 = os.getenv('ProgramFiles(x86)')
                        sEEDM = 'eSpeak/espeak-data/mbrola'
                        if (os.path.isfile(
                                os.path.join(sPFX86, sEEDM, a0[i]['a2']))):
                            _voice = 'mb-' + a0[i]['a2']
                            break
                else:
                    print(os.path.join('/usr/share/mbrola/voices', a0[i]['a2']))
                    if os.path.isfile(
                            os.path.join('/usr/share/mbrola/voices',
                                         a0[i]['a2'])):
                        _voice = 'mb-' + a0[i]['a2']
                        break
                    elif os.path.isfile(
                            os.path.join('/usr/share/mbrola/', a0[i]['a2'],
                                         a0[i]['a2'])):
                        _voice = 'mb-' + a0[i]['a2']
                        break
    # Determine the output file name
    _out_file = readtexttools.get_work_file_path(sTMP0, _image, 'OUT')
    # Determine the temporary file name
    _work_file = readtexttools.get_work_file_path(sTMP0, _image, 'TEMP')

    # Remove old files.
    if os.path.isfile(_work_file):
        os.remove(_work_file)
    if os.path.isfile(_out_file):
        os.remove(_out_file)
    try:
        if bool(readtexttools.gst_plugin_path('libgstespeak')):
            print(readtexttools.gst_plugin_path('libgstespeak'))
        # espeak must be in your system's path
        # for example: /usr/bin/ or /usr/local/bin/
        _app = ''

        for app_name in ['espeak-ng', 'speak-ng', 'espeak']:
            if readtexttools.have_posix_app(app_name, False):
                _app = app_name
                break
        sSub = 'eSpeak/command_line/espeak.exe'
        if 'nt' in os.name.lower():
            _app = readtexttools.get_nt_path(sSub)
        if bool(_app):
            _command = ''.join([
                '"', _app, '" -b 1 -p ', _pitch, ' -s ', _rate, ' -v ', _voice,
                ' -w "', _work_file, '" -f "', _text_path, '"'
            ])
        elif bool(readtexttools.gst_plugin_path('libgstespeak')):
            if not readtexttools.have_posix_app('gst-launch-1.0'):
                return False
            elif os.path.isfile(readtexttools.get_my_lock('lock')):
                # User requested play, but action is locked
                return False
            elif bool(
                    _imported_meta.execute_command(
                        'ps -a | grep gst-launch-1.0')):
                # Program is currently running;
                return False
            # Fall back - no application found, so use gst-launch to synthesise
            # text from the text file.
            _app = 'gst-launch-1.0'
            _content = _imported_meta.meta_from_file(_text_path)
            _content = _imported_meta.escape_gst_pipe_meta(_content)
            _command = '%(_app)s espeak text="%(_content)s" voice=%(_voice)s ! autoaudiosink' % locals(
            )
            _post_process = None
        if not bool(_app):
            return False
        readtexttools.my_os_system(_command)
        if not bool(_post_process):
            readtexttools.unlock_my_lock()
        elif _post_process == "process_wav_media":
            return bool(
                readtexttools.process_wav_media(_title, _work_file, _image,
                                                _out_file, _audible, _visible,
                                                _author, _dimensions))
        elif _post_process == "show_sound_length_seconds":
            print("show_sound_length_seconds")
            print(readtexttools.sound_length_seconds(_work_file))
            print("-----------------------------------------------------")
            return True
    except (IOError):
        print('I was unable to use espeak and read text tools!')
        usage()
        return False


def _espeak_rate(sA):
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
    except (TypeError):
        print('I was unable to determine espeak rate!')
    if i2 <= iMinVal:
        retVal = iMinVal
    elif i2 >= iMaxVal:
        retVal = iMaxVal
    else:
        retVal = i2
    return retVal


def _espeak_pitch(sA):
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
        print('I was unable to determine espeak pitch!')
    if i2 <= iMinVal:
        retVal = iMinVal
    elif i2 >= iMaxVal:
        retVal = iMaxVal
    else:
        retVal = i2
    return retVal


def main():
    '''Use espeak or espeak-ng'''
    _xml_tool = readtexttools.XmlTransform()
    _ipitch = 50
    _irate = 160
    _lang = 'en-US'
    _wave = ''
    _visible = ''
    _audible = ''
    _content = ''
    _rate_percent = '100%'
    _pitch_percent = '100%'
    _image = ''
    _title = ''
    _author = ''
    _dimensions = '600x600'
    _text_path = sys.argv[-1]

    if os.path.isfile(_text_path):
        if sys.argv[-1] == sys.argv[0]:
            usage()
            sys.exit(0)
        elif not os.path.isfile('/usr/bin/espeak'):
            if not os.path.isfile('/usr/bin/espeak-ng'):
                print(
                    'Please install espeak.  Use `sudo apt-get install espeak-ng`'
                )
                usage()
                sys.exit(0)
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hovalrpitnd', [
                'help', 'output=', 'visible=', 'audible=', 'language=', 'rate=',
                'pitch=', 'image=', 'title=', 'artist=', 'dimensions='
            ])
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
                _wave = a
            elif o in ('-v', '--visible'):
                _visible = a
            elif o in ('-a', '--audible'):
                _audible = a
            elif o in ('-l', '--language'):
                _lang = a
            elif o in ('-r', '--rate'):
                _rate_percent = a
                _irate = _espeak_rate(_rate_percent)
            elif o in ('-p', '--pitch'):
                _pitch_percent = a
                _ipitch = _espeak_pitch(_pitch_percent)
            elif o in ('-i', '--image'):
                _image = a
            elif o in ('-t', '--title'):
                _title = a
            elif o in ('-n', '--artist'):
                _author = a
            elif o in ('-d', '--dimensions'):
                _dimensions = a
            else:
                assert False, 'unhandled option'
        try:
            oFILE = codecs.open(_text_path, mode='r', encoding='utf-8')
        except IOError:
            print('I was unable to open the file you specified!')
            usage()
        else:
            _author = readtexttools.check_artist(_author)
            _title = readtexttools.check_title(_title, 'espeak')
            _post_process = 'process_wav_media'
            espkread(_text_path, _lang, _visible, _audible, _wave, _image,
                     _title, _post_process, _author, _dimensions, _ipitch,
                     _irate)
    sys.exit(0)


if __name__ == '__main__':
    main()
