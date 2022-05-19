#!/usr/bin/env python
# -*- coding: UTF-8-*-
'''
The Japanese TTS system "Open JTalk"
===================================

Reads an utf-8 text file using `open_jtalk` and a media player. 

The Open JTalk engine is a software speech synthesizer for Japanese.

Install `open_jtalk` using the following packages:

        open-jtalk
        libhtsengine1
        hts-voice-nitech-jp-atr503-m001
        open-jtalk-mecab-naist-
        
If you are creating the Open JTalk engine parts from source, you
must enable the `./configure --with-charset=UTF-8` property.

Read Selection... Dialog setup:
-------------------------------

External program:

        /usr/bin/python3

Command line options (default):

        "(OPENJTALK_READ_TEXT_PY)" "(TMP)"

or (save as a .wav file in the home directory):

         "(OPENJTALK_READ_TEXT_PY)" \
           --output "(HOME)(NOW).wav" "(TMP)"

See the manual page for `open_jtalk` for more detailed information

[Read Text Extension](http://sites.google.com/site/readtextextension/)

Mojibake?
---------

The Japanese source text might be coded as `shift_jis`:

[`shift_jis` to `utf_8`](https://gist.github.com/dogancelik/2777851)

Copyright (c) 2022 James Holgate

'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import getopt
import os
import sys
import readtexttools


def usage():
    '''
    Command line help
    '''
    print('''Open Jtalk Read Text
==============

Reads a utf-8 text file in Japanese using open-jtalk and a media player.

Converts format with `avconv`, `lame`, `faac` or `ffmpeg`.

Usage
-----

     openjtalk_read_text_file.py "input.txt"
     openjtalk_read_text_file.py --visible "false" "input.txt"
     openjtalk_read_text_file.py --output "output.wav" "input.txt"
     openjtalk_read_text_file.py --output "output.[m4a|mp2|mp3|ogg]" "input.txt"
     openjtalk_read_text_file.py --output "output.[avi|webm]"
       --image "input.[png|jpg] "input.txt"
     openjtalk_read_text_file.py --audible "false" --output "output.wav"
       "input.txt" ''')


def openjtalk_read(_in_text='',
                   _language='ja-JP',
                   _visible='false',
                   _audible='true',
                   _media_file='',
                   _image='',
                   _title='',
                   _artist='',
                   _dimensions='600x600'):
    '''
    _in_text file path containing the text to speak. The file must be written as utf-8.
    _language - Supported two or four letter language code
    _visible- Use a graphic media player, or False for invisible player
    _media_file - Name of desired output media file
    _audible - If false, then don't play the sound file
    _image - a .png or .jpg file if required.
    _title - Commentary or title for post processing
    _artist - Artist or Author
    _dimensions - Dimensions to scale photo '600x600'
    '''
    _out_file = ''
    if len(_language) == 0:
        _language = 'ja'
    elif _language[:2].lower() != 'ja':
        return False
    _app = 'open_jtalk'
    all_pass = '0.55'
    application = '/usr/bin/open_jtalk'
    dictionary = '/var/lib/mecab/dic/open-jtalk/naist-jdic'
    hts_voice = '/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice'
    rate = '1.0'  # 0 - 1
    sample_period = '240'
    sample = '48000'
    for resource in [application, dictionary, hts_voice, _in_text]:
        if not (os.path.isfile(resource) or os.path.isdir(resource)):
            return False
    # Determine the output file name
    _out_file = readtexttools.get_work_file_path(_media_file, _image, 'OUT')
    # Determine the temporary file name
    _work_file = readtexttools.get_work_file_path(_media_file, _image, 'TEMP')
    # Delete old versions
    if os.path.isfile(_work_file):
        os.remove(_work_file)
    if os.path.isfile(_out_file):
        os.remove(_out_file)
    try:
        _os_command = '"%(application)s" -s %(sample)s -p %(sample_period)s -a %(all_pass)s -m "%(hts_voice)s" -r %(rate)s -ow "%(_work_file)s" -x "%(dictionary)s" "%(_in_text)s"' % locals(
        )
        if readtexttools.my_os_system(_os_command):
            if len(_out_file) != 0:
                readtexttools.unlock_my_lock()
            if os.path.getsize(_work_file) == 0:
                return False
            if readtexttools.process_wav_media(_title, _work_file, _image,
                                               _out_file, _audible, _visible,
                                               _artist, _dimensions):
                return True
    except IOError:
        print('I was unable to read!')
        usage()
    return False


def main():
    '''OpenJtalk read text tools'''
    _language = 'ja-JP'
    _output = ''
    _visible = 'False'
    _audible = 'True'
    _image = ''
    _title = ''
    _artist = ''
    _dimensions = '600x600'
    _xml_transform = readtexttools.XmlTransform()
    _file_path = sys.argv[-1]
    if os.path.isfile(_file_path):
        if sys.argv[-1] == sys.argv[0]:
            usage()
            sys.exit(0)
        elif not os.path.isfile('/usr/bin/open_jtalk'):
            print('Please install open-jtalk.')
            usage()
            sys.exit(0)
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hovalitnd', [
                'help', 'output=', 'visible=', 'audible=', 'language=',
                'image=', 'title=', 'artist=', 'dimensions='
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
                _output = a
            elif o in ('-v', '--visible'):
                _visible = a
            elif o in ('-a', '--audible'):
                _audible = a
            elif o in ('-l', '--language'):
                _language = a
            elif o in ('-i', '--image'):
                _image = a
            elif o in ('-t', '--title'):
                _title = a
            elif o in ('-n', '--artist'):
                _artist = a
            elif o in ('-d', '--dimensions'):
                _dimensions = a
            else:
                assert False, 'unhandled option'

        _artist_ok = readtexttools.check_artist(_artist)
        _title_ok = readtexttools.check_title(_title, "open_jtalk")
        openjtalk_read(_file_path, _language, _visible, _audible, _output,
                       _image, _title_ok, _artist_ok, _dimensions)
    else:
        print('I was unable to find the file you specified!')
    sys.exit(0)


if __name__ == "__main__":
    main()
