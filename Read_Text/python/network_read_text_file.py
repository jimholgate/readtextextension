#!/usr/bin/env python3
# -*- coding: UTF-8-*-
"""
This text explains how to use a web service and media player to read a text
file. It outlines the terms and conditions associated with using the on-line
service, as well as the potential privacy and security risks. It introduces
text-to-speech tools like Mimic3, Rhvoice, MaryTTS and TTS, and how to
use them. It mentions the need to check if the network is available and to
set permissions when using these tools. Lastly, it provides advice on how to
update local libraries and packages when using these tools.

-----

This python tool reads a text file using an web service and a media player.
Online services require a network connection and installation of an online
connection library.

Computers can synthesise voices of people without their knowledge. Make sure
people you use as voice models were able to consent and that listeners have a
way to tell if a voice performance was made by a computer or by a real person.

Check the terms and conditions that apply to the on-line service provider.
There may be acceptable use policies, limits or costs.

* Variants like speech rate, pitch, voice and gender might
  not apply to all services or to all languages.
* Online services could be terminated without warning.
* Your content might not be private or secure.
* Your organization or local laws might restrict use of online
  data services. For example, they might restrict services
  provided outside of your country's jurisdiction.
* An online provider could block your access because your use
  is excessive or otherwise violates their terms of service.
* If you run the application in a protected container like a flatpak
  or snap, some functions might not work because the application
  does not have permission to execute them.
* On some systems, you might need to install additional software
  libraries like `bs4`, `docker.io`, `podman`, `python3-requests`
  and `ffmpeg` to ensure that libraries are available to download
  and process files.

Containers
----------

You can install some text to speech local host tools using docker.io or,
in some cases, podman.

If Read Text Extension documentation does not specifically state that it
supports a docker image, check if the docker image has a `maryTTS`
compatibility mode. The compatibility mode allows the speech synthesis
image to use the maryTTS address and port and the maryTTS Application
Program Interface (API) to list installed voices and to produce spoken
audio files over a local web service.

Rhasspy Piper
-------------

*September 6, 2025*

Piper TTS is a fast, local neural text-to-speech system that can run as a
network server to use onnx voice models and voices across devices. The updated
setup supports multiple platforms, but performance depends on your hardware
and home network, with container deployments (Podman or Docker) recommended
for stability.  A simple way to install it as a local user is to use the
`python3-pipx` application.

```bash
pipx install piper-tts[http]
pipx ensurepath
```
The current release of Piper offers a variety of voices and languages, each with
its own license terms.

When running the piper server in a command line window, it shows the following
warning:

> WARNING: This is a development server. Do not use it in a
> production deployment.

You can find out more at the HTTP API page on
[GitHub](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/API_HTTP.md)

See also:
[Source](https://raw.githubusercontent.com/jimholgate/readtextextension/refs/heads/master/Read_Text/python/netpiper.py)

Mimic 3
-------

*Nov 5, 2022*

"A fast local neural text to speech engine for Mycroft"

[Mycroft Mimic3](https://github.com/MycroftAI/mimic3) is a fast text to
speech tool that includes very high quality voice assets.

Mimic 3 covers a lot of languages. The locally hosted web page has a Feedback
button that encourages users to comment on how the pronunciation could be
improved.

If your computer architecture supports Mimic 3, you can use Mimic TTS with
speech-dispatcher or as a localhost web server with this application. When
installed from an apt archive, or a from compiled code, you can start the
local web server at startup using a command to initiate `mimic3-server`.

If you use a docker image, you can get the computer to start the mimic
localhost web server on startup by setting the Docker container restart policy
to "always".

### It doesn't work?

The first step is to check if the network is available. The
network service might offer an account status report page or
a help document to assist you.

The tool relies on external libraries or packages, and python
might not have access to the current required packages.

Some ways of installing your office application restrict the
application's ability to run third party extensions. You or
your system administrator might need to set permissions for
this extension to run or for the extension to access a
network resource.

Some of the network tools require specific versions of python
or a specific system platform like `amd64`, `arm64` or `v7`.
This script might not work with those tools because it can't use
the required libraries on an unsupported version of python.

If you use python pip to install local libraries, you might have to
manually update them from time to time. Packages that are managed
by update utilities like `apt-get`, `yum` and `dnf` are upgraded
by the distribution.

Rhvoice
-------

*May 30, 2024*

[Rhvoice-rest](https://hub.docker.com/r/aculeasis/rhvoice-rest) is
a docker image container that can read English, Esperanto, Georgian,
Kyrgyz, Macedonian, Portuguese, Russian, Tatar and Ukrainian using
docker.io or podman.io.

See also:

[Install Rhvoice](https://github.com/jimholgate/readtextextension/blob/master/Read_Text/python/netrhvoice.py)

MaryTTS
-------

*May 22, 2020*

[MaryTTS](http://mary.dfki.de/) (Modular Architecture for Research in Synthesis)
is an open-source, multilingual Text-to-Speech Synthesis platform written in Java.
It can turn text into speech in many different languages. It runs on a `localhost`
web resource on your computer using a Docker container. Using MaryTTS does not
require an on-line connection.

The Rhasspy MaryTTS docker image is an easy-to install web application that
includes voices in several languages by default, including,

* English
* French
* German
* Italian
* Swedish
* Russian
* Telugu
* Turkish

See also:

[Install MaryTTS](https://github.com/jimholgate/readtextextension/blob/master/Read_Text/python/netmary.py)

Additional Resources
--------------------

* [Adding-voices](https://rhasspy.readthedocs.io/en/v2.4.20/text-to-speech/#adding-voices)
* [Docker Docs](https://docs.docker.com/desktop/install/linux-install/)
* [Docker MaryTTS Image](https://hub.docker.com/r/synesthesiam/marytts)
* [Mimic TTS](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mimic-tts/mimic-3)
* [Rhasspy community](https://community.rhasspy.org/)
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

try:
    import getopt
except (ImportError, AssertionError, AttributeError):
    exit()

try:
    import netgtts
except (AttributeError, ImportError, SyntaxError):
    pass
try:
    import requests

    REQUESTS_OK = True
except (AttributeError, ImportError):
    REQUESTS_OK = False
try:
    import netmimic3
except (AttributeError, ImportError, SyntaxError):
    pass
try:
    import netmary
except (AttributeError, ImportError, SyntaxError):
    pass
try:
    import netopentts
except (AttributeError, ImportError, SyntaxError):
    pass
try:
    import netpiper
except (AttributeError, ImportError, SyntaxError):
    pass
try:
    import netrhvoice
except (AttributeError, ImportError, SyntaxError):
    pass
try:
    import readtexttools
except (AttributeError, ImportError, SyntaxError):
    pass
try:
    import netcommon
except (AttributeError, ImportError):
    pass


ENGINE_IDS = ["gtts", "mary", "mimic3", "opentts", "piper", "rhvoice"]


def usage():  # -> None
    """
    Command line help
    """
    print(
        """
Network Speech Synthesis
========================

Reads a text file using an on-line voice and a media player like `pw-cat`,
`ffmpeg`, `sox` or `avconv`.

Usage
-----

    network_read_text_file.py --language=ca-ES --visible=False "input.txt"
    network_read_text_file.py --language=ca-ES --rate=70% "input.txt"

Relies on optional external libraries and an on-line connection. With long
strings, or using a slow network, the latency might be longer than two
seconds, or retrieving the online resource might fail.

Local Server
------------

The extension can use a local server that is compatible with the application
programming interface (API) of a locally hosted speech server daemon.

It is normal for a local server to take a moment to start speaking the first
time that you use it.

* [MaryTTS](http://mary.dfki.de/)
* [Mimic TTS](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mimic-tts/mimic-3)
* [Open TTS](https://github.com/synesthesiam/opentts#open-text-to-speech-server)
* [Rhasspy Piper](https://github.com/rhasspy/piper)
* [Rhvoice-rest](https://hub.docker.com/r/aculeasis/rhvoice-rest)
"""
    )


def network_problem(voice="default"):  # -> str
    """Return suggestions to make an on-line voice work."""
    if len(voice) == 0:
        voice = "requested"
    return """Is the network connected?
=========================

+ The `{0}` on-line voice is currently unavailable.
+ It might help to restart your device, refresh the network
  or check your on-line account status.
+ If you are using a `localhost` server, it might help to
  enter the local speech server command in a terminal and
  read what it prints out.
  """.format(
        voice
    )


def network_ok(_iso_lang="en-US", _local_url="", requested_voice=""):  # -> bool
    """Do at least one of the classes support an on-line speech library?"""
    _continue = False
    if not _continue:
        try:
            _piper = netpiper.GPLPiperClass()
            _continue = _piper.language_supported(
                _iso_lang, _local_url, requested_voice
            )
        except NameError:
            pass
    if not _continue:
        try:
            _mimic3 = netmimic3.Mimic3Class()
            _continue = _mimic3.language_supported(_iso_lang, _local_url)
        except NameError:
            pass
    if not _continue:
        try:
            _rhvoice_rest = netrhvoice.RhvoiceLocalHost()
            _continue = _rhvoice_rest.language_supported(_iso_lang, _local_url)
        except NameError:
            pass
    if not _continue:
        try:
            _opentts = netopentts.OpenTTSClass()
            if _opentts.language_supported(_iso_lang, _local_url):
                _continue = True
        except NameError:
            pass
    if not _continue:
        try:
            _mary_tts = netmary.MaryTtsClass()
            _continue = _mary_tts.language_supported(_iso_lang, _local_url)
        except NameError:
            pass
    if not _continue:
        try:
            _gtts_class = netgtts.GoogleTranslateClass()
            if _gtts_class.check_version(_gtts_class.tested_version):
                _continue = True
        except NameError:
            pass
    return _continue


def is_ssml(_text=""):
    """Return `True` if text includes standard ssml tags and the string
    is valid XML,"""
    _ssml = "</speak>" in _text and "<speak" in _text
    if _ssml:
        # Check if `_text` is valid XML
        if readtexttools.strip_xml(_text) == _text:
            _ssml = False
    return _ssml


def identify_engine_by_vox(_vox=""):  # -> Tuple[str, str]
    """
    Identify if a given voice string includes the name of a known speech engine.

    Examples:
        - identify_engine_by_vox("mimic3") -> ("mimic3", "male1")
        - identify_engine_by_vox("mimic3/MALE1") -> ("mimic3", "mimic3/MALE1")
        - identify_engine_by_vox("mimic3/en_US/vctk_low#p227") -> ("mimic3", "mimic3/en_US/vctk_low#p227")
        - identify_engine_by_vox("MALE1") -> ("", "MALE1")

    Arguments:
        _vox (str): The `--voice` argument provided by the user.

    Returns:
        tuple:
            - str: Engine name if found, otherwise "".
            - str: The normalized `_vox` string or default `"male1"` if only the engine name was given.
    """

    if not _vox:
        return "", str(_vox)
    _vox = str(_vox)
    vox = _vox.lower()
    if vox in ENGINE_IDS:
        return vox, "male1"
    for _test in ENGINE_IDS:
        if _test in vox:
            return _test, _vox
    return "", _vox


def use_engine(this_engine="", _vox=""):  # type: (str, str) -> bool
    """
    Decide whether to use `this_engine` given the requested voice `_vox`.

    Rules:
        - If `_vox` has no known engine, return True (use this_engine).
        - If `_vox` specifies a known engine, return True only if it matches `this_engine` (case-insensitive).

    Examples:
        - use_engine("mimic3", "mimic3") -> True
        - use_engine("mimic3", "mimic3/MALE1") -> True
        - use_engine("mimic3", "mimic3/en_US/vctk_low#p227") -> True
        - use_engine("mimic3", "MALE1") -> True   # no engine specified
        - use_engine("espeak", "mimic3/MALE1") -> False
        - use_engine("", "MALE1") -> True         # treat as default: no engine specified

    Arguments:
        this_engine (str): The current engine id to evaluate (e.g., "mimic3").
        _vox (str): The `--voice` argument provided by the user.

    Returns:
        bool: True if `_vox` does not specify a different supported engine,
              or if it matches `this_engine`; otherwise False.
    """
    # Treat empty this_engine as "use the current/default engine"
    if not this_engine:
        this_engine = ""

    # No voice provided, so no engine specified, therefore use this_engine
    if not _vox:
        return True

    # engine is "" if none is found
    engine, ret_vox = identify_engine_by_vox(_vox)

    # If there is not a valid engine substring in _vox, use this_engine
    if not engine:
        return True

    # Otherwise, require exact engine match (case-insensitive)
    return engine == str(this_engine).lower()


def normalize_vox(_vox=""):
    """
    Remove the engine name from a voice description, returning only the voice ID.

    Examples:
        - normalize_vox("mimic3") -> "mimic3"
        - normalize_vox("mimic3/MALE1") -> "male1"
        - normalize_vox("mimic3/en_US/vctk_low#p227") -> "en_US/vctk_low#p227"
        - normalize_vox("MALE1") -> "male1"

    Arguments:
        _vox (str): The `--voice` argument provided by the user.

    Returns:
        str: A normalized voice string without the engine name.
             If no engine is detected, returns `_vox` (possibly lowercased).
             If `_vox` is empty, returns "".
    """

    if not _vox:
        return ""
    engine, test_vox = identify_engine_by_vox(_vox)
    if not engine:
        return test_vox
    if not str.islower(test_vox):
        if netcommon.is_voice_id_formatted_for_speechd(test_vox):
            test_vox = test_vox.lower()

    for item in [
        "{0}/".format(engine),
        "/{0}".format(engine),
        "({0})".format(engine),
    ]:
        if item in test_vox:
            return test_vox.replace(item, "").strip(" /\r\t\n#()")
    return test_vox


def network_main(
    _text_file_in="",
    _iso_lang="ca-ES",
    _visible="false",
    _audible="true",
    _media_out="",
    _writer="",
    _title="",
    _icon="",
    _size="600x600",
    _speech_rate=160,
    _vox="",
    _local_url="",
):  # -> Any
    """Read a text file aloud using a network resource."""
    _imported_meta = readtexttools.ImportedMetaData()
    _text = _imported_meta.meta_from_file(_text_file_in)
    if len(_text.strip()) == 0:
        return False
    _info = readtexttools.check_artist(_writer)
    clip_title = readtexttools.check_title(_title, "espeak")
    # If the library does not require a postprocess, use `0`,
    # otherwise use the item corresponding to the next action.

    _post_processes = [
        None,
        "process_mp3_media",
        "process_playlist",
        "process_riff_media",
        "process_vorbis_media",
        "process_wav_media",
        "process_audio_media",
        "process_stream_media",  # Look for best streaming option.
    ]
    _vox = _vox.strip("'\" \t\n")

    if netcommon.is_voice_id_formatted_for_speechd(_vox):
        _vox = _vox.lower()
    # Prioritize speech engines that use json to communicate data
    # because text tables can use ambiguous labels (i. e.: `NA`)
    # Prioritize engines where everything can be achieved using `urllib`
    # because some immutable office packages do not include `requests`
    # support.
    do_post = 5
    # if os.name == "nt":
    #     do_post = 6
    _g_class_ok = True
    if use_engine("piper", _vox):
        try:
            _piper = netpiper.GPLPiperClass()
            _ssml = False
            if _piper.language_supported(_iso_lang, _local_url, _vox):
                _vox = normalize_vox(_vox)
                _piper.read(
                    _text.strip(),
                    _iso_lang.strip(),
                    _visible,
                    _audible,
                    _media_out,
                    _icon,
                    clip_title,
                    _post_processes[do_post],
                    _info,
                    _size,
                    _speech_rate,
                    _vox,
                    4,
                    30,
                )
                return True
        except NameError:
            pass

    if use_engine("mimic3", _vox):
        try:
            _mimic3 = netmimic3.Mimic3Class()
            _vox = normalize_vox(_vox)
            if _mimic3.language_supported(_iso_lang, _local_url, _vox):
                if not _mimic3.spd_voice_to_mimic3_voice(_iso_lang, _local_url, _vox):
                    # Check the returned value:
                    # - *str* language/model#speaker: e.g.: `en_US/cmu-arctic_low#lnh` (`True`)
                    # - *str* language/model: e.g.: `pl_PL/piotr_nater` (`True`)
                    # - *str* no model `""` (`False`)
                    print(
                        """WARNING:
========

Could not match a Mimic3 model with `{0}`.

[Mimic3 Help]({1})""".format(
                            _vox, _mimic3.help_url
                        )
                    )
                _ssml = is_ssml(_text)
                _mimic3.read(
                    _text,
                    _iso_lang,
                    _visible,
                    _audible,
                    _media_out,
                    _icon,
                    clip_title,
                    _post_processes[do_post],
                    _info,
                    _size,
                    _speech_rate,
                    _ssml,
                    20,
                    60,
                )
                return True
        except NameError:
            pass

    if use_engine("rhvoice", _vox):
        _vox = normalize_vox(_vox)
        try:
            _rhvoice_rest = netrhvoice.RhvoiceLocalHost()
            if _rhvoice_rest.language_supported(_iso_lang, _local_url):
                _rhvoice_rest.read(
                    _text,
                    _iso_lang,
                    _visible,
                    _audible,
                    _media_out,
                    _icon,
                    clip_title,
                    _post_processes[do_post],
                    _info,
                    _size,
                    _speech_rate,
                    _vox,
                    4,
                    30,
                )
                return True
        except NameError:
            pass

    if use_engine("opentts", _vox):
        _vox = normalize_vox(_vox)
        try:
            _opentts = netopentts.OpenTTSClass()
            if _opentts.language_supported(_iso_lang, _local_url):
                _ssml = is_ssml(_text)
                _opentts.spd_voice_to_opentts_voice(_vox, _iso_lang)
                _opentts.read(
                    _text,
                    _iso_lang,
                    _visible,
                    _audible,
                    _media_out,
                    _icon,
                    clip_title,
                    _post_processes[do_post],
                    _info,
                    _size,
                    _ssml,
                    0.03,
                    20,
                    60,
                )
                return True
        except NameError:
            pass

    if use_engine("mary", _vox):
        _vox = normalize_vox(_vox)
        try:
            _marytts = netmary.MaryTtsClass()
            if _marytts.language_supported(_iso_lang, _local_url):
                _ssml = is_ssml(_text)
                if REQUESTS_OK:
                    if int(requests.__version__[0] == 1):
                        if _ssml:
                            _text = readtexttools.strip_xml(_text)
                            _ssml = False
                else:
                    if _ssml:
                        _text = readtexttools.strip_xml(_text)
                        _ssml = False
                _marytts.read(
                    _text,
                    _iso_lang,
                    _visible,
                    _audible,
                    _media_out,
                    _icon,
                    clip_title,
                    _post_processes[do_post],
                    _info,
                    _size,
                    _speech_rate,
                    _ssml,
                    _vox,
                    4,
                    15,
                )
                return True
        except NameError:
            pass

    if use_engine("gtts", _vox):
        _vox = normalize_vox(_vox)
        try:
            _gtts_class = netgtts.GoogleTranslateClass()
            remove_digits = lambda s: "".join(c for c in s if not c.isdigit())
            if _gtts_class.check_version(_gtts_class.tested_version):
                if remove_digits(_vox).lower() in _gtts_class.accept_voice:
                    _post_process = "process_mp3_media"
                    _gtts_class.read(
                        _text,
                        _iso_lang,
                        _visible,
                        _audible,
                        _media_out,
                        _icon,
                        clip_title,
                        _post_process,
                        _info,
                        _size,
                        _speech_rate,
                    )
                    return True
                else:
                    print(
                        """To use `gtts`, specify one of these these voices"

    {0}
    """.format(
                            "\n".join(_gtts_class.accept_voice)
                        )
                    )

        except NameError:
            _g_class_ok = False
        if netcommon.which("gtts_cli"):
            return _gtts_class.stream(
                _text,
                _iso_lang,
                _speech_rate,
            )
    # Just display a translation link.
    if _g_class_ok:
        try:
            _gtts_class.read(
                _text,
                _iso_lang,
                _visible,
                _audible,
                _media_out,
                _icon,
                clip_title,
                _post_processes[0],
                _info,
                _size,
                _speech_rate,
            )
        except UnboundLocalError:
            pass

    print(
        "No working network server was found, or the requested voice is unavailable.\n"
    )
    usage()
    return False


def main():  # -> NoReturn
    """Use network speech synthesis for supported languages while on-line"""
    if not sys.version_info >= (3, 6) or not os.name in ["posix", "nt"]:
        print("Your system does not support the network python tool.")
        usage()
        sys.exit(0)
    _speech_rate = 160
    _iso_lang = "en-US"
    try:
        _iso_lang = readtexttools.default_lang().replace("_", "-")
    except (AttributeError, ImportError):
        pass
    _media_out = ""
    _visible = "false"
    _audible = "true"
    _percent_rate = "100%"
    _speech_rate = netcommon.speech_wpm(_percent_rate)
    _denoiser_strength = 0.005
    _noise_scale = 0.667
    _icon = ""
    _title = ""
    _writer = ""
    _size = "600x600"
    _vox = "AUTO"
    _local_url = ""
    _text_file_in = sys.argv[-1]

    if os.path.isfile(_text_file_in):
        if sys.argv[-1] == sys.argv[0]:
            usage()
            sys.exit(0)
        try:
            opts, args = getopt.gnu_getopt(
                sys.argv[1:],
                "ovalritndxuech",
                [
                    "output=",
                    "visible=",
                    "audible=",
                    "language=",
                    "rate=",
                    "image=",
                    "title=",
                    "artist=",
                    "dimensions=",
                    "voice=",
                    "url=",
                    "denoiser_strength=",
                    "noise_scale=",
                    "help",
                ],
            )
        except getopt.GetoptError:
            print("option -a not recognized")
            usage()
            sys.exit(2)
        for o, a in opts:
            if o in ("-o", "--output"):
                _media_out = a
            elif o in ("-v", "--visible"):
                _visible = a
            elif o in ("-a", "--audible"):
                _audible = a
            elif o in ("-l", "--language"):
                _iso_lang = a
                if _iso_lang.startswith("zxx"):
                    _iso_lang = "en-US"
            elif o in ("-r", "--rate"):
                _percent_rate = a
                if len(_percent_rate) != 0:
                    _speech_rate = netcommon.speech_wpm(_percent_rate)
            elif o in ("-i", "--image"):
                _icon = a
            elif o in ("-t", "--title"):
                _title = a
            elif o in ("-n", "--artist"):
                _writer = a
            elif o in ("-d", "--dimensions"):
                _size = a
            elif o in ("-x", "--voice"):
                _vox = a
            elif o in ("-u", "--url"):
                _local_url = a
            elif o in ("-e", "--denoiser_strength"):
                try:
                    _denoiser_strength = float(o)
                except (AttributeError, TypeError, ValueError):
                    pass
                if not bool(_denoiser_strength):
                    _denoiser_strength = 0.005
            elif o in ("-c", "--noise_scale"):
                try:
                    _noise_scale = float(o)
                except (AttributeError, TypeError, ValueError):
                    pass
                if not bool(_noise_scale):
                    _noise_scale = 0.667
            elif o in ("-h", "--help"):
                usage()
                sys.exit(0)
            else:
                assert False, "unhandled option"
        network_main(
            _text_file_in,
            _iso_lang,
            _visible,
            _audible,
            _media_out,
            _writer,
            _title,
            _icon,
            _size,
            _speech_rate,
            _vox,
            _local_url,
        )
    else:
        usage()
    sys.exit(0)


if __name__ == "__main__":
    main()
