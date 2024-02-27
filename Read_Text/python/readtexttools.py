#!/usr/bin/env python
# -*- coding: UTF-8-*-
"""
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

Copyright (c) 2011 - 2024 James Holgate
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import codecs
import glob
import locale
import math
import mimetypes
import os
import sys
import tempfile
import threading
import time
import unicodedata

try:
    import dbus
except ImportError:
    pass

try:
    import getopt
except (ImportError, AssertionError):
    pass

try:
    import json
except (ImportError, AssertionError):
    pass

try:
    import platform
except (ImportError, AssertionError):
    pass

try:
    import psutil
except (ImportError, AssertionError):
    pass

try:
    import site
except (ImportError, AssertionError):
    pass

try:
    import subprocess
except (ImportError, AssertionError):
    pass

try:
    import check_dialog
except (ImportError, AssertionError):
    pass

try:
    import wave
except (ImportError, AssertionError):
    pass

try:
    import webbrowser
except (ImportError, AssertionError):
    pass

try:
    import winsound
except (ImportError, AssertionError):
    pass

try:
    import urllib.parse as urlparse
    import urllib.request as urllib
except (ImportError, AssertionError):
    try:
        import urlparse
        import urllib
    except ImportError:
        pass

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

try:
    import gi

    gi.require_version("Gst", "1.0")
    from gi.repository import Gst
except (ImportError, ValueError, AssertionError):
    pass

try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

try:
    import pathlib
except (ImportError, AssertionError):
    pass

try:
    import webbrowser
except (ImportError, AssertionError):
    pass

try:
    import l10n
except (ImportError, AssertionError, SyntaxError):
    pass

LOOK_UPS = 0

SITE_QR = """
    ██████████████████████████████████████████████████████████████████████████
    ██████████████████████████████████████████████████████████████████████████
    ██████████████████████████████████████████████████████████████████████████
    ██████████████████████████████████████████████████████████████████████████
    ████████              ██████  ██      ██          ██              ████████
    ████████  ██████████  ██  ██  ████████      ████  ██  ██████████  ████████
    ████████  ██      ██  ██████████  ████    ████  ████  ██      ██  ████████
    ████████  ██      ██  ██      ██        ██  ████████  ██      ██  ████████
    ████████  ██      ██  ████  ████████  ██          ██  ██      ██  ████████
    ████████  ██████████  ██    ██    ██    ████████████  ██████████  ████████
    ████████              ██  ██  ██  ██  ██  ██  ██  ██              ████████
    ██████████████████████████      ██████    ████    ████████████████████████
    ████████          ██        ██                  ██  ██  ██  ██  ██████████
    ████████        ██  ██    ██  ██  ██████        ████      ██████  ████████
    ████████████      ██    ████  ██████    ██  ████    ██    ████████████████
    ██████████        ██████  ████  ████      ██████  ██        ██  ██████████
    ████████████      ██                    ██  ██████  ██████    ████████████
    ████████████  ██    ██  ██████        ██  ████            ██████  ████████
    ████████    ████████  ██  ██  ██  ████        ██████  ██      ████████████
    ██████████    ██  ████    ████  ██████  ████████          ████  ██████████
    ████████████          ████              ██  ██  ██████  ██    ████████████
    ████████  ████      ██      ██  ████  ██                  ██  ██  ████████
    ████████  ██    ██    ████  ████████      ██  ██  ████    ██  ████████████
    ████████  ████      ██  ██      ██████    ████    ██  ████████  ██████████
    ████████  ██████████  ████  ██          ██  ████          ██      ████████
    ████████████████████████  ████  ████████  ██████  ██████          ████████
    ████████              ██    ████████    ██████    ██  ██      ████████████
    ████████  ██████████  ████  ████  ██  ██████      ██████  ████  ██████████
    ████████  ██      ██  ██  ████              ████          ██    ██████████
    ████████  ██      ██  ██  ████  ██  ████  ██      ████████    ██  ████████
    ████████  ██      ██  ██  ████████        ████                  ██████████
    ████████  ██████████  ██          ██████  ██████  ██    ██  ██  ██████████
    ████████              ██  ████████    ████      ████  ██      ████████████
    ██████████████████████████████████████████████████████████████████████████
    ██████████████████████████████████████████████████████████████████████████
    ██████████████████████████████████████████████████████████████████████████"""


def killall_process(_process=""):  # -> bool
    """If process is active, then stop it. Posix systems can use the posix
    `killall` command. Windows uses the `pip3` `psutil` library. Returns
    `True` if a process was stopped."""
    _success = False
    try:
        for proc in psutil.process_iter():
            if proc.name() == _process:
                proc.kill()
                _success = True
        return _success
    except NameError:
        if os.name == "posix":
            # `killall` might not be available to the script if it is running
            # in a container that does not include the `killall` command.
            return os.system("killall {0}".format(_process)) == 0
        elif os.name == "nt":
            # /f force /im <imagename>
            return os.system("taskkill /f /im {0}".format(_process)) == 0
        print("WARNING: NameError in `killall_process`. Requires pip3 `psutil`")
    return False


def write_plain_text_file(_file_path="", _body_text="", scodeco="utf-8"):  # -> bool
    """
    Create a plain text file.
    `write_plain_text_file("/path/file.txt", "Hello world", "utf-8")`
    """
    if not bool(_file_path):
        return False
    try:
        if os.path.isfile(_file_path):
            os.remove(_file_path)
        writer = codecs.open(_file_path, mode="w", encoding=scodeco, errors="replace")
        writer.write(_body_text)
        writer.close()
    except (ValueError, UnicodeEncodeError, UnicodeDecodeError, PermissionError):
        print("`write_plain_text_file` error in readtexttools.py")
    return os.path.isfile(_file_path)


def run_powershell(cmd=""):  # -> str
    """PowerShell automates tasks, manages systems, and can perform operations
    with Windows NET services like Azure, Microsoft 365, and SQL Server."""
    return subprocess.run(
        ["PowerShell", " -Command", cmd], capture_output=True, check=False
    )


def get_temp_prefix():  # -> str
    """
    Returns path to temporary directory plus a filename prefix.
    Need to supply an extension to determine the context - i.e:
     -sound.wav for sound
     -image.png for image
    """
    return tempfile.gettempdir()


def using_container(check_exec=False):  # ->bool
    """Check whether the extension is in a known container resource
    directory (snap, flatpack) or optionally if the application is
    mounted in a temporary directory (appimage)."""
    for test_path in ["/snap/libreoffice", "/var/", "/.var/"]:
        if test_path in os.path.realpath(__file__):
            return True
    if check_exec:
        if sys.executable.startswith("/tmp/.mount_"):
            return True
    return False


def have_posix_app(posix_app="vlc", do_test=True):  # -> bool
    """if the app exists and understands a `--version` or `--help` switch,
    then returns `True`, otherwise returns `False`.

    If `do_test` is `False`, then only look for the app installed in an
    specific `os.environ['PATH']` location, otherwise test for a manual
    or help response. A container version of an app might test `True`,
    but the python program might not be able to run the posix app.
    """
    if os.name != "posix":
        return False
    if not bool(posix_app):
        return False
    for _base_path in os.environ["PATH"].split(os.pathsep):
        if os.path.isfile(os.path.join(_base_path, posix_app)):
            return True
    if bool(do_test):
        os_sep = os.sep
        mute_response = "&> {0}dev{0}null &".format(os_sep)
        if os_sep in posix_app:
            posix_app = os.path.basename(posix_app)
        if my_os_system("man -w {0} {1}".format(posix_app, mute_response)):
            return True
        for tester in ["--version", "--help", "-h", "-?"]:
            app_switch = tester
            if my_os_system("{0} {1} {2}".format(posix_app, app_switch, mute_response)):
                # No error
                return True
    return False


class XmlTransform(object):
    """Prepare text for XML encoding."""

    def __init__(self):  # -> None
        """Initialize data"""
        self.caution = [
            "alias ",
            "awk ",
            "base64 ",
            "bash ",
            "curl ",
            "cut ",
            "echo ",
            "egrep ",
            "fgrep ",
            "glob",
            "grep ",
            "groff ",
            "hash ",
            "iconv ",
            "import ",
            "java ",
            "killall ",
            "node ",
            "python ",
            "python2 ",
            "python3 ",
            "ruby ",
            "sed ",
            "sh ",
            "split ",
            "sudo ",
            "tee ",
            "unhash ",
            "| ",
        ]
        try:
            # If the XML client can use all XML text substitutions,
            # escape the string for characters that can cause
            # problems in a Posix shell environment.
            self.caution_xml = str.maketrans(
                {
                    "&": "&amp;",
                    "_": " ",
                    '"': "",
                    "'": "",
                    "<": "",
                    ">": "",
                    "[": "",
                    "]": "",
                    "{": "",
                    "}": "",
                    "(": "",
                    ")": "",
                }
            )
            # For modern tts platforms that fully support W3C XML standards.
            self.safe_xml = str.maketrans(
                {
                    "&": "&#38;",
                    '"': "&#34;",
                    "'": "&#39;",
                    "<": "&#60;",
                    ">": "&#62;",
                    "[": "&#91;",
                    "]": "&#93;",
                    "{": "&#123;",
                    "}": "&#125;",
                    "(": "&#40;",
                    ")": "&#41;",
                }
            )
            # Minimum necessary for valid XML in a shell environment.
            self.base_xml = str.maketrans(
                {"&": "&amp;", '"': '\\"', "<": "&lt;", ">": "&gt;"}
            )
        except AttributeError:
            self.safe_xml = None
            self.base_xml = None
        self.use_mode = ["ssml", "text"][0]

    def clean_for_xml(self, test_text="", strict=True):  # -> str
        """The data portions of an XML file should escape characters
        with special properties. Not using `xml.sax.saxutils` because
        the replacements aren't always safe for uncontrolled input.

        For example, malformed scheme code strings or sable code could
        cause some speech synthesizers to crash.
        """
        _caution = False
        if not strict:
            if any(_test in test_text for _test in self.caution):
                _caution = True
        if bool(self.safe_xml):
            if strict:
                return str(test_text.translate(self.safe_xml))
            elif _caution:
                # Omit some characters in a shell command
                return str(test_text.translate(self.caution_xml))
            else:
                return str(test_text.translate(self.base_xml))
        # python 2 - slower equivalent
        if strict:
            for pair in [
                ["&", "&#38;"],
                ['"', "&#34;"],
                ["'", "&#39;"],
                ["<", "&#60;"],
                [">", "&#62;"],
                ["[", "&#91;"],
                ["]", "&#93;"],
                ["{", "&#123;"],
                ["}", "&#125;"],
                ["(", "&#40;"],
                [")", "&#41;"],
            ]:
                test_text = test_text.replace(pair[0], pair[1])
            return test_text
        elif _caution:
            for pair in [
                ["&", "&amp;"],
                ["_", " "],
                ['"', ""],
                ["'", ""],
                ["<", ""],
                [">", ""],
                ["[", ""],
                ["]", ""],
                ["{", ""],
                ["}", ""],
                ["(", ""],
                [")", ""],
            ]:
                test_text = test_text.replace(pair[0], pair[1])
            return test_text
        for pair in [["&", "&amp;"], ['"', '\\"'], ["<", "&gt;"], [">", "&lt;"]]:
            test_text = test_text.replace(pair[0], pair[1])
        return test_text


class ClassRemoveXML(HTMLParser):
    """Remove XML using python HTML parsing."""

    def __init__(self):
        self.reset()
        self.fed = []
        self.convert_charrefs = []

    def handle_data(self, d):
        """Handle string data."""
        self.fed.append(d)

    def get_fed_data(self):
        """Return fed data."""
        return "".join(self.fed)


def safechars(_test_string="", _allowed="1234567890,"):  # -> string
    """Removes unwanted characters from a string."""
    if not bool(_test_string):
        return ""
    try:
        for _letter in _test_string:
            if not _letter in _allowed:
                _test_string = _test_string.replace(_letter, "")
    except TypeError:
        return safechars(str(_test_string), _allowed)
    return _test_string


def remove_unsafe_chars(_test_string="", _forbidden="[]\\{}%|*"):  # -> string
    """Removes unwanted characters from a string."""
    if not bool(_test_string):
        return ""
    try:
        for _letter in _forbidden:
            _test_string = _test_string.replace(_letter, "")
    except TypeError:
        return remove_unsafe_chars(str(_test_string), _forbidden)
    return _test_string


def net_error_icon():  # -> string
    """Path to Gnome network error icon"""
    for _path in [
        "HighContrast/32x32/status/network-offline.png",
        "hicolor/32x32/apps/nm-no-connection.png",
        "HighContrast/32x32/apps/preferences-system-network.png",
        "Adwaita/32x32/legacy/network-error.png",
        "Humanity/actions/32/stock_not.svg",
    ]:
        _test = "/usr/share/icons/{0}".format(_path)
        if os.path.isfile(_test):
            return _test
    return ""


def strip_mojibake(concise_lang="en", _raw_text="", _strict=False):  # -> str
    """If possible, remove parts of text strings containing characters that a
    speech synthesizer cannot pronounce correctly.

    * `concise_lang` - The language in the form `en` or `en-US`
    * `_raw_text` - The text to check and modify
    * `_strict` - If not strict, then use all supported unicode characters if
      the text contains western European accented characters that English
      might employ. (i. e.: café, cliché, La Niña...). If strict, allow
      only plain characters (i. e.: computer safe code). `utf-8` encoded text
      uses `ascii` for the first 127 characters and `latin-1` for the first
      255 characters."""
    rare_chars = "ĿŀǾǿĲĳŠšŽžŠšŽžŒœŸÿẞŐőŰűḂḃĊċḊḋḞḟĠġṀṁṖṗṠṡṪṫẀẁẂẃŴŵẄẅỲỳŶŷŸ"
    if _strict:
        _ubound = 126
    else:
        _ubound = 255
    try:
        safe_chars = "".join((chr(i) for i in range(1, _ubound)))
    except UnicodeDecodeError:
        return strip_mojibake(concise_lang, _raw_text, True)
    if not _raw_text:
        return ""
    try:
        concise_lang = concise_lang[:2].lower()
    except (AttributeError, TypeError):
        concise_lang = "en"
    if concise_lang in [
        "af",
        "br",
        "co",
        "cy",
        "de",
        "en",
        "es",
        "et",
        "eu",
        "fi",
        "fo",
        "fr",
        "ga",
        "gd",
        "gl",
        "gv",
        "hu",
        "id",
        "is",
        "it",
        "lb",
        "nl",
        "oc",
        "pt",
        "rm",
        "sq",
        "sv",
        "tl",
        "wa",
    ]:
        # Use Western European supported characters.
        # French, German, Portuguese and other languages that mainly use
        # latin-1 script can include `rare_chars` glyphs that latin-1 doesn't
        # cover.
        _coding = "utf-8"
        if len(set(_raw_text).intersection(rare_chars)) == 0:
            try:
                returnval = set(_raw_text).intersection(safe_chars)
                return returnval.strip("\n\t .;\\{\\}()[]")
            except AttributeError:
                pass
    elif concise_lang in ["haw", "roo", "sw"]:
        _coding = "latin-1"
    else:
        # Use all supported unicode characters.
        _coding = "utf-8"
    try:
        _code = _raw_text.encode(_coding, "ignore")
        return _code.decode("utf-8", "ignore").strip("\n\t .;\\{\\}()[]")
    except LookupError:
        return _raw_text


def strip_xml(str1):  # -> str
    """
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
    """
    try:
        mydata = ClassRemoveXML()
        mydata.feed(str1)
        retval = mydata.get_fed_data()
    except Exception:
        # unexpected error
        retval = str1
    return retval


def usage():  # -> None
    """
    Displays the usage of the included python app "main", which can be used to
    convert wav files to other formats like ogg, opus, flac, and mp3.
    """
    sa1 = " " + os.path.split(sys.argv[0])[1]
    print(
        """
Read text tools
===============

Reads a .wav sound file, converts it and plays copy with a player.
To include enhanced mp3 meta-data, install a converter like `avconv`,
`lame` or `ffmpeg`.

## Usage

### Audio:

      {0} --sound="xxx.wav" --output="xxx.ogg"
      {0} --visible="false" --audible="true"  \\ 
       --sound="xxx.wav" --output="xxx.ogg"

### Video:

Makes an audio with a poster image.  Uses `avconv` or `ffmpeg`.

      {0} --image="xxx.png" --sound="xxx.wav" \\ 
      --output="xxx.webm"
      {0} --visible="true" --audible="true" --image="x.png" \\
       --sound="x.wav"--title="Title" --output="x.webm"
""".format(
            sa1
        )
    )


def app_signature():  # -> str
    """
    App signature can help identify file locations and shared settings.
    """
    return "ca.bc.vancouver.holgate.james.readtextextension"


def app_name():  # -> str
    """
    Application name in English
    """
    return "Read Text"


def app_release():  # -> str
    """
    Major, Minor, Version release.  Use to check if this is the required
    version.
    """
    return "0.9.2"


def default_lang():  # -> str
    """Returns the system language in the form `en_US`"""
    _lang = ""
    try:
        _lang = os.getenv("LANG")
    except (AttributeError, TypeError):
        pass
    if not bool(_lang):
        try:
            _lang = os.getenv("LANGUAGE")
        except (AttributeError, TypeError):
            pass
    if not bool(_lang):
        _lang = locale.getdefaultlocale()[0]
    if _lang:
        return _lang.split(".")[0].split(":")[0]
    return ""


def sys_machine_paths():  # list(str)
    """Return a list of posix `usr` architecture specific paths to resources
    like gstreamer plugins or espeak-ng-data."""
    machine_type = ""
    no_gnus = [
        "/usr/local/lib/",
        "/usr/lib/",
        "/usr/local/lib64/",
        "/usr/lib64/",
        "/usr/local/i386/",
        "/usr/i386/",
        "/usr/local/lib/i386-linux-gnu/",  # Work around wrong machine report.
        "/usr/lib/i386-linux-gnu/",  #Debian6.1.76-1(2024-02-01)',machine='i686')
        "/usr/local/share/",
        "/usr/share/",
        "/opt/",
    ]
    try:
        machine_type = platform.uname().machine
    except:
        _meta = ImportedMetaData()
        machine_type = _meta.execute_command("uname -m")
    if len(machine_type) == 0:
        machine_type = "x86_64"
    return [
        "/usr/local/lib/{0}-linux-gnu/".format(machine_type),
        "/usr/lib/{0}-linux-gnu/".format(machine_type),
    ] + no_gnus


def linux_machine_dir_path(search="espeak-ng-data"):  # -> str
    """If the architecture specific resource directory exists, return the full
    path, otherwise return `''`"""
    for _path in sys_machine_paths():
        try_path = "{0}{1}".format(_path, search)
        if os.path.isdir(try_path):
            return try_path
    return ""


def gst_plugin_path(plug_in_name="libgstvorbis"):  # -> str
    """
    Check directories for a named GST plugin (i. e.: `libgstvorbis`)
    """
    # This does not check for plugin by pad name, mime type or extension
    if not plug_in_name:
        return ""
    rt1 = ""
    version = ""

    g_versions = ["1.2", "1.1", "1.0", "1", "0.10"]
    _paths = sys_machine_paths()
    _ext = ".so"
    if have_posix_app("say", False):
        _paths = [
            os.path.join(os.path.expanduser("~"), os.path.sep),
            os.getenv("GST_PLUGIN_PATH"),
        ]
        _ext = ".dylib"
    elif os.name == "nt":
        _paths = [
            "".join([os.getenv("USERPROFILE"), os.path.sep]),
            os.path.join(os.getenv("HOMEDRIVE"), "gstreamer-sdk", os.path.sep),
            os.getenv("GST_PLUGIN_PATH"),
            os.path.join(os.getenv("HOMEDRIVE"), "opt", os.path.sep),
        ]
        _ext = ".dll"

    for path in _paths:
        for g_version in g_versions:
            rt1 = path
            version = g_version
            for file_test in [
                "{0}gstreamer-{1}/{2}{3}".format(rt1, version, plug_in_name, _ext),
                "{0}gstreamer-{1}/{2}".format(rt1, version, plug_in_name),
            ]:
                if os.path.isfile(file_test):
                    return file_test
    return ""


class ExtensionTable(object):
    """Common data and procedures for handling audio files"""

    def __init__(self):
        """Common data and procedures for handling audio files"""
        mac_afconvert = "/usr/bin/afconvert"
        self.vlc = ""
        if have_posix_app("vlc", False):
            self.vlc = "vlc"
        elif os.name == "nt":
            self.vlc = self.win_search("vlc", "vlc")
        elif os.path.exists("/Applications/VLC.app/Contents/MacOS/VLC"):
            if os.path.isfile("/usr/bin/python"):
                # VLC is not fully supported for legacy MacOS
                self.vlc = ""
            else:
                self.vlc = "/Applications/VLC.app/Contents/MacOS/VLC"
        w_flac = self.win_search("flac", "flac")
        w_twolame = self.win_search("twolame", "twolame")
        w_lame = self.win_search("lame", "lame")
        w_oggenc = self.win_search("oggenc", "oggenc")
        w_oggenc2 = self.win_search("oggenc2", "oggenc2")
        w_opus = None
        w_spx = None
        self.mime_video = False
        self.ffmpeg = ""
        if os.name == "posix":
            self.ffmpeg = ffmpeg_path()
        self.extension = 0
        self.filter = 1
        self.standalone = 2
        self.alt_standalones = 3
        self.extension_test = [
            [[".flac"], "libgstflac", "/usr/bin/flac", [w_flac, self.vlc]],
            [[".aac"], "alpha_libgstaac", mac_afconvert, []],
            [[".m4a"], "alpha_libgstm4a", mac_afconvert, []],
            [[".mp4"], "libgstbadvideo", self.ffmpeg, ["/usr/bin/avconv", self.ffmpeg]],
            [[".m4v"], "libgstbadvideo", self.ffmpeg, ["/usr/bin/avconv", self.ffmpeg]],
            [[".mp2"], "libgsttwolame", self.ffmpeg, ["/usr/bin/twolame", w_twolame]],
            [[".mp3"], "libgstlame", self.ffmpeg, ["/usr/bin/lame", self.vlc, w_lame]],
            [
                [".oga", ".ogg", ".ogv"],
                "libgstogg",
                self.ffmpeg,
                ["/usr/bin/oggenc", w_oggenc, w_oggenc2, self.vlc],
            ],
            [[".opus"], "libgstopus", self.ffmpeg, [w_opus, self.vlc]],
            [[".spx"], "libgstspeex", self.ffmpeg, [w_spx, self.vlc]],
            [[".wav"], "libwavenc", self.ffmpeg, [self.ffmpeg]],
            [[".webm"], "libgstmatroska", self.ffmpeg, []],
        ]

    def audio_extension_ok(
        self,
        test_file_spec="/tmp/file.opus",
        pendantic=True,
        test_can_export=True,
        exact_match=False,
    ):  # -> bool
        """
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
          the same mime-type, but the extensions are different."""
        if not test_file_spec:
            return False
        _ext = os.path.splitext(test_file_spec)[1].lower()
        _check_mime = self.get_mime(test_file_spec)
        if not _check_mime:
            self.mime_video = False
            return False
        elif _check_mime.startswith("audio/"):
            self.mime_video = False
        elif _check_mime.startswith("video/"):
            self.mime_video = True
            print("File mime-type: `{0}`".format(_check_mime))
        else:
            self.mime_video = False
            return False
        if not test_can_export:
            return True
        for _test in self.extension_test:
            if exact_match:
                does_match = _ext in _test[self.extension]
            else:
                does_match = _check_mime == self.get_mime(
                    "".join(["x/x", _test[self.extension][0]])
                )
            if does_match:
                if gst_plugin_path(_test[self.filter]):
                    return True
                elif bool(self.ffmpeg) or os.path.isfile(_test[self.standalone]):
                    return True
                elif pendantic:
                    alt_list = _test[self.alt_standalones]
                    if alt_list:
                        for _alt_path in alt_list:
                            if bool(_alt_path):
                                if os.path.isfile(_alt_path):
                                    return True
        return False

    def get_mime(self, test_file_spec="", strict=False):  # -> str
        """Return python's mime-type for a file path."""
        _ext = os.path.splitext(test_file_spec)[1].lower()
        if not _ext:
            _ext = test_file_spec.lower()
        if not test_file_spec:
            return ""
        try:
            mimetypes.init()
            return mimetypes.types_map[_ext]
        except (IndexError, KeyError):
            if strict:
                return ""
            # Darwin platform (a. k. a. MacOS) ?
            #
            # Gstreamer vorbis file family ; Specific mime type
            #
            # The information from gstreamer on open desktop is
            # via /usr/share/gstreamer-1.0/<fileextension>.gep
            for _test in ["flac", "ogg", "opus", "spx"]:
                if test_file_spec.endswith(".{0}".format(_test)):
                    return "audio/x-vorbis;audio/{0}".format(_test)
            for _test in ["ogv", "webm"]:
                if test_file_spec.endswith(".{0}".format(_test)):
                    return "video/x-vorbis;video/{0}".format(_test)
            for _test in ["md", "wiki"]:
                if test_file_spec.endswith(".{0}".format(_test)):
                    return "text/plain;application/x-{0}".format(_test)
            return ""

    def add_quotes_if_needed(self, app=""):  # -> str
        """Add Windows style Double Quotes to encompass paths that include spaces"""
        if " " in app:
            if not app.startswith('"'):
                app = '"{0}'.format(app)
            if not app.endswith('"'):
                app = '{0}"'.format(app)
        return app

    def check_path_str(self, file_path_str=""):  # -> str
        """Returns the file path as a string formatted for the
        current operating system.
        """
        os_sep = os.sep
        if not bool(file_path_str):
            return ""
        try:
            return str(pathlib.PurePath(file_path_str))
        except NameError:
            file_path_str = os.path.realpath(file_path_str)
            if os.name == "nt":
                return (
                    str(file_path_str)
                    .replace("/", os_sep)
                    .replace(os_sep + os_sep, os_sep)
                )
            return (
                str(file_path_str)
                .replace("\\", os_sep)
                .replace(os_sep + os_sep, os_sep)
            )

    def win_search(
        self, application_name="ffmpeg", application_executable="ffplay"
    ):  # -> str
        """Search for a Windows application executable

        Examples
        ---------

        print(win_search('ffmpeg', 'ffmpeg'))  \n
        print(win_search('ffmpeg','ffplay'))  \n
        print(win_search('lame', 'lame'))  \n
        print(win_search('LibreOffice', 'soffice'))  \n
        print(win_search('Pandoc', 'pandoc'))  \n
        """
        if not application_executable:
            return ""
        elif not application_name:
            return ""
        elif os.name != "nt":
            return ""
        os_sep = os.sep
        executable_extensions = [".exe", ".com"]
        common_app_executable = ""
        program_dir_searches = [
            "LOCALAPPDATA",
            "USERPROFILE",
            "ProgramFiles",
            "ProgramFiles(x86)",
            "HOMEDRIVE",
        ]
        application_searches = [
            "{0}{1}{0}command_line{0}".format(os_sep, application_name),
            "{0}Programs{0}{1}{0}".format(os_sep, application_name),
            "{0}{1}{0}bin{0}".format(os_sep, application_name),
            "{0}{1}{0}program{0}".format(os_sep, application_name),
            "{0}Programs{0}piper-tts{0}piper{0}".format(os_sep),
            "{0}Programs{0}piper{0}".format(os_sep),
            "{0}VideoLAN{0}VLC{0}".format(os_sep),
            "{0}{1}{0}".format(os_sep, application_name),
            "{0}".format(os_sep),
            "{0}Local{0}".format(os_sep),
            "{0}bin{0}".format(os_sep),
        ]
        for program_dir_search in program_dir_searches:
            get_env = os.getenv(program_dir_search)
            if not get_env:
                continue
            get_env = get_env.replace("\\", os_sep)
            for application_search in application_searches:
                for extension in executable_extensions:
                    common_app_executable = "{0}{1}{2}{3}".format(
                        get_env, application_search, application_executable, extension
                    )
                    if os.path.isfile(common_app_executable):
                        return self.add_quotes_if_needed(
                            self.check_path_str(common_app_executable)
                        )
                    else:
                        # Look for a directory like `ffmpeg-YYYY-MM-DD-git-xxxxxx`
                        developer_app_executables = glob.glob(
                            "{0}{1}{2}*".format(
                                get_env, application_search, application_executable
                            )
                        )
                        if bool(developer_app_executables):
                            # Get a matching item in `developer_app_executables`
                            # object.
                            for app_match in developer_app_executables:
                                if not app_match:
                                    continue
                                return_value = "{0}{1}{2}{3}".format(
                                    app_match, os_sep, application_executable, extension
                                )
                                return_value = return_value.replace("\\", os_sep)
                                if os.path.isfile(return_value):
                                    return self.add_quotes_if_needed(
                                        self.check_path_str(return_value)
                                    )
        return ""


def local_pip_search(
    profile="", lib_name="", py_search="", include_pipx=True
):  # -> str
    """Search local posix pip and optionally the posix pipx directories."""
    _add_path = os.path.join(profile, ".local", "lib", py_search, "site-packages")
    if not os.path.isdir(os.path.join(_add_path, lib_name.lower())):
        if include_pipx and not os.path.isdir(os.path.join(_add_path, lib_name)):
            _add_path = os.path.join(
                profile,
                ".local",
                "pipx",
                "venvs",
                lib_name.lower(),
                "lib",
                py_search,
                "site-packages",
            )
    if os.path.isdir(_add_path):
        return _add_path
    return ""


def find_local_pip(lib_name="qrcode", latest=True, _add_path=""):  # -> str
    """If you installed a pip tool as a local user, then
    return the library path, otherwise return `''`.

    If `latest` is `True`, return the last match, otherwise
    return the first match. When there is a history of several
    versions of python installed, there might be several
    pip libraries with different tools or different versions
    of the tools. A current good practice for programmers
    is to use `venv`. A good practice for users is to delete
    and rebuild your pip libraries when you do a major version
    upgrade of your system or of python. Best practice for MacOS
    is to set up a virtual environment using LibreOffice's
    python version. See the `pipx` venvs documentation."""
    retval = ""
    path1 = ""
    path2 = ""
    path3 = ""
    py_ver = "{0}.{1}".format(
        platform.python_version_tuple()[0], platform.python_version_tuple()[1]
    )
    if int(platform.python_version_tuple()[0].strip()) < 3:
        return ""
    if os.name == "nt":
        profile = os.getenv("LOCALAPPDATA").strip(os.path.sep)
        path1 = os.path.join(profile, "Programs", "Python")
        path2 = os.path.join("Lib", "site-packages")
        path3 = path2
    elif have_posix_app("say", False):
        profile = profile = os.path.expanduser("~")
        path1 = os.path.join(profile, "Library", "Python")
        py_search = "python{0}".format(py_ver)
        local_pip = local_pip_search(profile, lib_name, py_search)
        if len(local_pip) != 0:
            return local_pip
        if not os.path.isdir(path1):
            for _test in os.getenv("PATH").split(os.pathsep):
                if os.path.isdir(_test) and profile in _test:
                    path1 = _test
                    break
        path2 = os.path.join("lib", "python", "site-packages")
        path3 = os.sep + os.path.join(
            "Library",
            "Frameworks",
            "Python.framework",
            "Versions",
            py_ver,
            "lib",
            "python" + py_ver,
            "site-packages",
        )
    elif os.name == "posix":
        profile = os.path.expanduser("~")
        path1 = os.path.join(profile, ".local", "lib")
        path2 = os.path.join("lib", "python", "site-packages")
        path3 = path2
        pwd_dir = os.getenv("PWD")
        py_search = "python{0}".format(py_ver)
        if not profile == pwd_dir:
            if not pwd_dir.startswith(os.path.join(profile, ".config")):
                # snap & flatpak containment check
                return retval
        site_list = site.getsitepackages()
        if len(_add_path) == 0:
            _add_path = local_pip_search(profile, lib_name, py_search)
        if os.path.isdir(_add_path):
            # Use the most recent local library, not the distribution library.
            site_list.insert(0, _add_path)
        for _site in site_list:
            if os.path.isdir(os.path.join(_site, lib_name)):
                retval = _site
                if not latest:
                    return retval
        return retval
    py_path = ""
    path_result = ""
    for _item in [path1, path3]:
        if os.path.exists(_item):
            path_result = _item
            break
    if len(path_result) == 0:
        print("FAIL: `{0}` search: no directory at `{1}`".format(lib_name, path1))
        return ""
    with os.scandir(path_result) as it:
        for entry in it:
            for entry_name in [py_ver, entry.name]:
                if entry_name.startswith("."):
                    continue
                elif "dist-info" in entry_name:
                    continue
                py_path = os.path.join(path_result, entry_name, path2, lib_name)
                if not os.path.isdir(py_path):
                    if os.path.isdir(os.path.join(path_result, lib_name)):
                        py_path = path_result
                pipx_path = os.path.join(
                    path_result,
                    "pipx",
                    "venvs",
                    lib_name.lower(),
                    "lib",
                    py_ver,
                    "site-packages",
                )
                if os.path.isdir(pipx_path):
                    retval = pipx_path
                    break
                elif os.path.isdir(py_path):
                    retval = os.path.join(path1, entry_name, path2)
                    if not latest:
                        return retval
            if len(retval) != 0:
                break
    return retval


def my_os_system(_command):  # -> bool
    """
    This is equivalent to os.system(_command)
    Replaced os.system(_command) to avoid Windows path errors.
    * Returns `True` if there is no error
    * Returns `False` if there is an error
    """
    try:
        _command = _command.encode("utf-8")
    except AttributeError:
        # Not a string
        return False
    if os.name == "nt":
        try:
            retcode = subprocess.call(_command, shell=False)
            if retcode < 0:
                print("Process was terminated by signal")
                return False
            else:
                print("Process returned")
                return True
        except (NameError, OSError):
            print("Execution failed")
            return False
    else:
        retval = os.system(_command)
        return not bool(retval)


def get_nt_path(name="ffmpeg", app="ffplay"):  # -> str
    """
    Return the path to a Windows program if it is installed
    in a local or global program installation location.

    * `get_nt_path('ffmpeg', 'ffmpeg')`
    * `get_nt_path('ffmpeg','ffplay')`
    * `get_nt_path('lame', 'lame')`
    * `get_nt_path('LibreOffice', 'soffice')`
    * `get_nt_path('Pandoc', 'pandoc')`
    """
    _extension_table = ExtensionTable()
    return _extension_table.win_search(name, app)


def app_icon_image(image_selection="", asset_dir="images"):  # -> str
    """The path to an extension icon image or other asset, if it exists, or
    `''` if it doesn't exist."""
    path_root = os.path.split(os.path.realpath(__file__))[0]
    os_sep = os.sep
    folders = path_root.split(os_sep)
    count = len(folders)
    if not bool(image_selection):
        image_selection = "textToSpeechAbout_42.png"
    for _x in folders:
        test_root = os_sep.join(folders[:count])
        for image in [
            os.path.join(test_root, asset_dir, image_selection),
            os.path.join(test_root, asset_dir, "textToSpeech.svg"),
            os.path.join(test_root, asset_dir, "schooltools_42.svg"),
        ]:
            if os.path.isfile(image):
                return image
        if test_root.endswith("uno_packages"):
            return ""
        count = count - 1
    return ""


def is_container_instance():  # -> bool
    """If `is_container_instance` is `True` python3 cannot rely on expected
    desktop paths and user interactions. It might have limited access to
    the system and data from other applications."""
    try:
        if int(platform.python_version_tuple()[0]) < 3:
            return True
    except:
        pass
    tests = [
        "windowsapps",
        ".wine",
        "wineprefixes",
        "com.bottles.usebottles",
        ".var",
    ]
    if os.name == "posix":
        tests = [
            "/meta/",
            "/org.libreoffice.libreoffice/",
            "/run/",
            "/snap/",
            "/.var/",
        ]
    for _path in [
        os.path.realpath(__file__).lower(),
        sys.executable.lower(),
    ]:
        for _test in tests:
            if _test in _path:
                return True
    if os.path.exists(os.path.realpath("/.dockerenv")):
        return True
    for _test in [
        ["container", "oci"],
        ["container", "podman"],
        ["WINEUSERNAME", os.getenv("USERNAME")],
    ]:
        if os.getenv(_test[0]) == _test[1]:
            if bool(_test[1]):
                return True
    if os.name == "posix":
        if "microsoft" in os.uname().release:
            # Windows Subsystem for Linux
            return True
        block_dist = ["penguin", "server"]
        if os.uname().version.lower() in block_dist:
            return True
        return os.uname().sysname.lower() not in ["darwin", "linux"]
    return False


def local_host_pop(
    msg="", msg_h1="", dialog_title="", urgent=1, m_sec=5000, lang_region="en-US"
):  # -> bool
    """Check if localhost menu service is active. If `True`, then
    display the message in a web browser. Container versions of the
    office program cannot rely on using local directories or system
    installed programs like `wscript`, `mshta`, `osascript`, `dbus`
    `speech-dispatcher` etc."""
    _local_server = check_dialog.MyServer()
    _xml_transform = XmlTransform()
    if _local_server.is_valid_url(""):
        local_url = _local_server.host_and_port
    else:
        try:
            _local_server.start()
            local_url = _local_server.host_and_port
        except:
            return False
    _strict = True
    _msg = _xml_transform.clean_for_xml(msg, _strict)
    _msg_h1 = _xml_transform.clean_for_xml(msg_h1, _strict)
    _dialog_title = _xml_transform.clean_for_xml(dialog_title, _strict)
    s_icon = "1.png"
    # Only allow curated images
    if urgent in [0, 1, 2, 3]:
        s_icon = "{0}.png".format(str(urgent))
    s_icon = _xml_transform.clean_for_xml(s_icon, _strict)
    try:
        _stime = safechars(str(m_sec), "1234567890")
    except:
        _stime = "0"  # Do not automatically close the tab.
    _args = "?msg={0}&msg_h1={1}&dialog_title={2}&f_logo_src={3}&m_sec={4}&lang_region={5}".format(
        _msg, _msg_h1, _dialog_title, s_icon, _stime, lang_region
    )
    try:
        if webbrowser.open_new_tab("{0}{1}".format(local_url, _args)):
            time.sleep(5 + m_sec / 1000)
            _local_server.stop()
            return True
        else:
            _local_server.stop()
    except:
        pass
    return False


def pop_win_msg_box(
    msg="", msg_h1="", dialog_title="", urgent=1, m_sec=5000
):  # -> bool
    """
    Pop up a message box that closes after a few seconds. The dialog uses the
    Read Text logo and shows the information using standard Internet Explorer
    advisory style. NOTE: This method of displaying text will not work on all
    platforms (i. e. Wine for Posix or Python versions < 3.3).
    """
    if is_container_instance():
        return local_host_pop(msg, msg_h1, dialog_title, urgent, m_sec)
    _xml_transform = XmlTransform()

    # Malicious programs can use `mshta.exe` inappropriately, so always ensure
    # that the HTA applications you are running come from a trusted
    # source. The code below only uses it to display a message and to close
    # the window after a few seconds. It also "escapes" characters that
    # users might input that JavaScript uses so that it appears as inline
    # text instead of acting as program instructions. We only allow curated
    # images that are different than standard system images.
    #
    # Escape any code-like characters:
    _strict = True
    _msg = _xml_transform.clean_for_xml(msg, _strict)
    _msg_h1 = _xml_transform.clean_for_xml(msg_h1, _strict)
    _dialog_title = _xml_transform.clean_for_xml(dialog_title, _strict)
    out_file = os.path.join(tempfile.gettempdir(), "read-text-advisory.html")
    try:
        _stime = safechars(str(m_sec), "1234567890")
    except:
        _stime = "8000"
    try:
        if int(_stime) < 100:
            _stime = 100
    except ValueError:
        _stime = "8000"
    s_icon = "1.png"
    # Only allow curated images
    if urgent in [0, 1, 2, 3]:
        s_icon = "{0}.png".format(str(urgent))
    f_logo_src = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "check_dialog", s_icon
    )
    ie_css = """<link rel="stylesheet" type="text/css" 
      href="res://ieframe.dll/ErrorPageTemplate.css" />"""
    if not os.name == "nt" or is_container_instance():
        ie_css = """<style>
body {
font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif;
}
</style>"""
    try:
        s1 = """
<html>
<head>
<script> 
window.resizeTo(600,180);
setTimeout(function(){{window.close();}}, {_stime});
</script>
<HTA:APPLICATION ID="objReadTextDialog" 
                APPLICATIONNAME="READTEXTTOOLS" 
                SCROLL="no" 
                SINGLEINSTANCE="yes" 
                CAPTION="yes" 
                SHOWINTASKBAR="no" 
                maximizeButton="no" 
                minimizeButton="no">
{ie_css}
<meta http-equiv="Content-Type" 
      content="text/html; charset=UTF-8" />
<title>{_dialog_title}</title>
</head>
<body onkeydown="window.close();" onclick="window.close();" >
<table width="500" cellpadding="0" cellspacing="0" border="0">
<tr>
<td id="infoIconAlign" width="60" align="left" valign="top" rowspan="2">
<img src="{f_logo_src}" id="infoIcon" alt="Info icon">
</td>
<td id="mainTitleAlign" valign="middle" align="left"s width="*">
<h1 id="mainTitle">{_msg_h1}</h1>{_msg}
</td>
</tr>
<tr height = "60">
<td id="infoIconAlign2" rowspan="2"></td>
<td id="mainTitleAlign2" valign="bottom" align="left" width="*"></td>
</tr>
</table>
</body>
</html>
""".format(_stime=_stime, ie_css=ie_css, _dialog_title=_dialog_title,
           f_logo_src=f_logo_src, _msg_h1=_msg_h1, _msg=_msg)
    except (AttributeError, NameError, SyntaxError):
        return False
    with open(out_file, "w") as f:
        # Use XML substitution and combine Unicode duplicates for all non-ASCII charaters.
        f.write(
            unicodedata.normalize(
                "NFKD", s1.encode("ascii", "xmlcharrefreplace").decode()
            )
        )
    # show message
    try:
        command = ["mshta.exe", os.path.realpath(out_file)]
        subprocess.Popen(command)
    except (AttributeError, FileNotFoundError, NameError, TypeError):
        webbrowser.open_new_tab(
            "file://" + os.path.realpath(out_file).replace(os.pathsep, "/")
        )
    try:
        time.sleep(round(int(_stime) / 1000))
    except (TypeError, ValueError):
        time.sleep(5)
    if os.path.isfile(out_file):
        os.remove(out_file)
        return True
    return False


def translate_ui_element(iso_lang="en-US", msg=""):  # -> str
    """If a literal translation is available, then return the translated
    version of the string."""
    try:
        _translator = l10n.Translator()
        return _translator.get_translation(iso_lang, msg)
    except:
        pass
    return msg


def pop_message(
    summary="Read text", msg="", m_sec=8000, my_icon="", urgent=1, iso_lang="en-US"
):  # -> bool
    """Pop up a notification message if supported on the platform"""
    if not msg:
        return False
    if not summary:
        return False
    if not m_sec:
        m_sec = 5000
    if urgent not in [0, 1, 2]:
        urgent = 1
    if not os.path.isfile(my_icon):
        my_icon = "face-smile"
        for icon in [
            app_icon_image(),
            "/usr/share/icons/hicolor/scalable/apps/libreoffice-main.svg",
            "/usr/share/icons/hicolor/scalable/apps/openoffice-main.svg",
            "/usr/share/icons/hicolor/32x32/apps/libreoffice-startcenter.png",
            "/usr/share/icons/hicolor/32x32/apps/openoffice-startcenter.png",
            "/usr/share/icons/HighContrast/32x32/apps/libreoffice-startcenter.png",
            "/usr/share/icons/HighContrast/32x32/devices/multimedia-player.png",
            "/usr/share/icons/HighContrast/32x32/emotes/face-smile.png",
        ]:
            if os.path.isfile(icon):
                my_icon = icon
                break
    summary = translate_ui_element(iso_lang, summary)
    msg = translate_ui_element(iso_lang, msg)
    try:
        if bool(dbus):
            item = "org.freedesktop.Notifications"
            _interface = dbus.Interface(
                dbus.SessionBus().get_object(item, "/" + item.replace(".", "/")), item
            )
            _interface.Notify(
                "readtexttools.py",
                0,
                my_icon,
                summary,
                msg,
                [],
                {"urgency": urgent},
                m_sec,
            )
            return True
    except (NameError, ValueError, Exception):
        pass
    if have_posix_app("notify-send", False):
        my_os_system(
            'notify-send -i "{0}" -t {1} "{2}" "{3}"'.format(
                my_icon, m_sec, summary, msg
            )
        )
        return True
    elif have_posix_app("osascript", False) and not is_container_instance():
        for tag in ["<b>", "</b>", "<i>", "</i>"]:
            msg = msg.replace(tag, "")
        if urgent == 2:
            _sound = ' sound name "Sosumi"'
        elif urgent == 1:
            _sound = ' sound name "Tink"'
        else:
            _sound = ""
        my_os_system(
            """osascript -e 'display notification "{0}" with title "{1}"{2}' """.format(
                msg, summary, _sound
            )
        )
        return True
    main_title = summary.strip()
    _app = translate_ui_element(iso_lang, app_name())
    return pop_win_msg_box(msg, main_title, _app, urgent, m_sec)


def lax_bool(_test):  # -> bool
    """Given a string `true`, `yes` `1`, `-1` or a boolean `True` returns
    `True`, otherwise returns `False`."""
    if not bool(_test):
        return False
    if _test is True:
        # Checking for singleton value True
        return True
    try:
        if _test.lower() in ["true", "yes", "-1", "1"]:
            return True
    except [AttributeError, NameError, TypeError]:
        pass
    if _test in [True, -1, 1]:
        return True
    return False


def lax_mime_match(_wanted="", _testing=""):  # -> bool
    """If two file extensions are identical or if they share
    the same mime type, then return `True`, otherwise return
    `False`. For unknown mimetypes, compare extensions."""
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
    """
    ffmpeg may not be in the normal environment PATH, so we look for it, and
    return the location.
    """
    paths = [
        "/usr/local/bin/avconv",
        "/usr/local/bin/ffmpeg",
        "/usr/bin/avconv",
        "/usr/bin/ffmpeg",
    ]
    if os.name == "nt":
        paths = [get_nt_path("ffmpeg", "ffmpeg"), get_nt_path("avconv", "avconv.exe")]
    elif have_posix_app("say", False):
        mvc = "Miro Video Converter"
        paths = [
            "/usr/local/bin/ffmpeg",
            "/Applications/Miro.app/Contents/Helpers/ffmpeg",
            "/Applications/{0}.app/Contents/Helpers/ffmpeg".format(mvc),
            "/Applications/Shotcut/Shotcut.app/bin/ffmpeg",
        ]
    for path in paths:
        if os.path.isfile(path):
            return path
    return ""


def get_work_file_path(_work="", _image="", _type=""):  # -> str
    """
    Determine the temporary filename or output filename
    Given the filename _work, returns a temporary filename if _type is 'TEMP'
    or the output filename if _type is anything else.
    Example:
    import readtexttools
    * Determine the temporary file name
    `_work = readtexttools.get_work_file_path(_work, _image, 'TEMP')`
    * Determine the output file name
    `_out = readtexttools.get_work_file_path(_work, _image, 'OUT')`
    """
    _extension_table = ExtensionTable()
    _out = ""
    _alt_ext = ""
    if _work == "":
        if have_posix_app("say", False):
            _work = os.path.join(get_temp_prefix(), "rte-speech.aiff")
        else:
            _work = os.path.join(get_temp_prefix(), "rte-speech.wav")
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
    if _work_ext in [".aac"]:
        if have_posix_app("afconvert", False):
            _out = _work
            _work = "{0}.aiff".format(_out)
    elif _work_ext in [".m4a", "m4r"]:
        if (
            have_posix_app("faac", False)
            or bool(get_nt_path("nero", "neroAacEnc"))
            or bool(get_nt_path("faac", "faac"))
        ):
            _out = _work
            _work = "{0}.wav".format(_out)
        elif have_posix_app("afconvert", False):
            _out = _work
            _work = "{0}.aiff".format(_out)
        else:
            # Can't make m4a, so make wav
            _out = "{0}.wav".format(_work)
            _work = _out
    elif lax_mime_match(_work_ext, ".mp3"):
        # _extension_table = ExtensionTable()
        if media_converter_installed():
            if (
                len(gst_plugin_path("libgstlame")) != 0
                or os.path.isfile("/usr/share/doc/liblame0/copyright")
                or os.path.isfile("/usr/share/doc/libmp3lame0/copyright")
                or os.path.isdir("/usr/share/doc/lame-libs/")
                or have_posix_app("lame", False)
                or os.path.isfile("/usr/lib/x86_64-linux-gnu/libmp3lame.so.0")
                or os.path.isfile(_extension_table.vlc)
                or bool(get_nt_path("lame", "lame"))
            ):
                _out = _work
                _work = "{0}.wav".format(_out)
            else:
                # Can't make mp3, so make wav
                _out = "{0}.wav".format(_work)
                _work = _out
        else:
            # Can't make mp3, so make wav
            _out = "{0}.wav".format(_work)
            _work = _out
    elif _work_ext in [".mp2"]:
        if media_converter_installed():
            if (
                len(gst_plugin_path("libgstlame")) != 0
                or os.path.isfile("/usr/share/doc/libtwolame0/copyright")
                or bool(get_nt_path("twolame", "twolame"))
            ):
                _out = _work
                _work = "{0}.wav".format(_out)
            else:
                _out = "{0}.wav".format(_work)
                _work = _out
        else:
            # Can't make mp2, so make wav
            _out = "{0}.wav".format(_work)
            _work = _out
    elif lax_mime_match(_work_ext, ".ogg"):
        if media_converter_installed():
            if (
                len(gst_plugin_path("libgstogg")) != 0
                or os.path.isfile("/usr/share/doc/libogg0/copyright")
                or os.path.isfile(_extension_table.vlc)
                or bool(get_nt_path("oggenc", "oggenc"))
                or bool(get_nt_path("oggenc2", "oggenc2"))
            ):
                _out = _work
                _work = "{0}.wav".format(_out)
            else:
                _out = "{0}.wav".format(_work)
                _work = _out
        else:
            # Can't make ogg, so make wav
            _out = "{0}.wav".format(_work)
            _work = _out
    elif lax_mime_match(_work_ext, ".aif"):
        if media_converter_installed():
            _out = _work
            _work = "{0}.wav".format(_out)
        else:
            # Can't make aif, so make wav
            _out = "{0}.wav".format(_work)
            _work = _out
    elif lax_mime_match(_work_ext, ".flac"):
        # WARNING: `flac` audio file authoring might not work on all platforms.
        if len(gst_plugin_path("libgstflac")) != 0 or bool(get_nt_path("flac", "flac")):
            _out = _work
            _work = "{0}.wav".format(_out)
        else:
            # Can't make flac, so make wav
            _out = "{0}.wav".format(_work)
            _work = _out
    elif lax_mime_match(_work_ext, ".opus"):
        if len(gst_plugin_path("libgstopus")) != 0:
            _out = _work
            _work = "{0}.wav".format(_out)
        else:
            # Can't make opus, so make wav
            _out = "{0}.wav".format(_work)
            _work = _out
    elif lax_mime_match(_work_ext, ".spx"):
        # DEPRECIATED: `opus` replaces `spx` audio compression.
        if len(gst_plugin_path("libgstspeex")) != 0:
            _out = _work
            _work = "{0}.wav".format(_out)
        else:
            # Can't make spx, so make wav
            _out = "{0}.wav".format(_work)
            _work = _out
    elif "video/" in _mime:
        if len(ffmpeg_path()) != 0 and _image_ext.lower() in [
            ".gif",
            ".jpeg",
            ".jpg",
            ".png",
        ]:
            _out = _work
            _work = "{0}.wav".format(_out)
        elif os.path.isfile(app_icon_image("poster-001.png")):
            _out = _work
            _work = "{0}.wav".format(_out)
        else:
            _alt_ext = ".ogg"
            _out = "{0}{1}".format(os.path.splitext(_work)[0], _alt_ext)
            _work = "{0}.wav".format(_out)

    if _type.lower() == "temp":
        if bool(_alt_ext):
            print(
                """
The `{0}` video format you requested needs an image.
Using the `{1}` audio format.""".format(
                    _wanted_ext, _alt_ext
                )
            )
        _return_value = _work
    else:
        _return_value = _out
    if _return_value:
        make_output_directory(_out)
    return _return_value


def media_converter_installed():  # -> bool
    """Check if ffmpeg, Gst or VLC are installed"""
    _extension_table = ExtensionTable()
    if len(ffmpeg_path()) != 0:
        return True
    elif have_posix_app("afconvert", False):
        return True
    elif have_posix_app("vlc", False):
        return True
    elif bool(_extension_table.win_search("vlc", "vlc")):
        return True
    else:
        try:
            dummy = bool(Gst)
            return dummy
        except NameError:
            pass
    return False


def make_output_directory(_out):  # -> str
    """Make sure that the destination directory exists"""
    _out_directory = os.path.dirname(_out)
    if not os.path.exists(_out_directory):
        try:
            os.makedirs(_out_directory)
        except:
            _out_directory = ""
    return _out_directory


def posix_compressor_ok(_ext=""):  # -> bool
    """Check if a stand alone compressor app that works with the
    working file extension is installed."""
    if not os.name == "posix":
        return False
    _apps = [
        ["flac", [".flac"]],
        ["lame", [".mp2", ".mp3"]],
        ["twolame", [".mp2"]],
        ["oggenc", [".oga", ".ogg"]],
    ]
    for _app in _apps:
        if have_posix_app(_app[0], False):
            if _ext in _app[1]:
                return True
    return False


def process_wav_media(
    _title="untitled",
    _work="",
    _image="",
    _out="",
    _audible="true",
    _visible="false",
    _artist="",
    _dimensions="600x600",
):  # -> bool
    """
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
    """
    if not bool(_work):
        return False
    _extension_table = ExtensionTable()
    if not _extension_table.audio_extension_ok(_out):
        clean_temp_files(_work)
        if os.path.isfile(get_my_lock("lock")):
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
            if have_posix_app("afconvert", False):
                if not vlc_wav_to_media(_work, _out, _audible, _visible, False, _title):
                    wav_to_media(
                        _title,
                        _work,
                        _image,
                        _out,
                        _audible,
                        _visible,
                        _artist,
                        _dimensions,
                    )
                break
            elif (
                bool(_ffmpeg)
                or os.path.isfile(_test[_extension_table.standalone])
                or posix_compressor_ok(out_ext)
            ):
                wav_to_media(
                    _title,
                    _work,
                    _image,
                    _out,
                    _audible,
                    _visible,
                    _artist,
                    _dimensions,
                )
                break
            elif gst_plugin_path(_test[_extension_table.filter]):
                if not gst_wav_to_media(
                    _title,
                    _work,
                    _image,
                    _out,
                    _audible,
                    _visible,
                    _artist,
                    _dimensions,
                ):
                    vlc_wav_to_media(_work, _out, _audible, _visible, False, _title)
                break
    clean_temp_files(_work)
    if os.path.isfile(_work):
        if os.path.isfile(_out):
            try:
                os.remove(_work)
            except (OSError, FileNotFoundError):
                print("OSError: could not remove {0}".format(_work))
    return os.path.isfile(_out)


def do_gst_parse_launch(_pipe=""):  # -> bool
    """
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
    Documentation
    -------------

    [Gitlab](https://gitlab.freedesktop.org/gstreamer/gstreamer)

    *PyGObject API Reference*. "Gst 1.0 (1.22.8.0) - Gst 1.0".
    [GitHub](https://lazka.github.io/pgi-docs/#Gst-1.0)

    Stewart, Ian "GStreamer - Gst : An Introduction to using GStreamer in
    Python3 Programs". [GitHub](https://github.com/irsbugs/GStreaming), 2020.
    """
    if not _pipe:
        return True
    filesink_location = ""
    if "filesink location=" in _pipe:
        filesink_location = _pipe.rsplit("=", 1)[-1].replace('"', "")
    try:
        Gst.init(None)
        _player = Gst.parse_launch("{0}".format(_pipe))
        _player.set_state(Gst.State.NULL)
        _player.set_state(Gst.State.READY)
        _player.set_state(Gst.State.PAUSED)
        _player.set_state(Gst.State.PLAYING)
        _player.get_bus().poll(
            Gst.MessageType.EOS | Gst.MessageType.ERROR, Gst.CLOCK_TIME_NONE
        )
        _player.set_state(Gst.State.PAUSED)
        _player.set_state(Gst.State.READY)
        _player.set_state(Gst.State.NULL)
        if len(filesink_location) != 0:
            try:
                # Waits until file is ready before measuring the size.
                return os.path.getsize(filesink_location) != 0
            except FileNotFoundError:
                return False
        return True
    # gi.repository.GLib.Error: gst_parse_error: no element "filesrc" (1)
    except:
        try:
            _terminator = "\u0000"
            Gst.init(None)
            Gst.ParseContext.new()
            Gst.parse_launchv("{0}{1}".format(_pipe, _terminator))
            Gst.ParseContext.free()
            return True
        except:
            for launch in ["gst-launch-1.0"]:
                if have_posix_app(launch, False):
                    os.environ.setdefault(
                        "GST_PLUGIN_PATH", gst_plugin_path("libgstwavenc")[0]
                    )
                    gst_l = launch
                    if my_os_system("{0} {1}".format(gst_l, _pipe)):
                        print("{0} {1}".format(gst_l, _pipe))
                        if len(filesink_location) != 0:
                            try:
                                return os.path.getsize(filesink_location) != 0
                            except FileNotFoundError:
                                return False
                        return True
    return False


def web_info_translate(
    _msg="WARNING:\n\nPython `speechd` Error.", _language="en"
):  # -> bool
    """Opens a web browser with the text of the message and a local translation.
    Users of a sandboxed program can get a message."""
    try:
        _web_text = urllib.parse.quote(_msg)
    except NameError:
        _web_text = path2url(_msg).replace("file:///", "")
    try:
        if _language[:2] in ["en"]:
            _language = "es"
        webbrowser.open_new(
            "https://translate.google.com/?sl=auto&tl={0}&text={1}&op=translate".format(
                _language, _web_text
            )
        )
        return True
    except NameError:
        return False


class JsonTools(object):
    """Use simple json data"""

    def __init__(self):
        try:
            self.safe_json = str.maketrans(
                {
                    "\\": "\\u005C",
                    "{": "\\u007B",
                    "}": "\\u0070",
                    '"': "\\u0022",
                    "@": "\\u0040",
                    "|": "\\u007C",  # VERTICAL LINE
                    "'": "\\u0027",  # APOSTROPHE
                    "%": "\\u0025",  # PERCENT SIGN
                    "$": "\\u0024",  # DOLLAR
                    "&": "\\u0026",  # AMPERSAND
                    "^": "\\u005E",  # CARET
                    "!": "\\u0021",  # EXCLAMATION POINT
                }
            )
        except AttributeError:
            self.safe_json = None

    def sanitize_json(self, content=""):  # -> str
        """Escape json characters in content"""
        try:
            test_text = content.strip("\\{}\n\t")
        except AttributeError:
            try:
                test_text = content.strip("'\\{}\n\t")
                if test_text == "None":
                    return ""
            except AttributeError:
                return ""
        if bool(self.safe_json):
            return str(test_text.translate(self.safe_json))
        return (
            test_text.replace("\\", "\\u005C")
            .replace("{", "\\u007B")
            .replace("}", "\\u0070")
            .replace('"', "\\u0022")
            .replace("@", "\\u0040")
            .replace("{", "\\u007B")
            .replace("|", "\\u007C")
            .replace("}", "\\u007D")
            .replace("'", "\\u0027")
            .replace("%", "\\u0025")
            .replace("$", "\\u0024")
            .replace("&", "\\u0026")
            .replace("^", "\\u005E")
            .replace("!", "\\u0021")
            .replace('"', '\\"')
        )

    def set_json_content(
        self,
        language="en",
        voice="AUTO",
        i_rate=0,
        file_spec="",
        output_module="",
        flags="",
        album="",
        author="",
        genre="",
        title="",
        track=1,
    ):  # -> str
        """Sanitize content and return json string"""
        try:
            s_rate = str(i_rate)
        except AttributeError:
            s_rate = "0"
        try:
            s_track = str(track)
        except AttributeError:
            s_track = "1"
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
        s_key = "{0}.json".format(file_spec)
        l_cur = "{"
        r_cur = "}"
        return """{0}
  "album": "{1}",
  "author": "{2}",
  "file_spec": "{3}",
  "flags": "{4}",
  "genre": "{5}",
  "i_rate": {6},
  "i_track": {7},
  "language": "{8}",
  "output_module": "{9}",
  "secret_key": "{10}",
  "title": "{11}",
  "voice": "{12}"
{13}""".format(
            l_cur,
            album,
            author,
            file_spec,
            genre,
            flags,
            s_rate,
            s_track,
            language,
            output_module,
            s_key,
            title,
            voice,
            r_cur,
        )


def sound_length_seconds(_work):  # -> int
    """
    Tells approximately how long a sound file is in seconds as an integer
    We round up so that processes that call for sleep have time to finish.
    """
    _work_ext = os.path.splitext(_work)[1].lower()
    _return_value = 0
    mimetypes.init()
    _mime = "xxz-xzz-no-match"
    if len(_work_ext) != 0:
        try:
            _mime = mimetypes.types_map[_work_ext]
        except IndexError:
            return 0
    if _mime == mimetypes.types_map[".wav"]:
        try:
            snd_read = wave.open(_work, "r")
            _return_value = (
                math.ceil(snd_read.getnframes() // snd_read.getframerate()) + 1
            )
            snd_read.close()
        except:
            pass
    return _return_value


class ImportedMetaData(object):
    """Get your media's metadata ready to include in new media"""

    def __init__(self):  # ' -> None
        """Define shared values"""
        self.date = time.strftime("%Y-%M-%d")
        self.identity = None
        self.title = None
        self.genre = None
        self.track = None
        self.album = None
        self.composer = None
        self.year = time.strftime("%Y")
        self.image = None
        self.image_extensions = [".gif", ".jpeg", ".jpg", ".png"]
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
            self.safe_gst_pipe = str.maketrans(
                {
                    " ": "\u005C ",
                    '"': '\u005C"',
                    "'": "\u005C'",
                    ":": "\u005C:",
                    "!": "\u005C!",
                }
            )
        except AttributeError:
            self.safe_gst_pipe = None

    def get_defaults(self):  # -> None
        """Initialize the values.
        TODO: Check for and handle `.xml` or `.json` settings file"""
        if self.identity:
            if not self.composer:
                self.composer = self.identity
        else:
            self.identity = "USERNAME"
            for user_env in ["USER", "USERNAME"]:
                try:
                    self.identity = os.getenv(user_env)
                    if self.identity:
                        break
                except TypeError:
                    continue
        if not self.title:
            self.title = time_for_title()
        if not self.genre:
            self.genre = "Speech"
        if not self.track:
            self.track = str(1)
        if not self.album:
            self.album = "{0}__{1}_".format(
                app_name().lower().replace(" ", "_"), date_for_album()
            )

    def escape_gst_pipe_meta(self, test_text=""):  # -> str
        """Returns safe value for gst pipe metadata"""
        if not test_text:
            return ""
        if self.safe_gst_pipe:
            return str(test_text.translate(self.safe_gst_pipe))
        for item in """ "':!""":
            test_text = test_text.replace(item, "".join(["\u005C", item]))
        return test_text

    def execute_command(self, a_command="", safer=True):
        """
        This is similar to `os.system(a_command)`, but we can get output
        from program commands.
        """
        # a_command is a normal command line instruction.
        if safer:
            for block_item in [
                "sudo",
                "-version",
                "-quiet",
                "-log",
                "-list",
                "-help",
                "--",
                ":",
                "$",
                "|",
                "<",
                "[",
                "#",
                "%",
                "{",
                ".",
                "^",
            ]:
                if a_command.strip().startswith(block_item):
                    # it is not a command
                    return ""
        try:
            return unicode(
                subprocess.check_output(a_command, shell=True), errors="ignore"
            )
        except NameError:
            # Python 3
            try:
                retval = subprocess.check_output(a_command.encode("utf-8"), shell=True)
                return retval.decode("utf-8")
            except (
                AttributeError,
                NameError,
                OSError,
                subprocess.CalledProcessError,
                TypeError,
            ):
                # nt
                try:
                    retval = subprocess.check_output(a_command, shell=True)
                    return retval.decode("utf-8")
                except (NameError, OSError, subprocess.CalledProcessError, TypeError):
                    # For example, the command results in an error.
                    return ""
        except (OSError, subprocess.CalledProcessError):
            return ""

    def set_time_meta(self, file_path=""):  # -> str
        """Calculate the number of seconds of a local sound file. Return
        the value as a string and set the `self.seconds` value to an integer."""
        _extension_table = ExtensionTable()
        # if self.seconds:
        #    return self.seconds
        if not os.path.isfile(file_path):
            self.seconds = 0
            return self.seconds
        if os.path.splitext(file_path)[1].lower() in [".aif", ".wav"]:
            self.seconds = sound_length_seconds(file_path)
            return self.seconds
        elif _extension_table.get_mime(file_path).startswith("audio/"):
            if have_posix_app("gst-discoverer-1.0", False):
                time_list = ["_duration_not_found", "0", "0", "0"]
                _result = self.execute_command(
                    'gst-discoverer-1.0 -v "{0}" | grep Duration:', format(file_path)
                )
                # Duration: 0:00:03.857687075
                if _result:
                    _result = _result.replace(" ", "")
                    try:
                        # ['Duration', 'H', 'M', 'S']
                        time_list = _result.split(":")
                    except:
                        pass
                try:
                    self.seconds = (
                        int(float(time_list[1])) * 360
                        + int(float(time_list[2])) * 60
                        + int(float(time_list[3]) + 0.5)
                    )
                except IndexError:
                    self.seconds = 0
                return self.seconds
            else:
                return self.seconds
        else:
            return "0"

    def get_app_meta_string(self, index=13, author="", image="", out_path=""):  # -> str
        """Return the metadata options for the converter command line."""
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
        lame_image = ""
        image_uri = ""
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
                    lame_image = ' --ti "{0}"'.format(image)
                    image_uri = path2url(image)
                else:
                    image = ""
            else:
                image = ""
        gstreamer_meta = ""
        x_album = _xml_transform.clean_for_xml(album)
        x_author = _xml_transform.clean_for_xml(author)
        x_genre = _xml_transform.clean_for_xml(genre)
        x_title = _xml_transform.clean_for_xml(title)
        x_display_path = "~/..."
        profile = os.path.expanduser("~")
        for env_key in ["HOME", "HOMEPATH", "PWD"]:
            if bool(os.getenv(env_key)):
                x_display_path = _xml_transform.clean_for_xml(out_path).replace(
                    profile, "~"
                )
                break
        out_uri = ""
        if out_path:
            out_uri = path2url(out_path)
        if bool(gst_plugin_path("libgsttaglib")) and bool(
            gst_plugin_path("libgstid3demux")
        ):
            g_album = self.escape_gst_pipe_meta(album)
            g_author = self.escape_gst_pipe_meta(author)
            g_genre = self.escape_gst_pipe_meta(genre)
            g_title = self.escape_gst_pipe_meta(title)

            # When using Gst with a pipe, the Composer, Track and Date are
            # omitted. See:
            # <https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-good/html/gst-plugins-good-plugins-taginject.html>
            gstreamer_meta = """! taginject tags="album=\\"{0}\\",artist=\\"{1}\\",genre=\\"{2}\\",title=\\"{3}\\"" ! id3v2mux""".format(
                g_album, g_author, g_genre, g_title
            )
        if self.title == time_for_title() or not bool(self.title):
            gstreamer_meta = ""

        option = [
            ["Gstreamer", gstreamer_meta],  # 0
            [  # 1
                "Avconv or ffmpeg MPEG",
                """ -metadata album="{album}" -metadata artist="{author}" -metadata genre="{genre}" -metadata title="{title}" -metadata track="{track}" -metadata Year="{year}" -acodec libmp3lame -ab 320k -aq 0 """.format(
                    album=album,
                    author=author,
                    genre=genre,
                    title=title,
                    track=track,
                    year=year,
                ),
            ],
            [  # 2
                "Avconv or ffmpeg image",
                ' -i "{image}" -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (Front)" -y'.format(
                    image=image
                ),
            ],
            [  # 3
                "OGG encoder",
                """ -metadata album='{album}' -metadata artist='{author}' -metadata genre='{genre}' -metadata title='{title}' -metadata track='{track}' -metadata Year='{year}' """.format(
                    album=album,
                    author=author,
                    genre=genre,
                    title=title,
                    track=track,
                    year=year,
                ),
            ],
            [  # 4
                "Nero encoder",
                """ -meta:album="{album}" -meta:artist="{author}" -meta:genre="{genre}" -meta:title="{title}" -meta:track="{track}" -meta:year="{year}" """.format(
                    album=album,
                    author=author,
                    genre=genre,
                    title=title,
                    track=track,
                    year=year,
                ),
            ],
            [  # 5
                "Lame (Win)",
                """ {lame_image} --tl "{album}" --ta "{author}" --tt "{title}" --tg "{genre}" --tn "{track}" --ty {year} """.format(
                    lame_image=lame_image,
                    album=album,
                    author=author,
                    title=title,
                    genre=genre,
                    track=track,
                    year=year,
                ),
            ],
            [  # 6
                "Lame (Posix)",
                """ --vbr-old {lame_image} --tl "{album}" --ta "{author}" --tt "{title}" --tg "{genre}" --tn "{track}" --ty {year} """.format(
                    lame_image=lame_image,
                    album=album,
                    author=author,
                    genre=genre,
                    title=title,
                    track=track,
                    year=year,
                ),
            ],
            ["Track", "{0}".format(track)],  # 7
            ["Album or document", "{0}".format(album)],  # 8
            ["Artist or author", "{0}".format(author)],  # 9
            ["Track title", "{0}".format(title)],  # 10
            ["Genre", "{0}".format(genre)],  # 11
            [  # 12
                "VLC Playlist",
                """<?xml version="1.0" encoding="UTF-8"?>
<playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1">
    <title>Playlist</title>
    <trackList>
        <track>
            <location>{out_uri}</location>
            <creator>{x_author}</creator>
            <album>{x_album}</album>
            <duration>{seconds}500</duration>
            <title>{x_title}</title>
            <annotation>{x_genre}</annotation>
            <image>{image_uri}</image>
            <extension application="http://www.videolan.org/vlc/playlist/0">
                <vlc:id>0</vlc:id>
            </extension>
        </track>
    </trackList>
    <extension application="http://www.videolan.org/vlc/playlist/0">
        <vlc:item tid="0"/>
    </extension>
</playlist>""".format(
                    out_uri=out_uri,
                    x_author=x_author,
                    x_album=x_album,
                    seconds=seconds,
                    x_title=x_title,
                    x_genre=x_genre,
                    image_uri=image_uri,
                ),
            ],
            [  # 13
                "M3U playlist",
                """#EXTM3U\nEXTINF:{seconds},{author} - {title}\n{out_uri}\n""".format(
                    seconds=seconds, author=author, title=title, out_uri=out_uri
                ),
            ],
            [  # 14
                "Metadata",
                """ * Album: {album}\n * Artist: {author}\n * Composer: {composer}\n * Genre: {genre}\n * Title: {title}\n * Track: {track}\n * Year: {year}""".format(
                    album=album,
                    author=author,
                    composer=composer,
                    genre=genre,
                    title=title,
                    track=track,
                    year=year,
                ),
            ],
            [  # 15
                "Avconv or ffmpeg Meta File",
                """;FFMETADATA1
;https://ffmpeg.org/ffmpeg-all.html#toc-Metadata-1
title={title}
YEAR={year}
ALBUM={album}
ARTIST={author}
GENRE={genre}
track={track}""".format(
                    title=title,
                    year=year,
                    album=album,
                    author=author,
                    genre=genre,
                    track=track,
                ),
            ],
            [  # 16
                "Avconv or ffmpeg Meta",
                """ -metadata album="{album}" -metadata artist="{author}" -metadata genre="{genre}" -metadata title="{title}" -metadata track="{track}" -metadata Year="{year}" """.format(
                    album=album,
                    author=author,
                    genre=genre,
                    title=title,
                    track=track,
                    year=year,
                ),
            ],
            ["XML Track", "{0}".format(track)],  # 17
            ["XML Album or document", "{0}".format(x_album)],  # 18
            ["XML Artist or author", "{0}".format(x_author)],  # 19
            ["XML Track title", "{0}".format(x_title)],  # 20
            ["XML Genre", "{0}".format(x_genre)],  # 21
            [  # 22
                "Popup Meta",
                """<b>{x_album}</b>\n{x_title} \n<i>{x_display_path}</i>""".format(
                    x_album=x_album, x_title=x_title, x_display_path=x_display_path
                ),
            ],
        ]
        if index > len(option):
            return option[0]
        try:
            return option[index]
        except:
            return option[0]

    def meta_from_file(
        self, _file_path="", erase=False, _errors="backslashreplace"
    ):  # -> str
        """If the specified text file exists, then return the contents,
        otherwise return `''`."""
        return_value = ""
        _encoding = "utf-8"
        if os.name == "nt":
            if sys.stdin.encoding != _encoding:
                _encoding = "utf_8_sig"
        try:
            if os.path.isfile(_file_path):
                f = codecs.open(
                    _file_path, mode="r", encoding=_encoding, errors=_errors
                )
                return_value = f.read()
                f.close()
                if erase:
                    try:
                        os.remove(_file_path)
                    except:
                        pass
                return return_value
            else:
                return ""
        except UnicodeDecodeError:
            return_value = self.meta_from_file(_file_path, erase, "backslashreplace")
            print(
                """WARNING: Could not decode characters in the file:
`{0}`""".format(
                    _file_path
                )
            )
            return return_value
        except Exception:
            return ""

    def get_my_id(self, erase=True):  # -> str
        """
        Returns the user name, author, artist or performer
        """
        returned_value = self.meta_from_file(get_my_lock("lock.id"), erase)
        if bool(returned_value):
            self.identity = returned_value
        else:
            self.get_defaults()
        return self.identity

    def get_my_composer(self, erase=True):  # -> str
        """
        Returns the composer name.
        """
        returned_value = self.meta_from_file(get_my_lock("lock.composer"), erase)
        if bool(returned_value):
            self.composer = returned_value
        else:
            self.get_defaults()
        return self.composer

    def get_my_title(self, erase=True):  # -> str
        """
        Returns the song name (a. k. a. title).
        """
        returned_value = self.meta_from_file(get_my_lock("lock.title"), erase)
        if bool(returned_value):
            self.title = returned_value
        else:
            self.get_defaults()
        return self.title

    def get_my_genre(self, erase=True):  # -> str
        """
        Returns the song genre.
        """
        returned_value = self.meta_from_file(get_my_lock("lock.genre"), erase)
        if bool(returned_value):
            self.genre = returned_value
        else:
            self.get_defaults()
        return self.genre

    def get_my_track(self, erase=True):  # -> str
        """
        Returns the song track number.
        """
        returned_value = self.meta_from_file(get_my_lock("lock.track"), erase)
        if bool(returned_value):
            self.track = returned_value
        else:
            self.get_defaults()
        return self.track

    def get_my_album(self, erase=True):  # -> str
        """
        Returns the album name.
        """
        # If the file is located on a remote url
        # then the file name might be expressed
        # as a URI. Therefore, replace `%20` with
        # a space for the title.
        returned_value = self.meta_from_file(get_my_lock("lock.album"), erase).replace(
            "%20", " "
        )
        if bool(returned_value):
            self.album = returned_value
        else:
            self.get_defaults()
        return self.album

    def custom_lexicon_path(self, erase=True):  # -> str
        """
        Returns the path to a lexicon settings directory.
        """
        returned_value = self.meta_from_file(get_my_lock("lock.lexicon"), erase)
        if bool(returned_value):
            return returned_value
        return ""


class WinMediaPlay(object):
    """Play a sound file in Windows. Use `winsound` with uncompressed files
    instead because Windows Media Player takes more time to start up."""

    def __init__(self):
        """Item`[0]` of `extensions` is a file extension. Item `[1]` of
        `extensions` is an experientially calculated divisor based on
        speech using the default Windows 10 SAPI `en-US` voice. `app`
        is the path to the app or a blank string if the app is not
        found. `rest` is the approximate length of the speech in
        seconds."""
        self.extensions = [
            [".aif", 0],
            [".aiff", 0],
            [".m4a", 12209],
            [".mp2", 12209],
            [".mp3", 12209],
            [".snd", 88320],
            [".wav", 0],
            [".wma", 12209],
        ]
        self.app = get_nt_path("Windows Media Player", "wmplayer.exe")
        self.rest = 0

    def app_ok(self, file_path=""):  # -> bool
        """Can the Windows Media Player application play the sound file?
        Estimate the play time in seconds."""
        for _test in [self.app, file_path]:
            if len(_test.strip()) == 0:
                return False
        if not os.path.isfile(file_path):
            return False
        _continue = False
        _ext = os.path.splitext(file_path)[1]
        if any(_test[0] == _ext for _test in self.extensions):
            _continue = True
        if not _continue:
            return False
        _denominator = 12209
        if any(
            os.path.splitext(file_path.lower())[1] == _test[0]
            for _test in self.extensions
        ):
            _denominator = _test[1]
        if _denominator == 0:
            self.rest = sound_length_seconds(file_path)
        else:
            self.rest = int(os.path.getsize(file_path) / _denominator) + 1
        return self.rest != 0

    def _windowsmedia(self, file_path=""):  # -> bool
        """(Local use) Initiate Windows Media Player without a user interface"""
        if not os.path.isfile(file_path):
            return False
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        _app = self.app
        a = subprocess.call(
            '{0} /play /close "{1}"'.format(_app, file_path), startupinfo=startupinfo
        )
        return bool(a)

    def play(self, file_path=""):  # -> bool
        """Play an audio file using Windows Media Player. You must initialize
        with `app_ok` to check `wmplayer` and estimate the rest time, then if
        the file can be played `wmplayer` plays it. For supported audio files
        like `.wav` the Windows python3 `winsound` library is much faster."""
        if self.rest == 0:
            return False
        mythread = threading.Thread(target=self._windowsmedia, args=[file_path])
        mythread.start()
        time.sleep(self.rest)
        try:
            return os.system("taskkill /im wmplayer.exe") == 0
        except [SyntaxError, TypeError]:
            return False


def clean_temp_files(_out=""):  # -> Bool
    """Clean text and image files used to create media"""
    try:
        for _temp_file in [
            "{0}.wav.txt".format(_out),
            "{0}.txt".format(_out),
            "{0}temp.lock".format(_out),
            "{0}.wav.png".format(_out),
            "{0}.wav.jpg".format(_out),
        ]:
            if os.path.isfile(_temp_file):
                os.remove(_temp_file)
        return True
    except:
        pass
    return False


def gst_wav_to_media(
    _title="untitled",
    _work="",
    _image="",
    _out="",
    _audible="true",
    _visible="false",
    _artist="",
    _dimensions="600x600",
    _show_meta=True,
):  # -> bool
    """
    If `avconv` is not installed and `ffmpeg` is not installed, use
    `gst-launch` to convert media.  Note that gst_wav_to_media omits
    some meta-data (Image, track and year)

    Returns `True` on success, `False` if unable to create new media.
    <https://community.nxp.com/pwmxy87654/attachments/pwmxy87654/imx-processors%40tkb/15/2/i.MX8GStreamerUserGuide.pdf >
    """
    if have_posix_app("say", False):
        return False
    s_out_extension = ""
    _metas = ImportedMetaData()
    _metas.set_time_meta(_work)

    if _out:
        if os.path.isfile(_out):
            print(
                """`gst_wav_to_media` says:
`{0}` already_exists. Exiting.""".format(
                    _out
                )
            )
            return True
        s_out_extension = os.path.splitext(_out)[1].lower()
    # Use libgstid3demux? id3 is not the normal meta format of audio files
    # like .ogg, .opus and .spx! Install ffmpeg or avconv for metadata.
    b_use_id3_metadata = False
    b_audible = lax_bool(_audible)
    b_visible = lax_bool(_visible)
    pipe = ""
    in_uri = ""
    code_pad = ""
    _location = '''filesrc location="{_work}"'''.format(_work=_work)
    if not os.path.isfile(_work):
        return None
    in_uri = path2url(_work)
    in_pad = " decodebin ! audioresample "
    if os.path.splitext(_work)[1] == ".wav":
        in_pad = " wavparse "
    if s_out_extension in [".mp2", ".mp3"]:
        if gst_plugin_path("libgstlame"):
            code_pad = "! lamemp3enc"
            b_use_id3_metadata = True
    elif s_out_extension in [".mka", ".mkv"]:
        if gst_plugin_path("libgstmatroska"):
            code_pad = "! vorbisenc ! matroskamux"
    elif s_out_extension == ".flac":
        if gst_plugin_path("libgstflac"):
            code_pad = "! flacenc ! oggmux"
    elif s_out_extension in [".oga", ".ogg"]:
        if gst_plugin_path("libgstogg"):
            code_pad = "! vorbisenc ! oggmux"
    elif s_out_extension == ".opus":
        if gst_plugin_path("libgstopus"):
            # debian-12-2023-09-29
            # Opus sample rates can be 8000, 12000, 16000, 24000,
            # or 48000. Gstreamer needs a streaming pipe for the
            # resampling to work. 16000 is excellent for voice.
            # <https://datatracker.ietf.org/doc/html/rfc6716#section-4.2.9>
            _q_work = quote(_work)
            _location = 'uridecodebin uri="file://{_q_work}"'.format(_q_work=_q_work)
            in_pad = " audioconvert ! audioresample "
            code_pad = "! audio/x-raw, rate=16000 !  opusenc ! oggmux"
    elif s_out_extension == ".spx":
        if gst_plugin_path("libgstspeex"):
            code_pad = "! speexenc ! oggmux"
    elif s_out_extension == ".wav":
        if gst_plugin_path("libgstwavenc"):
            code_pad = "! wavenc"
    if code_pad:
        gmeta = ""
        if b_use_id3_metadata:
            gmeta = get_meta_data(_metas.i_gst, _artist, _image, _out)
        pipe = '''{_location} ! {in_pad} ! audioconvert {code_pad} {gmeta} ! filesink location="{_out}"'''.format(
            _location=_location,
            in_pad=in_pad,
            code_pad=code_pad,
            gmeta=gmeta,
            _out=_out,
        )
        pipe2 = '''{_location} !  ! {in_pad} ! audioconvert {code_pad} ! filesink location="{_out}"'''.format(
            _location=_location, in_pad=in_pad, code_pad=code_pad, _out=_out
        )
    if pipe:
        if do_gst_parse_launch(pipe):
            if _show_meta:
                pop_message(
                    app_name(),
                    get_meta_data(_metas.i_popup_meta, _artist, _image, _out),
                    8000,
                )
        else:
            # Try omitting the metadata
            if do_gst_parse_launch(pipe2):
                if _show_meta:
                    pop_message(app_name(), _out, 5000)
            else:
                # Error or incompatible format, so play the file
                if not s_out_extension:
                    s_out_extension = ".wav"
                if s_out_extension == ".wav" and not b_visible:
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
        if os.path.isfile(get_my_lock("lock")):
            exit()
        in_uri = path2url(_work)
        # Concise pipe; some sinks can have different settings with a verbose pipee
        pipe = 'playbin uri="{0}"'.format(in_uri)
        lock_my_lock()
        if os.path.splitext(_work)[1].lower() == ".wav":
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
            gst_wav_to_media(
                _title, _out, "", _image, "true", "false", _artist, _dimensions
            )
        elif b_visible:
            print(
                """Play is off - file will not play.
The file was saved to:  {0}""".format(
                    _out
                )
            )
    return True


class VlcMuxInfo(object):
    """The default settings for VideoLAN VLC media conversions"""

    def __init__(self):
        """Default conversion setting variables"""
        self.ext = []
        self.audio_codec = ""
        self.average_bitrate = ""
        self.sample_rate = ""
        self.mux = ""
        self.channel_count = "1"

    def opus(self):
        """Opus is a free and flexible audio codec"""
        self.ext = [".opus"]
        self.audio_codec = "opus"
        self.average_bitrate = "16"
        self.sample_rate = "16000"
        self.mux = "ogg"
        self.channel_count = "2"

    def flac(self):
        """Flac is a free high quality audio codec"""
        self.ext = [".flac"]
        self.audio_codec = "flac"
        self.average_bitrate = "128"
        self.sample_rate = "44100"
        self.mux = "raw"
        self.channel_count = "1"

    def mp3(self):
        """Mp3 is a common audio codec"""
        self.ext = [".mp3"]
        self.audio_codec = "mp3"
        self.average_bitrate = "128"
        self.sample_rate = "44100"
        self.mux = "dummy"
        self.channel_count = "2"

    def ogg(self):
        """Ogg is a free audio codec"""
        self.ext = [".ogg", ".oga"]
        self.audio_codec = "vorb"
        self.average_bitrate = "128"
        self.sample_rate = "44100"
        self.mux = "ogg"
        self.channel_count = "2"

    def wave(self):
        """A wave file is a standard uncompressed audio format"""
        self.ext = [".wav"]
        self.audio_codec = "s161"
        self.average_bitrate = "0"
        self.sample_rate = "16000"
        self.mux = "wav"
        self.channel_count = "1"

    def evaluate_ext(self, _ext):
        """Set up the variables according to the file extension"""
        if _ext in self.ext:
            return True
        return False


def vlc_wav_to_media(
    in_sound_path="",
    out_sound_path="",
    _audible="true",
    _visible="false",
    allow_linux_snap=False,
    _show_meta=True,
    _title="untitled",
):  # -> bool
    """Converts a wav audio file to a plain mp3 or ogg muxed audio file.
    This conversion does not include meta-data. Retunrs `True` if a new
    file is created, otherwise `False`."""
    _extension_table = ExtensionTable()
    app = _extension_table.vlc
    if not bool(app):
        if allow_linux_snap:
            if have_posix_app("vlc", True):
                app = "vlc"
        if not bool(app):
            return False
    elif not os.path.isfile(in_sound_path):
        return False
    elif not bool(out_sound_path):
        return False
    b_audible = lax_bool(_audible)
    b_visible = lax_bool(_visible)
    ext = os.path.splitext(out_sound_path)[1]
    channel_count = ["1", "2"][1]  # mono, stereo
    verbosity = ["", "-vvv "][0]  # no debug, debug
    _mux_info = VlcMuxInfo()
    if ext == ".flac":
        _mux_info.flac()
    elif ext == ".mp3":
        _mux_info.mp3()
    elif ext in [".ogg", ".oga"]:
        _mux_info.ogg()
    elif ext == ".opus":
        _mux_info.opus()
    elif ext == ".wav":
        _mux_info.wave()
    else:
        return False
    command = """{app} "{in_sound_path}" --intf dummy {verbosity}--sout="#transcode{{vcodec=none,acodec={audio_codec},ab={average_bitrate},channels={channel_count},samplerate={sample_rate}}}:std{{access=file,mux={mux},dst='{out_sound_path}'}}" vlc://quit""".format(
        app=app,
        in_sound_path=in_sound_path,
        verbosity=verbosity,
        audio_codec=_mux_info.audio_codec,
        average_bitrate=_mux_info.average_bitrate,
        channel_count=channel_count,
        sample_rate=_mux_info.sample_rate,
        mux=_mux_info.mux,
        out_sound_path=out_sound_path,
    )
    if my_os_system(command):
        if _show_meta:
            pop_message(app_name(), out_sound_path, 5000)
        print(
            """
VideoLAN VLC 
============
* audio codec = '{audio_codec}'
* average bitrate = '{average_bitrate}'
* channel count = '{channel_count}'
* mux = '{mux}'
* sample rate = '{sample_rate}'
""".format(
                audio_codec=_mux_info.audio_codec,
                average_bitrate=_mux_info.average_bitrate,
                channel_count=channel_count,
                mux=_mux_info.mux,
                sample_rate=_mux_info.sample_rate,
            )
        )
        if b_visible and b_audible:
            show_with_app(out_sound_path)
        elif b_audible:
            lock_my_lock()
            play_wav_no_ui(out_sound_path)
            unlock_my_lock()
        return True
    return False


def get_meta_data(_index=0, _artist="", _image="", _work=""):  # -> str
    """Get a metadata command string for a program.
    * `_index` is an integer that tells which program command format.
    * `_artist` is an author, artist or composer specified
      on the command line.
    + `_image` is the path to a cover image
    + `_work` is the local path to the source sound file.
    """
    # Look up data
    _metas = ImportedMetaData()
    _metas.set_time_meta(_work)
    # Format the string with tags
    _text = _metas.get_app_meta_string(_index, _artist, _image, _work)[1]
    if bool(_text) and bool(_work):
        _title = _metas.get_app_meta_string(_index, _artist, _image, _work)[0]
        _info = _metas.get_app_meta_string(_metas.i_pretty, _artist, _image, _work)[1]
        print("\n## {0} ##\n\n{1}".format(_title, _info))
    return _text


def wav_to_media(
    _title="",
    _work="",
    _image="",
    _out="",
    _audible="",
    _visible="",
    _artist="",
    _dimensions="",
):  # -> None
    """
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
    """
    _metas = ImportedMetaData()
    _metas.set_time_meta(_work)
    _xml_transform = XmlTransform()
    _extension_table = ExtensionTable()
    _out_ext = os.path.splitext(_out)[1].lower()
    _work_ext = os.path.splitext(_work)[1].lower()
    _ffmpeg_avconv = ffmpeg_path()
    if not os.path.isfile(_image):
        # Video encoders fail if there's no image or stream.
        if "video/" in _extension_table.get_mime(_out):
            _image = app_icon_image("poster-001.png")
    lock_my_lock()
    if len(_dimensions) == 0:
        _dimensions = "600x600"
    # Check for mimetype extensions like `.aif` and `.aiff.`
    mimetypes.init()
    try:
        _meta_data = ""
        if lax_mime_match(_out_ext, ".ogg"):
            # '.ogg', '.oga', '.opus' - 'audio/ogg'
            _meta_data = get_meta_data(_metas.i_ffmpeg_meta, _artist, _out)
            if os.name == "nt":
                # C:/opt/oggenc2.exe
                # Get oggenc2.exe: http://www.rarewares.org/ogg-oggenc.php
                nt_command = get_nt_path("oggenc2", "oggenc2")
                if bool(nt_command):
                    nt_command = get_nt_path("oggenc", "oggenc")
                if nt_command:
                    my_os_system('"{0}" -o "{1}" "{2}"'.format(nt_command, _out, _work))
                elif bool(_ffmpeg_avconv):
                    my_os_system(
                        '"{0}" -i "{1}" {2} -acodec libvorbis -ab 320k -aq 0 -y "{3}"'.format(
                            _ffmpeg_avconv, _work, _meta_data, _out
                        )
                    )
            else:
                my_os_system(
                    '"{0}" -i "{1}" {2} -acodec libvorbis -ab 320k -aq 0 -y "{3}"'.format(
                        _ffmpeg_avconv, _work, _meta_data, _out
                    )
                )
        elif _out_ext in [".aac"]:
            if have_posix_app("afconvert", False):
                my_os_system('afconvert -f adts -d aac "{0}" "{1}"'.format(_work, _out))
        elif _out_ext in [".m4a", "m4r"]:
            if have_posix_app("afconvert", False):
                my_os_system('afconvert -f m4af -d aac "{0}" "{1}"'.format(_work, _out))
        elif lax_mime_match(_out_ext, ".mp3"):
            # Try lame for mp3 or 'audio/mpeg' files that haven't been
            #  dealt with above.
            s_lame = ""
            if have_posix_app("lame", False):
                s_lame = "lame"
            elif (
                have_posix_app("twolame", False) and os.path.splitext(_out)[1] == ".mp2"
            ):
                s_lame = "twolame"
            elif os.name == "nt":
                if get_nt_path("lame", "lame"):
                    s_lame = get_nt_path("lame", "lame")
                elif (
                    get_nt_path("twolame", "twolame")
                    and os.path.splitext(_out)[1] == ".mp2"
                ):
                    s_lame = get_nt_path("twolame", "twolame")

            if bool(s_lame):
                if os.name == "nt":
                    # See: http://www.rarewares.org/mp3-lame-bundle.php
                    _meta_data = get_meta_data(_metas.i_winlame, _artist, _out)
                    my_os_system(
                        '{0} -V 4 {1} "{2}" "{3}"'.format(
                            s_lame, _meta_data, _work, _out
                        )
                    )
                else:
                    _meta_data = get_meta_data(_metas.i_unixlame, _artist, _image, _out)
                    my_os_system(
                        '{0} {1} "{2}" "{3}"'.format(s_lame, _meta_data, _work, _out)
                    )
            elif bool(_ffmpeg_avconv):
                if len(_image) != 0:
                    _out_temp = "{0}.mp3".format(_out)
                else:
                    _out_temp = _out
                _meta_data = get_meta_data(_metas.i_avconv, _artist, _image, _out)
                my_os_system(
                    '{0} -i "{1}" {2} "{3}"'.format(
                        _ffmpeg_avconv, _work, _meta_data, _out_temp
                    )
                )
                if len(_image) != 0:
                    # Add image.  Make a straight copy of the audio
                    # so the quality remains the same.
                    _meta_data = get_meta_data(_metas.i_avimage, _artist, _image, _out)
                    my_os_system(
                        '{0} -i "{1}" {2} "{3}"'.format(
                            _ffmpeg_avconv, _out_temp, _meta_data, _out
                        )
                    )
                    if os.path.isfile(_out):
                        os.remove(_out_temp)
                    else:
                        os.rename(_out_temp, _out)
        elif lax_mime_match(_out_ext, ".aif"):
            # .aif doesn't have metadata.
            my_os_system('"{0}" -i "{1}" -y "{2}"'.format(_ffmpeg_avconv, _work, _out))
        elif lax_mime_match(_out_ext, ".flac"):
            # flac - free lossless audio codec.
            _meta_data = get_meta_data(_metas.i_ffmpeg_meta, _artist, _image, _out)
            # https://ffmpeg.org/ffmpeg-all.html#flac-1
            if os.name == "nt":
                # The programs is supplied in a zip file.  To use it,
                # extract it to the directory shown.
                # C:/opt/flac.exe
                # See: http://flac.sourceforge.net/
                nt_command = get_nt_path("flac", "flac")
                if bool(nt_command):
                    my_os_system(
                        '"{0}" -f -o "{1}" "{2}"'.format(nt_command, _out, _work)
                    )
                else:
                    my_os_system(
                        '"{0}" -i "{1}" -af aformat=s16:44100 {2} -y "{3}"'.format(
                            _ffmpeg_avconv, _work, _meta_data, _out
                        )
                    )
            else:
                my_os_system(
                    '"{0}" -i "{1}" -af aformat=s16:44100 {2} -y "{3}"'.format(
                        _ffmpeg_avconv, _work, _meta_data, _out
                    )
                )
        elif lax_mime_match(_out_ext, ".webm") and bool(_ffmpeg_avconv):
            # Chrome, Firefox (Linux) and totem can open webm directly.
            _meta_data = get_meta_data(_metas.i_ffmpeg_meta, _artist, _out)
            my_os_system(
                '{0} -loop 1 -i "{1}" -i "{2}" -c:v libvpx -r 1 -c:a copy -shortest {3} -acodec libvorbis -ab 320k -aq 0 -auto-alt-ref 0 -y "{4}"'.format(
                    _ffmpeg_avconv, _image, _work, _meta_data, _out
                )
            )
        elif lax_mime_match(_out_ext, ".ogv") and bool(_ffmpeg_avconv):
            _meta_data = get_meta_data(_metas.i_ffmpeg_meta, _artist, _out)
            my_os_system(
                '{0} -loop 1 -i "{1}" -i "{2}" -c:v libtheora -r 1 -c:a copy -shortest {3} -acodec libvorbis -ab 320k -aq 0 -y "{4}"'.format(
                    _ffmpeg_avconv, _image, _work, _meta_data, _out
                )
            )
        elif _out_ext in [".m4v", ".mp4"] and bool(_ffmpeg_avconv):
            _program = "ffmpeg"
            if "avconv" in _ffmpeg_avconv.lower():
                _program = "avconv"
            _meta_data = get_meta_data(_metas.i_avconv, _artist, _out)
            if my_os_system(
                '{0} -loop 1 -i "{1}" -i "{2}"  -ac 2 -c:v libx264 -r 25 -c:a aac -shortest {3} -y "{4}"'.format(
                    _ffmpeg_avconv, _image, _work, _meta_data, _out
                )
            ):
                print(
                    """WARNING: The {0} encoder uses `libx264` and `aac`
to encode video and audio tracks. Some Windows and MacOS
players cannot play this `video/mp4` file. Try [VideoLan
VLC](https://videolan.org/vlc).""".format(
                        _program
                    )
                )
            else:
                print(
                    """FAIL: The {0} app is missing
the `libx264` or `aac` package to convert media to`video/mp4`.""".format(
                        _program
                    )
                )
        else:
            _out = _work
        if os.path.isfile(_out):
            if not lax_bool(_audible):
                print(
                    """Play is off - file will not play.
'The file was saved to:   {0}""".format(
                        _out
                    )
                )
                if have_posix_app("osascript", False):
                    pop_message(app_name(), _out, 8000)
                else:
                    pop_message(
                        app_name(),
                        get_meta_data(_metas.i_popup_meta, _artist, _image, _out),
                        8000,
                    )
            else:
                # Play the file
                if not lax_bool(_visible):
                    play_wav_no_ui(_out)
                else:
                    show_with_app(_out)
        else:
            print("No output file was created.")
        clean_temp_files(_out)
    except IOError:
        print(app_name() + " Tools execution failed")
        pop_message(app_name(), "python error", 5000)
        sys.exit(2)
    unlock_my_lock()


def clean_str(test_text="", beautify_quotes=True):  # -> str
    """
    * `test_text` - string to clean
    * `beautify_quotes` - use smart quotes

    Modifies some characters from strings for use in 'song' data.

    For this toolbox, `test_text = 'Blah'`  is good, but `
    test_text = "Blah"` is bad.
    """
    if not test_text:
        return ""
    _text = test_text
    try:
        if beautify_quotes:
            for quot in [[" '", " \u2018"], [' "', " \u201C"]]:
                _text = _text.replace(quot[0], quot[1])
        try:
            if beautify_quotes:
                trans_quot = str.maketrans({"'": "\u2019", '"': "\u201D"})
                _text = str(_text.translate(trans_quot))
            trans_essentials = str.maketrans(
                {"\n": " ", "\f": "", "\r": "", "\t": "", '"': " "}
            )
            return str(_text.translate(trans_essentials))
        except (AttributeError, NameError):
            if beautify_quotes:
                for quot in [["'", "\u2019"], ['"', "\u201D"]]:
                    _text = _text.replace(quot[0], quot[1])
            for pair1 in [["\n", " "], ["\f", ""], ["\r", ""], ["\t", " "], ['"', " "]]:
                _text = _text.replace(pair1[0], pair1[1])
            return _text
    except UnicodeDecodeError:
        print(_text + " error in readtexttools.clean_str")
    return _text


def count_items_in_dir(_dir=""):
    """Count many items are in a directory"""
    _init = 0
    if not os.path.isdir(_dir):
        return _init
    for _path in os.listdir(_dir):
        if os.path.exists(os.path.join(_dir, _path)):
            _init += 1
    return _init


def time_for_title():  # -> str
    """
    Returns an unambiguous time expression for a title in an
    international format
    """
    return time.strftime("%Y-%m-%d_%H:%M:%S-%Z")


def date_for_album():  # -> str
    """
    Returns a date expression for an album in an international
    format.
    """
    return time.strftime("%Y-%m-%d")


def check_title(_title="", _tool=""):  # -> str
    """
    If it is not a working title, replace title.
    """
    try:
        if len(_title) == 0:
            return _tool + " " + time_for_title()
        else:
            return _title
    except UnicodeDecodeError:
        return _tool + " " + time_for_title()


def check_artist(_artist):  # -> str
    """
    If not a working artist, replaces artist with user name.
    """
    _metas = ImportedMetaData()

    try:
        if len(_artist) != 0:
            return _artist
        else:
            return _metas.get_my_id(False)
    except UnicodeDecodeError:
        return _metas.get_my_id(False)


def lock_my_lock(lock="lock"):  # -> None
    """
    Create a file that informs the world that the application.
    is at work.
    """
    write_plain_text_file(get_my_lock(lock), app_signature())


def unlock_my_lock(lock="lock"):  # -> None
    """
    Create a file that informs the world that the application
    is finished.
    """
    try:
        os.remove(get_my_lock(lock))
    except:
        pass


def get_my_lock(_lock=""):  # -> str
    """
    Returns path to a temporary directory plus a lock file name.
    Use an value like 'lock' for `_lock`.  You can use more than
    one lock if you use different values for `_lock`.
    """
    if not _lock:
        return ""
    _lock = remove_unsafe_chars(_lock, "[]\\{}%|*/")
    p_lock = ".{0}".format(_lock)
    app_sign = app_signature()
    env_path = os.getenv("READTEXTTEMP")

    if (
        env_path is not None
        and os.path.isdir(env_path)
        and os.access(env_path, os.W_OK)
    ):
        if os.name == "nt":
            return os.path.join(
                env_path, app_sign + "." + os.getenv("USERNAME") + p_lock
            )
        elif have_posix_app("say", False):
            if bool(os.getenv("USERNAME")):
                return os.path.join(
                    env_path, app_sign + "." + os.getenv("USERNAME") + p_lock
                )
            else:
                # MacOS 11
                return os.path.join(
                    env_path, app_sign + "." + os.getenv("USER") + p_lock
                )
        else:
            return os.path.join(env_path, app_sign + "." + os.getenv("USER") + p_lock)
    elif os.name == "nt":
        return os.path.join(
            os.getenv("TMP"), app_sign + "." + os.getenv("USERNAME") + p_lock
        )
    elif have_posix_app("say", False):
        if bool(os.getenv("TMPDIR")):
            mac_temp = os.getenv("TMPDIR")
        elif bool(os.getenv("TMP")):
            mac_temp = os.getenv("TMP")
        else:
            mac_temp = os.join(os.path.expanduser("~"), "_temporary")
        if bool(os.getenv("USERNAME")):
            mac_user = os.getenv("USERNAME")
        elif bool(os.getenv("USER")):
            mac_user = os.getenv("USER")
        else:
            mac_user = "MacUser"
        return os.path.join(mac_temp, app_sign + "." + mac_user + p_lock)
    else:
        if os.path.isdir("/tmp") and os.access("/tmp", os.W_OK):
            return os.path.join("/tmp", app_sign + "." + os.getenv("USER") + p_lock)
        elif os.path.isdir(
            os.path.join(os.path.expanduser("~"), ".config/")
        ) and os.access(os.path.join(os.path.expanduser("~"), ".config/"), os.W_OK):
            return os.path.join(
                os.path.expanduser("~"),
                ".config/" + app_sign + "." + os.getenv("USER") + p_lock,
            )
        else:
            return os.path.join(
                os.path.expanduser("~"), app_sign + "." + os.getenv("USER") + p_lock
            )
    return ""


def media_mac_os_ok(_out=""):  # -> bool
    """MacOS native apps can play the media type"""
    return os.path.splitext(_out)[1] in [
        ".aif",
        ".aiff",
        ".wav",
        ".aac",
        "mp4",
        ".mp3",
        ".m4v",
        ".m4a",
        ".mov",
        ".dv",
        ".mpeg",
        ".avi",
    ]


def media_open_browser_ok(_out=""):  # -> bool
    """Most web browser apps can play the media type"""
    return os.path.splitext(_out)[1] in [
        ".flac",
        "mp2",
        ".mp3",
        ".m4a",
        ".mpeg",
        ".ogg",
        ".opus",
        ".spx",
        ".webm",
    ]


def app_mac_os_command(_app="Safari", _out=""):  # -> str
    """If a GUI Media App is installed in a normal Application directory then
    return a command to play a media file, otherwise return `''`."""
    _search = "".join([_app.replace(".app", ""), ".app"])
    _app_description = _app.lower().replace(".app", "")
    for _prefix in [
        "/",
        "/System",
        os.path.expanduser("~/"),
        os.path.expanduser("~/System"),
    ]:
        _dir = os.path.join(_prefix, "Applications", _search)
        if os.path.exists(_dir):
            return 'open -a "{0}" "{1}"'.format(_app_description, _out)
    return ""


def show_with_app(_out):  # -> bool
    """
    Same as double clicking the document - opens in default application.
    """
    if have_posix_app("say", False):
        # MacOS - override defaults for audio media
        _command = ""
        if media_open_browser_ok(_out) or media_mac_os_ok(_out):
            for _application in ["Brave", "Chrome", "Edge", "VLC"]:
                _command = app_mac_os_command(_application, _out)
                if len(_command) != 0:
                    break
        if len(_command) == 0:
            if media_open_browser_ok(_out):
                for _application in ["Firefox", "Firefox LTS"]:
                    _command = app_mac_os_command(_application, _out)
                    if len(_command) != 0:
                        break
        if len(_command) == 0:
            if media_mac_os_ok(_out):
                for _application in ["Orion", "Safari", "QuickTime Player"]:
                    _command = app_mac_os_command(_application, _out)
                    if len(_command) != 0:
                        break
        if len(_command) == 0:
            # Default for MacOS.
            _command = 'open "{0}"'.format(_out)
        return my_os_system(_command)
    elif os.name == "nt":
        # Windows
        try:
            os.startfile(_out)
            return True
        except NameError:
            return False
    else:
        for opener in ["xdg-open", "gnome-open", "kde-open"]:
            if have_posix_app(opener, True):
                _open = opener
                my_os_system('{0} "{1}"'.format(_open, _out))
                return True
    return False


def path2url(_file_path):  # -> str
    """Convert a file path to a file URL"""
    try:
        return urlparse.urljoin("file:", urllib.pathname2url(_file_path))
    except NameError:
        # Fall back works on Posix
        return "file://{0}".format(_file_path.replace(" ", "%20"))


def office_user_dir(_top="uno_packages"):  # -> str
    """Returns the local user directory where office stores user assets like
    uno_packages, settings and images. See also `app_icon_image()` for a
    resource search restricted to this extension directory, which your program
    should treat as read-only."""
    path_root = os.path.split(os.path.realpath(__file__))[0]
    os_sep = os.sep
    folders = path_root.split(os_sep)
    drill = os_sep
    if os.name == "nt":
        drill = ""
    for _subdir in folders:
        if _subdir == _top:
            if os.name == "nt":
                return drill.replace(":", ":{os_sep}".format(os_sep=os_sep))
            return drill
        drill = os.path.join(drill, _subdir)
    return drill


def memory_warning():
    """Memory warning for local pronunciation. A looping
    function can increase exponentially with malicious data"""
    return """
WARNING: A user entered phoneme string values that cause an
unexpected increase in the string size. Check the phoneme values
for an unusually large length. Python is breaking now to protect
your system. Some words might not be pronounced correctly."""


def prefix_ohs(_int=1, _str_len=10, _symbol="0"):  # -> str
    """Given an integer `_int`, returns a string of length `_str_len`
    prefixed by `_symbol` character (zeros by default)."""
    _ohs = _str_len * _symbol
    return (_ohs + str(_int))[0 - _str_len :]


# NOTE:
# -----
#
# A particular model uses a subset of the International Phonetic Alphabet
# (IPA). To check which symbols are supported in a specific language
# model, consult the `phonemes` field in the `test_xx-xx.jsonl` at the
# `rhasspy/piper` GitHub site.
# [link](https://github.com/rhasspy/piper/tree/master/etc/test_sentences)
#
# Some language models allow you to embed phonetuc code inline with the text
# using delimiters to signal that it is a code.
#
#     He [sed] that he was fine.
#     He /sed/ that he was fine.
#
# Code example:
#
# <https://raw.githubusercontent.com/rhasspy/piper/master/etc/test_sentences/test_en-us.jsonl>


def uses_international_phonetic_alphabet(_str_test=""):  # -> bool
    """Return True if `_str_test` uses the International Phonetic
    Alphabet. IPA Extensions is a block (U+0250 to U+02AF) of the
    Unicode standard."""
    if len(_str_test) == 0:
        return False
    _min = 592  # int("0250", 16)
    _max = 687  # int("02AF", 16)
    if len(_str_test) == 1:
        _test = ord(_str_test)
        return False if _test < _min else False if _test > _max else True
    if any(chr(_test) in _str_test for _test in range(_min, _max)):
        return True
    return False


def local_pronunciation(
    iso_lang="en-CA",
    text="",
    my_dir="macos_say",
    my_env="MACOS_SAY_USER_DIRECTORY",
    is_dev=False,
    _verbose=False,
    _phonemic_alphabet="",
):  # -> list [str]
    """Given a language and region, compatible audible lexical code for
    localized words and phrases. If `is_dev` is `True`, then the last
    item of the list is a json string representing grapheme to phoneme
    transliterations with a correct and concise format, otherwise returns
    `''`. It's normally `False` to reduce extra processing.
    """
    _json_file = ""
    _json_text = ""
    _pls_text = ""
    _json_tools = JsonTools()
    _imported_meta = ImportedMetaData()
    _used_graphemes = [""]
    _good_list = []
    _user_dir = os.path.join(office_user_dir(), "config", "lexicons", my_dir)
    if my_env in os.environ:
        _user_dir = os.getenv(my_env)
    for _lang in [iso_lang, iso_lang.split("-")[0].split("_")[0]]:
        _test = _lang
        _os_sep = os.sep
        _json_search1 = app_icon_image(
            "{0}_lexicon.json".format(_test), "po{0}{1}".format(_os_sep, my_dir)
        )
        _json_search2 = os.path.join(_user_dir, "{0}_lexicon.json".format(_test))
        _json_search3 = os.path.join(
            _imported_meta.custom_lexicon_path(),
            my_dir,
            "{0}_lexicon.json".format(_test),
        )
        for _json_search in [_json_search3, _json_search2, _json_search1]:
            if len(_json_search) != 0 and os.path.isfile(_json_search):
                _json_file = _json_search
                break
        if len(_json_file) != 0:
            break
    if len(_json_file) == 0:
        print(
            """NOTE: Did not edit the text because no `{0}_lexicon.json`
file for `{1}` was found.""".format(
                _test, my_dir
            )
        )
        return [text, _json_text]
    _date = time.strftime("%Y-%m-%d_%H:%M:%S")
    try:
        _content = ""
        with codecs.open(
            _json_file, mode="r", encoding="utf-8", errors="replace"
        ) as file_obj:
            _content = file_obj.read()
        with codecs.open(
            _json_file, mode="r", encoding="utf-8", errors="replace"
        ) as file_obj:
            data = json.load(file_obj)
            l_text = text.lower()
            if bool(data):
                if is_dev:
                    # return json with standard formatting and
                    # removing duplicate graphemes in list item
                    _xml_transform = XmlTransform()
                    _count_j = 0
                    _json_text = "{\n"
                    _footnotes = [
                        '    "{0}_99998":{{"g":"$[LOCALE]","p":"{1}"}},'.format(
                            _test, _test
                        ),
                        '    "{0}_99999":{{"g":"$[REVISION]","p":"{1}"}}'.format(
                            _test, _date
                        ),
                        "}",
                        "",
                    ]
                    do_ipa_test = uses_international_phonetic_alphabet(_content)
                    _note = "Phonemic alphabet: {0}".format(_phonemic_alphabet)
                    if len(_phonemic_alphabet) == 0:
                        if do_ipa_test:
                            _note = "https://en.wikipedia.org/wiki/International_Phonetic_Alphabet"
                            _phonemic_alphabet = "ipa"
                        else:
                            _note = "https://en.wikipedia.org/wiki/X-SAMPA"
                            _phonemic_alphabet = "x-sampa"
                    _pls_text = """<?xml version="1.0" encoding="UTF-8"?>
<lexicon version="1.0"
\txmlns="http://www.w3.org/2005/01/pronunciation-lexicon"
\txmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
\txsi:schemaLocation="http://www.w3.org/2005/01/pronunciation-lexicon http://www.w3.org/TR/2007/CR-pronunciation-lexicon-20071212/pls.xsd"
\talphabet="{0}" xml:lang="{1}">
<!-- REVISION: {2}
{3} -->""".format(
                        _phonemic_alphabet, iso_lang, _date, _note
                    )
                    _u007b = "{"
                    _u0070 = "}"
                    for _item in data:
                        _grapheme = _json_tools.sanitize_json(data[_item]["g"])
                        _phoneme = _json_tools.sanitize_json(data[_item]["p"])
                        if data[_item]["g"] in [
                            data[_item]["g"].upper(),
                            data[_item]["g"].capitalize(),
                        ]:
                            test_item = data[_item]["g"]
                        else:
                            # Where possible, avoid invisible duplications
                            # <https://docs.python.org/3/howto/unicode.htmls>
                            try:
                                test_item = data[_item]["g"].casefold()
                            except (AttributeError, SyntaxError):
                                test_item = data[_item]["g"].lower()
                        if (
                            "$[" in _grapheme
                            or test_item in _used_graphemes
                            or len(_phoneme) == 0
                        ):
                            continue
                        _used_graphemes.append(test_item)
                        _good_list.append(
                            '":{0}"g":"{1}","p":"{2}"{3},'.format(
                                _u007b, _grapheme, _phoneme, _u0070
                            )
                        )
                        _grapheme = _xml_transform.clean_for_xml(data[_item]["g"])
                        _alias = _xml_transform.clean_for_xml(data[_item]["p"])
                        # W3C -> World Wide Web Consortium
                        _apre = "</grapheme>\n\t\t<alias>"
                        _apost = "</alias>\n\t</lexeme>"
                        if do_ipa_test:
                            if (_alias.startswith("[") and _alias.endswith("]")) or (
                                _alias.startswith("/") and _alias.endswith("/")
                            ):
                                # IPA or X-SAMPA
                                # said -> [sed] or said -> /sed/
                                _alias = _alias[:-1][1:]
                                _apre = "</grapheme>\n\t\t<phoneme>"
                                _apost = "</phoneme>\n\t</lexeme>"
                                do_ipa_test = False
                        if do_ipa_test:
                            if any(
                                uses_international_phonetic_alphabet(_letter)
                                for _letter in _alias
                            ):
                                # W3C -> wɝːld waɪd web kənˈsɔːr.ʃəm
                                _apre = "</grapheme>\n\t\t<phoneme>"
                                _apost = "</phoneme>\n\t</lexeme>"
                        _pls_text = "{0}{1}{2}{3}{4}{5}".format(
                            _pls_text,
                            "\n\t<lexeme>\n\t\t<grapheme>",
                            _grapheme,
                            _apre,
                            _alias,
                            _apost,
                        )
                    _good_list = sorted(sorted(_good_list), key=len)
                    _pls_text = "{0}{1}".format(_pls_text, "\n</lexicon>\n")
                    for _item in _good_list:
                        _count_j += 1
                        _json_text = "{0}{1}{2}{3}{4}{5}{6}".format(
                            _json_text,
                            '    "',
                            _test,
                            "_",
                            prefix_ohs(_count_j, 5, "0"),
                            _item,
                            "\n",
                        )
                    for _addenda in _footnotes:
                        _json_text = "{0}{1}{2}".format(_json_text, _addenda, "\n")
                        if _verbose:
                            try:
                                print("\n{0}".format(_json_text))
                            except UnicodeEncodeError:
                                pass
            _len_text3 = len(text) * 3
            try:
                if _len_text3 > sys.maxsize / 2:
                    _len_text3 = sys.maxsize / 2
            except [AttributeError, NameError]:
                _len_text3 = 1073741823
            for _item in data:
                if len(data[_item]["g"]) == 0:
                    continue
                elif len(text) == 0:
                    break
                elif len(text) > _len_text3:
                    print(memory_warning())
                    break
                grapheme = data[_item]["g"].lower()
                if l_text.count(grapheme) != 0 or "]" in grapheme:
                    text = text.replace(data[_item]["g"], data[_item]["p"]).replace(
                        grapheme, data[_item]["p"]
                    )
    except KeyError:
        _pls_text = ""
        print(
            """WARNING: A text string was not edited because a `json` lexicon
is incorrectly formatted for this application. (`KeyError`)

{0}""".format(
                _json_file
            )
        )
        _json_text = """{{
    "{0}_99997":{{"g":"$[ERROR]","p":"JSONDecodeError"}},
    "{1}_99998":{{"g":"$[LOCALE]","p":"{2}"}},
    "{3}_99999":{{"g":"$[REVISION]","p":"{4}"}}
}}""".format(
            _test, _test, _test, _test, _date
        )
    except ImportError:  # i. e. : python 3 json.decoder.JSONDecodeError:
        _pls_text = ""
        print(
            """WARNING: A text string was not edited because a `json` lexicon
file is missing or is incorrectly formatted for this application.

{0}.""".format(
                _json_file
            )
        )
        _json_text = """{{
    "{0}_99997":{{"g":"$[ERROR]","p":"JSONDecodeError"}},
    "{1}_99998":{{"g":"$[LOCALE]","p":"{2}"}},
    "{3}_99999":{{"g":"$[REVISION]","p":"{4}"}}
}}""".format(
            _test, _test, _test, _test, _date
        )
    return [text.strip(), _json_text, _pls_text]


def pipewire_supported():  # -> bool
    """Check if the system has compatible pipewire audio."""
    # Check that the distribution works with .mp3 before adding to the list.
    if os.name != "posix":
        return False
    _ed_ver = ["0", "3", "48"]
    _meta = ImportedMetaData()
    try:
        if have_posix_app("pw-cat", False):
            _ed_ver = safechars(
                _meta.execute_command("pw-cat --version | grep Linked"),
                "1234567890.",
            ).split(".")
            if int(_ed_ver[0]) != 0 or (int(_ed_ver[1]) > 2 and int(_ed_ver[2]) > 64):
                return True
    except (IndexError, TypeError, ValueError):
        pass
    return False


class PosixAudioPlayers(object):
    """Check for an available player on platforms like Linux and MacOS"""

    def __init__(self):
        """List of known sound file players"""
        self.afplay_exts = [
            ".3gp",
            ".3g2",
            ".aac",
            ".adts",
            ".aiff",
            ".aif",
            ".amr",
            ".m4a",
            ".m4r",
            ".m4b",
            ".caf",
            ".ec3",
            ".flac",
            ".mp1",
            ".mp2",
            ".mp3",
            ".mpeg",
            ".mpa",
            ".mp4",
            ".snd",
            ".wav",
            ".w64",
        ]
        self.apt_get = 0
        self.app = 1
        self.command_get = 2
        self.universal_play = 3  # verified to play compressed formats
        self.found_player = "Unknown player"
        first_player = ["afplay", "afplay", '"%(file_path)s"', True]  # Darwin
        if pipewire_supported():
            first_player = ["pipewire-bin", "pw-cat", '-p "%(file_path)s"', True]
        self.players = [
            first_player,
            ["paplay", "paplay", '"%(file_path)s"', False],
            ["esdplay", "esdplay", '"%(file_path)s"', False],
            ["ossplay", "ossplay", '"%(file_path)s"', False],
            ["artsplay", "artsplay", '"%(file_path)s"', False],
            ["roarcat", "roarcat", '"%(file_path)s"', False],
            ["roarcatplay", "roarcatplay", '"%(file_path)s"', False],
            ["aplay", "aplay", ' --nonblock "%(file_path)s"', False],
            [
                "ffmpeg",
                "ffplay",
                ' -autoexit -hide_banner -loglevel info -nostats -nodisp "%(file_path)s"',
                True,
            ],
            ["avconv", "avplay", ' -autoexit -nodisp "%(file_path)s"', True],
            ["vlc", "vlc", " --intf dummy %(uri_path)s vlc://quit ", True],
            [
                "gstreamer1.0-tools",
                "gst-launch-1.0",
                'playbin uri="%(uri_path)s" ',
                True,
            ],
            ["sox", "play", '"%(file_path)s"', True],
        ]

    def player_packages(self):  # -> list
        """Player package list (suggestions for `apt-get` or `dnf`
        package managers)"""
        _list = []
        for _item in self.players:
            _list.append(_item[self.apt_get])
        return _list

    def player_applications(self):  # -> list
        """Posix player application list including uninstalled applications"""
        _list = []
        for _item in self.players:
            _list.append(_item[self.app])
        return _list

    def player_command(
        self, file_path="/path/rte-play.ec3", check_is_file=False
    ):  # -> str
        """Get an audio player command on your system
        that is compatible with the audio file type."""
        if "." not in file_path:
            return ""
        if check_is_file:
            if not os.path.isfile(file_path):
                return ""
        for player in self.players:
            if player == "afplay":
                b_play_more = os.path.splitext(file_path)[1] in self.afplay_exts
            else:
                b_play_more = player[self.universal_play]
            if have_posix_app(player[self.app], False):
                if os.path.splitext(file_path)[1].lower() == ".wav" or b_play_more:
                    self.found_player = player[self.app]
                    return " ".join(
                        [player[self.app], player[self.command_get] % locals()]
                    )
        return ""

    def player_app(self, file_path="/path/rte-play.ec3"):  # -> str
        """Get the an audio player on your system that is
        compatible with the audio file type."""
        if "." not in file_path:
            return ""
        _command = self.player_command(file_path, False)
        if len(_command) != 0:
            return self.found_player
        return ""


def show_and_play(_command="", a_app="", display_file="", file_path=""):  # -> bool
    """Print the play status and play an audio file"""
    if len(_command) != 0:
        if os.path.getsize(file_path) == 0:
            print("""[>]  {0} cannot play `{1}`""".format(a_app, display_file))
            return True
        print("[>] {0} playing `{1}`".format(a_app, display_file))
        return os.system(_command) == 0
    return False


def play_wav_no_ui(file_path=""):  # -> bool
    """
    Opens using command line shell.
    """
    _command = ""
    a_app = "System audio"
    uri_path = path2url(file_path)
    display_file = os.path.split(file_path)[1]
    _pipe = ""
    if os.name == "nt":
        # Windows
        _win_ext = os.path.splitext(file_path)[1].lower()
        if _win_ext in [".m4a", ".mp2", ".mp3", ".wma"]:
            a_app = "Windows Media Player"
            _winm = WinMediaPlay()
            if _winm.app_ok(file_path):
                print("[>] {0} playing `{1}`".format(a_app, display_file))
                _winm.play(file_path)
                return True
            else:
                try:
                    return os.startfile(file_path) == 0
                except NameError:
                    return False
        elif _win_ext in [".mp4", ".oga", ".ogg", ".opus", ".spx", ".webm"]:
            try:
                os.startfile(file_path)
                return True
            except NameError:
                pass
        else:
            try:
                print("[>] {0} playing `{1}`".format(a_app, display_file))
                winsound.PlaySound(
                    file_path, winsound.SND_FILENAME | winsound.SND_NOWAIT
                )
                return True
            except (NameError, ImportError):
                try:
                    return os.startfile(file_path) == 0
                except AttributeError:
                    return False
    else:
        _audio_play = PosixAudioPlayers()
        _command = _audio_play.player_command(file_path, True)
        if len(_command) == 0:
            try:
                if bool(Gst):
                    _pipe = 'playbin uri="{0}" '.format(uri_path)
                    do_gst_parse_launch(_pipe)
            except NameError:
                _pipe = ""
            if len(_pipe) == 0:
                try:
                    print(
                        "[>] {0} (default) is playing `{1}`".format(a_app, display_file)
                    )
                    webbrowser.open(uri_path)
                    return True
                except (ImportError, NameError):
                    _apt_get_list = ""
                    for app in _audio_play.player_packages():
                        _apt_get_list = "\n * ".join(
                            [_apt_get_list, app[_audio_play.apt_get]]
                        )
                    print(
                        "-" * 78,
                        "\nPython could not access a player for `{0}`:{1}\n".format(
                            display_file, _apt_get_list
                        ),
                    )
                    return False
    return show_and_play(_command, _audio_play.found_player, display_file, file_path)


def handle_sound_playing(_media_work="", lock="lock"):  # -> bool
    """If a sound is playing in the background, then try to stop it,
    or at least stop it from starting a new process. Return `False`
    if it did not find a known player working, otherwise return `True`"""
    _audio_players = PosixAudioPlayers()
    if len(_media_work) == 0:
        return False
    if os.path.isfile(get_my_lock(lock)):
        unlock_my_lock(lock)
        _player_app = _audio_players.player_app(_media_work)
        if len(_player_app) == 0:
            return False
        if killall_process(_player_app):
            print("\n[>] {0} stopping".format(_player_app))
        else:
            print("\n[>] {0} is not ready. Try later.".format(_player_app))
        return True
    return False


def main():  # -> NoReturn
    """
    Converts the input wav sound to another format.  Ffmpeg
    can include a still frame movie if you include an image.
    """
    if sys.argv[-1] == sys.argv[0]:
        usage()
        sys.exit(0)
    _work = ""
    _visible = ""
    _audible = ""
    _image = ""
    _out = ""
    _artist = ""
    _dimensions = "600x600"
    _title = "Video memo"
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "ovaistndh",
            [
                "output=",
                "visible=",
                "audible=",
                "image=",
                "sound=",
                "title=",
                "artist=",
                "dimensions=",
                "help",
            ],
        )
    except getopt.GetoptError:
        # print help information and exit
        print("An option was not recognized")
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-o", "--output"):
            _out = a
        elif o in ("-v", "--visible"):
            _visible = a
        elif o in ("-a", "--audible"):
            _audible = a
        elif o in ("-i", "--image"):
            _image = a
        elif o in ("-s", "--sound"):
            _work = a
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
            usage()
    if len(_out) == 0 or len(_work) == 0:
        usage()

    else:
        process_wav_media(
            _title, _work, _image, _out, _audible, _visible, _artist, _dimensions
        )
    sys.exit(0)


if __name__ == "__main__":
    main()
###############################################################################

# Read Text Extension
#
# Copyright And License
#
# (c) 2024 [James Holgate Vancouver, CANADA](readtextextension(a)outlook.com)
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
