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

Fedora
------

Users may experience a delay producing spoken text when reading long strings
using some high quality voices. [Flite][1] is a fast, compact alternative.

High quality [scriptable][2] English or other supported language

    sudo dnf upgrade
    sudo dnf install festival

Small footprint English

    sudo dnf upgrade
    sudo dnf install flite

Ubuntu
-------

High quality scriptable English

    sudo apt install festival festvox-us-slt-hts

Small footprint English

    sudo apt install festival

Other supported languages and voices

    sudo apt install festival <name_of_voice_package>

Read Selection... Dialog setup:
-------------------------------

External program:

    /usr/bin/python3  

Command line options (default):

    "(FESTIVAL_READ_TEXT_PY)" "(TMP)"

or (save as a .wav file in the home directory):

    "(FESTIVAL_READ_TEXT_PY)" --output "(HOME)(NOW).wav" "(TMP)"

or (speak more slowly with a lowered pitch):

    "(FESTIVAL_READ_TEXT_PY)" --rate=75% --pitch=75% "(TMP)"

Festival can use [Sable][1] XML code to change speech rate and pitch, but
not all voices support Sable markup.  For unsupported voices, the rate and
pitch command line arguments do not change the sound rate and pitch.

See the info pages for `festival` for more information.

[Read Text Extension][3]

Copyright (c) 2011 - 2022 James Holgate

  [1]: http://cmuflite.org
  [2]: https://www.cs.cmu.edu/~awb/festival_demos/sable.html
  [3]: http://sites.google.com/site/readtextextension/

'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import codecs
import getopt
import os
import sys
import readtexttools


def usage():
    '''
    Command line help
    '''
    _imported_meta = readtexttools.ImportedMetaData()
    _version = ''
    _app = 'festival or flite'
    try:
        _version = _imported_meta.execute_command('festival --version')
        _app = 'text2wave'
    except Exception:
        pass
    if not bool(_version):
        if readtexttools.have_posix_app('flite', False):
            _version = '''Carnegie Mellon University, Copyright (c) 1999-2016, all rights reserved
version: flite-2.1-release Dec 2017 (http://cmuflite.org)'''
            _app = 'flite - a small simple speech synthesizer'
    print('''
Festival Read Text
==================

%(_version)s

Reads a text file using %(_app)s.

Converts format with `avconv`, `lame`, `faac` or `ffmpeg`.

Usage
-----

     festival_read_text_file.py "input.txt"
     festival_read_text_file.py --eval "kal_diphone" "input.txt"
     festival_read_text_file.py --visible "false" "input.txt"
     festival_read_text_file.py --output "output.wav" "input.txt"
     festival_read_text_file.py --output "output.[flac|mp2|mp3|ogg|opus]" "input.txt"
     festival_read_text_file.py --output "output.webm" \\ 
       --image "input.[png|jpg] "input.txt"
     festival_read_text_file.py --audible "false" --output "output.wav" \\ 
       "input.txt"
''' % locals())


def festival_read(_file_path='',
                  _visible='false',
                  _audible='false',
                  _wave='',
                  _image='',
                  _content='',
                  _eval_token='',
                  _title='',
                  _writer='',
                  _image_size=''):  # -> bool
    '''
Creates a temporary speech-synthesis sound file and optionally
reads the file aloud.

+ `_file_path` - Text File to speak
+ `_visible`- Use a graphic media player, or False for invisible player
+ `_wave` - Name of desired output file
+ `_audible` - If false, then don't play the sound file
+ `_image` - a .png or .jpg file if required.
+ `_content` - text
+ `_eval_token` - Linux text2wave command prefix, like `(voice_upc_ca_ona_hts)`
+ `_title` - title
+ `_writer` - artist or author
+ `_image_size` - Dimensions to scale photo '600x600'
    '''
    if not os.path.isfile(_file_path):
        return False
    # Determine the output file name
    _out_file = readtexttools.get_work_file_path(_wave, _image, "OUT")
    # Determine the temporary file name
    _work_file = readtexttools.get_work_file_path(_wave, _image, "TEMP")

    # Delete old versions
    if os.path.isfile(_work_file):
        os.remove(_work_file)
    if os.path.isfile(_out_file):
        os.remove(_out_file)
    if not bool(_content):
        # Empty string - nothing to read.
        return True
    if 'nt' in os.name.lower():
        _app = readtexttools.get_nt_path('festival/festival.exe')
        if not bool(_app):
            return False
        if readtexttools.get_nt_path('festival/text2wave'):
            _script = readtexttools.get_nt_path('festival/text2wave')
            _command = '''%(_app)s --script %(_script)s "%(file_path)s" -o "%(_work_file)s"''' %locals()
        else:
            # With Windows, this script only supports reading text aloud.
            _command = '%(_app)s --tts  "%(_file_path)s"' %locals()
    else:
        if readtexttools.have_posix_app('text2wave', False):
            _app = 'text2wave'
            # text2wave is an executable festival script
            if len(_eval_token) == 0:
                _switch = ''
            else:
                _switch = ' -eval "%(_eval_token)s"' %locals()
            _command = '%(_app)s%(_switch)s "%(_file_path)s" -o "%(_work_file)s"' %locals()
        elif readtexttools.have_posix_app('flite', False):
            # Flite reates a compact .wav file - Signed 16 bit Little Endian,
            # Rate 8000 Hz, Mono. This format works with vlc, aplay & paplay,
            # but might not with a gstreamer app like totem or gst-launch-1.0
            if os.path.splitext(_file_path)[1] not in ['.txt']:
                return False
            _command = 'flite -f "%(_file_path)s" -o "%(_work_file)s"' %locals()
    try:
        readtexttools.my_os_system(_command)
    except IOError as err:
        print('I was unable to read!')
        usage()
        sys.exit(2)
    if os.path.isfile(_work_file):
        readtexttools.process_wav_media(_title, _work_file, _image,
                                            _out_file, _audible, _visible,
                                            _writer, _image_size)
        return True
    return False



def festival_speaker_name(sA=''):  # -> str
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
        return sA.replace('(voice_', '').replace(')', '')
    return retVal


def festival_rate(sA='100%'):
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
    except (TypeError):
        print('I was unable to determine festival rate!')
    if i2 <= iMinVal:
        retVal = iMinVal
    elif i2 >= iMaxVal:
        retVal = iMaxVal
    else:
        retVal = i2
    myStr = str(retVal) + '%'
    return myStr


def festival_pitch(sA='100%'):
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
    except (TypeError):
        print('I was unable to determine festival pitch!')
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
    _xml_tool = readtexttools.XmlTransform()
    _sable = ''
    _wave = ''
    _visible = ''
    _audible = ''
    _sable_speaker = ''
    _sable_rate = '0%'
    _sable_pitch = '0%'
    _rate = '100%'
    _pitch = '100%'
    _image = ''
    _eval_token = ''
    _title = ''
    _writer = ''
    _image_size = '600x600'
    concise_lang = os.getenv('LANG')
    if not concise_lang:
        concise_lang = os.getenv('LANGUAGE')
    if not concise_lang:
        # Use utf-8; don't correct Mojibaki
        concise_lang = 'ja-JP'

    _file_path = sys.argv[-1]
    if not os.path.isfile(_file_path):
        print('I was unable to find the file you specified!...')
        sys.exit(0)
    elif (sys.argv[-1] == sys.argv[0]):
        usage()
        sys.exit(0)
    elif not readtexttools.have_posix_app(
        'text2wave', False) and not readtexttools.have_posix_app(
            'flite', False) and not bool(
                readtexttools.get_nt_path('festival/festival.exe')):
        usage()
        sys.exit(0)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hovarpietnd', [
            'help', 'output=', 'visible=', 'audible=', 'rate=', 'pitch=',
            'image=', 'eval=', 'title=', 'artist=', 'dimensions='
        ])
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
            _wave = a
        elif o in ('-v', '--visible'):
            _visible = a
        elif o in ('-a', '--audible'):
            _audible = a
        elif o in ('-r', '--rate'):
            _rate = a
            _sable_rate = festival_rate(_rate)
        elif o in ('-p', '--pitch'):
            _pitch = a
            _sable_pitch = festival_pitch(_pitch)
        elif o in ('-i', '--image'):
            _image = a
        elif o in ('-e', '--eval'):
            _eval_token = a
            _sable_speaker = festival_speaker_name(_eval_token)
        elif o in ('-t', '--title'):
            _title = a
        elif o in ('-n', '--artist'):
            _writer = a
        elif o in ('-d', '--dimensions'):
            _image_size = a
        else:
            assert False, 'unhandled option'
    try:
        # https://docs.python.org/3/library/codecs.html#standard-encodings
        #
        #
        # Festival voices use Sable markup instead of w3 SMIL
        #
        _file_handle = codecs.open(_file_path, mode='r', encoding='utf-8')
    except (IOError):
        print('I was unable to open the file you specified!!!')
        usage()
    else:
        _content = _file_handle.read()
        _file_handle.close()
        if len(_content) == 0:
            sys.exit(0)
        _content = readtexttools.strip_xml(_content)
        if len(_content) == 0:
            sys.exit(0)

        _content = readtexttools.strip_mojibake(concise_lang, _content)
        if (not bool(_sable_rate) and not bool(_sable_pitch) and
                not bool(_sable_speaker)):
            # Pass plain text
            _content = readtexttools.clean_str(_content, False)
            _file_content = _content
        else:
            # Prepare Sable XML (To SLOW DOWN speech use --RATE=75%)
            _content = _xml_tool.clean_for_xml(_content)
            _file_content = ''.join([
                '<SABLE>\n', '<SPEAKER NAME="', _sable_speaker + '">\n',
                '<RATE SPEED="', _sable_rate + '">\n', '<PITCH BASE="',
                _sable_pitch, '">\n', _content, '\n</PITCH>',
                '\n</SPEAKER>', '\n</SABLE>'
            ])
            # os.remove(_file_path)
            _sable = _file_path + ".sable"
            _file_handle2 = codecs.open(_sable, mode='w', encoding='utf-8')
            _file_handle2.write(_file_content)
            _file_handle2.close()
            _writer = readtexttools.check_artist(_writer)
            _title = readtexttools.check_title(_title, 'festival')

            if not festival_read(_sable, _visible, _audible, _wave, _image,
                                 _content, _eval_token, _title, _writer,
                                 _image_size):
                festival_read(_file_path, _visible, _audible, _wave, _image,
                              _content, "", _title, _writer, _image_size)


if __name__ == '__main__':
    main()
