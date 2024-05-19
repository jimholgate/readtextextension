#!/usr/bin/env python
# -*- coding: UTF-8-*-
"""Common tools for network and neural speech synthesis clients"""


import math
import os
import platform
import time

try:
    import socket
except ImportError:
    pass
import sys
import readtexttools

NET_SERVICE_LIST = [
    "AUTO",
    "NETWORK",
    "GTTS",
    "LARYNX",
    "MARYTTS",
    "MIMIC",
    "OPENTTS",
    "RHVOICE",
    "TTS",
]


def have_gpu(_test="Radeon"):  # -> bool
    """If the system can detect the specified GPU string, return `True`,
    otherwise return `False`"""
    _test_app = "lspci"
    if not readtexttools.have_posix_app(_test_app, False):
        return False
    _imported_meta = readtexttools.ImportedMetaData()
    return (
        _test.lower()
        in _imported_meta.execute_command("{0} | grep VGA").format(_test_app).lower()
    )


def spd_voice_list(_min=0, _max=100, _roots=["female", "male"]):  # -> list[str]
    """Return a list in the form `['female0', 'male0', 'female1' ...]`"""
    retval = []
    for _digit in range(_min, _max + 1):
        for _root in _roots:
            retval.append("".join([_root, str(_digit)]))
    return retval


def index_number_to_list_item(_vox_number=0, _list=None):  # -> str
    """Return a specific voice_id using vox_number as an index in the list.
    Handle out of range numbers using a modulus (`int % len(_list)`) value."""
    try:
        if not bool(_list):
            return ""
        if not _vox_number > len(_list) - 1:
            return _list[_vox_number]
        return _list[(_vox_number % abs(len(_list)))]
    except ZeroDivisionError:
        return _list[0]
    except [IndexError, TypeError]:
        pass
    return ""


def speech_wpm(_percent="100%"):  # -> int
    """
    _percent - rate expressed as a percentage.
    Use '100%' for default rate of 160 words per minute (wpm).
    Returns rate between 20 and 640.
    """
    _calc_product = 0
    _result = 0
    _minimum = 20
    _maximum = 640
    _normal = 160
    _p_cent = ""

    try:
        if "%" in _percent:
            _p_cent = readtexttools.safechars(_percent, "1234567890.")
            _calc_product = float(_p_cent) if "." in _p_cent else int(_p_cent) / 100
            _result = math.ceil(_calc_product * _normal)
        else:
            _calc_product = float(_percent) if "." in _percent else int(_percent)
            _result = math.ceil(_calc_product)
    except (TypeError, ValueError):
        return _normal
    if _result == 0:
        return _normal
    elif _result <= _minimum:
        return _minimum
    elif _result >= _maximum:
        return _maximum
    return _result


class LocalCommons(object):
    """Shared items for local speech servers"""

    def __init__(self):  # -> None
        self.debug = [0, 1, 2, 3][0]

        self.default_lang = readtexttools.default_lang()
        self.default_extension = ".wav"
        self.help_icon = "/usr/share/icons/HighContrast/32x32/apps/web-browser.png"
        self.length_scales = [
            [320, 289, "---------|", 0.50],
            [288, 257, "--------|-", 0.55],
            [256, 225, "-------|--", 0.62],
            [224, 193, "------|---", 0.71],
            [192, 161, "-----|----", 0.83],
            [160, 159, "-----|----", 1.00],
            [158, 128, "---|-----", 1.15],
            [127, 110, "---|-----", 1.25],
            [109, 97, "---|-----", 1.50],
            [96, 66, "--|------", 1.66],
            [64, 33, "-|-------", 2.50],
            [32, 0, "|--------", 5.00],
        ]
        self.spd_fm = [
            "female1",
            "female2",
            "female3",
            "female4",
            "female5",
            "female6",
            "female7",
            "female8",
            "female9",
            "child_female",
            "child_female1",
        ]
        self.spd_m = [
            "male1",
            "male2",
            "male3",
            "male4",
            "male5",
            "male6",
            "male7",
            "male8",
            "male9",
            "child_male",
            "child_male1",
        ]
        self.pause_list = [
            "(",
            "\n",
            "\r",
            "\u2026",
            "\u201C",
            "\u2014",
            "\u2013",
            "\u00A0",
        ]
        self.rhasspy_fm = [
            "eva_k",
            "hokuspokus",
            "kerstin",
            "rebecca_braunert_plunkett",
            "blizzard_fls",
            "blizzard_lessac",
            "cmu_clb",
            "cmu_eey",
            "cmu_ljm",
            "cmu_lnh",
            "cmu_rms",
            "cmu_slp",
            "cmu_slt",
            "ek",
            "harvard",
            "judy_bieber",
            "kathleen",
            "ljspeech",
            "southern_english_female",
            "karen_savage",
            "siwis",
            "lisa",
            "nathalie",
            "hajdurova",
        ]
        # Updated for spacy 3.5
        self.spacy_dat = [
            [["en"], "_core_web_sm"],
            [
                [
                    "ca",
                    "da",
                    "de",
                    "el",
                    "es",
                    "fi",
                    "fr",
                    "hr",
                    "it",
                    "ja",
                    "ko",
                    "lt",
                    "mk",
                    "nb",
                    "nl",
                    "pl",
                    "pt",
                    "ro",
                    "ru",
                    "sv",
                    "uk",
                    "zh",
                ],
                "_core_news_sm",
            ],
            [["xx"], "_ent_wiki_sm"],
        ]
        self.checked_spacy = False
        self.ai_developer_platforms = [
            "centos",
            "darwin",
            "debian",
            "fedora",
            "raspbian",
            "rhel",
            "sles",
            "ubuntu",
            "preempt_dynamic",
        ]
        try:
            self.add_pause = str.maketrans(
                {
                    "\n": ";\n",
                    "\r": ";\r",
                    "(": " ( ",
                    "\u201C": "\u201C;",
                    "\u2026": "\u2026;",
                    "\u2014": "\u2014;",
                    "\u2013": "\u2013;",
                    "\u00A0": " ",
                }
            )
        except AttributeError:
            self.add_pause = None
        try:
            self.base_curl = str.maketrans(
                {
                    "\\": " ",
                    '"': '\\"',
                    """
""": """\
""",
                    "\r": " ",
                }
            )
        except AttributeError:
            self.base_curl = None
        self.is_x86_64 = sys.maxsize > 2**32
        self.locker = "net_speech"
        self.generic_problem = """The application cannot load a sound file.
Your computer might be missing a required library, or an operation might have
taken too long."""
        if readtexttools.using_container(False):
            self.generic_problem = """The container application cannot load
a sound file. It might be missing a required library or an operation might
have taken too long."""

    def big_play_list(self, _text="", _lang_str="en", _verbose=True):  # -> list
        """Split a long string of sentences or paragraphs into a list.
        Best practice is to install [spacy](https://spacy.io/)
        in a virtual environment and download the parsing components."""
        retval = _text.splitlines()
        try:
            import spacy
        except (ImportError, ModuleNotFoundError, KeyError, TypeError):
            try:
                _local_pip = readtexttools.find_local_pip("spacy")
                if len(_local_pip) != 0:
                    sys.path.append(_local_pip)
                    try:
                        import spacy
                    except:
                        return retval
            except:
                return retval
        spaceval = []
        trained_pipeline = "xx_ent_wiki_sm"
        for _item in self.spacy_dat:
            if _lang_str in _item[0]:
                trained_pipeline = "".join([_lang_str, _item[1]])
                break
        try:
            nlp = spacy.load(trained_pipeline)
            try:
                # The `senter` component is ~10× faster than `parser` and
                # more accurate than the rule-based sentencizer. Not all
                # models include the `senter` component.
                nlp.disable_pipe("parser")
                nlp.enable_pipe("senter")
            except AttributeError:
                try:
                    nlp.enable_pipe("parser")
                except AttributeError:
                    pass
            doc = nlp(_text)
            for item in doc.sents:
                if len(item.text) != 0:
                    spaceval.append(item.text)
            self.checked_spacy = True
        except:
            self.checked_spacy = False
        if len(spaceval) == 0 and _verbose:
            if not readtexttools.using_container(True):
                print(
                    """The python `spacy` library or a `{0}` language model is unavailable.
Falling back to `.splitlines()`

    sudo apt-get install pipx
    pipx install spacy
    spacy download {1}

* See: <https://pypi.org/project/spacy/>
* Package list: <https://spacy.io/models/ca>""".format(_lang_str, trained_pipeline)
                )
            for _item in ".?!`":
                _text = _text.replace(_item, _item + "\n")
            retval = _text.splitlines()
            return retval
        return spaceval

    def is_ai_developer_platform(self):  # -> bool
        """Does the posix platform include options for docker, system
        contributor or non-free components for some ai models?
        """
        # i. e.: MacOS, Docker container or Ubuntu compatible?
        if os.name == "posix":
            try:
                _uname_ver = platform.uname().version
            except (AttributeError, NameError, TypeError):
                try:
                    _importmeta = readtexttools.ImportedMetaData()
                    _uname_ver = _importmeta.execute_command("uname -a")
                except:
                    return False
            for _item in self.ai_developer_platforms:
                if _item.lower() in _uname_ver.lower():
                    return True
        return False

    def verify_spacy(self, _lang="en"):  # -> bool
        """spaCy is a free open-source library for Natural Language
        Processing in Python.

        Do a test run of the python `spacy` library, and check whether it
        completes the task with no errors with the specified language
        (`_lang`)."""
        if self.checked_spacy:
            return True
        _verbose = self.is_ai_developer_platform()
        if len(self.big_play_list("123.\n456", _lang, _verbose)) == 0:
            return False
        return self.checked_spacy

    def set_urllib_timeout(self, _ok_wait=4):  # -> bool
        """Try to set sockets timeout before transfering a file using
        `urllib`.
        https://docs.python.org/3/howto/urllib2.html#sockets-and-layers"""
        try:
            socket.setdefaulttimeout(_ok_wait)
        except:
            return False
        return True

    def rate_to_rhasspy_length_scale(self, _speech_rate=160):  # -> list
        """Look up the Larynx or Mimic3 length scale appropriate for requested
        `_speech rate`. Rates have discreet steps. In English, a common speech
        rate is about 160 words per minute, but individuals vary widely. Some
        voices do not sound good with an altered rate."""
        _length_scale = 1
        _length_bar = ""
        for _item in self.length_scales:
            if not _speech_rate > _item[0] and not _speech_rate < _item[1]:
                _length_scale = _item[3]
                _length_bar = _item[2]
                break
        return [_length_scale, _length_bar]

    def ssml_xml(
        self, _text="", _voice="en_UK/apope_low", _speech_rate=160, _xml_lang="en-US"
    ):  # -> str
        """Change the speed that a reader reads plain text aloud using
        w3.org `SSML`. The reader should use standard XML conventions like
        `&amp;`, `&gt;` and `&lt;`.  Mimic3 supports a subset of SSML.
        Not all models support SSML prosody rate.

        <https://www.w3.org/TR/speech-synthesis11/ >"""
        _xmltransform = readtexttools.XmlTransform()
        _text = _xmltransform.clean_for_xml(_text, False)
        _xml_lang = _xml_lang.replace("_", "-")
        try:
            # 160 wpm (Words per minute) yields 100% prosody rate
            if _speech_rate < 40:
                _speech_rate = 40
            _rate = "".join([str(int(_speech_rate / 1.6)), "%"])
        except [AttributeError, TypeError]:
            _rate = "100%"
        return """<?xml version="1.0"?>en
<speak version="1.1" xmlns="http://www.w3.org/2001/10/synthesis"
xml:lang="{0}">
<p>
<prosody rate="{1}"><voice name="{2}" languages="{3}" required="languages">
{4}</voice></prosody></p></speak>""".format(_xml_lang, _rate, _voice, _xml_lang, _text)

    def do_net_sound(
        self,
        _info="",
        _media_work="",
        _icon="",
        _media_out="",
        _audible="true",
        _visible="false",
        _writer="",
        _size="600x600",
        _post_process="",
        handle_unlock=False,
    ):  # -> bool
        """Play `_media_work` or export it to `_media_out` format."""
        # use `getsize` to ensure that python waits for file to finish download
        if not os.path.isfile(_media_work):
            return False
        if os.path.getsize(_media_work) == 0:
            time.sleep(2)
        if os.path.isfile(_media_work) and _post_process in [
            "process_audio_media",
            "process_wav_media",
        ]:
            if os.path.getsize(_media_work) == 0:
                print("Unable to write media work file.")
                return False
            # NOTE: Calling process should unlock_my_lock()
            # In a loop, this would cause the voice to continue..
            if handle_unlock:
                readtexttools.unlock_my_lock()
            readtexttools.process_wav_media(
                _info,
                _media_work,
                _icon,
                _media_out,
                _audible,
                _visible,
                _writer,
                _size,
            )
            return True
        return False
