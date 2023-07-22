#!/usr/bin/env python
# -*- coding: UTF-8-*-
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
        self.accept_voice = [
            "", "all", "auto", "child_female", "child_male", "gtts"
        ]
        self.translator = "Google"
        self.translator_domain = self.translator.lower()
        self.default_extension = ".mp3"
        self.tested_version = 2.3  # April, 2023

    def version(self):  # -> string
        """Returns the version in the form `nn.nn.nn`."""
        try:
            return gtts.version.__version__
        except (AttributeError, NameError):
            self.ok = False
            return ""

    def check_version(self, minimum_version=0):  # -> bool
        """Check for minimum version."""
        if minimum_version == 0:
            minimum_version = self.tested_version
        if os.name == "nt":
            # The library is not available in the LibreOffice
            # and OpenOffice for Windows python environments.
            # winsound.PlaySound does not play mp3 content.
            self.ok = False
            return self.ok
        _test_version = self.version()
        try:
            self.ok = float(".".join(
                _test_version.split(".")[:2])) >= minimum_version
        except (AttributeError, IndexError, ValueError):
            self.ok = False
        _commons = netcommon.LocalCommons()
        self.accept_voice.extend(
            netcommon.spd_voice_list(0, 100, ["female", "male"]))
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
        _slow = False
        _lang_check = True
        _lang = _iso_lang
        _error_icon = readtexttools.net_error_icon()
        _version = self.version()
        _env_lang = readtexttools.default_lang()
        _domain = self.translator_domain
        _provider = self.translator
        _provider_logo = (
            "/usr/share/icons/hicolor/scalable/apps/goa-account-%(_domain)s.svg"
            % locals())
        if not os.path.isfile(_provider_logo):
            # Modified high contrast icon - GNU LESSER GENERAL PUBLIC LICENSE
            # Version 3, 29 June 2007
            # https://raw.githubusercontent.com/shgysk8zer0/adwaita-icons/master/LICENSE
            _provider_logo = readtexttools.app_icon_image(
                "goa-account-google_hc.svg")
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
                "domain": "com.au",
                "iso_code": "AU",
                "lang1": "en",
                "lang2": "zh-CN"
            },
            {
                "domain": "co.uk",
                "iso_code": "GB",
                "lang1": "en",
                "lang2": "pl"
            },
            {
                "domain": "ca",
                "iso_code": "CA",
                "lang1": "en",
                "lang2": "fr"
            },
            {
                "domain": "co.nz",
                "iso_code": "NZ",
                "lang1": "en",
                "lang2": "zh-CN"
            },
            {
                "domain": "com.hk",
                "iso_code": "CN",
                "lang1": "zh",
                "lang2": "en"
            },
            {
                "domain": "com.hk",
                "iso_code": "HK",
                "lang1": "zh",
                "lang2": "en"
            },
            {
                "domain": "com.hk",
                "iso_code": "MO",
                "lang1": "zh",
                "lang2": "pt"
            },
            {
                "domain": "com.tw",
                "iso_code": "TW",
                "lang1": "zh-TW",
                "lang2": "en"
            },
            {
                "domain": "co.in",
                "iso_code": "IN",
                "lang1": "hi",
                "lang2": "en"
            },
            {
                "domain": "ie",
                "iso_code": "IE",
                "lang1": "en",
                "lang2": "pl"
            },
            {
                "domain": "co.za",
                "iso_code": "ZA",
                "lang1": "af",
                "lang2": "en"
            },
            {
                "domain": "fr",
                "iso_code": "FR",
                "lang1": "fr",
                "lang2": "ar"
            },
            {
                "domain": "com.br",
                "iso_code": "BR",
                "lang1": "pt",
                "lang2": "de"
            },
            {
                "domain": "pt",
                "iso_code": "PT",
                "lang1": "pt",
                "lang2": "en"
            },
            {
                "domain": "com.mx",
                "iso_code": "MX",
                "lang1": "es",
                "lang2": "en"
            },
            {
                "domain": "es",
                "iso_code": "ES",
                "lang1": "es",
                "lang2": "ca"
            },
            {
                "domain": "ar",
                "iso_code": "AR",
                "lang1": "es",
                "lang2": "en"
            },
            {
                "domain": "ci",
                "iso_code": "CI",
                "lang1": "es",
                "lang2": "en"
            },
            {
                "domain": "ru",
                "iso_code": "RU",
                "lang1": "ru",
                "lang2": "uk"
            },
            {
                "domain": "com.ua",
                "iso_code": "UA",
                "lang1": "uk",
                "lang2": "ru"
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
        _media_work = "".join([
            readtexttools.get_work_file_path(_out_path, _icon, "TEMP"),
            self.default_extension,
        ])
        if len(_out_path) == 0 and bool(_post_process):
            if readtexttools.handle_sound_playing(_media_work):
                return True
        # Remove old files.
        if os.path.isfile(_media_work):
            os.remove(_media_work)
        if os.path.isfile(_media_out):
            os.remove(_media_out)
        _max_words = 20
        _short_text = "%20".join(
            _text.replace("+", "%2B").split(" ")[:_max_words])

        for _punctuation in "\n.?!":
            if _punctuation in _short_text:
                _short_text = _short_text.split(_punctuation)[0]
                break
        if _lang != _lang1:
            # Translate **to** default language
            _lang2 = _lang1
        if readtexttools.have_posix_app("osascript", False):
            _msg = "https://translate.%(_domain)s.%(_tld)s" % locals()
        else:
            _msg = (
                "`<https://translate.%(_domain)s.%(_tld)s?&langpair=auto|%(_lang2)s&tbb=1&ie=&hl=%(_env_lang)s&text=%(_short_text)s>"
                % locals())
        if not self.language_supported(_iso_lang):
            # Fallback: display a link to translate using Google Translate.
            readtexttools.pop_message(
                "%(_provider)s Translate\u2122" % locals(),
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
                readtexttools.pop_message("`gtts-%(_version)s`" % locals(),
                                          _msg, 5000, _provider_logo, 0)
        except gtts.tts.gTTSError:
            readtexttools.pop_message(
                "`gtts-%(_version)s` failed to connect." % locals(),
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
                "%(_provider)s Translate\u2122" % locals(),
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
            if os.path.getsize(_media_work) == 0:
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
            readtexttools.pop_message("Python `gtts-%(_version)s`" % locals(),
                                      _msg, 5000, _error_icon, 1)
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
