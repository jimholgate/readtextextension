#!/usr/bin/env python
# -*- coding: UTF-8-*-
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

Copyright (c) 2011 - 2022 James Holgate
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import aifc
import codecs
import getopt
import glob
import locale
import math
import mimetypes
import os
import platform
import sunau
import sys
import time

try:
    import dbus
except ImportError:
    pass

try:
    import site
except ImportError:
    pass

try:
    import subprocess
except ImportError:
    pass

try:
    import tkinter
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
except (ImportError, ValueError):
    pass

try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

try:
    import pathlib
except ImportError:
    pass

from xml.etree.ElementTree import TreeBuilder

try:
    import webbrowser
except:
    pass

def write_plain_text_file(_file_path='',
                          _body_text='',
                          scodeco='utf-8'):  # -> bool
    '''
    Create a plain text file.
    `write_plain_text_file("/path/file.txt", "Hello world", "utf-8")`
    '''
    if not bool(_file_path):
        return False
    try:
        try:
            os.remove(_file_path)
        except:
            pass
        writer = codecs.open(_file_path,
                             mode='w',
                             encoding=scodeco,
                             errors='replace')
        writer.write(_body_text)
        writer.close()
    except:
        print('`write_plain_text_file` error in readtexttools.py')
    return os.path.isfile(_file_path)


def get_temp_prefix():  # -> str
    '''
    Returns path to temporary directory plus a filename prefix.
    Need to supply an extension to determine the context - i.e:
     -sound.wav for sound
     -image.png for image
    '''
    if os.name == 'nt':
        return os.path.join(os.getenv('TMP'), os.getenv('USERNAME'))
    elif have_posix_app('say', False):
        return os.path.join(os.getenv('TMPDIR'), os.getenv('USER'))
    return os.path.join('/tmp', os.getenv('USER'))


class XmlTransform(object):
    '''Prepare text for XML encoding.'''

    def __init__(self):  # -> None
        '''Initialize data'''
        try:
            self.safe_xml = str.maketrans({
                "&": "&#38;",
                '"': "&#34;",
                "'": "&#39;",
                '<': "&#60;",
                ">": "&#62;",
                "[": "&#91;",
                "]": "&#93;",
                "{": "&#123;",
                "}": "&#125;",
                "(": "&#40;",
                ")": "&#41;"
            })
        except AttributeError:
            self.safe_xml = None
        self.use_mode = ['ssml', 'text'][0]

    def clean_for_xml(self, test_text):  # -> str
        '''The data portions of an XML file should escape characters
        with special properties. Not using `xml.sax.saxutils` because
        the replacements aren't always safe for uncontrolled input.

        For example, malformed scheme code strings or sable code could
        cause some speech synthesizers to crash.
        '''
        if bool(self.safe_xml):
            return str(test_text.translate(self.safe_xml))
        else:
            # python 2 - slower equivalent
            for pair in [["&", "&#38;"], ['"', "&#34;"], ["'", "&#39;"],
                         ["<", "&#60;"], [">", "&#62;"], ["[", "&#91;"],
                         ["]", "&#93;"], ["{", "&#123;"], ["}", "&#125;"],
                         ["(", "&#40;"], [")", "&#41;"]]:
                test_text = test_text.replace(pair[0], pair[1])
            return test_text


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


def safechars(_test_string='', _allowed='1234567890,'):  # -> string
    '''Removes unwanted characters from a string.'''
    if not bool(_test_string):
        return ''
    for _letter in _test_string:
        if not _letter in _allowed:
            _test_string = _test_string.replace(_letter, '')
    return _test_string


def remove_unsafe_chars(_test_string='', _forbidden='[]\\{}%|*'):  # -> string
    '''Removes unwanted characters from a string.'''
    if not bool(_test_string):
        return ''
    for _letter in _forbidden:
        _test_string = _test_string.replace(_letter, '')
    return _test_string


def net_error_icon():  # -> string
    '''Path to Gnome network error icon'''
    for _path in [
            'HighContrast/32x32/status/network-offline.png',
            'hicolor/32x32/apps/nm-no-connection.png',
            'HighContrast/32x32/apps/preferences-system-network.png',
            'Adwaita/32x32/legacy/network-error.png',
            'Humanity/actions/32/stock_not.svg'
    ]:
        _test = '/usr/share/icons/%(_path)s' % locals()
        if os.path.isfile(_test):
            return _test
    return ''


def strip_mojibake(concise_lang='en', _raw_text=''):
    '''Remove parts of text strings containing characters that a
    speech synthesizer cannot pronounce correctly.

    * `concise_lang` - The language in the form `en` or `en-US`
    * `_raw_text - The text to check and modify'''
    if not _raw_text:
        return ''
    try:
        concise_lang = concise_lang[:2].lower()
    except (AttributeError, TypeError):
        concise_lang = 'en'
    if concise_lang in ('en'):
        # Use Western European encoded characters.
        _coding = 'latin_1'
    else:
        # Use all supported unicode characters.
        _coding = 'utf-8'
    try:
        _code = _raw_text.encode(_coding, 'ignore')
        return _code.decode('utf-8', 'ignore').strip('\n\t .;\\{\\}()[]')
    except LookupError:
        return _raw_text


def strip_xml(str1):  # -> str
    '''
    `strip_xml(str1)`

    Plain text output
    =================

    When `strip_xml` is applied to a string, python converts the
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


def usage():  # -> None
    '''
    Displays the usage of the included python app "main", which can be used to
    convert wav files to other formats like ogg, opus, flac, and mp3.
    '''
    sa1 = ' ' + os.path.split(sys.argv[0])[1]
    print('''
Read text tools
===============

Reads a .wav sound file, converts it and plays copy with a player.
To include enhanced mp3 meta-data, install a converter like `avconv`,
`lame` or `ffmpeg`.

## Usage

### Audio:

      %(sa1)s --sound="xxx.wav" --output="xxx.ogg"
      %(sa1)s --visible="false" --audible="true"  \\ 
       --sound="xxx.wav" --output="xxx.ogg"

### Video:

Makes an audio with a poster image.  Uses `avconv` or `ffmpeg`.

      %(sa1)s --image="xxx.png" --sound="xxx.wav" \\ 
      --output="xxx.webm"
      %(sa1)s --visible="true" --audible="true" --image="x.png" \\
       --sound="x.wav"--title="Title" --output="x.webm"
''' % locals())


def app_signature():  # -> str
    '''
    App signature can help identify file locations and shared settings.
    '''
    return 'ca.bc.vancouver.holgate.james.readtextextension'


def app_name():  # -> str
    '''
    Application name in English
    '''
    return 'Read Text'


def app_release():  # -> str
    '''
    Major, Minor, Version release.  Use to check if this is the required
    version.
    '''
    return '0.9.2'

def default_lang():  # -> str
    '''Returns the system language in the form `en_US`'''
    _lang = ''
    try:
        _lang = os.getenv('LANG')
    except AttributeError:
        pass
    if not bool(_lang):
        try:
            _lang = os.getenv('LANGUAGE')
        except AttributeError:
            pass
    if not bool(_lang):
        _lang = locale.getdefaultlocale()[0]
    if _lang:
        return _lang.split('.')[0].split(':')[0]
    return ''


def gst_plugin_path(plug_in_name='libgstvorbis'):  # -> str
    '''
    Check directories for a named GST plugin (i. e.: `libgstvorbis`)
    '''
    # This does not check for plugin by pad name, mime type or extension
    if not plug_in_name:
        return ''
    rt1 = ''
    version = ''

    g_versions = ['1.2', '1.1', '1.0', '1', '0.10']
    _paths = [
        '/usr/local/lib/x86_64-linux-gnu/',
        '/usr/local/lib/',
        '/usr/lib/x86_64-linux-gnu/',
        '/usr/lib/',
        '/usr/local/lib64/',
        '/usr/lib64/',
        '/usr/local/i386/',
        '/usr/i386/',
        '/usr/local/lib/i386-linux-gnu/',
        '/usr/lib/i386-linux-gnu/',
        '/usr/local/lib/amd64-linux-gnu/',
        '/usr/lib/amd64-linux-gnu/',
        '/usr/local/lib/armel-linux-gnu/',
        '/usr/lib/armel-linux-gnu/',
        '/usr/local/lib/armhf-linux-gnu/',
        '/usr/lib/armhf-linux-gnu/',
        '/usr/local/lib/arm64-linux-gnu/',
        '/usr/lib/arm64-linux-gnu/',
        '/usr/local/lib/mips-linux-gnu/',
        '/usr/lib/mips-linux-gnu/',
        '/usr/local/lib/mips64el-linux-gnu/',
        '/usr/lib/mips64el-linux-gnu/',
        '/usr/local/lib/mipsel-linux-gnu/',
        '/usr/lib/mipsel-linux-gnu/',
        '/usr/local/lib/ppc64el-linux-gnu/',
        '/usr/lib/ppc64el-linux-gnu/',
        '/usr/local/lib/s390x-linux-gnu/',
        '/usr/lib/s390x-linux-gnu/',
        ]
    _ext = '.so'
    if have_posix_app('say', False):
        _paths = [
            os.path.join(os.getenv('HOME'), '/'),
            os.getenv('GST_PLUGIN_PATH')
        ]
        _ext = '.dylib'
    elif os.name == 'nt':
        _paths = [
            ''.join([os.getenv('USERPROFILE'), '\\']),
            os.path.join(os.getenv('HOMEDRIVE'), 'gstreamer-sdk', '/'),
            os.getenv('GST_PLUGIN_PATH'),
            os.path.join(os.getenv('HOMEDRIVE'), '/opt/')
        ]
        _ext = '.dll'

    for path in _paths:
        for g_version in g_versions:
            rt1 = path
            version = g_version
            file_test = '%(rt1)sgstreamer-%(version)s/%(plug_in_name)s%(_ext)s' % locals(
            )
            if os.path.isfile(file_test):
                return file_test
            file_test = '%(rt1)sgstreamer-%(version)s/%(plug_in_name)s' % locals(
            )
            if os.path.isfile(file_test):
                return file_test
    return ''


class ExtensionTable(object):
    '''Common data and procedures for handling audio files'''

    def __init__(self):
        '''Common data and procedures for handling audio files'''
        mac_afconvert = '/usr/bin/afconvert'
        self.vlc = ''
        if have_posix_app('vlc', False):
            self.vlc = 'vlc'
        elif os.name == 'nt':
            self.vlc = self.win_search('vlc', 'vlc')
        elif os.path.exists('/Applications/VLC.app/Contents/MacOS/VLC'):
            self.vlc = '/Applications/VLC.app/Contents/MacOS/VLC'
        w_flac = self.win_search('flac', 'flac')
        w_twolame = self.win_search('twolame', 'twolame')
        w_lame = self.win_search('lame', 'lame')
        w_oggenc = self.win_search('oggenc', 'oggenc')
        w_oggenc2 = self.win_search('oggenc2', 'oggenc2')
        w_opus = None
        w_spx = None
        self.mime_video = False
        self.ffmpeg = ''
        if os.name == 'posix':
            self.ffmpeg = ffmpeg_path()
        self.extension = 0
        self.filter = 1
        self.standalone = 2
        self.alt_standalones = 3
        self.extension_test = [[['.flac'], 'libgstflac', '/usr/bin/flac',
                                [w_flac, self.vlc]],
                               [['.aac'], 'alpha_libgstaac', mac_afconvert,
                                []],
                               [['.m4a'], 'alpha_libgstm4a', mac_afconvert,
                                []],
                               [['.mp4'], 'libgstbadvideo', self.ffmpeg,
                                ['/usr/bin/avconv', self.ffmpeg]],
                               [['.m4v'], 'libgstbadvideo', self.ffmpeg,
                                ['/usr/bin/avconv', self.ffmpeg]],
                               [['.mp2'], 'libgsttwolame', self.ffmpeg,
                                ['/usr/bin/twolame', w_twolame]],
                               [['.mp3'], 'libgstlame', self.ffmpeg,
                                ['/usr/bin/lame', self.vlc, w_lame]],
                               [['.oga', '.ogg', '.ogv'], 'libgstogg',
                                self.ffmpeg,
                                ['/usr/bin/oggenc', w_oggenc, w_oggenc2, self.vlc]],
                               [['.opus'], 'libgstopus', self.ffmpeg, [w_opus, self.vlc]],
                               [['.spx'], 'libgstspeex', self.ffmpeg, [w_spx, self.vlc]],
                               [['.wav'], 'libwavenc', self.ffmpeg, [self.ffmpeg]],
                               [['.webm'], 'libgstmatroska', self.ffmpeg, []]]

    def audio_extension_ok(self,
                           test_file_spec='/tmp/file.opus',
                           pendantic=True,
                           test_can_export=True,
                           exact_match=False):  # -> bool
        '''
        Make sure that the multimedia settings are initialized
        and return `True` or `False` before continuing.

        * `test_file_spec` - file type to test
        * `pendantic` - check Windows and uncommon Posix paths.
        * `test_can_export` - only return `True` if the system
           includes tools to convert from Wave format to the
           specified audio format otherwise just check if it
           has a multimedia file type.
        * `exact_match` - if `True` the file extension needs
          to match the extension in the table. If `False`,
          then the two mime-types need to match. For example,
          python says that `file.mp2` and `file.mp3` have
          the same mime-type, but the extensions are different.'''
        if not test_file_spec:
            return False
        _ext = os.path.splitext(test_file_spec)[1].lower()
        _check_mime = self.get_mime(test_file_spec)
        if not _check_mime:
            self.mime_video = False
            return False
        elif _check_mime.startswith('audio/'):
            self.mime_video = False
        elif _check_mime.startswith('video/'):
            self.mime_video = True
            print('File mime-type: `%(_check_mime)s`' % locals())
        else:
            self.mime_video = False
            return False
        if not test_can_export:
            return True
        for _test in self.extension_test:
            if exact_match:
                does_match = _ext in _test[self.extension]
            else:
                does_match = _check_mime == self.get_mime(''.join(
                    ['x/x', _test[self.extension][0]]))
            if does_match:
                if gst_plugin_path(_test[self.filter]):
                    return True
                elif bool(self.ffmpeg) or os.path.isfile(
                        _test[self.standalone]):
                    return True
                elif pendantic:
                    alt_list = _test[self.alt_standalones]
                    if alt_list:
                        for _alt_path in alt_list:
                            if bool(_alt_path):
                                if os.path.isfile(_alt_path):
                                    return True
        return False

    def get_mime(self, test_file_spec='', strict=False):  # -> str
        '''Return python's mime-type for a file path.'''
        _ext = os.path.splitext(test_file_spec)[1].lower()
        if not _ext:
            _ext = test_file_spec.lower()
        if not test_file_spec:
            return ''
        try:
            mimetypes.init()
            return mimetypes.types_map[_ext]
        except (IndexError, KeyError):
            if strict:
                return ''
            # Darwin platform (a. k. a. MacOS) ?
            #
            # Gstreamer vorbis file family ; Specific mime type
            #
            # The information from gstreamer on open desktop is
            # via /usr/share/gstreamer-1.0/<fileextension>.gep
            for _format in ['flac', 'ogg', 'opus', 'spx']:
                format = _format
                if test_file_spec.endswith('.%(format)s' %locals()):
                    return 'audio/x-vorbis;audio/%(format)s' %locals()
            for _format in ['ogv', 'webm']:
                format = _format
                if test_file_spec.endswith('.%(format)s' %locals()):
                    return 'video/x-vorbis;video/%(format)s' %locals()
            for _format in ['md', 'wiki']:
                format = _format
                if test_file_spec.endswith('.%(format)s' %locals()):
                    return 'text/plain;application/x-%(format)s'
            return ''

    def add_quotes_if_needed(self, app=''):  # -> str
        '''Add Windows style Double Quotes to encompass paths that include spaces'''
        if ' ' in app:
            if not app.startswith('"'):
                app = ''.join(['"', app])
            if not app.endswith('"'):
                app = ''.join([app, '"'])
        return app

    def check_path_str(self, file_path_str=''):  # -> str
        ''' Returns the file path as a string formatted for the
        current operating system.
        '''
        os_sep = os.sep
        if not bool(file_path_str):
            return ''
        try:
            return str(pathlib.PurePath(file_path_str))
        except NameError:
            file_path_str = os.path.realpath(file_path_str)
            if os.name == 'nt':
                return str(file_path_str).replace('/', os_sep).replace(
                    os_sep + os_sep, os_sep)
            return str(file_path_str).replace('\\', os_sep).replace(
                os_sep + os_sep, os_sep)

    def win_search(self,
                   application_name='ffmpeg',
                   application_executable='ffplay'):  # -> str
        '''Search for a Windows application executable

        Examples
        ---------

        print(win_search('ffmpeg', 'ffmpeg'))  \n
        print(win_search('ffmpeg','ffplay'))  \n
        print(win_search('lame', 'lame'))  \n
        print(win_search('LibreOffice', 'soffice'))  \n
        print(win_search('Pandoc', 'pandoc'))  \n
        '''
        if not application_executable:
            return ''
        elif not application_name:
            return ''
        elif os.name != 'nt':
            return ''
        os_sep = os.sep
        executable_extensions = ['.exe', '']
        common_app_executable = ''
        program_dir_searches = [
            'LOCALAPPDATA', 'USERPROFILE', 'ProgramFiles', 'ProgramFiles(x86)',
            'HOMEDRIVE'
        ]
        application_searches = [
            '%(os_sep)s%(application_name)s%(os_sep)scommand_line%(os_sep)s' %
            locals(),
            '%(os_sep)s%(application_name)s%(os_sep)sbin%(os_sep)s' % locals(),
            '%(os_sep)s%(application_name)s%(os_sep)sprogram%(os_sep)s' %
            locals(),
            '%(os_sep)sVideoLAN%(os_sep)sVLC%(os_sep)s' % locals(),
            '%(os_sep)s%(application_name)s%(os_sep)s' % locals(),
            '%(os_sep)s' % locals(),
            '%(os_sep)sLocal%(os_sep)s' % locals(),
            '%(os_sep)sbin%(os_sep)s' % locals()
        ]
        for program_dir_search in program_dir_searches:
            get_env = os.getenv(program_dir_search)
            if not get_env:
                continue
            get_env = get_env.replace('\\', os_sep)
            for extension in executable_extensions:
                for application_search in application_searches:
                    common_app_executable = '%(get_env)s%(application_search)s%(application_executable)s%(extension)s' % locals(
                    )
                    if os.path.isfile(common_app_executable):
                        return self.add_quotes_if_needed(
                            self.check_path_str(common_app_executable))
                    else:
                        # Look for a directory like `ffmpeg-YYYY-MM-DD-git-xxxxxx`
                        developer_app_executables = glob.glob(
                            '%(get_env)s%(application_search)s%(application_executable)s*'
                            % locals())
                        if bool(developer_app_executables):
                            # Get a matching item in `developer_app_executables`
                            # object.
                            for app_match in developer_app_executables:
                                if not app_match:
                                    continue
                                return_value = '%(app_match)s%(os_sep)s%(application_executable)s%(extension)s' % locals(
                                )
                                return_value = return_value.replace(
                                    '\\', os_sep)
                                if os.path.isfile(return_value):
                                    return self.add_quotes_if_needed(
                                        self.check_path_str(return_value))
        return ''


def find_local_pip(lib_name='qrcode'): # -> str
    '''If you installed a pip tool as a local user, then
    return the library path, otherwise return `''` '''
    if int(platform.python_version_tuple()[0]) < 3:
        return ''
    elif os.name == 'nt':
        profile = os.getenv("LOCALAPPDATA")
        path1 = os.path.join(profile, 'Programs\\Python\\')
        path2 = '\\Lib\\site-packages'
    elif have_posix_app('say', False):
        profile = os.getenv("HOME")
        path1 = os.path.join(profile, 'Library/Python/')
        path2 = '/lib/python/site-packages'
    elif os.name == 'posix':
        site_list = site.getsitepackages()
        for _site in site_list:
            if os.getenv("PWD") in _site and len(os.getenv) != 0:
                if os.path.isdir(os.path.join(_site, lib_name)):
                    return _site
        return ''
    py_path = ''
    with os.scandir(path1) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_dir():
                py_path = ''.join([path1, entry.name, path2, os.sep, lib_name])
                if os.path.isdir(py_path):
                    return ''.join([path1, entry.name, path2])
    return ''

def my_os_system(_command):  # -> bool
    '''
    This is equivalent to os.system(_command)
    Replaced os.system(_command) to avoid Windows path errors.
    * Returns `True` if there is no error
    * Returns `False` if there is an error
    '''
    _command = _command.encode('utf-8')
    if os.name == 'nt':
        try:
            retcode = subprocess.call(_command, shell=False)
            if retcode < 0:
                print('Process was terminated by signal')
                return False
            else:
                print('Process returned')
                return True
        except (NameError, OSError):
            print('Execution failed')
            return False
    else:
        retval = os.system(_command)
        return not bool(retval)


def have_posix_app(posix_app='vlc', do_test=True):  # -> bool
    '''if the app exists and understands a `--version` or `--help` switch,
    then returns `True`, otherwise returns `False`.

    If `do_test` is `False`, then only look for the app installed in the
    standard system-wide location, otherwise test for a manual or help
    response. A container version of an app might test `True`, but the
    python program might not be able to run the posix app.
    '''
    os_sep = os.sep
    mute_response = '&> %(os_sep)sdev%(os_sep)snull &' % locals()
    if os.name != 'posix':
        return False
    if not bool(posix_app):
        return False
    if os.path.isfile('/usr/bin/%(posix_app)s' % locals()):
        return True
    if os_sep in posix_app:
        posix_app = os.path.basename(posix_app)
    if bool(do_test) and my_os_system(
            'man -w %(posix_app)s %(mute_response)s' % locals()):
        return True
    if bool(do_test):
        for tester in ['--version', '--help', '-h', '-?']:
            app_switch = tester
            if my_os_system('%(posix_app)s %(app_switch)s %(mute_response)s' %
                            locals()):
                # No error
                return True
    return False


def get_nt_path(name='ffmpeg', app='ffplay'):  # -> str
    '''
    Return the path to a Windows program if it is installed
    in a local or global program installation location.

    * `get_nt_path('ffmpeg', 'ffmpeg')`
    * `get_nt_path('ffmpeg','ffplay')`
    * `get_nt_path('lame', 'lame')`
    * `get_nt_path('LibreOffice', 'soffice')`
    * `get_nt_path('Pandoc', 'pandoc')`
    '''
    _extension_table = ExtensionTable()
    return _extension_table.win_search(name, app)


def app_icon_image(image_selection=''):  # -> str
    '''The path to an extension icon image, if it exists,
    or `''` if it doesn't exist.'''
    path_root = os.path.split(os.path.realpath(__file__))[0]
    os_sep = os.sep
    folders = path_root.split(os_sep)
    count = len(folders)
    if not bool(image_selection):
        image_selection = 'textToSpeechAbout_42.png'
    for _x in folders:
        test_root = os_sep.join(folders[:count])
        for image in [
                os.path.join(test_root, 'images', image_selection),
                os.path.join(test_root, 'images', 'textToSpeech.svg'),
                os.path.join(test_root, 'images', 'schooltools_42.svg'),
        ]:
            if os.path.isfile(image):
                return image
        if test_root.endswith('uno_packages'):
            return ''
        count = count - 1
    return ''


def pop_message(summary="Note",
                msg='',
                m_sec=8000,
                my_icon='',
                urgent=1):  # -> bool
    '''Pop up a notification message if supported on the platform'''
    if not msg:
        return False
    if not summary:
        return False
    if not m_sec:
        m_sec = 5000
    if urgent not in [0, 1, 2]:
        urgent = 1
    if not os.path.isfile(my_icon):
        my_icon = 'face-smile'
        for icon in [
                app_icon_image(),
                '/usr/share/icons/hicolor/scalable/apps/libreoffice-main.svg',
                '/usr/share/icons/hicolor/scalable/apps/openoffice-main.svg',
                '/usr/share/icons/hicolor/32x32/apps/libreoffice-startcenter.png',
                '/usr/share/icons/hicolor/32x32/apps/openoffice-startcenter.png',
                '/usr/share/icons/HighContrast/32x32/apps/libreoffice-startcenter.png',
                '/usr/share/icons/HighContrast/32x32/devices/multimedia-player.png',
                '/usr/share/icons/HighContrast/32x32/emotes/face-smile.png'
        ]:
            if os.path.isfile(icon):
                my_icon = icon
                break
    try:
        if bool(dbus):
            item = "org.freedesktop.Notifications"
            _interface = dbus.Interface(
                dbus.SessionBus().get_object(item,
                                             "/" + item.replace(".", "/")),
                item)
            _interface.Notify("readtexttools.py", 0, my_icon, summary, msg, [],
                              {"urgency": urgent}, m_sec)
            return True
    except (NameError, ValueError):
        try:
            if bool(tkinter):
                for tag in ['<b>', '</b>', '<i>', '</i>']:
                    msg = msg.replace(tag, ' ')
                tkinter.messagebox(summary, msg)
                return True
        except (AttributeError, NameError, ValueError):
            pass
    if have_posix_app('notify-send', False):
        my_os_system(
            'notify-send -i "%(my_icon)s" -t %(m_sec)s "%(summary)s" "%(msg)s"'
            % locals())
        return True
    elif have_posix_app('osascript', False):
        for tag in ['<b>', '</b>', '<i>', '</i>']:
            msg = msg.replace(tag, '')
        if urgent == 2:
            _sound = ' sound name "Sosumi"'
        elif urgent == 1:
            _sound = ' sound name "Tink"'
        else:
            _sound = ''
        my_os_system('''osascript -e 'display notification "%(msg)s" with title "%(summary)s"%(_sound)s' ''' %locals())
        return True
    return False


def lax_bool(_test):  # -> bool
    '''Given a string `true`, `yes` `1`, `-1` or a boolean `True` returns
    `True`, otherwise returns `False`.'''
    if not bool(_test):
        return False
    try:
        if _test.lower() in ['true', 'yes', '-1', '1']:
            return True
    except [AttributeError, NameError, TypeError]:
        pass
    if _test in [True, -1, 1]:
        return True
    return False


def lax_mime_match(_wanted='', _testing=''):  # -> bool
    '''If two file extensions are identical or if they share
    the same mime type, then return `True`, otherwise return
    `False`. For unknown mimetypes, compare extensions.'''
    if not _wanted:
        return False
    if not _testing:
        return False
    mimetypes.init()
    try:
        return mimetypes.types_map[_wanted] == mimetypes.types_map[_testing]
    except:
        # Note: catching classes that do not inherit from BaseException
        # is not allowed on some platforms, so allow a general exception.
        # Different versions and platforms do not have the same coverage
        # of mimetypes, so fall back to trivial match
        try:
            return _wanted.lower() == _testing.lower()
        except [AttributeError, NameError, TypeError]:
            pass
    return False


def ffmpeg_path():  # -> str
    '''
    ffmpeg may not be in the normal environment PATH, so we look for it, and
    return the location.
    '''
    paths = [
        '/usr/local/bin/avconv', '/usr/local/bin/ffmpeg', '/usr/bin/avconv',
        '/usr/bin/ffmpeg'
    ]
    if os.name == 'nt':
        paths = [
            get_nt_path('ffmpeg', 'ffmpeg'),
            get_nt_path('avconv', 'avconv.exe')
        ]
    elif have_posix_app('say', False):
        mvc = 'Miro Video Converter'
        paths = [
            '/usr/local/bin/ffmpeg',
            '/Applications/Miro.app/Contents/Helpers/ffmpeg',
            '/Applications/%(mvc)s.app/Contents/Helpers/ffmpeg' % locals(),
            '/Applications/Shotcut/Shotcut.app/bin/ffmpeg'
        ]
    for path in paths:
        if os.path.isfile(path):
            return path
    return ''


def get_work_file_path(_work='', _image='', _type=''):  # -> str
    '''
    Determine the temporary filename or output filename
    Given the filename _work, returns a temporary filename if _type is 'TEMP'
    or the output filename if _type is anything else.
    Example:
    import readtexttools
    * Determine the temporary file name
    `_work = readtexttools.get_work_file_path(_work, _image, 'TEMP')`
    * Determine the output file name
    `_out = readtexttools.get_work_file_path(_work, _image, 'OUT')`TreeBuilder
    '''
    _extension_table = ExtensionTable()
    _out = ''
    _alt_ext = ''
    if _work == '':
        if have_posix_app('say', False):
            _work = get_temp_prefix() + u'-speech.aiff'
        else:
            _work = get_temp_prefix() + u'-speech.wav'
    _work_ext = os.path.splitext(_work)[1].lower()
    _wanted_ext = _work_ext
    _image_ext = os.path.splitext(_image)[1].lower()
    mimetypes.init()
    _mime = "xxz/xxz-do-not-match"
    if len(_work_ext) != 0:
        try:
            _mime = mimetypes.types_map[_work_ext]
        except (IndexError, KeyError):
            pass
    # afconvert is for MacOS formats
    if _work_ext in ['.aac']:
        if have_posix_app('afconvert', False):
            _out = _work
            _work = '%(_out)s.aiff' % locals()
    elif _work_ext in ['.m4a', 'm4r']:
        if have_posix_app('faac', False) or bool(
                get_nt_path('nero', 'neroAacEnc')) or bool(
                    get_nt_path('faac', 'faac')):
            _out = _work
            _work = '%(_out)s.wav' % locals()
        elif have_posix_app('afconvert', False):
            _out = _work
            _work = '%(_out)s.aiff' % locals()
        else:
            # Can't make m4a, so make wav
            _out = '%(_work)s.wav' % locals()
            _work = _out
    elif lax_mime_match(_work_ext, '.mp3'):
        # _extension_table = ExtensionTable()
        if media_converter_installed():
            if (os.path.isfile('/usr/share/doc/liblame0/copyright') or
                    os.path.isfile('/usr/share/doc/libmp3lame0/copyright') or
                    have_posix_app('lame', False) or
                    os.path.isfile('/usr/lib/x86_64-linux-gnu/libmp3lame.so.0') or
                    os.path.isfile(_extension_table.vlc) or
                    bool(get_nt_path('lame', 'lame'))):
                _out = _work
                _work = '%(_out)s.wav' % locals()
            else:
                # Can't make mp3, so make wav
                _out = '%(_work)s.wav' % locals()
                _work = _out
        else:
            # Can't make mp3, so make wav
            _out = '%(_work)s.wav' % locals()
            _work = _out
    elif _work_ext in ['.mp2']:
        if media_converter_installed():
            if (os.path.isfile('/usr/share/doc/libtwolame0/copyright') or
                    bool(get_nt_path('twolame', 'twolame'))):
                _out = _work
                _work = '%(_out)s.wav' % locals()
            else:
                _out = '%(_work)s.wav' % locals()
                _work = _out
        else:
            # Can't make mp2, so make wav
            _out = '%(_work)s.wav' % locals()
            _work = _out
    elif lax_mime_match(_work_ext, '.ogg'):
        if media_converter_installed():
            if (os.path.isfile('/usr/share/doc/libogg0/copyright') or
                    os.path.isfile(_extension_table.vlc) or
                    bool(get_nt_path('oggenc', 'oggenc')) or
                    bool(get_nt_path('oggenc2', 'oggenc2'))):
                _out = _work
                _work = '%(_out)s.wav' % locals()
            else:
                _out = '%(_work)s.wav' % locals()
                _work = _out
        else:
            # Can't make ogg, so make wav
            _out = '%(_work)s.wav' % locals()
            _work = _out
    elif lax_mime_match(_work_ext, '.aif'):
        if media_converter_installed():
            _out = _work
            _work = '%(_out)s.wav' % locals()
        else:
            # Can't make aif, so make wav
            _out = '%(_work)s.wav' % locals()
            _work = _out
    elif lax_mime_match(_work_ext, '.flac'):
        if (
                media_converter_installed() or
                bool(get_nt_path('flac', 'flac'))):
            _out = _work
            _work = '%(_out)s.wav' % locals()
        else:
            # Can't make flac, so make wav
            _out = '%(_work)s.wav' % locals()
            _work = _out
    elif lax_mime_match(_work_ext, '.opus'):
        if media_converter_installed():
            _out = _work
            _work = '%(_out)s.wav' % locals()
        else:
            # Can't make opus, so make wav
            _out = '%(_work)s.wav' % locals()
            _work = _out
    elif 'video/' in _mime:
        if len(ffmpeg_path()) != 0 and _image_ext.lower() in [
                '.gif', '.jpeg', '.jpg', '.png'
        ]:
            _out = _work
            _work = '%(_out)s.wav' % locals()
        elif os.path.isfile(app_icon_image('poster-001.png')):
            _out = _work
            _work = '%(_out)s.wav' % locals()
        else:
            _alt_ext = '.ogg'
            _out = ''.join([os.path.splitext(_work)[0], _alt_ext])
            _work = '%(_out)s.wav' % locals()

    if _type.lower() == 'temp':
        if bool(_alt_ext):
            print('''
The `%(_wanted_ext)s` video format you requested needs an image.
Using the `%(_alt_ext)s` audio format.''' % locals())
        _return_value = _work
    else:
        _return_value = _out
    if _return_value:
        make_output_directory(_out)
    return _return_value


def media_converter_installed():  # -> bool
    '''Check if ffmpeg, Gst or VLC are installed'''
    _extension_table = ExtensionTable()
    if len(ffmpeg_path()) != 0:
        return True
    elif have_posix_app('afconvert', False):
        return True
    elif have_posix_app('vlc', False):
        return True
    elif bool(_extension_table.win_search('vlc', 'vlc')):
        return True
    else:
        try:
            dummy = bool(Gst)
            return dummy
        except NameError:
            pass
    return False


def make_output_directory(_out):  # -> str
    ''' Make sure that the destination directory exists'''
    _out_directory = os.path.dirname(_out)
    if not os.path.exists(_out_directory):
        try:
            os.makedirs(_out_directory)
        except:
            _out_directory = ''
    return _out_directory


def process_wav_media(_title='untitled',
                      _work='',
                      _image='',
                      _out='',
                      _audible='true',
                      _visible='false',
                      _artist='',
                      _dimensions='600x600'):  # -> bool
    '''
    # If no _out

    + play the `_work` working file aloud
    + if `_visible`, play using a player with a user interface,
      otherwise try to play with a hidden player.
    + ignore status of `_audible`; always play.

    # If _out

    Converts audio file, plays copy and deletes original
    + _title is brief title
    + _work is working file name (wav)
    + _image is image to add to video.  Ignored if making audio only
    + _out is output file name.( webm, ogg etc.)
    + _audible - Do we play the file after conversion?
    + _visible - Do we use a GUI or the console?
    '''
    if not bool(_work):
        return False
    _extension_table = ExtensionTable()
    if not _extension_table.audio_extension_ok(_out):
        clean_temp_files(_work)
        if os.path.isfile(get_my_lock('lock')):
            return True
        # ignore `_audible` status
        if lax_bool(_visible):
            show_with_app(_work)
        else:
            lock_my_lock()
            play_wav_no_ui(_work)
            unlock_my_lock()
        return True

    out_ext = os.path.splitext(_out)[1].lower()
    _ffmpeg = ffmpeg_path()
    for _test in _extension_table.extension_test:
        if out_ext in _test[_extension_table.extension]:
            if have_posix_app('afconvert', False):
                if not vlc_wav_to_media(_work, _out, _audible, _visible, False):
                    wav_to_media(_title, _work, _image, _out, _audible, _visible,
                                 _artist, _dimensions)
                break
            elif bool(_ffmpeg) or os.path.isfile(
                    _test[_extension_table.standalone]):
                wav_to_media(_title, _work, _image, _out, _audible, _visible,
                             _artist, _dimensions)
                break
            elif gst_plugin_path(_test[_extension_table.filter]):
                if not gst_wav_to_media(_title, _work, _image, _out, _audible,
                                        _visible, _artist, _dimensions):
                    vlc_wav_to_media(_work, _out, _audible, _visible, False)
                break
    clean_temp_files(_work)
    if os.path.isfile(_work):
        if os.path.isfile(_out):
            try:
                os.remove(_work)
            except (OSError, FileNotFoundError):
                print('OSError: could not remove %(sTMP)s' % locals())
    return os.path.isfile(_out)


def do_gst_parse_launch(_pipe=''):  # -> bool
    '''
    Execute a GStreamer command. This usually includes a source,
    a series of pads, and a sink. Return `True` on success,
    or `False` on fail.

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

    Stewart, Ian "GStreamer - Gst : An Introduction to using GStreamer in
    Python3 Programs". [GitHub](https://github.com/irsbugs/GStreaming), 2020.
    '''
    if not _pipe:
        return True
    try:
        Gst.init(None)
        _player = Gst.parse_launch('%(_pipe)s' % locals())
        _player.set_state(Gst.State.NULL)
        _player.set_state(Gst.State.READY)
        _player.set_state(Gst.State.PAUSED)
        _player.set_state(Gst.State.PLAYING)
        _player.get_bus().poll(Gst.MessageType.EOS | Gst.MessageType.ERROR,
                               Gst.CLOCK_TIME_NONE)
        _player.set_state(Gst.State.PAUSED)
        _player.set_state(Gst.State.READY)
        _player.set_state(Gst.State.NULL)
        return True
    except:  # gi.repository.GLib.Error: gst_parse_error: no element "filesrc" (1)
        try:
            _terminator = u'\u0000'
            Gst.init(None)
            Gst.ParseContext.new()
            Gst.parse_launchv('%(_pipe)s%(_terminator)s' % locals())
            Gst.ParseContext.free()
            return True
        except:
            for launch in ['gst-launch-1.0']:
                if have_posix_app(launch, False):
                    gst_l = launch
                    if my_os_system('%(gst_l)s %(_pipe)s' % locals()):
                        print('%(gst_l)s %(_pipe)s' % locals())
                        return True
    return False


def web_info_translate(_msg='WARNING:\n\nPython `speechd` Error.', _language='en'):  # -> bool
    '''Opens a web browser with the text of the message and a local translation.
    Users of a sandboxed program can get a message.'''
    _web_text = path2url(_msg).replace('file:///', '')
    try:
        if _language[:2] in ['en']:
            _language = 'es'
        webbrowser.open_new(
            'https://translate.google.com/?sl=auto&tl=%(_language)s&text=%(_web_text)s&op=translate' %locals()
            )
        return True
    except NameError:
        return False


class JsonTools(object):
    '''Use simple json data'''
    def __init__(self):
        try:
            self.safe_json = str.maketrans({
                "{": "'\\u007B'",
                "}": "\\u0070",
                '"': "\\u0022",
                "@": "\\u0040"
            })
        except AttributeError:
            self.safe_json = None

    def sanitize_json(self, content=''):  # -> str
        '''Escape json characters in content'''
        try:
            test_text = content.strip()
        except AttributeError:
            try:
                test_text = str(content).strip()
                if test_text == 'None':
                    return ''
            except AttributeError:
                return ''
        if bool(self.safe_json):
            return str(test_text.translate(self.safe_json))
        return test_text.replace(
            '{', '\\u007B').replace(
                '}', '\\u0070').replace(
                    '"', '\\u0022').replace(
                        '@', '\\u0040')

    def set_json_content(self, language='en', voice='AUTO', i_rate=0,
                         file_spec='', output_module='', flags= '', album='',
                         author='', genre='', title='', track=1): # -> str
        '''Sanitize content and return json string'''
        try:
            s_rate = str(i_rate)
        except AttributeError:
            s_rate = '0'
        try:
            s_track = str(track)
        except AttributeError:
            s_track = '1'
        album = self.sanitize_json(album)
        author = self.sanitize_json(author)
        file_spec = self.sanitize_json(file_spec)
        flags = self.sanitize_json(flags)  # `;` list of dev flags
        genre = self.sanitize_json(genre)
        language = self.sanitize_json(language)
        output_module = self.sanitize_json(output_module)
        s_rate = self.sanitize_json(s_rate)
        s_track = self.sanitize_json(s_track)
        title = self.sanitize_json(title)
        voice = self.sanitize_json(voice)
        return '''{
  "album": "%(album)s",
  "author": "%(author)s",
  "file_spec": "%(file_spec)s",
  "flags": "%(flags)s",
  "genre": "%(genre)s",
  "i_rate": %(s_rate)s,
  "i_track": %(s_track)s,
  "language": "%(language)s",
  "output_module": "%(output_module)s",
  "secret_key": "%(file_spec)s.json",
  "title": "%(title)s",
  "voice": "%(voice)s"
}''' %locals()


class ImportedMetaData(object):
    '''Get your media's metadata ready to include in new media'''

    def __init__(self):  # ' -> None
        '''Define shared values'''
        self.date = time.strftime('%Y-%M-%d')
        self.identity = None
        self.title = None
        self.genre = None
        self.track = None
        self.album = None
        self.composer = None
        self.year = time.strftime('%Y')
        self.image = None
        self.image_extensions = ['.gif', '.jpeg', '.jpg', '.png']
        self.seconds = 0
        # Metadata string indexes
        self.i_gst = 0
        self.i_avconv = 1
        self.i_avimage = 2
        self.i_oggenc = 3
        self.i_neromp4 = 4
        self.i_winlame = 5
        self.i_unixlame = 6
        self.i_vlc_track = 7
        self.i_vlc_album = 8
        self.i_vlc_author = 9
        self.i_vlc_title = 10
        self.i_vlc_genre = 11
        self.i_vlc_xspf = 12
        self.i_m3u = 13
        self.i_pretty = 14
        self.i_ffmpeg_meta_file = 15
        self.i_ffmpeg_meta = 16
        self.i_xml_track = 17
        self.i_xml_album = 18
        self.i_xml_author = 19
        self.i_xml_title = 20
        self.i_xml_genre = 21
        self.i_popup_meta = 22
        try:
            self.safe_gst_pipe = str.maketrans({
                " ": u"\u005C ",
                '"': u'\u005C"',
                "'": u"\u005C'",
                ':': u"\u005C:",
                "!": u"\u005C!"
            })
        except AttributeError:
            self.safe_gst_pipe = None

    def get_defaults(self):  # -> None
        '''Initialize the values.
        TODO: Check for and handle `.xml` or `.json` settings file'''
        if self.identity:
            if not self.composer:
                self.composer = self.identity
        else:
            self.identity = 'USERNAME'
            for user_env in ['USER', 'USERNAME']:
                try:
                    self.identity = os.getenv(user_env)
                    if self.identity:
                        break
                except:
                    continue
        if not self.title:
            self.title = time_for_title()
        if not self.genre:
            self.genre = 'Speech'
        if not self.track:
            self.track = str(1)
        if not self.album:
            self.album = ''.join([
                "_",
                app_name().lower().replace(" ", "_"), "_",
                date_for_album(), ""
            ])

    def escape_gst_pipe_meta(self, test_text=''):  # -> str
        '''Returns safe value for gst pipe metadata'''
        if not test_text:
            return ''
        if self.safe_gst_pipe:
            return str(test_text.translate(self.safe_gst_pipe))
        for item in ''' "':!''':
            test_text = test_text.replace(item, ''.join([u"\u005C", item]))
        return test_text

    def execute_command(self, a_command='', safer=True):
        '''
        This is similar to `os.system(a_command)`, but we can get output
        from program commands.
        '''
        # a_command is a normal command line instruction.
        if safer:
            for block_item in [
                    'sudo', '-version', '-quiet', '-log', '-list', '-help',
                    '--', ':', '$', '|', '<', '[', '#', '%', '{', '.', '^'
            ]:
                if a_command.strip().startswith(block_item):
                    # it is not a command
                    return ''
        try:
            return unicode(subprocess.check_output(a_command, shell=True),
                           errors='ignore')
        except NameError:
            # Python 3
            try:
                retval = subprocess.check_output(a_command.encode('utf-8'),
                                                 shell=True)
                return retval.decode('utf-8')
            except (AttributeError, NameError, OSError,
                    subprocess.CalledProcessError, TypeError):
                # nt
                try:
                    retval = subprocess.check_output(a_command, shell=True)
                    return retval.decode('utf-8')
                except (NameError, OSError, subprocess.CalledProcessError,
                        TypeError):
                    # For example, the command results in an error.
                    return ""
        except (OSError, subprocess.CalledProcessError):
            return ""

    def set_time_meta(self, file_path=''):  # -> str
        '''Calculate the number of seconds of a local sound file. Return
        the value as a string and set the `self.seconds` value to an integer.'''
        _extension_table = ExtensionTable()
        #if self.seconds:
        #    return self.seconds
        if not os.path.isfile(file_path):
            self.seconds = 0
            return self.seconds
        if os.path.splitext(file_path)[1].lower() in [
                '.aif', '.aifc', '.au', '.wav'
        ]:
            self.seconds = sound_length_seconds(file_path)
            return self.seconds
        elif _extension_table.get_mime(file_path).startswith('audio/'):
            if have_posix_app('gst-discoverer-1.0', False):
                time_list = ['_duration_not_found', '0', '0', '0']
                _result = self.execute_command(
                    'gst-discoverer-1.0 -v "%(file_path)s" | grep Duration:' %
                    locals())
                # Duration: 0:00:03.857687075
                if _result:
                    _result = _result.replace(' ', '')
                    try:
                        time_list = _result.split(
                            ':')  # ['Duration', 'H', 'M', 'S']
                    except:
                        pass
                try:
                    self.seconds = int(float(time_list[1])) * 360 + int(
                        float(time_list[2])) * 60 + int(
                            float(time_list[3]) + 0.5)
                except IndexError:
                    self.seconds = 0
                return self.seconds
            else:
                temp_wave = '%(file_path)s_temp.wav' % locals()
                if gst_wav_to_media('untitled', file_path, '', temp_wave,
                                    'false', 'false', '', '600x600', False):
                    self.seconds = sound_length_seconds(temp_wave)
                    if os.path.isfile(temp_wave):
                        os.remove(temp_wave)
                return self.seconds
        else:
            return '0'

    def get_app_meta_string(self,
                            index=13,
                            author='',
                            image='',
                            out_path=''):  # -> str
        '''Return the metadata options for the converter command line.'''
        _xml_transform = XmlTransform()
        album = clean_str(self.get_my_album(False), True)
        if not bool(author):
            author = self.get_my_id(False)
        author = clean_str(author)
        composer = clean_str(self.get_my_composer(False), True)
        genre = clean_str(self.get_my_genre(False), True)
        title = clean_str(self.get_my_title(False), True)
        track = self.get_my_track(False)
        year = self.year
        lame_image = ''
        image_uri = ''
        seconds = str(self.seconds).strip()
        if os.path.isfile(out_path):
            if not self.seconds:
                seconds = self.set_time_meta(out_path)
                if seconds:
                    self.seconds = seconds
                    seconds = str(seconds)
        if image:
            if os.path.splitext(image)[1] in self.image_extensions:
                if os.path.isfile(image):
                    lame_image = ' --ti "%(image)s"' % locals()
                    image_uri = path2url(image)
                else:
                    image = ''
            else:
                image = ''
        gstreamer_meta = ''
        x_album = _xml_transform.clean_for_xml(album)
        x_author = _xml_transform.clean_for_xml(author)
        x_genre = _xml_transform.clean_for_xml(genre)
        x_title = _xml_transform.clean_for_xml(title)
        x_display_path = _xml_transform.clean_for_xml(out_path).replace(
            os.getenv('HOME'), '~')
        out_uri = ''
        if out_path:
            out_uri = path2url(out_path)
        if bool(gst_plugin_path('libgsttaglib')) and bool(
                gst_plugin_path('libgstid3demux')):
            g_album = self.escape_gst_pipe_meta(album)
            g_author = self.escape_gst_pipe_meta(author)
            g_composer = self.escape_gst_pipe_meta(composer)
            g_genre = self.escape_gst_pipe_meta(genre)
            g_title = self.escape_gst_pipe_meta(title)

            # When using Gst with a pipe, the Composer, Track and Date are
            # omitted. See:
            # <https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-good/html/gst-plugins-good-plugins-taginject.html>
            gstreamer_meta = '''! taginject tags="album=\\"%(g_album)s\\",artist=\\"%(g_author)s\\",genre=\\"%(g_genre)s\\",title=\\"%(g_title)s\\"" ! id3v2mux''' % locals(
            )
        if self.title == time_for_title() or not bool(self.title):
            gstreamer_meta = ''

        option = [
            [  # 0
                "Gstreamer", gstreamer_meta
            ],
            [  # 1
                "Avconv or ffmpeg MPEG",
                ''' -metadata album="%(album)s" -metadata artist="%(author)s" -metadata genre="%(genre)s" -metadata title="%(title)s" -metadata track="%(track)s" -metadata Year="%(year)s" -acodec libmp3lame -ab 320k -aq 0 '''
                % locals()
            ],
            [  # 2
                'Avconv or ffmpeg image',
                ' -i "%(image)s" -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (Front)" -y'
                % locals()
            ],
            [  # 3
                "OGG encoder",
                ''' -metadata album='%(album)s' -metadata artist='%(author)s' -metadata genre='%(genre)s' -metadata title='%(title)s' -metadata track='%(track)s' -metadata Year='%(year)s' '''
                % locals()
            ],
            [  # 4
                "Nero encoder",
                ''' -meta:album="%(album)s" -meta:artist="%(author)s" -meta:genre="%(genre)s" -meta:title="%(title)s" -meta:track="%(track)s" -meta:year="%(year)s" '''
                % locals()
            ],
            [  #5
                "Lame (Win)",
                ''' %(lame_image)s --tl "%(album)s" --ta "%(author)s" --tt "%(title)s" --tg "%(genre)s" --tn "%(track)s" --ty %(year)s '''
                % locals()
            ],
            [  # 6
                "Lame (Posix)",
                ''' --vbr-old %(lame_image)s --tl "%(album)s" --ta "%(author)s" --tt "%(title)s" --tg "%(genre)s" --tn "%(track)s" --ty %(year)s '''
                % locals()
            ],
            [  # 7
                "Track", "%(track)s" % locals()
            ],
            [  # 8
                "Album or document",
                "%(album)s" % locals()
            ],
            [  # 9
                "Artist or author",
                "%(author)s" % locals()
            ],
            [  # 10
                "Track title", "%(title)s" % locals()
            ],
            [  # 11
                "Genre", "%(genre)s" % locals()
            ],
            [  #12
                "VLC Playlist",
                '''<?xml version="1.0" encoding="UTF-8"?>
<playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1">
    <title>Playlist</title>
    <trackList>
        <track>
            <location>[%(out_uri)s]</location>
            <creator>%(x_author)s</creator>
            <album>%(x_album)s</album>
            <duration>%(seconds)s500</duration>
            <title>%(x_title)s</title>
            <annotation>%(x_genre)s</annotation>
            <image>%(image_uri)s</image>
            <extension application="http://www.videolan.org/vlc/playlist/0">
                <vlc:id>0</vlc:id>
            </extension>
        </track>
    </trackList>
    <extension application="http://www.videolan.org/vlc/playlist/0">
        <vlc:item tid="0"/>
    </extension>
</playlist>''' % locals()
            ],
            [  #13
                "M3U playlist",
                '''#EXTM3U\nEXTINF:%(seconds)s,%(author)s - %(title)s\n%(out_uri)s\n'''
                % locals()
            ],
            [  #14
                "Metadata",
                ''' * Album: %(album)s\n * Artist: %(author)s\n * Composer: %(composer)s\n * Genre: %(genre)s\n * Title: %(title)s\n * Track: %(track)s\n * Year: %(year)s'''
                % locals()
            ],
            [  #15
                "Avconv or ffmpeg Meta File",
                ''';FFMETADATA1
;https://ffmpeg.org/ffmpeg-all.html#toc-Metadata-1
title=%(title)s
YEAR=%(year)s
ALBUM=%(album)s
ARTIST=%(author)s
GENRE=%(genre)s
track=%(track)s''' % locals()
            ],
            [  #16
                "Avconv or ffmpeg Meta",
                ''' -metadata album="%(album)s" -metadata artist="%(author)s" -metadata genre="%(genre)s" -metadata title="%(title)s" -metadata track="%(track)s" -metadata Year="%(year)s" '''
                % locals()
            ],
            [  # 17
                "XML Track", "%(track)s" % locals()
            ],
            [  # 18
                "XML Album or document",
                "%(x_album)s" % locals()
            ],
            [  # 19
                "XML Artist or author",
                "%(x_author)s" % locals()
            ],
            [  # 20
                "XML Track title",
                "%(x_title)s" % locals()
            ],
            [  # 21
                "XML Genre", "%(x_genre)s" % locals()
            ],
            [  #22
                "Popup Meta",
                '''<b>%(x_album)s</b>\n%(x_title)s \n<i>%(x_display_path)s</i>'''
                % locals()
            ]
        ]
        if index > len(option):
            return option[0]
        try:
            return option[index]
        except:
            return option[0]

    def meta_from_file(self, _file_path='', erase=False):  # -> str
        '''If the specified text file exists, then return the
        contents, otherwise return `''`. '''
        try:
            if os.path.isfile(_file_path):
                f = codecs.open(_file_path, mode='r', encoding='utf-8')
                return_value = f.read()
                f.close()
                if erase:
                    try:
                        os.remove(_file_path)
                    except:
                        pass
                return return_value
            else:
                return ''
        except:
            return ''

    def get_my_id(self, erase=True):  # -> str
        '''
        Returns the user name, author, artist or performer
        '''
        returned_value = self.meta_from_file(get_my_lock('lock.id'), erase)
        if bool(returned_value):
            self.identity = returned_value
        else:
            self.get_defaults()
        return self.identity

    def get_my_composer(self, erase=True):  # -> str
        '''
        Returns the composer name.
        '''
        returned_value = self.meta_from_file(get_my_lock('lock.composer'),
                                             erase)
        if bool(returned_value):
            self.composer = returned_value
        else:
            self.get_defaults()
        return self.composer

    def get_my_title(self, erase=True):  # -> str
        '''
        Returns the song name (a. k. a. title).
        '''
        returned_value = self.meta_from_file(get_my_lock('lock.title'), erase)
        if bool(returned_value):
            self.title = returned_value
        else:
            self.get_defaults()
        return self.title

    def get_my_genre(self, erase=True):  # -> str
        '''
        Returns the song genre.
        '''
        returned_value = self.meta_from_file(get_my_lock('lock.genre'), erase)
        if bool(returned_value):
            self.genre = returned_value
        else:
            self.get_defaults()
        return self.genre

    def get_my_track(self, erase=True):  # -> str
        '''
        Returns the song track number.
        '''
        returned_value = self.meta_from_file(get_my_lock('lock.track'), erase)
        if bool(returned_value):
            self.track = returned_value
        else:
            self.get_defaults()
        return self.track

    def get_my_album(self, erase=True):  # -> str
        '''
        Returns the album name.
        '''
        # If the file is located on a remote url
        # then the file name might be expressed
        # as a URI. Therefore, replace `%20` with
        # a space for the title.
        returned_value = self.meta_from_file(
            get_my_lock(
                'lock.album'), erase).replace('%20', ' ')
        if bool(returned_value):
            self.album = returned_value
        else:
            self.get_defaults()
        return self.album

def clean_temp_files(_out=''):  # -> Bool
    '''Clean text and image files used to create media'''
    try:
        for _temp_file in ['%(_out)s.wav.txt' %locals(),
                           '%(_out)s.txt' %locals(),
                           '%(_out)stemp.lock' %locals(),
                           '%(_out)s.wav.png' %locals(),
                           '%(_out)s.wav.jpg' %locals()]:
            if os.path.isfile(_temp_file):
                os.remove(_temp_file)
        return True
    except:
        pass
    return False
        
def gst_wav_to_media(_title='untitled',
                     _work='',
                     _image='',
                     _out='',
                     _audible='true',
                     _visible='false',
                     _artist='',
                     _dimensions='600x600',
                     _show_meta=True):  # -> bool
    '''
    If `avconv` is not installed and `ffmpeg` is not installed, use
    `gst-launch` to convert media.  Note that gst_wav_to_media omits
    some meta-data (Image, track and year)

    Returns `True` on success, `False` if unable to create new media.
    <https://community.nxp.com/pwmxy87654/attachments/pwmxy87654/imx-processors%40tkb/15/2/i.MX8GStreamerUserGuide.pdf >
    '''
    if have_posix_app('say', False):
        return False
    s_out_extension = ''
    _metas = ImportedMetaData()
    _metas.set_time_meta(_work)

    if _out:
        s_out_extension = os.path.splitext(_out)[1].lower()
    b_audible = lax_bool(_audible)
    b_visible = lax_bool(_visible)
    pipe = ''
    in_uri = ''
    code_pad = ''
    if not os.path.isfile(_work):
        return None
    in_uri = path2url(_work)
    in_pad = ' decodebin ! audioresample '
    if os.path.splitext(_work)[1] == '.wav':
        in_pad = ' wavparse '
    if s_out_extension in ['.mp2', '.mp3']:
        if gst_plugin_path('libgstlame'):
            code_pad = '! lamemp3enc'
    elif s_out_extension in ['.mka', '.mkv']:
        if gst_plugin_path('libgstmatroska'):
            code_pad = '! matroskamux'
    elif s_out_extension == ".flac":
        if gst_plugin_path('libgstflac'):
            code_pad = "! flacenc ! oggmux"
    elif s_out_extension in [".oga", '.ogg']:
        if gst_plugin_path('libgstogg'):
            code_pad = '! vorbisenc ! oggmux'
    elif s_out_extension == '.opus':
        if gst_plugin_path('libgstopus'):
            code_pad = '! opusenc ! oggmux'
    elif s_out_extension == '.spx':
        if gst_plugin_path('libgstspeex'):
            code_pad = '! speexenc ! oggmux'
    elif s_out_extension == '.wav':
        if gst_plugin_path('libgstwavenc'):
            code_pad = '! wavenc'
    if code_pad:
        gmeta = get_meta_data(_metas.i_gst, _artist, _image, _out)
        pipe = '''filesrc location="%(_work)s" ! %(in_pad)s ! audioconvert %(code_pad)s %(gmeta)s ! filesink location="%(_out)s"''' % locals(
        )
        pipe2 = '''filesrc location="%(_work)s" ! %(in_pad)s ! audioconvert %(code_pad)s ! filesink location="%(_out)s"''' % locals(
        )
    if pipe:
        if do_gst_parse_launch(pipe):
            if _show_meta:
                pop_message(
                    app_name(),
                    get_meta_data(_metas.i_popup_meta, _artist, _image, _out),
                    8000)
        else:
            # Try omitting the metadata
            if do_gst_parse_launch(pipe2):
                if _show_meta:
                    pop_message(app_name(), _out, 5000)
            else:
                # Error or incompatible format, so play the file
                if not s_out_extension:
                    s_out_extension = ".wav"
                if s_out_extension == '.wav' and not b_visible:
                    lock_my_lock()
                    if b_audible:
                        play_wav_no_ui(_work)
                    unlock_my_lock()
                elif b_audible:
                    unlock_my_lock()
                    show_with_app(_work)
            unlock_my_lock()
        clean_temp_files(_out)
    else:
        if os.path.isfile(get_my_lock('lock')):
            exit()
        in_uri = path2url(_work)
        # Concise pipe; some sinks can have different settings with a verbose pipee
        pipe = 'playbin uri="%(in_uri)s"' % locals()
        lock_my_lock()
        if os.path.splitext(_work)[1].lower() == '.wav':
            if b_audible:
                if not play_wav_no_ui(_work):
                    do_gst_parse_launch(pipe)
            unlock_my_lock()
        elif b_audible:
            show_with_app(_work)
        return True

    if os.path.isfile(_out) and not bool(in_uri):
        if b_visible and b_audible:
            show_with_app(_out)
        elif b_audible:
            unlock_my_lock()
            gst_wav_to_media(_title, _out, '', _image, 'true', 'false', _artist,
                             _dimensions)
        elif b_visible:
            print('''Play is off - file will not play.
The file was saved to:  %(_out)s''' % locals())
    return True


def vlc_wav_to_media(in_sound_path='',
                     out_sound_path='',
                     _audible='true',
                     _visible='false',
                     allow_linux_snap=False,
                     _show_meta=True):  # -> bool
    '''Converts a wav audio file to a plain mp3 or ogg muxed audio file.
    This conversion does not include meta-data. Retunrs `True` if a new
    file is created, otherwise `False`.'''
    _extension_table = ExtensionTable()
    app = _extension_table.vlc
    if not bool(app):
        if allow_linux_snap:
            if have_posix_app('vlc', True):
                app = 'vlc'
        if not bool(app):
            return False
    elif not os.path.isfile(in_sound_path):
        return False
    elif not bool(out_sound_path):
        return False
    b_audible = lax_bool(_audible)
    b_visible = lax_bool(_visible)
    ext = os.path.splitext(out_sound_path)[1]
    channel_count = ['1', '2'][1]  # mono, stereo
    verbosity = ['', '-vvv '][0]  # no debug, debug
    if ext == '.flac':
        audio_codec = 'flac'
        average_bitrate = '128'
        sample_rate = '44100'
        mux = 'raw'
    elif ext == '.mp3':
        audio_codec = 'mp3'
        average_bitrate = '128'
        sample_rate = '44100'
        mux = 'dummy'
    elif ext in ['.ogg', '.oga']:
        audio_codec = 'vorb'
        average_bitrate = '128'
        sample_rate = '44100'
        mux = 'ogg'
    elif ext == '.opus':
        audio_codec = 'opus'
        average_bitrate = '16'
        sample_rate = '16000'
        mux = 'ogg'
    elif ext == '.wav':
        audio_codec = 's16l'
        average_bitrate = '0'
        sample_rate = '16000'
        mux = 'wav'
    else:
        return False
    command = '''%(app)s "%(in_sound_path)s" --intf dummy %(verbosity)s--sout="#transcode{vcodec=none,acodec=%(audio_codec)s,ab=%(average_bitrate)s,channels=%(channel_count)s,samplerate=%(sample_rate)s}:std{access=file,mux=%(mux)s,dst='%(out_sound_path)s'}" vlc://quit''' % locals(
    )
    if my_os_system(command):
        if _show_meta:
            pop_message(app_name(), out_sound_path, 5000)
        print('''
VideoLAN VLC 
============
* audio codec = '%(audio_codec)s'
* average bitrate = '%(average_bitrate)s'
* channel count = '%(channel_count)s'
* mux = '%(mux)s'
* sample rate = '%(sample_rate)s'
''' % locals())
        if b_visible and b_audible:
            show_with_app(out_sound_path)
        elif b_audible:
            lock_my_lock()
            play_wav_no_ui(out_sound_path)
            unlock_my_lock()
        return True
    return False


def sound_length_seconds(_work):  # -> int
    '''
    Tells approximately how long a sound file is in seconds as an integer
    We round up so that processes that call for sleep have time to finish.
    '''
    _work_ext = os.path.splitext(_work)[1].lower()
    _return_value = 0
    mimetypes.init()
    _mime = "xxz-xzz-no-match"
    if len(_work_ext) != 0:
        try:
            _mime = mimetypes.types_map[_work_ext]
        except IndexError:
            return 0
    if _mime == mimetypes.types_map['.wav']:
        try:
            snd_read = wave.open(_work, 'r')
            _return_value = math.ceil(
                snd_read.getnframes() // snd_read.getframerate()) + 1
            snd_read.close()
        except:
            pass
    elif _mime == mimetypes.types_map['.au']:
        try:
            snd_read = sunau.open(_work, 'r')
            _return_value = math.ceil(
                snd_read.getnframes() // snd_read.getframerate()) + 1
            snd_read.close()
        except:
            pass
    elif _mime == (mimetypes.types_map['.aif'] or
                   _mime == mimetypes.types_map['.aifc']):
        try:
            snd_read = aifc.open(_work, 'r')
            _return_value = math.ceil(
                snd_read.getnframes() // snd_read.getframerate()) + 1
            snd_read.close()
        except:
            pass
    return _return_value


def get_meta_data(_index=0, _artist='', _image='', _work=''):  # -> str
    '''Get a metadata command string for a program.
    * `_index` is an integer that tells which program command format.
    * `_artist` is an author, artist or composer specified
      on the command line.
    + `_image` is the path to a cover image
    + `_work` is the local path to the source sound file.
    '''
    # Look up data
    _metas = ImportedMetaData()
    _metas.set_time_meta(_work)
    # Format the string with tags
    _text = _metas.get_app_meta_string(_index, _artist, _image, _work)[1]
    if bool(_text) and bool(_work):
        _title = _metas.get_app_meta_string(_index, _artist, _image, _work)[0]
        _info = _metas.get_app_meta_string(_metas.i_pretty, _artist, _image,
                                           _work)[1]
        print('\n## %(_title)s ##\n\n%(_info)s' % locals())
    return _text


def wav_to_media(_title='',
                 _work='',
                 _image='',
                 _out='',
                 _audible='',
                 _visible='',
                 _artist='',
                 _dimensions=''):  # -> None
    '''
    wav_to_media
    =========

    Converts a wave audio file to another format and plays a copy.

            _title is brief title
            _work is working file name (wav)
            _image is image to add to video.  Ignored if making audio only
            _out is output file name.( webm, ogg etc.)
            _audible - Do we play the file after conversion?
            _visible - Do we use a GUI or the console?
            _artist - Artist
            _dimensions - Dimensions of poster image '600x600'
    '''
    _metas = ImportedMetaData()
    _metas.set_time_meta(_work)
    _xml_transform = XmlTransform()
    _extension_table = ExtensionTable()
    _out_ext = os.path.splitext(_out)[1].lower()
    _work_ext = os.path.splitext(_work)[1].lower()
    _ffmpeg_avconv = ffmpeg_path()
    if not os.path.isfile(_image):
        # Video encoders fail if there's no image or stream.
        if 'video/' in _extension_table.get_mime(_out):
            _image = app_icon_image('poster-001.png')
    lock_my_lock()
    if len(_dimensions) == 0:
        _dimensions = '600x600'
    # Check for mimetype extensions like `.aif` and `.aiff.`
    mimetypes.init()
    try:
        _meta_data = ''
        if lax_mime_match(_out_ext, '.ogg'):
            # '.ogg', '.oga', '.opus' - 'audio/ogg'
            _meta_data = get_meta_data(_metas.i_ffmpeg_meta, _artist, _out)
            if os.name == 'nt':
                # C:/opt/oggenc2.exe
                # Get oggenc2.exe: http://www.rarewares.org/ogg-oggenc.php
                nt_command = get_nt_path('oggenc2', 'oggenc2')
                if bool(nt_command):
                    nt_command = get_nt_path('oggenc', 'oggenc')
                if nt_command:
                    my_os_system('"%(nt_command)s" -o "%(_out)s" "%(_work)s"' %
                                 locals())
                elif bool(_ffmpeg_avconv):
                    my_os_system(
                        '"%(_ffmpeg_avconv)s" -i "%(_work)s" %(_meta_data)s -acodec libvorbis -ab 320k -aq 0 -y "%(_out)s"'
                        % locals())
            else:
                my_os_system(
                    '"%(_ffmpeg_avconv)s" -i "%(_work)s" %(_meta_data)s -acodec libvorbis -ab 320k -aq 0 -y "%(_out)s"'
                    % locals())
        elif _out_ext in ['.aac']:
            if have_posix_app('afconvert', False):
                my_os_system(
                    'afconvert -f adts -d aac "%(_work)s" "%(_out)s"' % locals())
        elif _out_ext in ['.m4a', 'm4r']:
            if have_posix_app('afconvert', False):
                my_os_system(
                    'afconvert -f m4af -d aac "%(_work)s" "%(_out)s"' % locals())
        elif lax_mime_match(_out_ext, '.mp3'):
            # Try lame for mp3 or 'audio/mpeg' files that haven't been
            #  dealt with above.
            s_lame = ''
            if have_posix_app('lame', False):
                s_lame = 'lame'
            elif have_posix_app('twolame', False) and os.path.splitext(
                    _out)[1] == '.mp2':
                s_lame = 'twolame'
            elif os.name == 'nt':
                if get_nt_path('lame', 'lame'):
                    s_lame = get_nt_path('lame', 'lame')
                elif get_nt_path(
                        'twolame',
                        'twolame') and os.path.splitext(_out)[1] == '.mp2':
                    s_lame = get_nt_path('twolame', 'twolame')

            if bool(s_lame):
                if os.name == 'nt':
                    # See: http://www.rarewares.org/mp3-lame-bundle.php
                    _meta_data = get_meta_data(_metas.i_winlame, _artist, _out)
                    my_os_system(
                        '%(s_lame)s -V 4 %(_meta_data)s "%(_work)s" "%(_out)s"'
                        % locals())
                else:
                    _meta_data = get_meta_data(_metas.i_unixlame, _artist,
                                               _image, _out)
                    my_os_system(
                        '%(s_lame)s %(_meta_data)s "%(_work)s" "%(_out)s"' %
                        locals())
            elif bool(_ffmpeg_avconv):
                if len(_image) != 0:
                    _out_temp = '%(_out)s.mp3' % locals()
                else:
                    _out_temp = _out
                _meta_data = get_meta_data(_metas.i_avconv, _artist, _image,
                                           _out)
                my_os_system(
                    '%(_ffmpeg_avconv)s -i "%(_work)s" %(_meta_data)s "%(_out_temp)s"'
                    % locals())
                if len(_image) != 0:
                    # Add image.  Make a straight copy of the audio
                    # so the quality remains the same.
                    _meta_data = get_meta_data(_metas.i_avimage, _artist,
                                               _image, _out)
                    my_os_system(
                        '%(_ffmpeg_avconv)s -i "%(_out_temp)s" %(_meta_data)s "%(_out)s"'
                        % locals())
                    if os.path.isfile(_out):
                        os.remove(_out_temp)
                    else:
                        os.rename(_out_temp, _out)
        elif lax_mime_match(_out_ext, '.aif'):
            # .aif doesn't have metadata.
            my_os_system('"%(_ffmpeg_avconv)s" -i "%(_work)s" -y "%(_out)s"' %
                         locals())
        elif lax_mime_match(_out_ext, '.flac'):
            # flac - free lossless audio codec.
            _meta_data = get_meta_data(_metas.i_ffmpeg_meta, _artist, _image,
                                       _out)
            # https://ffmpeg.org/ffmpeg-all.html#flac-1
            if os.name == 'nt':
                # The programs is supplied in a zip file.  To use it,
                # extract it to the directory shown.
                # C:/opt/flac.exe
                # See: http://flac.sourceforge.net/
                nt_command = get_nt_path('flac', 'flac')
                if bool(nt_command):
                    my_os_system(
                        '"%(nt_command)s" -f -o "%(_out)s" "%(_work)s"' %
                        locals())
                else:
                    my_os_system(
                        '"%(_ffmpeg_avconv)s" -i "%(_work)s" -af aformat=s16:44100 %(_meta_data)s -y "%(_out)s"'
                        % locals())
            else:
                my_os_system(
                    '"%(_ffmpeg_avconv)s" -i "%(_work)s" -af aformat=s16:44100 %(_meta_data)s -y "%(_out)s"'
                    % locals())
        elif lax_mime_match(_out_ext, '.webm') and bool(_ffmpeg_avconv):
            # Chrome, Firefox (Linux) and totem can open webm directly.
            _meta_data = get_meta_data(_metas.i_ffmpeg_meta, _artist, _out)
            my_os_system(
                '%(_ffmpeg_avconv)s -loop 1 -i "%(_image)s" -i "%(_work)s" -c:v libvpx -r 1 -c:a copy -shortest %(_meta_data)s -acodec libvorbis -ab 320k -aq 0 -auto-alt-ref 0 -y "%(_out)s"'
                % locals())
        elif lax_mime_match(_out_ext, '.ogv') and bool(_ffmpeg_avconv):
            _meta_data = get_meta_data(_metas.i_ffmpeg_meta, _artist, _out)
            my_os_system(
                '%(_ffmpeg_avconv)s -loop 1 -i "%(_image)s" -i "%(_work)s" -c:v libtheora -r 1 -c:a copy -shortest %(_meta_data)s -acodec libvorbis -ab 320k -aq 0 -y "%(_out)s"'
                % locals())
        elif _out_ext in ['.m4v', '.mp4'] and bool(_ffmpeg_avconv):
            _program = 'ffmpeg'
            if 'avconv' in _ffmpeg_avconv.lower():
                _program = 'avconv'
            _meta_data = get_meta_data(_metas.i_avconv, _artist, _out)
            if my_os_system(
                    '%(_ffmpeg_avconv)s -loop 1 -i "%(_image)s" -i "%(_work)s"  -ac 2 -c:v libx264 -r 25 -c:a aac -shortest %(_meta_data)s -y "%(_out)s"'
                    % locals()):
                print(
                    '''WARNING: The %(_program)s encoder uses `libx264` and `aac`
to encode video and audio tracks. Some Windows and MacOS
players cannot play this `video/mp4` file. Try [VideoLan
VLC](https://videolan.org/vlc).''' % locals())
            else:
                print('''FAIL: The %(_program)s app is missing
the `libx264` or `aac` package to convert media to`video/mp4`.''')
        else:
            _out = _work
        if os.path.isfile(_out):
            if not lax_bool(_audible):
                print('''Play is off - file will not play.
'The file was saved to:   %(_out)s''' % locals())
                if have_posix_app('osascript', False):
                    pop_message(
                        app_name(),
                        _out,
                        8000)
                else:
                    pop_message(
                        app_name(),
                        get_meta_data(_metas.i_popup_meta, _artist, _image, _out),
                        8000)
            else:
                # Play the file
                if not lax_bool(_visible):
                    play_wav_no_ui(_out)
                else:
                    show_with_app(_out)
        else:
            print('No output file was created.')
        clean_temp_files(_out)
    except IOError:
        print(app_name() + " Tools execution failed")
        pop_message(app_name(), "python error", 5000)
        sys.exit(2)
    unlock_my_lock()


def clean_str(test_text='', beautify_quotes=True):  #-> str
    '''
    * `test_text` - string to clean
    * `beautify_quotes` - use smart quotes

    Modifies some characters from strings for use in 'song' data.

    For this toolbox, `test_text = 'Blah'`  is good, but `
    test_text = "Blah"` is bad.
    '''
    if not test_text:
        return ''
    _text = test_text
    try:
        if beautify_quotes:
            for quot in [[" '", u" \u2018"], [' "', u' \u201C']]:
                _text = _text.replace(quot[0], quot[1])
        try:
            if beautify_quotes:
                trans_quot = str.maketrans({"'": u"\u2019", '"': u"\u201D"})
                _text = str(_text.translate(trans_quot))
            trans_essentials = str.maketrans({
                "\n": " ",
                "\f": "",
                '\r': '',
                "\t": "",
                '"': " "
            })
            return str(_text.translate(trans_essentials))
        except (AttributeError, NameError):
            if beautify_quotes:
                for quot in [["'", u"\u2019"], ['"', u"\u201D"]]:
                    _text = _text.replace(quot[0], quot[1])
            for pair1 in [['\n', ' '], ['\f', ''], ['\r', ''], ['\t', ' '],
                          ['"', ' ']]:
                _text = _text.replace(pair1[0], pair1[1])
            return _text
    except UnicodeDecodeError:
        print(_text + ' error in readtexttools.clean_str')
    return _text


def count_items_in_dir(_dir=''):
    '''Count many items are in a directory'''
    _init = 0
    if not os.path.isdir(_dir):
        return _init
    for _path in os.listdir(_dir):
        if os.path.exists(os.path.join(_dir, _path)):
            _init += 1
    return _init


def time_for_title():  # -> str
    '''
    Returns an unambiguous time expression for a title in an
    international format
    '''
    return time.strftime('%Y-%m-%d_%H:%M:%S-%Z')


def date_for_album():  # -> str
    '''
    Returns a date expression for an album in an international
    format.
    '''
    return time.strftime('%Y-%m-%d')


def check_title(_title='', _tool=''):  #-> str
    '''
    If it is not a working title, replace title.
    '''
    try:
        if len(_title) == 0:
            return _tool + u' ' + time_for_title()
        else:
            return _title
    except UnicodeDecodeError:
        return _tool + u' ' + time_for_title()


def check_artist(_artist):  # -> str
    '''
    If not a working artist, replaces artist with user name.
    '''
    _metas = ImportedMetaData()

    try:
        if len(_artist) != 0:
            return _artist
        else:
            return _metas.get_my_id(False)
    except UnicodeDecodeError:
        return _metas.get_my_id(False)


def lock_my_lock():  # -> None
    '''
    Create a file that informs the world that the application.
    is at work.
    '''
    write_plain_text_file(get_my_lock('lock'), app_signature())


def unlock_my_lock():  # -> None
    '''
    Create a file that informs the world that the application
    is finished.
    '''
    try:
        os.remove(get_my_lock('lock'))
    except:
        pass


def get_my_lock(_lock=''):  # -> str
    '''
    Returns path to a temporary directory plus a lock file name.
    Use an value like 'lock' for `_lock`.  You can use more than
    one lock if you use different values for `_lock`.
    '''
    if not _lock:
        return ''
    p_lock = '.%(_lock)s' % locals()
    app_sign = app_signature()
    env_path = os.getenv('READTEXTTEMP')

    if env_path is not None and os.path.isdir(env_path) and os.access(
            env_path, os.W_OK):
        if os.name == 'nt':
            return os.path.join(env_path,
                                app_sign + '.' + os.getenv('USERNAME') + p_lock)
        elif have_posix_app('say', False):
            if bool(os.getenv('USERNAME')):
                return os.path.join(
                    env_path, app_sign + '.' + os.getenv('USERNAME') + p_lock)
            else:
                # MacOS 11
                return os.path.join(env_path,
                                    app_sign + '.' + os.getenv('USER') + p_lock)
        else:
            return os.path.join(env_path,
                                app_sign + '.' + os.getenv('USER') + p_lock)
    elif os.name == 'nt':
        return os.path.join(os.getenv('TMP'),
                            app_sign + '.' + os.getenv('USERNAME') + p_lock)
    elif have_posix_app('say', False):
        if bool(os.getenv("TMPDIR")):
            mac_temp = os.getenv("TMPDIR")
        elif bool(os.getenv("TMP")):
            mac_temp = os.getenv("TMP")
        else:
            mac_temp = os.join(os.getenv("HOME"), "_temporary")
        if bool(os.getenv("USERNAME")):
            mac_user = os.getenv("USERNAME")
        elif bool(os.getenv("USER")):
            mac_user = os.getenv("USER")
        else:
            mac_user = "MacUser"
        return os.path.join(mac_temp, app_sign + '.' + mac_user + p_lock)
    else:
        if os.path.isdir('/tmp') and os.access('/tmp', os.W_OK):
            return os.path.join('/tmp',
                                app_sign + '.' + os.getenv('USER') + p_lock)
        elif os.path.isdir(os.path.join(
                os.getenv('HOME'), '.config/')) and os.access(
                    os.path.join(os.getenv('HOME'), '.config/'), os.W_OK):
            return os.path.join(
                os.getenv('HOME'),
                '.config/' + app_sign + '.' + os.getenv('USER') + p_lock)
        else:
            return os.path.join(os.getenv('HOME'),
                                app_sign + '.' + os.getenv('USER') + p_lock)
    return ''


def show_with_app(_out):  # -> bool
    '''
    Same as double clicking the document - opens in default
    application.
    '''
    if have_posix_app('say', False):
        # MacOS
        _command = 'open "%(_out)s"' % locals()
        my_os_system(_command)
        return True
    elif os.name == 'nt':
        # Windows
        os.startfile(_out)
        return True
    else:
        for opener in ['xdg-open', 'gnome-open', 'kde-open']:
            if have_posix_app(opener, True):
                _open = opener
                my_os_system('%(_open)s "%(_out)s"' % locals())
                return True
    return False


def path2url(_file_path):  # -> str
    '''Convert a file path to a file URL'''
    try:
        return urlparse.urljoin('file:', urllib.pathname2url(_file_path))
    except NameError:
        # Fall back works on Posix
        return ''.join(['file://', _file_path.replace(' ', '%20')])


def play_wav_no_ui(file_path=''):  # -> bool
    '''
    Opens using command line shell.
    '''
    _command = ''
    a_app = 'System audio'
    uri_path = path2url(file_path)
    _extension_table = ExtensionTable()
    if os.name == 'nt':
        # Windows
        if os.path.splitext(file_path)[1].lower() in [
                '.m4a', '.mp3', '.mp4', '.oga', '.ogg', '.opus', '.spx',
                '.webm']:
            os.startfile(file_path)
            return True
        else:
            try:
                import winsound
                winsound.PlaySound(file_path,
                                   winsound.SND_FILENAME | winsound.SND_NOWAIT)
                return True
            except:
                try:
                    os.startfile(file_path)
                    return True
                except:
                    return False
    else:
        _apt_get = 0
        _app = 1
        _command = 2
        _universal_play = 3  # verified to play compressed formats
        players = [
            ['afplay', 'afplay',  # Darwin
             ' "%(file_path)s"' % locals(), True],
            ['esdplay', 'esdplay',
             ' "%(file_path)s"' % locals(), False],
            ['ossplay', 'ossplay',
             ' "%(file_path)s"' % locals(), False],
            ['paplay', 'paplay',
             ' "%(file_path)s"' % locals(), False],
            ['artsplay', 'artsplay',
             ' "%(file_path)s"' % locals(), False],
            ['roarcat', 'roarcat',
             ' "%(file_path)s"' % locals(), False],
            [
                'roarcatplay', 'roarcatplay',
                ' "%(file_path)s"' % locals(), False
            ],
            ['aplay', 'aplay',
             ' --nonblock "%(file_path)s"' % locals(), False],
            [
                'ffmpeg', 'ffplay',
                ' -autoexit -hide_banner -loglevel info -nostats -nodisp "%(file_path)s"'
                % locals(), True
            ],
            [
                'avconv', 'avplay',
                ' -autoexit -nodisp "%(file_path)s"' % locals(), True
            ],
            [
                'vlc', 'vlc',
                ' --intf dummy %(uri_path)s vlc://quit ' % locals(), True
            ],
            [
                'gstreamer1.0-tools', 'gst-launch-1.0',
                'playbin uri="%(uri_path)s" ' % locals(), True
            ]
        ]
        for player in players:
            if os.path.isfile('/usr/bin/' + player[_app]):
                if os.path.splitext(file_path)[1].lower(
                ) == '.wav' or player[_universal_play]:
                    a_app = player[_app]
                    a_command = player[_command]
                    _command = '%(a_app)s %(a_command)s' % locals()
                    break
        if not _command:
            _apt_get_list = ''
            for app in players:
                _apt_get_list = '\n * '.join([_apt_get_list, app[_apt_get]])
            print('You need an audio player:%(_apt_get_list)s' % locals())

    if _command:
        display_file = os.path.split(file_path)[1]
        if os.path.getsize(file_path) == 0:
            print('''[>]  %(a_app)s cannot play `%(display_file)s`''' %locals())
            return True
        print('[>] %(a_app)s playing `%(display_file)s`' %locals())
        my_os_system(_command)
        return True
    return False


def main():  # -> NoReturn
    '''
    Converts the input wav sound to another format.  Ffmpeg
    can include a still frame movie if you include an image.
    '''
    if sys.argv[-1] == sys.argv[0]:
        usage()
        sys.exit(0)
    _work = ''
    _visible = ''
    _audible = ''
    _image = ''
    _out = ''
    _artist = ''
    _dimensions = '600x600'
    _title = 'Video memo'
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hovaistnd', [
            'help', 'output=', 'visible=', 'audible=', 'image=', 'sound=',
            'title=', 'artist=', 'dimensions='
        ])
    except getopt.GetoptError:
        # print help information and exit
        print('An option was not recognized')
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif o in ('-o', '--output'):
            _out = a
        elif o in ('-v', '--visible'):
            _visible = a
        elif o in ('-a', '--audible'):
            _audible = a
        elif o in ('-i', '--image'):
            _image = a
        elif o in ('-s', '--sound'):
            _work = a
        elif o in ('-t', '--title'):
            _title = a
        elif o in ('-n', '--artist'):
            _artist = a
        elif o in ('-d', '--dimensions'):
            _dimensions = a
        else:
            assert False, 'unhandled option'
            usage()
    if len(_out) == 0 or len(_work) == 0:
        usage()

    else:
        process_wav_media(_title, _work, _image, _out, _audible, _visible,
                          _artist, _dimensions)
    sys.exit(0)


if __name__ == '__main__':
    main()
###############################################################################

# Read Text Extension
#
# Copyright And License
#
# (c) 2022 [James Holgate Vancouver, CANADA](readtextextension(a)outlook.com)
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
