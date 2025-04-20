#!/usr/bin/env python
# -*- coding: UTF-8-*-
"""A client of the gtts python library

Powered by Google\u2122

"Google", "Google Cloud", "Google Translate" and the stylized "G" logo are
trademarks of Google Inc.

The contents of this resource are not affiliated with, sponsored by, or endorsed
by Google nor does the documention represent the views or opinions of Google or
Google personnel.
"""


import os
import sys
import netcommon
import readtexttools

try:
    import gtts
except (AttributeError, ImportError, ModuleNotFoundError):
    try:
        if len(readtexttools.find_local_pip("gtts")) != 0:
            sys.path.append(readtexttools.find_local_pip("gtts"))
            try:
                import gtts
            except:
                pass
    except:
        pass


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
        self.accept_voice = ["", "all", "auto", "child_female", "child_male", "gtts"]
        self.translator = "Google"
        self.translator_domain = self.translator.lower()
        self.default_extension = ".mp3"
        self.tested_version = 2.5  # May, 2024 - Ubuntu LTS 20.04 depreciated.

    def version(self):  # -> string
        """Returns the version in the form `nn.nn.nn`."""
        try:
            return gtts.version.__version__
        except (AttributeError, NameError):
            self.ok = False
            return "0.0.0"

    def check_version(self, minimum_version=0):  # -> bool
        """Check for minimum version."""
        if minimum_version == 0:
            minimum_version = self.tested_version
        if readtexttools.is_container_instance():
            self.ok = False
            return self.ok
        if os.name == "nt":
            # Require Windows Media Player play mp3 audio files.
            _wmp = readtexttools.WinMediaPlay()
            if len(_wmp.get_nt_path("Windows Media Player", "wmplayer.exe")) == 0:
                self.ok = False
                return self.ok
        _test_version = self.version()
        try:
            self.ok = float(".".join(_test_version.split(".")[:2])) >= minimum_version
        except (AttributeError, IndexError, ValueError):
            self.ok = False
        _commons = netcommon.LocalCommons()
        self.accept_voice.extend(
            netcommon.spd_voice_list(0, 100, ["female", "male", "auto"])
        )
        return self.ok

    def read(
        self,
        _text="",
        _iso_lang="en-US",
        _visible="false",
        _audible="true",
        _out_path="",
        _icon="",
        _info="",
        _post_process=None,
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
        _version = self.version()
        _env_lang = readtexttools.default_lang()
        _domain = self.translator_domain
        _provider = self.translator
        _provider_logo = (
            f"/usr/share/icons/hicolor/scalable/apps/goa-account-{_domain}.svg)"
        )
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

        domain_table = [
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
                "domain": "de",
                "iso_code": "DE",
                "lang1": "de",
                "lang2": "en",
                "comment": "Germany",
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
                "lang1": "es",
                "lang2": "en",
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
                "domain": "fr",
                "iso_code": "FR",
                "lang1": "fr",
                "lang2": "ar",
                "comment": "France",
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
                "domain": "us",
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
                "domain": "co.hn",
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
                "domain": "co.uk",
                "iso_code": "GB",
                "lang1": "en",
                "lang2": "pl",
                "comment": "Great Britain",
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
                "iso_code": "CN",
                "lang1": "zh",
                "lang2": "en",
                "comment": "Mandarin (Simplified)",
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
                "domain": "com.ve",
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
        for i in range(len(domain_table)):
            if domain_table[i]["iso_code"] == _region.upper():
                _tld = domain_table[i]["domain"]
                _lang1 = domain_table[i]["lang1"]
                _lang2 = domain_table[i]["lang2"]
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
        _max_words = 20
        _short_text = "%20".join(_text.replace("+", "%2B").split(" ")[:_max_words])

        for _punctuation in "\n.?!":
            if _punctuation in _short_text:
                _short_text = _short_text.split(_punctuation)[0]
                break
        if _lang != _lang1:
            # Translate **to** default language
            _lang2 = _lang1
        if readtexttools.have_posix_app("osascript", False) or os.name == "nt":
            _msg = f"https://translate.{_domain}.{_tld}"
        else:
            _msg = f"`<https://translate.{_domain}.{_tld}?&langpair=auto|{_lang2}&tbb=1&ie=&hl={_env_lang}&text={_short_text}>"
        if not self.language_supported(_iso_lang):
            # Fallback: display a link to translate using Google Translate.
            readtexttools.pop_message(
                f"{_provider} Translate\u2122",
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
                print(
                    f"""# {_provider} Translate\u2122"

* gtts-{_version}
* <{_msg}>
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
        except (AssertionError, NameError, ValueError, RuntimeError):
            # gtts error. Consider using pip3 to check for an update.
            readtexttools.pop_message(
                f"{_provider} Translate\u2122",
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

    def language_supported(self, iso_lang="ca-ES"):  # -> bool
        """Check if the library supports the language."""
        test_lang = ""
        if len(iso_lang) == 0:
            return False
        try:
            for sep in ["-", "_"]:
                if sep in iso_lang:
                    test_lang = iso_lang.split(sep)[0]
                    break
        except (AttributeError, NameError):
            return False
        try:
            for _test in [iso_lang, test_lang]:
                if _test in gtts.tts.tts_langs():
                    return True
        except NameError:
            pass
        return False
