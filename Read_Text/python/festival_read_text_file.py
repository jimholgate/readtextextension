#!/usr/bin/env python
# -*- coding: UTF-8-*-
'''
Festival
========

Reads a text file using festival and a media player. Some voices let you
change the pitch and speed.

The festival engine is a software speech synthesizer.

Install festival using a package manager to install a festivox or festival
voice.  The package manager should automatically select the festival package
and the required support files.

Some platforms allow you to use festival with `speech-dispatcher` so that you
can use different speech platforms for different languages.

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


Debian and derivatives like Mint and Ubuntu
-------------------------------------------

High quality scriptable English

    sudo apt install festival festvox-us-slt-hts

Small footprint English

    sudo apt install festival

Other supported languages and voices

    sudo apt install festival <name_of_voice_package>
    
If you install rhvoice with apt-get or your normal package manager
then some voices installed in the festival directory might not be
compatible with festival. Using the `rhvoice-rest` docker image with
`network_read_text_file.py` avoids this problem.

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

Depending on the platform, version and the available voices, Festival
might be able to use [Sable][1] XML code to change speech rate and pitch.
Not all voices or platforms support Sable markup. In these cases, the
command line arguments might not change the voice, sound rate or pitch.

If festival stops working after you install a particular voice, try
uninstalling the voice and restarting your computer.

See the info pages for `festival` for more information.

See "Festival can not speak other voices than default english" (sic)
<https://bugs.launchpad.net/ubuntu/+source/festival/+bug/688940>

[Read Text Extension][3]

Copyright (c) 2011 - 2023 James Holgate

  [1]: http://cmuflite.org
  [2]: https://www.cs.cmu.edu/~awb/festival_demos/sable.html
  [3]: http://sites.google.com/site/readtextextension/

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
    _imported_meta = readtexttools.ImportedMetaData()
    _version = ''
    _app = 'festival or flite'
    try:
        _version = _imported_meta.execute_command('festival --version').strip()
        _app = 'text2wave'
    except Exception:
        pass
    if not bool(_version):
        if readtexttools.have_posix_app('flite', False):
            _version = '''Carnegie Mellon University, Copyright (c) 1999-2016,
all rights reserved
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


class ReadFestivalClass(object):
    '''Read long strings aloud with low latency.'''

    def __init__(self):
        self.player = ''
        if os.name == 'nt':
            self.player = readtexttools.get_nt_path('festival/festival.exe')
        elif readtexttools.have_posix_app('festival', False):
            self.player = 'festival'
        self.replacements = u'''?!\uFF1F\uFF01.,¡()[]¿…‥،;:—。，、：\n'''
        self._divider = u'\u2424'
        self.lock = readtexttools.get_my_lock('lock')
        self.script = readtexttools.get_my_lock("festival.scr")
        self.voice_eval = ''
        self.lang = ''
        try:
            self.punctuation = str.maketrans({
                u"?": u"?\u2424",
                u"!": u"!\u2424",
                u"\uFF1F": u"\uFF1F\u2424",
                u"\uFF01": u"\uFF01\u2424",
                u".": u".\u2424",
                #u",": u",\u2424",
                u"¡": u"¡\u2424",
                u"(": u"(\u2424",
                u")": u")\u2424",
                u"[": u"[\u2424",
                u"]": u"]\u2424",
                u"¿": u"¿\u2424",
                u"…": u"…\u2424",
                u"‥": u"‥\u2424",
                u"،": u"،\u2424",
                u";": u";\u2424",
                u":": u":\u2424",
                u"—": u"—\u2424",
                u"。": u"。\u2424",
                u"\uFF0C": u"\uFF0C\u2424",
                u"、": u"、\u2424",
                u"\uFF1A": u"\uFF1A\u2424",
                u"\n": u"\n\u2424"
            })
            self.replacements = None
        except AttributeError:
            self.punctuation = None

        self.domain_table = [{
            'package':
            'american_english',
            'sample':
            'Hello. I am an English system voice.',
            'iso_code':
            'US',
            'lang1':
            'en',
            'amp':
            'and',
            'voices': [
                "us/cmu_us_slt_arctic_hts", "us/cmu_us_slt_cg",
                "us/cmu_us_awb_arctic_hts", "us/cmu_us_awb_cg",
                "us/cmu_us_bdl_arctic_hts", "us/cmu_us_bdl_cg",
                "us/cmu_us_clb_arctic_hts", "us/cmu_us_clb_cg",
                "us/cmu_us_jmk_arctic_hts", "us/cmu_us_jmk_cg",
                "us/cmu_us_rms_arctic_hts", "us/cmu_us_rms_cg",
                "english/nitech_us_awb_arctic_hts",
                "english/nitech_us_bdl_arctic_hts",
                "english/nitech_us_clb_arctic_hts",
                "english/nitech_us_jmk_arctic_hts",
                "english/nitech_us_rms_arctic_hts",
                "english/nitech_us_slt_arctic_hts", "english/us1_mbrola",
                "english/us2_mbrola", "english/us3_mbrola",
                "english/kal_diphone"
            ]
        }, {
            'package':
            'british_english',
            'sample':
            'Hello. I am an English system voice.',
            'iso_code':
            'GB',
            'lang1':
            'en',
            'amp':
            'and',
            'voices': [
                "english/kal_diphone", "english/ked_diphone",
                "english/don_diphone", "english/en1_mbrola",
                "english/gsw_diphone", "english/rab_diphone"
            ]
        }, {
            'package':
            'english',
            'sample':
            'Hello. I am an English system voice.',
            'iso_code':
            'GB',
            'lang1':
            'en',
            'amp':
            'and',
            'voices': [
                "us/cmu_us_slt_arctic_hts", "us/cmu_us_slt_cg",
                "english/kal_diphone", "english/ked_diphone",
                "english/don_diphone", "english/en1_mbrola",
                "english/gsw_diphone", "english/rab_diphone"
            ]
        }, {
            'package':
            'italian',
            'sample':
            'Ciao. Sono una voce di sistema italiana.',
            'iso_code':
            'IT',
            'lang1':
            'it',
            'amp':
            'e',
            'voices': ["italian/lp_diphone", "italian/pc_diphone"]
        }, {
            'package': 'catalan',
            'sample': 'Hola. Sóc una veu del sistema castellà.',
            'iso_code': 'ES',
            'lang1': 'ca',
            'amp': 'i',
            'voices': ["catalan/upc_ca_ona_hts"]
        }, {
            'package': 'castillian_spanish',
            'sample': 'Hola. Soy un vox del sistema castellano.',
            'iso_code': 'ES',
            'lang1': 'es',
            'amp': 'y',
            'voices': ["spanish/el_diphone"]
        }, {
            'package': 'russian',
            'sample': 'Здравствуйте. Я - русский голос системы.',
            'iso_code': 'RU',
            'lang1': 'ru',
            'amp': u'\u0438',
            'voices': ["russian/msu_ru_nsh_clunits"]
        }, {
            'package':
            'finnish',
            'sample':
            "Hei. Olen suomalainen järjestelmäääni.",
            'iso_code':
            'FI',
            'lang1':
            'fi',
            'amp':
            'ja',
            'voices':
            ["finnish/hy_fi_mv_diphone", "finnish/suo_fi_lj_diphone"]
        }, {
            'package':
            'czech',
            'sample':
            "Ahoj. Jsem český systémový hlas.",
            'iso_code':
            'CZ',
            'lang1':
            'cz',
            'amp':
            'a',
            'voices': [
                "czech/czech_dita", "czech/czech_krb", "czech/czech_machac",
                "czech/czech_ph"
            ]
        }, {
            'package': 'german',
            'sample': "Hallo. Ich bin eine deutsche Stimme.",
            'iso_code': 'DE',
            'lang1': 'de',
            'amp': 'und',
            'voices': ["german/german_de2_os"]
        }, {
            'package': 'hindi',
            'sample': "Namaskāra. Mī ēka marāṭhī āvāja āhē.",
            'iso_code': 'IN',
            'lang1': 'hi',
            'amp': 'और',
            'voices': ["hindi/hindi_NSK_diphone"]
        }, {
            'package': 'marathi',
            'sample': "Namaskāra. Mī ēka marāṭhī āvāja āhē.",
            'iso_code': 'IN',
            'lang1': 'mr',
            'amp': 'आणि',
            'voices': ["marathi/marathi_NSK_diphone"]
        }, {
            'package': 'telugu',
            'sample': "Halō. Nēnu telugu vāṇini.",
            'iso_code': 'IN',
            'lang1': 'te',
            'amp': 'మరియు',
            'voices': ["telugu/telugu_NSK_diphone"]
        }, {
            'package':
            'vietnamese',
            'sample':
            "Xin chào. Tôi là một giọng nói việt nam.",
            'iso_code':
            'VN',
            'lang1':
            'vi',
            'amp':
            'và',
            'voices':
            ["vietnamese/wow_vi_liz_diphone", "vietnamese/wow_vi_ptn_diphone"]
        }, {
            'package':
            'welsh',
            'sample':
            'Helo. Llais system cymraeg ydw i.',
            'iso_code':
            'GB',
            'lang1':
            'cy',
            'amp':
            'a',
            'voices': [
                "welsh/cb_cy_llg_diphone",
                "welsh/cb_cy_cw_diphone",
                "welsh/hl_diphone",
            ]
        }]

    def first_good_voice(self, _test):  # -> str
        '''Return the first voice in the list. If the voice is
        not supported, then Festival normally shows a message
        then continues in English.'''

        if not _test:
            return ''
        test_path = ''
        path_stem = ''
        if os.name == 'nt':
            voice_roots = [
                os.path.join(os.getenv('ProgramFiles'), 'Festival', 'Voices'),
                os.path.join(os.getenv('ProgramFiles(x86)'), 'Festival',
                             'Voices')
            ]
        else:
            voice_roots = [
                '/usr/share/festival/voices/',
                '/usr/share/festival/lib/voices/'
            ]
        for _root in voice_roots:
            for _path in _test:
                test_path = os.path.join(_root, _path)
                if os.path.isdir(test_path):
                    path_stem = os.path.split(test_path)[1]
                    return '(voice_%(path_stem)s)' % locals()
        return ''

    def count_your_voices(self):  # -> int
        ''''Return a non-zero value only if a festival voice is installed.'''
        _count = 0
        test_dir = '/usr/share/festival/voices'
        _count = (readtexttools.count_items_in_dir(test_dir))
        if _count == 1:
            test_dir = os.path.join(test_dir, os.listdir(test_dir)[0])
            _count = readtexttools.count_items_in_dir(test_dir)
        return _count

    def iso_lang_to_fest_lang(self, iso_lang='en-US'):  # -> str
        '''Check if the library supports the language or voice.
        If so, return festival's name of the language, otherwise return
        `''`.

        Update `self.voice_eval` to a known available voice in the
        form `(voice_cmu_us_slt_arctic_hts)` if your system supports it.'''
        test_lang = ''
        test_region = ''
        try:
            for sep in ['-', '_']:
                if sep in iso_lang:
                    test_lang = iso_lang.split(sep)[0]
                    test_region = iso_lang.split(sep)[1]
                    break
        except (AttributeError, NameError):
            return ''
        try:
            domain_table = self.domain_table
            _tld = ''
            _lang1 = ''
            _region = ''
            _voices = ['']
            for i in range(len(domain_table)):
                _region = '-'.join(
                    [domain_table[i]['lang1'], domain_table[i]['iso_code']])
                if _region.strip() == iso_lang.strip():
                    self.voice_eval = self.first_good_voice(
                        domain_table[i]['voices'])
                    if len(self.voice_eval) != 0:
                        self.lang = domain_table[i]['lang1']
                        return self.domain_table[i]['package']
            for i in range(len(domain_table)):
                if domain_table[i]['lang1'] == test_lang.lower():
                    _tld = domain_table[i]['package']
                    _lang1 = domain_table[i]['lang1']
                    _region = '-'.join([_lang1, domain_table[i]['iso_code']])
                    _voices = domain_table[i]['voices']
                    break
            for _test in [iso_lang, test_lang]:
                if len(_voices[0]) == 0:
                    if len(_test) != 0:
                        if not '-' in _test:
                            return _test
                elif _test.lower() == _region.lower():
                    self.voice_eval = self.first_good_voice(
                        domain_table[i]['voices'])
                    self.lang = domain_table[i]['lang1']
                    return self.domain_table[i]['package']
                elif _test.lower() == _lang1:
                    self.voice_eval = self.first_good_voice(
                        domain_table[i]['voices'])
                    self.lang = domain_table[i]['lang1']
                    return self.domain_table[i]['package']
                elif _test.lower() == _tld.lower():
                    self.voice_eval = self.first_good_voice(
                        domain_table[i]['voices'])
                    self.lang = domain_table[i]['lang1']
                    return self.domain_table[i]['package']
                elif _test in _voices:
                    self.voice_eval = self.first_good_voice(
                        domain_table[i]['voices'])
                    self.lang = domain_table[i]['lang1']
                    return _test
                elif _test.lower() in _voices:
                    self.voice_eval = self.first_good_voice(
                        domain_table[i]['voices'])
                    self.lang = domain_table[i]['lang1']
                    return _test
        except NameError:
            self.lang = ''
        return ''

    def language_ok(self, _lang):  # -> bool
        '''Third party voices installed in the festival directory might
        not be compatible with the `text2wave` program, and cause a crash.'''
        if _lang[:2] in ['uk', 'tt', 'sq', 'ru', 'pt', 'pl', 'mk', 'kg', 'eo']:
            for third_party in [
                    '/usr/share/doc/rhvoice', '/usr/local/share/doc/rhvoice',
                    '/opt/rhvoice'
            ]:
                if os.path.isdir(third_party):
                    return False
        return True

    def list_sentences(self, _test_string=''):  # -> [list[str] | None]
        '''Generate a list of sentences from a string.'''
        _iter = ''
        _divider = self._divider
        if not bool(_test_string):
            return None
        if self.punctuation:
            return str(_test_string.translate(
                self.punctuation)).split(_divider)
        for _item in self.replacements:
            _iter = _item
            _test_string = _test_string.replace(
                _iter, u'%(_iter)s%(_divider)s' % locals())
        return _test_string.split(_divider)

    def festival_read(self,
                      _file_path='',
                      _visible='false',
                      _audible='false',
                      _output='',
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
+ `_output` - Name of desired output file
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
        _out_file = readtexttools.get_work_file_path(_output, _image, "OUT")
        # Determine the temporary file name
        _work_file = readtexttools.get_work_file_path(_output, _image, "TEMP")

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
                _command = '''%(_app)s --script %(_script)s "%(file_path)s" -o "%(_work_file)s"''' % locals(
                )
            else:
                # With Windows, this script only supports reading text aloud.
                _command = '%(_app)s --tts  "%(_file_path)s"' % locals()
        else:
            if readtexttools.have_posix_app('text2wave', False):
                _app = 'text2wave'
                # text2wave is an executable festival script
                if len(_eval_token) == 0:
                    _switch = ''
                else:
                    _switch = ' -eval "%(_eval_token)s"' % locals()
                _command = '%(_app)s%(_switch)s "%(_file_path)s" -o "%(_work_file)s"' % locals(
                )
            elif readtexttools.have_posix_app('flite', False):
                # Flite reates a compact .wav file - Signed 16 bit Little Endian,
                # Rate 8000 Hz, Mono. This format works with vlc, aplay & paplay,
                # but might not with a gstreamer app like totem or gst-launch-1.0
                if os.path.splitext(_file_path)[1] not in ['.txt']:
                    return False
                _command = 'flite -f "%(_file_path)s" -o "%(_work_file)s"' % locals(
                )
        try:
            if not readtexttools.my_os_system(_command):
                # try with _switch = '' -- default voice
                _command = '%(_app)s "%(_file_path)s" -o "%(_work_file)s"' % locals(
                )
        except IOError:
            print('I was unable to read!')
            usage()
            sys.exit(2)
        if os.path.isfile(_work_file):
            if os.path.getsize(_work_file) == 0:
                return False
            readtexttools.process_wav_media(_title, _work_file, _image,
                                            _out_file, _audible, _visible,
                                            _writer, _image_size)
            return True
        return False

    def sable_speaker_name(self, _test=''):  # -> str
        '''
        Sable
        =====

        Use [Sable](https://www.cs.cmu.edu/~awb/festival_demos/sable.html)
        name in `<SPEAKER NAME="kal_diphone">` markup
        `(voice_upc_ca_ona_hts)` becomes `upc_ca_ona_hts`
        `(voice_kal_diphone)` becomes `kal_diphone`
        '''
        my_val = 'male1'

        if '(voice_' in _test:
            return _test.replace('(voice_', '').replace(')', '')
        elif len(self.iso_lang_to_fest_lang(_test)) != 0:
            my_val = self.voice_eval.replace('(voice_', '').replace(')', '')
        return my_val

    def festival_rate(self, _test='100%'):
        '''
        Use RATE for value of Sable `<RATE SPEED="50%">` markup.
        Converts w3 Smil style percentage to Sable style percentage
        _test - rate expressed as a percentage.
        Use '100%' for default rate of 0% in Sable.
        Returns Sable rate as string between -99% and 100%.
        '''
        i2 = 0
        min_val = -99
        max_val = 100
        my_val = 0
        s1 = ''
        try:
            if '%' in _test:
                s1 = _test.replace('%', '')
                s1 = s1.replace('-', '')
                i2 = int(s1) - 100
            else:
                i2 = 0
        except TypeError:
            print('I was unable to determine festival rate!')
        if i2 <= min_val:
            my_val = min_val
        elif i2 >= max_val:
            my_val = max_val
        else:
            my_val = i2
        myStr = str(my_val) + '%'
        return myStr

    def in_festival_defaults(self, _test='0%'):  # -> bool
        '''Check if a parameter value is like a default setting.'''
        if _test in [None, False, '0', '0%', '']:
            return True
        return False

    def festival_pitch(self, _test='100%'):
        '''
        Use PITCH for value of Sable `<PITCH BASE="50%">` markup.
        Converts w3 Smil style percentage to Sable percentage
        _test - Pitch expressed as a percentage.
        Use '100%' for default Pitch of 0% in Sable markup
        Returns pitch value as string between -99% and 100%'''
        i2 = 0
        min_val = -99
        max_val = 100
        my_val = 0
        s1 = ''
        try:
            if '%' in _test:
                s1 = _test.replace('%', '')
                s1 = s1.replace('-', '')
                i2 = int(s1) - 100
            else:
                i2 = 0
        except TypeError:
            print('I was unable to determine festival pitch!')
        if i2 <= min_val:
            my_val = min_val
        elif i2 >= max_val:
            my_val = max_val
        else:
            my_val = i2
        return str(my_val) + '%'


def main():  # -> NoReturn
    '''
Creates a temporary speech-synthesis sound file and optionally
reads the file aloud.
    '''
    _read_festival = ReadFestivalClass()
    _imported_meta = readtexttools.ImportedMetaData()
    _xml_tool = readtexttools.XmlTransform()
    _sable = ''
    _output = ''
    _visible = ''
    _audible = ''
    _eval_lang = 'zz-ZY'
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
    _lang = readtexttools.default_lang()
    concise_lang = _lang.split('_')[0].split('-')[0]
    if not concise_lang:
        concise_lang = 'hi'
    _file_path = sys.argv[-1]
    if not os.path.isfile(_file_path):
        print('I was unable to find the file you specified!...')
        sys.exit(0)
    elif sys.argv[-1] == sys.argv[0]:
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
            _output = a
        elif o in ('-v', '--visible'):
            _visible = a
        elif o in ('-a', '--audible'):
            _audible = a
        elif o in ('-r', '--rate'):
            _rate = a
            _sable_rate = _read_festival.festival_rate(_rate)
        elif o in ('-p', '--pitch'):
            _pitch = a
            _sable_pitch = _read_festival.festival_pitch(_pitch)
        elif o in ('-i', '--image'):
            _image = a
        elif o in ('-e', '--eval'):
            _eval_token = a
            _eval_lang = _eval_token
            _sable_speaker = _read_festival.sable_speaker_name(_eval_token)
            if '-' in _eval_token:
                _eval_token = _read_festival.voice_eval
        elif o in ('-t', '--title'):
            _title = a
        elif o in ('-n', '--artist'):
            _writer = a
        elif o in ('-d', '--dimensions'):
            _image_size = a
        else:
            assert False, 'unhandled option'
    if not _read_festival.language_ok(_eval_lang):
        print('FAIL: `%(_eval_lang)s` - incompatible language or voice.' %
              locals())
        sys.exit(0)
    _content = _imported_meta.meta_from_file(_file_path)
    if len(_content) == 0:
        sys.exit(0)
    _content = readtexttools.strip_xml(_content)
    if len(_content) == 0:
        sys.exit(0)
    if bool(_read_festival.lang):
        concise_lang = _read_festival.lang
    _content = readtexttools.strip_mojibake(concise_lang, _content)
    if _read_festival.in_festival_defaults(
            _sable_rate) and _read_festival.in_festival_defaults(
                _sable_pitch) and _read_festival.in_festival_defaults(
                    _sable_speaker):
        # Pass plain text
        _content = readtexttools.clean_str(_content, False)
        _file_content = _content
        _read_festival.festival_read(_file_path, _visible, _audible, _output,
                                     _image, _content, "", _title, _writer,
                                     _image_size)
    else:
        # Prepare Sable XML (To SLOW DOWN speech use --RATE=75%)
        _domain_table = _read_festival.domain_table
        for i in range(len(_domain_table)):
            if _domain_table[i]['lang1'] == concise_lang:
                _content = _content.replace('&', _domain_table[i]['amp'])
                break
        _content = _xml_tool.clean_for_xml(_content, True)
        _content = readtexttools.local_pronunciation(
            _eval_lang, _content, 'festival', 'FESTIVAL_TTS_USER_DIRECTORY',
            False)[0]
        _file_content = '''<SABLE><SPEAKER NAME="%(_sable_speaker)s">
<RATE SPEED="%(_sable_rate)s"><PITCH BASE="%(_sable_pitch)s">
%(_content)s</PITCH></RATE></SPEAKER></SABLE>''' % locals()
        _sable = _file_path + ".sable"
        readtexttools.write_plain_text_file(_sable, _file_content, 'utf-8')
        _writer = readtexttools.check_artist(_writer)
        _title = readtexttools.check_title(_title, 'festival')
        if _read_festival.count_your_voices() == 1:
            _read_festival.festival_read(_file_path, _visible, _audible,
                                         _output, _image, _content, "", _title,
                                         _writer, _image_size)
        elif not _read_festival.festival_read(
                _sable, _visible, _audible, _output, _image, _content,
                _eval_token, _title, _writer, _image_size):
            _read_festival.festival_read(_file_path, _visible, _audible,
                                         _output, _image, _content, "", _title,
                                         _writer, _image_size)


if __name__ == '__main__':
    main()
