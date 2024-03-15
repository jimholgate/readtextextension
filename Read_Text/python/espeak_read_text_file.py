#!/usr/bin/env python
# -*- coding: UTF-8-*-
"""
Read text
=========

Reads a text file using espeak, mbrola and a media player.

The espeak program is a software speech synthesizer.
The mbrola synthesiser can improve the naturalness of speech.  However, it
has licensing restrictions, and is not part of Debian's main repository.
Ubuntu makes mbrola and mbrola voices available in the multiverse repository.

Install mbrola by installing mbrola using your package manager or downloading
the mbrola binary and installing it.  Download mbrola voices and copy or link
the dictionary files into the appropriate directory. For example:

        /usr/share/mbrola/voices (Linux, OSX)
        C:/Program Files (x86)/eSpeak/espeak-data (Windows 64 bit)
        C:/Program Files/eSpeak/espeak-data (Windows 32 bit)

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

        "(ESPEAK_READ_TEXT_PY)" --language=(SELECTION_LANGUAGE_CODE)
          --output="(HOME)(NOW).wav" "(TMP)"

or (speak more slowly with a lowered pitch):

        "(ESPEAK_READ_TEXT_PY)" --language=(SELECTION_LANGUAGE_CODE)
          --rate=80% --pitch=80% "(TMP)"

See the manual page for `espeak` for more detailed information

[Read Text Extension](http://sites.google.com/site/readtextextension/)

Copyright (c) 2011 - 2024 James Holgate

"""
from __future__ import absolute_import, division, print_function, unicode_literals
import getopt
import math
import os
import sys
import readtexttools
import find_replace_phonemes


def usage():
    """
    Command line help
    """
    print(
        """
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
"""
    )


def espeak_path():  # -> str
    """Returns path to espeak program, name or `''` if it cannot be found."""
    if os.name == "nt":
        _app = "eSpeak/command_line/espeak.exe"
        return readtexttools.get_nt_path(_app)
    else:
        for app_name in ["espeak-ng", "speak-ng", "espeak"]:
            if readtexttools.have_posix_app(app_name, False):
                return app_name
    return ""


def espeak_ng_list():  # -> list(str)
    """Return list of `espeak-ng` dictionary language codes like `en` and
    `de`."""
    _ng_list = []
    _dir = readtexttools.linux_machine_dir_path("espeak-ng-data")
    if len(_dir) == 0:
        return _ng_list
    _dir = os.listdir(_dir)
    for _item in _dir:
        if _item.endswith("_dict"):
            _ng_list.append(_item[:-5])
    return sorted(_ng_list)


def espk_languages():  # -> list[str]
    """If using `espeak-ng`, return a language_list of voices that `espeak-ng`
    supports, otherwise return a list of supported`espeak` voices.
    """
    _app_name = espeak_path()
    if len(_app_name) == 0:
        return []
    _imported_meta = readtexttools.ImportedMetaData()
    _reported_langs = []
    _espk_lang = _imported_meta.execute_command(
        "{0} --voices".format(_app_name)
    ).replace("  ", "\t")
    if "Ukrainian" in _espk_lang:  # espeak-ng Debian 12 (bookworm) or newer
        for _line in _espk_lang.splitlines():
            if _line.count("\t") != 0:
                _reported_langs.append(_line.split("\t")[1])
    if _app_name.count("-ng") != 0:
        _ng_list = espeak_ng_list()
        if len(_ng_list) != 0:
            return _ng_list
        return [
            "af",
            "am",
            "an",
            "ar",
            "as",
            "az",
            "ba",
            "be",
            "bg",
            "bn",
            "bpy",
            "bs",
            "ca",
            "chr",
            "cmn",
            "cs",
            "cv",
            "cy",
            "da",
            "de",
            "el",
            "en",
            "eo",
            "es",
            "et",
            "eu",
            "fa",
            "fi",
            "fr",
            "ga",
            "gd",
            "gn",
            "grc",
            "gu",
            "hak",
            "haw",
            "he",
            "hi",
            "hr",
            "ht",
            "hu",
            "hy",
            "ia",
            "id",
            "io",
            "is",
            "it",
            "ja",
            "jbo",
            "ka",
            "kk",
            "kl",
            "kn",
            "ko",
            "kok",
            "ku",
            "ky",
            "la",
            "lb",
            "lfn",
            "lt",
            "lv",
            "mi",
            "mk",
            "ml",
            "mr",
            "ms",
            "mt",
            "my",
            "nci",
            "ne",
            "nl",
            "no",
            "nog",
            "om",
            "or",
            "pa",
            "pap",
            "piqd",
            "pl",
            "pt",
            "py",
            "qdb",
            "qu",
            "quc",
            "qya",
            "ro",
            "ru",
            "sd",
            "shn",
            "si",
            "sjn",
            "sk",
            "sl",
            "smj",
            "sq",
            "sr",
            "sv",
            "sw",
            "ta",
            "te",
            "th",
            "tk",
            "tn",
            "tr",
            "tt",
            "ug",
            "uk",
            "ur",
            "uz",
            "vi",
            "yue",
        ] + _reported_langs
    return [
        "af",
        "bs",
        "ca",
        "cs",
        "cy",
        "da",
        "de",
        "el",
        "eo",
        "fi",
        "fr",
        "hi",
        "hr",
        "hu",
        "hy",
        "id",
        "is",
        "it",
        "ku",
        "la",
        "lv",
        "mk",
        "nl",
        "pl",
        "ro",
        "ru",
        "sk",
        "sq",
        "sr",
        "sv",
        "sw",
        "ta",
        "tr",
        "vi",
    ] + _reported_langs


def espkread(
    _text_path,
    _lang,
    _visible,
    _audible,
    _tmp0,
    _image,
    _title,
    _post_process,
    _author,
    _dimensions,
    _ipitch,
    _irate,
):  # -> int
    """
    Creates a temporary speech-synthesis sound file and optionally
    reads the file aloud.

    + `_text_path` - Name of text file to speak
    + `_lang` - Supported two or four letter language code - defaults to US English
    + `_visible` - Use a graphic media player, or False for invisible player
    + `_tmp0` - Name of desired output media file
    + `_audible` - If false, then don't play the sound file
    + `_image` - a .png or .jpg file if required.
    + `_title` - Commentary or title for post processing
    + `_post_process` - Get information, play file, or convert a file
    + `_author` - Artist or Author
    + `_dimensions` - Dimensions to scale photo '600x600'
    + `_ipitch` - pitch value from 5 to 100, default 50
    + `_irate` - rate value from 20 to 640, default 160
    """
    _imported_meta = readtexttools.ImportedMetaData()
    _out_file = ""
    _pitch = str(_ipitch)
    _rate = str(_irate)
    _rate = "100"
    _concise_lang = _lang.split("-")[0].split("_")[0].lower()
    _app_name = espeak_path()
    _voice = ""
    _command = ""
    if _concise_lang in ["de"]:
        s = "de"
    elif _concise_lang in ["en"]:
        if _lang[-2:].upper() in [
            "AU",
            "BD",
            "BS",
            "CA",
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
            s = "en"
        else:
            s = "en-us"
    elif _concise_lang in ["es"]:
        if _lang[-2:].upper() in ["ES"]:
            s = "es"
        elif _lang[-2:].upper() in ["MX"]:
            s = "es-mx"
        else:
            s = "es-la"
    elif _concise_lang in ["nb"]:
        # *Office uses language code for Norwegian Bokmal - nb
        #  NO is the country code for Norway, not an official language code.
        s = "no"
    elif _concise_lang in ["pt"]:
        if _lang[-2:].upper() in ["PT"]:
            s = "pt-pt"
        else:
            s = "pt"
    elif _concise_lang in ["zh"]:
        if _lang[-2:].upper() in ["HK", "MO"]:
            # Yue is official language in Hong Kong & Macau
            s = "zh-yue"
        else:
            s = "zh"
    elif _concise_lang in espk_languages():
        s = _concise_lang
    else:
        print(
            """`espeak_read_text_file.py` says:
`{0}` is an unsupported language.  Exiting.""".format(_lang)
        )
        return 0
    _voice = s  # standard espeak dictionary
    if _post_process == "process_wav_media":
        # If an mbrola dictionary is available for the language, use it.
        # If not use the default.  If there are several compatible mbrola
        # voices, this python script will choose the first one - for example:
        # de2 instead of de7.
        #
        # In the `a0` list, `a2` is the locally installed language abbreviation;
        # `a1` is the equivalent ISO 639-1 standard for languages, except in
        # the cases of pt-PT and en-US, which include a regional ISO code.
        a0 = [
            {"a2": "af1", "a1": "af"},
            {"a2": "br1", "a1": "pt"},
            {"a2": "br3", "a1": "pt"},
            {"a2": "br4", "a1": "pt"},
            {"a2": "cr1", "a1": "hr"},
            {"a2": "cz2", "a1": "cs"},
            {"a2": "de2", "a1": "de"},
            {"a2": "de4", "a1": "de"},
            {"a2": "de5", "a1": "de"},
            {"a2": "de6", "a1": "de"},
            {"a2": "de7", "a1": "de"},
            {"a2": "en1", "a1": "en"},
            {"a2": "es1", "a1": "es"},
            {"a2": "es2", "a1": "es"},
            {"a2": "fr1", "a1": "fr"},
            {"a2": "fr4", "a1": "fr"},
            {"a2": "gr2", "a1": "el"},
            {"a2": "hu1", "a1": "hu"},
            {"a2": "id1", "a1": "id"},
            {"a2": "it3", "a1": "it"},
            {"a2": "it4", "a1": "it"},
            {"a2": "la2", "a1": "la"},
            {"a2": "nl2", "a1": "nl"},
            {"a2": "pl1", "a1": "pl"},
            {"a2": "pt1", "a1": "pt-pt"},
            {"a2": "ro1", "a1": "ro"},
            {"a2": "sw1", "a1": "sv"},
            {"a2": "sw2", "a1": "sv"},
            {"a2": "tr1", "a1": "tr"},
            {"a2": "tr2", "a1": "tr"},
            {"a2": "us1", "a1": "en-us"},
            {"a2": "us2", "a1": "en-us"},
            {"a2": "us3", "a1": "en-us"},
            {"a2": "en1", "a1": "en-us"},
        ]

        for i in range(len(a0)):
            # Identify an mbrola dict if it is installed

            if a0[i]["a1"] == s:
                if os.name == "nt":
                    if os.path.isfile(
                        os.path.join(
                            os.getenv("ProgramFiles"),
                            "eSpeak/espeak-data/mbrola",
                            a0[i]["a2"],
                        )
                    ):
                        _voice = "mb-" + a0[i]["a2"]
                        break
                    elif os.getenv("ProgramFiles(x86)"):
                        _pfx86 = os.getenv("ProgramFiles(x86)")
                        _mbrola = "eSpeak/espeak-data/mbrola"
                        if os.path.isfile(os.path.join(_pfx86, _mbrola, a0[i]["a2"])):
                            _voice = "mb-" + a0[i]["a2"]
                            break
                else:
                    if os.path.isfile(
                        os.path.join("/usr/share/mbrola/voices", a0[i]["a2"])
                    ):
                        _voice = "mb-" + a0[i]["a2"]
                        break
                    elif os.path.isfile(
                        os.path.join("/usr/share/mbrola/", a0[i]["a2"], a0[i]["a2"])
                    ):
                        _voice = "mb-" + a0[i]["a2"]
                        break
    # Determine the output file name
    _out_file = readtexttools.get_work_file_path(_tmp0, _image, "OUT")
    # Determine the temporary file name
    _work_file = readtexttools.get_work_file_path(_tmp0, _image, "TEMP")

    # Remove old files.
    if os.path.isfile(_work_file):
        os.remove(_work_file)
    if os.path.isfile(_out_file):
        os.remove(_out_file)
    try:
        if bool(readtexttools.gst_plugin_path("libgstespeak")):
            print(readtexttools.gst_plugin_path("libgstespeak"))
        # espeak must be in your system's path
        # for example: /usr/bin/ or /usr/local/bin/
        _app = espeak_path()
        if bool(_app):
            if sys.version_info >= (3, 6):
                find_replace_phonemes.fix_up_text_file(
                    _text_path, "", _lang, "default", "SPEECH_USER_DIRECTORY", False
                )
            _command = "".join(
                [
                    '"',
                    _app,
                    '" -b 1 -p ',
                    _pitch,
                    " -s ",
                    _rate,
                    " -v ",
                    _voice,
                    ' -w "',
                    _work_file,
                    '" -f "',
                    _text_path,
                    '"',
                ]
            )
        elif bool(readtexttools.gst_plugin_path("libgstespeak")):
            if not readtexttools.have_posix_app("gst-launch-1.0", False):
                return 0
            elif os.path.isfile(readtexttools.get_my_lock("lock")):
                # User requested play, but action is locked
                return 0
            elif bool(_imported_meta.execute_command("ps -a | grep gst-launch-1.0")):
                # Program is currently running;
                return 0
            # Fall back - no application found, so use gst-launch to synthesise
            # text from the text file.
            _app = "gst-launch-1.0"
            _content = _imported_meta.meta_from_file(_text_path)
            _content = readtexttools.local_pronunciation(
                _lang, _content, "default", "SPEECH_USER_DIRECTORY", False
            )[0]
            _content = _imported_meta.escape_gst_pipe_meta(_content)
            _command = (
                '{0} espeak text="{1}" voice={2} ! autoaudiosink'.format(
                    _app, _content, _voice
                    )
            )
            _post_process = None
        if not bool(_app):
            return 0
        readtexttools.my_os_system(_command)
        if not bool(_post_process):
            readtexttools.unlock_my_lock()
        elif _post_process == "process_wav_media":
            if not os.path.isfile(_work_file):
                return 0
            if os.path.getsize(_work_file) == 0:
                return 0
            if bool(
                readtexttools.process_wav_media(
                    _title,
                    _work_file,
                    _image,
                    _out_file,
                    _audible,
                    _visible,
                    _author,
                    _dimensions,
                )
            ):
                return readtexttools.sound_length_seconds(_work_file)
        elif _post_process == "show_sound_length_seconds":
            _seconds = readtexttools.sound_length_seconds(_work_file)
            print("show_sound_length_seconds")
            print(_seconds)
            print("-----------------------------------------------------")
            return _seconds
    except (IOError, OSError):
        print("I was unable to use espeak and read text tools!")
        usage()
        return 0


def _espeak_rate(sA):
    """
    sA - rate expressed as a percentage.
    Use '100%' for default rate of 160 words per minute (wpm).
    Returns rate between 20 and 640.
    """
    i1 = 0
    i2 = 0
    _minval = 20
    _maxval = 640
    _myval = 160
    s1 = ""

    try:
        if "%" in sA:
            s1 = sA.replace("%", "")
            i1 = float(s1) if "." in s1 else int(s1) / 100
            i2 = math.ceil(i1 * _myval)
        else:
            i1 = float(sA) if "." in sA else int(sA)
            i2 = math.ceil(i1)
    except TypeError:
        print("I was unable to determine espeak rate!")
    if i2 <= _minval:
        _myval = _minval
    elif i2 >= _maxval:
        _myval = _maxval
    else:
        _myval = i2
    return _myval


def _espeak_pitch(sA):
    """
    sA - Pitch expressed as a percentage.
    Use '100%' for default Pitch of 50.
    "aah" pitch: 0% = a1, 50% = b1, 100% = e2, 200% = d3#
    Returns pitch value between 0 and 100.
    """
    i1 = 0
    i2 = 0
    _minval = 0
    _maxval = 100
    _myval = 50
    s1 = ""

    try:
        if "%" in sA:
            s1 = sA.replace("%", "")
            i1 = float(s1) if "." in s1 else int(s1) / 100
            i2 = math.ceil(i1 * _myval)
        else:
            i1 = float(sA) if "." in sA else int(sA)
            i2 = math.ceil(i1)
    except TypeError:
        print("I was unable to determine espeak pitch!")
    if i2 <= _minval:
        _myval = _minval
    elif i2 >= _maxval:
        _myval = _maxval
    else:
        _myval = i2
    return _myval


def main():  # -> NoReturn
    """Use espeak or espeak-ng"""
    _xml_tool = readtexttools.XmlTransform()
    _ipitch = 50
    _irate = 160
    _lang = "en-US"
    _wave = ""
    _visible = ""
    _audible = ""
    _rate_percent = "100%"
    _pitch_percent = "100%"
    _image = ""
    _title = ""
    _author = ""
    _dimensions = "600x600"
    _text_path = sys.argv[-1]
    if not os.path.isfile(_text_path):
        sys.exit(0)
    if sys.argv[-1] == sys.argv[0]:
        usage()
        sys.exit(0)
    elif not bool(espeak_path()):
        print("Please install espeak.  Use `sudo apt-get install espeak-ng`")
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
            _wave = a
        elif o in ("-v", "--visible"):
            _visible = a
        elif o in ("-a", "--audible"):
            _audible = a
        elif o in ("-l", "--language"):
            _lang = a
        elif o in ("-r", "--rate"):
            _rate_percent = a
            _irate = _espeak_rate(_rate_percent)
        elif o in ("-p", "--pitch"):
            _pitch_percent = a
            _ipitch = _espeak_pitch(_pitch_percent)
        elif o in ("-i", "--image"):
            _image = a
        elif o in ("-t", "--title"):
            _title = a
        elif o in ("-n", "--artist"):
            _author = a
        elif o in ("-d", "--dimensions"):
            _dimensions = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        else:
            assert False, "unhandled option"
    _author = readtexttools.check_artist(_author)
    _title = readtexttools.check_title(_title, "espeak")
    _post_process = "process_wav_media"
    espkread(
        _text_path,
        _lang,
        _visible,
        _audible,
        _wave,
        _image,
        _title,
        _post_process,
        _author,
        _dimensions,
        _ipitch,
        _irate,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
