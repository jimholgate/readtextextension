#!/usr/bin/env python
# -*- coding: UTF-8-*-
"""A client of the gtts python library

Powered by Google\u2122

"Google", "Google Cloud", "Google Translate" and the stylized "G" logo are
trademarks of Google Inc.

The contents of this resource are not affiliated with, sponsored by, or endorsed
by Google nor does the documention represent the views or opinions of Google or
Google personnel.

This script looks for the `gtts` library in specific local directories, and so
it will not work if the office application is in a sandbox or container. Test
normal functioning with `gtts-cli 'hello world' | play -t mp3 -`
"""


import os
import subprocess
import sys
import shlex
import netcommon
import netsplit
import readtexttools
from importlib.metadata import version

try:
    import gtts
except (AttributeError, ImportError, ModuleNotFoundError):
    try:
        _try_path = readtexttools.pip_dir_search("gtts", "", True, "")
        if _try_path:
            sys.path.append(_try_path)
            try:
                import gtts
            except Exception as e:
                print("Exception (editing `sys.path`): ", e)
    except Exception as e:
        print("Exception (importing gtts): ", e)


class GoogleTranslateClass(object):
    """The following notice should be displayed in a dialog when users click
    *About...* or the equivalent in their language when this class is enabled.

    Powered by Google\u2122

    "Google", "Google Cloud", "Google Translate" and the stylized "G" logo are
    trademarks of Google Inc.

    The contents of this resource are not affiliated with, sponsored by, or endorsed
    by Google nor does the documention represent the views or opinions of Google or
    Google personnel.

    The creators of the `gTTS` python library are the originators of the library
    enabling the `GoogleTranslateClass` class.

    The `gTTS` library can only be enabled by electing to install it on a supported
    platform. Read the documentation for help installing `gTTS` or to get help with
    troubleshooting if `gTTS` does not work when using your Linux package manager.

        sudo apt -y install python3-gtts

    or

        pipx install gTTS

    See:

    * <https://github.com/pndurette/gTTS>
    * <https://gtts.readthedocs.io/en/latest/>
    """

    def __init__(self):  # -> None
        """Initialize data"""
        self.ok = True
        self.accept_voice = [
            "",
            "all",
            "auto",
            "child_female",
            "child_male",
            "gtts",
            "female",
            "male",
        ]
        self.translator = "Google"
        self.translator_domain = self.translator.lower()
        self.default_extension = ".mp3"
        self.tested_version = 2.5
        self.version_string = ""
        self.domain_table = [
            {
                "domain": "de",
                "iso_code": "DE",
                "lang1": "de",
                "lang2": "en",
                "comment": "Germany",
            },
            {
                "domain": "co.uk",
                "iso_code": "GB",
                "lang1": "en",
                "lang2": "pl",
                "comment": "Great Britain",
            },
            {
                "domain": "es",
                "iso_code": "ES",
                "lang1": "es",
                "lang2": "en",
                "comment": "Spain",
            },
            {
                "domain": "fr",
                "iso_code": "FR",
                "lang1": "fr",
                "lang2": "ar",
                "comment": "France",
            },
            {
                "domain": "com.hk",
                "iso_code": "CN",
                "lang1": "zh",
                "lang2": "en",
                "comment": "Mandarin (Simplified)",
            },
            {
                "domain": "ar",
                "iso_code": "AR",
                "lang1": "es",
                "lang2": "en",
                "comment": "Argentina",
            },
            {
                "domain": "at",
                "iso_code": "AT",
                "lang1": "de",
                "lang2": "en",
                "comment": "Austria",
            },
            {
                "domain": "be",
                "iso_code": "BE",
                "lang1": "nl",
                "lang2": "fr",
                "comment": "Belgium",
            },
            {
                "domain": "bg",
                "iso_code": "BG",
                "lang1": "bg",
                "lang2": "en",
                "comment": "Bulgaria",
            },
            {
                "domain": "ca",
                "iso_code": "CA",
                "lang1": "en",
                "lang2": "fr",
                "comment": "Canada",
            },
            {
                "domain": "ca",
                "iso_code": "CA",
                "lang1": "fr",
                "lang2": "en",
                "comment": "Canada",
            },
            {
                "domain": "ch",
                "iso_code": "CH",
                "lang1": "de",
                "lang2": "fr",
                "comment": "Switzerland",
            },
            {
                "domain": "ch",
                "iso_code": "CH",
                "lang1": "fr",
                "lang2": "de",
                "comment": "Switzerland",
            },
            {
                "domain": "ci",
                "iso_code": "CI",
                "lang1": "fr",
                "lang2": "en",
                "comment": "Cote d'Ivoire",
            },
            {
                "domain": "cl",
                "iso_code": "CL",
                "lang1": "es",
                "lang2": "en",
                "comment": "Chile",
            },
            {
                "domain": "cz",
                "iso_code": "CZ",
                "lang1": "cs",
                "lang2": "en",
                "comment": "Czechia",
            },
            {
                "domain": "dk",
                "iso_code": "DK",
                "lang1": "da",
                "lang2": "en",
                "comment": "Denmark",
            },
            {
                "domain": "ee",
                "iso_code": "EE",
                "lang1": "et",
                "lang2": "en",
                "comment": "Estonia",
            },
            {
                "domain": "es",
                "iso_code": "ES",
                "lang1": "ca",
                "lang2": "es",
                "comment": "Spain",
            },
            {
                "domain": "es",
                "iso_code": "ES",
                "lang1": "eu",
                "lang2": "es",
                "comment": "Spain",
            },
            {
                "domain": "es",
                "iso_code": "ES",
                "lang1": "gl",
                "lang2": "es",
                "comment": "Spain",
            },
            {
                "domain": "fi",
                "iso_code": "FI",
                "lang1": "fi",
                "lang2": "sv",
                "comment": "Finland",
            },
            {
                "domain": "gl",
                "iso_code": "GL",
                "lang1": "da",
                "lang2": "en",
                "comment": "Greenland",
            },
            {
                "domain": "gr",
                "iso_code": "GR",
                "lang1": "el",
                "lang2": "en",
                "comment": "Greece",
            },
            {
                "domain": "hu",
                "iso_code": "HU",
                "lang1": "hu",
                "lang2": "en",
                "comment": "Hungary",
            },
            {
                "domain": "ie",
                "iso_code": "IE",
                "lang1": "en",
                "lang2": "ga",
                "comment": "Ireland",
            },
            {
                "domain": "it",
                "iso_code": "IT",
                "lang1": "it",
                "lang2": "en",
                "comment": "Italy",
            },
            {
                "domain": "lu",
                "iso_code": "LU",
                "lang1": "fr",
                "lang2": "lb",
                "comment": "Luxembourg",
            },
            {
                "domain": "lv",
                "iso_code": "LV",
                "lang1": "lv",
                "lang2": "en",
                "comment": "Latvia",
            },
            {
                "domain": "nl",
                "iso_code": "NL",
                "lang1": "nl",
                "lang2": "en",
                "comment": "Netherlands",
            },
            {
                "domain": "pl",
                "iso_code": "PL",
                "lang1": "pl",
                "lang2": "en",
                "comment": "Poland",
            },
            {
                "domain": "pt",
                "iso_code": "PT",
                "lang1": "pt",
                "lang2": "en",
                "comment": "Portugal",
            },
            {
                "domain": "ro",
                "iso_code": "RO",
                "lang1": "ro",
                "lang2": "en",
                "comment": "Romania",
            },
            {
                "domain": "ru",
                "iso_code": "RU",
                "lang1": "ru",
                "lang2": "en",
                "comment": "Russia",
            },
            {
                "domain": "se",
                "iso_code": "SE",
                "lang1": "sv",
                "lang2": "en",
                "comment": "Sweden",
            },
            {
                "domain": "si",
                "iso_code": "SI",
                "lang1": "sl",
                "lang2": "en",
                "comment": "Slovenia",
            },
            {
                "domain": "sk",
                "iso_code": "SK",
                "lang1": "sk",
                "lang2": "en",
                "comment": "Slovakia",
            },
            {
                "domain": "com",
                "iso_code": "US",
                "lang1": "en",
                "lang2": "es",
                "comment": "United States of America",
            },
            {
                "domain": "co.cr",
                "iso_code": "CR",
                "lang1": "es",
                "lang2": "en",
                "comment": "Costa Rica",
            },
            {
                "domain": ".hn",
                "iso_code": "HN",
                "lang1": "es",
                "lang2": "en",
                "comment": "Honduras",
            },
            {
                "domain": "co.in",
                "iso_code": "IN",
                "lang1": "hi",
                "lang2": "en",
                "comment": "India",
            },
            {
                "domain": "co.nz",
                "iso_code": "NZ",
                "lang1": "en",
                "lang2": "zh-CN",
                "comment": "New Zealand",
            },
            {
                "domain": "co.za",
                "iso_code": "ZA",
                "lang1": "af",
                "lang2": "en",
                "comment": "South Africa",
            },
            {
                "domain": "com.au",
                "iso_code": "AU",
                "lang1": "en",
                "lang2": "zh-CN",
                "comment": "Australia",
            },
            {
                "domain": "com.bd",
                "iso_code": "BD",
                "lang1": "bn",
                "lang2": "en",
                "comment": "Bangladesh",
            },
            {
                "domain": "com.bo",
                "iso_code": "BO",
                "lang1": "es",
                "lang2": "en",
                "comment": "Bolivia",
            },
            {
                "domain": "com.br",
                "iso_code": "BR",
                "lang1": "pt",
                "lang2": "de",
                "comment": "Brazil",
            },
            {
                "domain": "com.bz",
                "iso_code": "BZ",
                "lang1": "en",
                "lang2": "es",
                "comment": "Beliz",
            },
            {
                "domain": "com.co",
                "iso_code": "CO",
                "lang1": "es",
                "lang2": "en",
                "comment": "Colombia",
            },
            {
                "domain": "com.cy",
                "iso_code": "CY",
                "lang1": "el",
                "lang2": "en",
                "comment": "Cyprus",
            },
            {
                "domain": "com.ec",
                "iso_code": "EC",
                "lang1": "es",
                "lang2": "en",
                "comment": "Ecuador",
            },
            {
                "domain": "com.gt",
                "iso_code": "GT",
                "lang1": "es",
                "lang2": "en",
                "comment": "Guatemala",
            },
            {
                "domain": "com.hk",
                "iso_code": "HK",
                "lang1": "yue",
                "lang2": "zh",
                "comment": "Cantonese",
            },
            {
                "domain": "com.hk",
                "iso_code": "MO",
                "lang1": "zh",
                "lang2": "pt",
                "comment": "Mandarin (Simplified)",
            },
            {
                "domain": "com.mt",
                "iso_code": "MT",
                "lang1": "en",
                "lang2": "mt",
                "comment": "Malta",
            },
            {
                "domain": "com.mx",
                "iso_code": "MX",
                "lang1": "es",
                "lang2": "en",
                "comment": "Mexico",
            },
            {
                "domain": "com.my",
                "iso_code": "MY",
                "lang1": "ms",
                "lang2": "en",
                "comment": "Malaysia",
            },
            {
                "domain": "com.ng",
                "iso_code": "NG",
                "lang1": "en",
                "lang2": "ha",
                "comment": "Nigeria",
            },
            {
                "domain": "com.ni",
                "iso_code": "NI",
                "lang1": "es",
                "lang2": "en",
                "comment": "Nicaragua",
            },
            {
                "domain": "com.pa",
                "iso_code": "PA",
                "lang1": "es",
                "lang2": "en",
                "comment": "Panama",
            },
            {
                "domain": "com.pe",
                "iso_code": "PE",
                "lang1": "es",
                "lang2": "en",
                "comment": "Peru",
            },
            {
                "domain": "com.ph",
                "iso_code": "PH",
                "lang1": "tl",
                "lang2": "en",
                "comment": "Philippines",
            },
            {
                "domain": "com.pk",
                "iso_code": "PK",
                "lang1": "ur",
                "lang2": "en",
                "comment": "Pakistan",
            },
            {
                "domain": "com.py",
                "iso_code": "PY",
                "lang1": "es",
                "lang2": "en",
                "comment": "Paraguay",
            },
            {
                "domain": "com.sg",
                "iso_code": "SG",
                "lang1": "zh",
                "lang2": "en",
                "comment": "Singapore",
            },
            {
                "domain": "com.sv",
                "iso_code": "SV",
                "lang1": "es",
                "lang2": "en",
                "comment": "El Salvador",
            },
            {
                "domain": "com.tw",
                "iso_code": "TW",
                "lang1": "zh-TW",
                "lang2": "en",
                "comment": "Mandarin (Traditional)",
            },
            {
                "domain": "co.ve",
                "iso_code": "VE",
                "lang1": "es",
                "lang2": "pt",
                "comment": "Venezuela",
            },
            {
                "domain": "com.ua",
                "iso_code": "UA",
                "lang1": "uk",
                "lang2": "ru",
                "comment": "Ukraine",
            },
            {
                "domain": "com.uy",
                "iso_code": "UY",
                "lang1": "es",
                "lang2": "en",
                "comment": "Uraguay",
            },
        ]
        _common = netcommon.LocalCommons()
        self.locker = _common.locker

    def get_version(self):  # -> string
        """Returns the version in the form `nn.nn.nn`."""
        try:
            return str(gtts.__init__.version)
        except (AttributeError, NameError):
            try:
                cmd = shlex.split("gtts-cli --version")
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                # Example output: "gtts-cli, version 2.5.4"
                for token in result.stdout.split():
                    if token[0].isdigit():
                        self.version = token.strip()
                        break
            except Exception as e:
                print("Exception (CLI fallback):", e)
                self.version = "0.0.0"
        return self.version

    def check_version(self, minimum_version=0):  # -> bool
        """Check for minimum version."""
        if not minimum_version:
            minimum_version = self.tested_version
        if readtexttools.is_container_instance():
            self.ok = False
            return self.ok
        if os.name == "nt":
            # Require Windows Media Player play mp3 audio files.
            _wmp = readtexttools.WinMediaPlay()
            if not _wmp.app:
                self.ok = False
                return self.ok
        _test_version = self.get_version()
        try:
            self.ok = float(".".join(_test_version.split(".")[:2])) >= minimum_version
        except (AttributeError, IndexError, ValueError):
            self.ok = False
        _commons = netcommon.LocalCommons()
        return self.ok

    def stream(self, _text="", _iso_lang="en", _speech_rate=160):
        """If python is incompatable, try the pipx command line."""
        if not netcommon.which("gtts-cli"):
            return False
        if not _text:
            return False

        def gst_speak(_text="", _iso_lang="en", _speech_rate=160):
            # Launch gtts-cli and pipe its output into GStreamer
            if os.path.isfile(self.locker):
                readtexttools.killall_process("gtts-cli")
                readtexttools.unlock_my_lock(self.locker)
                return True
            _slower = ""
            _top_level_domain = "com"
            data = self.get_tld_data(_iso_lang)
            _top_level_domain, _, _, _, _ = data
            if int(_speech_rate) < 160:
                _slower = " --slow"
            gst_cmd = "gst-launch-1.0 fdsrc ! decodebin ! audioconvert ! audioresample ! autoaudiosink"
            _lang = "en"
            if self.language_supported(_iso_lang):
                _lang = self.supported_language(_iso_lang)
            readtexttools.lock_my_lock(self.locker)
            _netsplitlocal = netsplit.LocalHandler()
            _items = _netsplitlocal.create_play_list(_text, _iso_lang.split("-")[0])
            for phrase in _items:
                gtts_cmd = f'gtts-cli{_slower} --tld {_top_level_domain} --lang {_lang} "{phrase}" --output -'
                with subprocess.Popen(
                    shlex.split(gtts_cmd), stdout=subprocess.PIPE
                ) as gtts_proc:
                    subprocess.run(
                        shlex.split(gst_cmd), stdin=gtts_proc.stdout, check=False
                    )
            readtexttools.unlock_my_lock(self.locker)
            return True

        return gst_speak(_text, _iso_lang, _speech_rate)

    def get_tld_data(self, iso_lang="en-US"):  # -> list[str]
        """
        Returns TLD translation info based on ISO language code.

        Priority:
        1. Exact country and language match
        2. First available entry with matching language
        3. Fallback to 'en-US' or hardcoded default
        """

        def format_entry(entry):
            return [
                entry.get("domain", ""),
                entry.get("iso_code", ""),
                entry.get("lang1", ""),
                entry.get("lang2", ""),
                entry.get("comment", ""),
            ]

        parts = iso_lang.replace("_", "-").split("-")
        lang = parts[0].lower()
        country = parts[1].upper() if len(parts) > 1 else ""

        # Priority 1: Exact match
        for entry in self.domain_table:
            if (
                entry.get("lang1", "").lower() == lang
                and entry.get("iso_code", "").upper() == country
            ):
                return format_entry(entry)

        # Priority 2: Language match only
        for entry in self.domain_table:
            if entry.get("lang1", "").lower() == lang:
                return format_entry(entry)

        # Priority 3: Fallback to 'en-US'
        for entry in self.domain_table:
            if entry.get("iso_code", "").upper() == "US":
                return format_entry(entry)

        return ["com", "US", "en", "es", "United States of America"]

    def read(
        self,
        _text="",
        _iso_lang="en-US",
        _visible="false",
        _audible="true",
        _out_path="",
        _icon="",
        _info="",
        _post_process="process_mp3_media",
        _writer="",
        _size="600x600",
        _speech_rate=160,
    ):  # -> bool
        """
        Setup
        -----

        + See: <https://gtts.readthedocs.io/en/latest/>
        + Package Manager: `sudo dnf install python3-pip` or `sudo apt install python3-pip`
        + Pip Installer: `pip3 install gTTS gTTS-token` (*Not* `sudo`!)

        + `_text` - Text to speak
        + `_iso_lang` - Supported letter language code - defaults to English
        + `_visible` - Use a graphic media player, or False for invisible player
        + `_out_path` - Name of desired output media file
        + `_audible` - If false, then don't play the sound file
        + `_icon` - a .png or .jpg file if required.
        + `_info` - Commentary or title for post processing
        + `_post_process` - Get information, play file, or convert a file
        + `_writer` - Artist or Author
        + `_size` - Dimensions to scale photo '600x600'
        + `_speech_rate` - Two speeds supported: 100% or above is Normal;
           Any value less is Slow.
        """
        if len(_text) == 0:
            return False
        _tld = "com"
        _region = "US"
        _lang1 = "en"
        _lang2 = "es"
        _short_text = ""
        _slow = False
        _lang_check = True
        _lang = _iso_lang
        _msg = ""
        _error_icon = readtexttools.net_error_icon()
        _version = self.get_version()
        _env_lang = readtexttools.default_lang()
        _provider = self.translator
        _provider_logo = f"/usr/share/icons/hicolor/scalable/apps/goa-account-{self.translator_domain}.svg)"
        if not os.path.isfile(_provider_logo):
            # Modified high contrast icon - GNU LESSER GENERAL PUBLIC LICENSE
            # Version 3, 29 June 2007
            # https://raw.githubusercontent.com/shgysk8zer0/adwaita-icons/master/LICENSE
            _provider_logo = readtexttools.app_icon_image("goa-account-google_hc.svg")
        for _dash in ["-", "_"]:
            if _dash in _iso_lang:
                _lang = _iso_lang.split(_dash)[0]
                _region = _iso_lang.split(_dash)[1]
                break
        try:
            if _speech_rate < 160:
                _slow = True
        except (NameError, TypeError):
            self.ok = False

        for entry in self.domain_table:
            if entry["iso_code"] == _region.upper():
                _tld = entry["domain"]
                _lang1 = entry["lang1"]
                _lang2 = entry["lang2"]
                break

        _media_out = ""
        # Determine the output file name
        _media_out = readtexttools.get_work_file_path(_out_path, _icon, "OUT")
        # Determine the temporary file name
        _media_work = "".join(
            [
                readtexttools.get_work_file_path(_out_path, _icon, "TEMP"),
                self.default_extension,
            ]
        )
        if len(_out_path) == 0 and bool(_post_process):
            if readtexttools.handle_sound_playing(_media_work):
                return True
        # Remove old files.
        if os.path.isfile(_media_work):
            os.remove(_media_work)
        if os.path.isfile(_media_out):
            os.remove(_media_out)
        _max_words = 25
        _short_text = "%20".join(_text.replace("+", "%2B").split(" ")[:_max_words])

        for _punctuation in "\n.?!":
            if _punctuation in _short_text:
                _short_text = _short_text.split(_punctuation)[0]
                break
        if _lang != _lang1:
            # Translate **to** default language
            _lang2 = _lang1
        if readtexttools.have_posix_app("osascript", False) or os.name == "nt":
            _header = "Read Text"
            _msg = "No voice model found"
        else:
            _header = f"""{_provider} Translate\u2122"""
            _msg = f"<https://translate.{self.translator_domain}.{_tld}?&langpair=auto|{_lang2}&tbb=1&ie=&hl={_env_lang}&text={_short_text}>"
        if not self.language_supported(_iso_lang):
            readtexttools.pop_message(
                _header,
                _msg,
                5000,
                _provider_logo,
                0,
            )
            return True
        try:
            tts = gtts.gTTS(_text, _tld, _lang, _slow, _lang_check)
            tts.save(_media_work)
            if os.path.isfile(_media_work):
                readtexttools.pop_message(
                    f"`gtts-{_version}`", _msg, 5000, _provider_logo, 0
                )
                heading1 = f"""{_provider} Translate\u2122"""
                underline = len(heading1) * "="
                print(
                    f"""{heading1}
{underline}

* gtts-{_version}
* {_msg}
"""
                )
        except gtts.tts.gTTSError:
            readtexttools.pop_message(
                f"`gtts-{_version}` failed to connect.",
                _msg,
                5000,
                _error_icon,
                2,
            )
            self.ok = False
            return False
        except (
            AssertionError, NameError, ValueError, RuntimeError
        ):
            # gtts error. Consider using pip3 or pipx for an update.
            readtexttools.pop_message(
                f"""{_provider} Translate\u2122""",
                _msg,
                5000,
                _provider_logo,
                0,
            )
            self.ok = False
            return False
        if os.path.isfile(_media_work) and _post_process in [
            "process_mp3_media",
            "process_audio_media",
        ]:
            if os.path.getsize(os.path.realpath(_media_work)) == 0:
                return False
            # NOTE: Calling process must unlock_my_lock()
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
        else:
            _msg = "Could not play a network media file locally. Try `pip3 install gTTS gTTS-token`."
            if bool(_media_out):
                _msg = "Could not save a network media file locally. Try `pip3 install gTTS gTTS-token`."
            readtexttools.pop_message(
                f"Python `gtts-{_version}`", _msg, 5000, _error_icon, 1
            )
        self.ok = False
        return False

    def supported_language(self, iso_lang="ca-ES"):  # -> str
        """Return the matched supported language code, or an empty string if unsupported."""
        if not iso_lang:
            return ""

        test_lang = (
            iso_lang.split("-")[0] if "-" in iso_lang else iso_lang.split("_")[0]
        )

        # Step 1: Try gtts library
        try:
            for _test in [iso_lang, test_lang]:
                if _test in gtts.tts.tts_langs():
                    return _test
        except Exception as e:
            print("Exception (gtts library):", e)

        # Step 2: CLI fallback
        try:
            cmd = shlex.split("gtts-cli --all")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            supported_langs = []

            for line in result.stdout.splitlines():
                if ":" in line and "-" in line:
                    lang_code = line.strip().split(":")[0].strip()
                    supported_langs.append(lang_code)
            for line in result.stdout.splitlines():
                if ":" in line and "-" not in line:
                    lang_code = line.strip().split(":")[0].strip()
                    supported_langs.append(lang_code)
            for _test in [iso_lang, test_lang]:
                if _test in supported_langs:
                    return _test
        except Exception as e:
            print("Exception (CLI fallback):", e)

        return ""

    def language_supported(self, iso_lang="ca-ES"):  # -> bool
        """Check if the library supports the language."""

        if self.supported_language(iso_lang):
            return True
        return False
