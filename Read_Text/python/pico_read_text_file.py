#!/usr/bin/env python
# -*- coding: UTF-8-*-
"""
Pico
====

Reads a text file using pico2wave and a media player.

The SVOX Pico engine is a software speech synthesizer for German, English (GB
and US), Spanish, French and Italian.

SVOX produces a clear and distinct speech output made possible by the use of
Hidden Markov Model (HMM) algorithms.

[SVOX Pico](http://dafpolo.free.fr/telecharger/svoxpico/SVOX_Pico_Manual.pdf)

Install `pico2wave` using a package manager to install the following packages:

    libttspico0
    libttspico-utils
    libttspico-data

Due to license restrictions,the packages are formally part of Debian's
non-free category rather than Debian proper ("main"). The packages are also
available in Ubuntu's multiverse repository, and might be available in third
party repositories on other Linux platforms.

For systems that can not use `apt` package manager, see the `picotts-install.sh`
shell script at <https://github.com/stevenmirabito/asterisk-picotts/>.

Read Selection... Dialog setup:
-------------------------------

External program:

        /usr/bin/python3

Command line options (default):

        "(PICO_READ_TEXT_PY)" --language (SELECTION_LANGUAGE_CODE) "(TMP)"

or (save as a .wav file in the home directory):

         "(PICO_READ_TEXT_PY)" --language (SELECTION_LANGUAGE_CODE) \
           --output "(HOME)(NOW).wav" "(TMP)"

or (speak more slowly with a lowered pitch):

        "(PICO_READ_TEXT_PY)" --language (SELECTION_LANGUAGE_CODE) \
          --rate 80% --pitch 80% "(TMP)"

See the manual page for `pico2wave` for more detailed information

[Read Text Extension](http://sites.google.com/site/readtextextension/)

Copyright (c) 2011 - 2025 James Holgate

"""


from __future__ import absolute_import, division, print_function, unicode_literals

try:
    import getopt
except (ImportError, AssertionError, AttributeError):
    exit()
import os
import sys
import readtexttools


def usage():
    """
    Command line help
    """
    print(
        """Pico Read Text
==============

Reads a text file using pico2wave and a media player.

Converts format with `avconv`, `lame`, `faac` or `ffmpeg`.

Usage
-----

     pico_read_text_file.py "input.txt"
     pico_read_text_file.py --language [de|en|en-GB|es|fr|it] "input.txt"
     pico_read_text_file.py --visible "false" "input.txt"
     pico_read_text_file.py --rate=100% --pitch=100% "input.txt"
     pico_read_text_file.py --output "output.wav" "input.txt"
     pico_read_text_file.py --output "output.[m4a|mp2|mp3|ogg]" "input.txt"
     pico_read_text_file.py --output "output.[avi|webm]"
       --image "input.[png|jpg] "input.txt"
     pico_read_text_file.py --audible "false" --output "output.wav"
       "input.txt" """
    )


def picoread(
    _text="",
    _language="en-US",
    _visible="false",
    _audible="true",
    _media_file="",
    _image="",
    _title="",
    _artist="",
    _dimensions="600x600",
):  # -> bool
    """
    _text - Actual text to speak. The file must be written as utf-8.
    _language - Supported two or four letter language code - defaults to US English
    _visible- Use a graphic media player, or False for invisible player
    _media_file - Name of desired output media file
    _audible - If false, then don't play the sound file
    _image - a .png or .jpg file if required.
    _title - Commentary or title for post processing
    _artist - Artist or Author
    _dimensions - Dimensions to scale photo '600x600'
    """
    picoread = False
    _out_file = ""
    if _language[:2].lower() == "de":
        _lang = "de-DE"
    elif _language[:2].lower() == "en":
        if _language[-2:].upper() in [
            "AU",
            "BD",
            "BS",
            "GB",
            "GH",
            "HK",
            "IE",
            "IN",
            "JM",
            "NZ",
            "PK",
            "SA",
            "TT",
        ]:
            _lang = "en-GB"
        else:
            _lang = "en-US"
    elif _language[:2].lower() == "es":
        _lang = "es-ES"
    elif _language[:2].lower() == "fr":
        _lang = "fr-FR"
    elif _language[:2].lower() == "it":
        _lang = "it-IT"
    else:
        _lang = "en-US"
    # Determine the output file name
    _out_file = readtexttools.get_work_file_path(_media_file, _image, "OUT")
    # Determine the temporary file name
    _work_file = readtexttools.get_work_file_path(_media_file, _image, "TEMP")
    # Delete old versions
    if os.path.isfile(_work_file):
        os.remove(_work_file)
    if os.path.isfile(_out_file):
        os.remove(_out_file)
    try:
        if os.name == "nt":
            if readtexttools.is_container_instance():
                return False
            _command = readtexttools.get_nt_path("opt/picosh.exe")
            if "de" in _lang.lower():
                _os_command = '{0} -v de-DE_gl0 "{1}" "{2}"'.format(
                    _command, _text, _work_file
                )
            else:  # Pico for Windows defaults to British English
                _os_command = '{0} "{1}" "{2}"'.format(_command, _text, _work_file)
        else:
            _command = "pico2wave"
            _os_command = '{0} -l {1} -w "{2}"  {3}'.format(
                _command, _lang, _work_file, _text
            )
        if readtexttools.my_os_system(_os_command):
            if os.path.getsize(os.path.realpath(_work_file)) == 0:
                return False
            return bool(
                readtexttools.process_wav_media(
                    _title,
                    _work_file,
                    _image,
                    _out_file,
                    _audible,
                    _visible,
                    _artist,
                    _dimensions,
                )
            )
    except IOError:
        print("I was unable to read!")
        usage()
    return False


def main():  # -> NoReturn
    """Pico read text tools"""
    _imported_meta = readtexttools.ImportedMetaData()
    _language = "en-US"
    _output = ""
    _visible = ""
    _audible = ""
    _strict = "false"
    _text = ""
    _rate = "100%"
    _pitch = "100%"
    _image = ""
    _title = ""
    _artist = ""
    _dimensions = "600x600"
    _xml_transform = readtexttools.XmlTransform()
    _file_path = sys.argv[-1]
    if not os.path.isfile(_file_path):
        sys.exit(0)
    if sys.argv[-1] == sys.argv[0]:
        usage()
        sys.exit(0)
    elif not os.path.isfile("/usr/bin/pico2wave"):
        print("Please install libttspico-utils.")
        usage()
        sys.exit(0)
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "ovalrpitndh",
            [
                "output=",
                "visible=",
                "audible=",
                "language=",
                "rate=",
                "pitch=",
                "image=",
                "title=",
                "artist=",
                "dimensions=",
                "help",
            ],
        )
    except getopt.GetoptError:
        # print help information and exit
        print("option -a not recognized")
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-o", "--output"):
            _output = a
        elif o in ("-v", "--visible"):
            _visible = a
        elif o in ("-a", "--audible"):
            _audible = a
        elif o in ("-l", "--language"):
            _language = a
            if _language.startswith("zxx"):
                _language = "en-US"
                default_lang = readtexttools.default_lang()
                if default_lang.split("_")[0] in ["de", "en", "es", "fr", "it"]:
                    _language = default_lang.replace("_", "-")
        elif o in ("-r", "--rate"):
            _rate = a
        elif o in ("-p", "--pitch"):
            _pitch = a
        elif o in ("-s", "--strict"):
            _strict = a
        elif o in ("-i", "--image"):
            _image = a
        elif o in ("-t", "--title"):
            _title = a
        elif o in ("-n", "--artist"):
            _artist = a
        elif o in ("-d", "--dimensions"):
            _dimensions = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        else:
            assert False, "unhandled option"
    _text = _imported_meta.meta_from_file(_file_path)
    if len(_text) != 0:
        if not _language[:2].lower() in ["de", "es", "en", "fr", "it"]:
            _language = "en-US"
        _text = readtexttools.local_pronunciation(
            _language, _text, "svox_pico", "SVOX_PICO_USER_DIRECTORY", False
        )[0]
        if _pitch == "100%" and _rate == "100%":
            _text = _text.replace('"', '\\"')
            _text = readtexttools.strip_mojibake(_language, _text)
            _pico_text = '"{}"'.format(_text)
        else:
            _text = readtexttools.strip_mojibake(_language, _text)
            _text = _xml_transform.clean_for_xml(
                _text.strip(), readtexttools.lax_bool(_strict)
            )
            _pico_text = '''"<speed level = '{}'>
<pitch level = '{}'>'{}</pitch></speed>"'''.format(
                _rate, _pitch, _text
            )
    if len(_pico_text) != 0:
        _artist_ok = readtexttools.check_artist(_artist)
        _title_ok = readtexttools.check_title(_title, "pico")
        picoread(
            _pico_text,
            _language,
            _visible,
            _audible,
            _output,
            _image,
            _title_ok,
            _artist_ok,
            _dimensions,
        )
    sys.exit(0)


if __name__ == "__main__":
    main()
