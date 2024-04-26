#!/usr/bin/env python
# -*- coding: UTF-8-*-
"""Module supporting Docker OpenTTS speech synthesis"""


import os
import platform
import tempfile
import netcommon
import readtexttools

try:
    import urllib
    import json

    BASICS_OK = True
except ImportError:
    BASICS_OK = False


class OpenTTSClass(object):
    """OpenTTS is a text to speech local host voice server. This client
    does not support pitch or speed. Not all speech engines support
    all genders; therefore, sometimes the gender will be ignored.

    You can set up OpenTTS as a local web server and connect it to various
    language systems. The particular systems vary according to language and
    what additional language systems you install.

    English, French, German, Italian, and Spanish can use OpenTTS with
    nanotts, an implementation of SVOX Pico. SVOX produces a clear and
    distinct speech output made possible by the use of Hidden Markov Model
    (HMM) algorithms.

    The [docker container](https://hub.docker.com/r/synesthesiam/opentts)
    allows you to install specific languages.

    `docker run -it -p 5500:5500 synesthesiam/opentts:<LANGUAGE>`

    Excluding `espeak` (robotic voices) removes support for some languages:

    `docker run -it -p 5500:5500 synesthesiam/opentts:<LANGUAGE> --no-espeak`

    [OpenTTS local host](http://0.0.0.0:5500)

    [More...](https://github.com/synesthesiam/opentts#open-text-to-speech-server)
    """

    def __init__(self) -> None:
        """Initialize data."""
        _common = netcommon.LocalCommons()
        self.common = _common
        self.locker = _common.locker
        self.debug = _common.debug
        self.default_extension = _common.default_extension
        self.ok = False
        self.voice_name = ""
        # This is the default. You can set up OpenTTS to use a different port.
        self.url = "http://0.0.0.0:5500"  # localhost port 5500
        self.help_icon = _common.help_icon
        self.help_heading = "OpenTTS"
        self.help_url = (
            "https://github.com/synesthesiam/opentts#open-text-to-speech-server"
        )
        self.voice = ""
        self.voice_id = ""  # larynx and  glow-speak use AI.
        # This subset of models omits espeak and festival.
        # In June, 2023, the OpenTTS speech engines that support languages
        # other than English include nanotts and marytts.
        self.vmodels = [
            "flite",
            "glow-speak",
            "larynx",
            "marytts",
            "nanotts",  # aka svox pico
        ]

        self.accept_voice = [
            "",
            "all",
            "auto",
            "child_female1",
            "child_male1",
            "opentts",
            "localhost",
            "docker",
            "local_server",
        ]
        # The routine uses the default voice as a fallback. The routine
        # prioritizes a voice that you chose to install.
        self.default_lang = _common.default_lang
        self.default_voice = "flite:cmu_us_bdl"
        self.default_extension = _common.default_extension
        self.full_names = []
        self.female_names = []
        self.male_names = []
        self.data = {}
        self.is_x86_64 = _common.is_x86_64
        self.pause_list = _common.pause_list
        self.add_pause = _common.add_pause
        self.max_chars = 360

    def spd_voice_to_opentts_voice(
        self, _search="female1", _iso_lang="en-US", _alt_local_url=""
    ) -> str:
        """Assign an OpenTTS name like `festival:cmu_us_slt_arctic_hts` to a
        spd_voice like `male1`"""
        _search = _search.strip("'\" \n")
        if len(self.full_names) == 0:
            if not self.language_supported(_iso_lang, _alt_local_url, _search):
                self.voice_id = ""
                return self.voice_id
        _vox_number = int(
            "".join(["0", readtexttools.safechars(_search, "1234567890")])
        )
        if _search in self.full_names:
            self.voice_id = _search
        elif _search.lower().startswith("female"):
            self.voice_id = netcommon.index_number_to_list_item(
                _vox_number, self.female_names
            )
        elif _search.lower().startswith("male"):
            self.voice_id = netcommon.index_number_to_list_item(
                _vox_number, self.male_names
            )
        else:
            self.voice_id = netcommon.index_number_to_list_item(
                _vox_number, self.full_names
            )
        _url = self.url
        voice_id = self.voice_id
        _help_url = self.help_url
        print(
            f"""
OpenTTS
=======

* Requested Voice:  {_search}
* Language:  {_iso_lang}
* OpenTTS Voice:  {voice_id}
* OpenTTS Server:  {_url}

[OpenTTS]({_help_url})
"""
        )
        return self.voice_id

    def language_supported(
        self, iso_lang="en-US", alt_local_url="", vox="auto"
    ) -> bool:
        """Is the language or voice supported?
        + `iso_lang` can be in the form `en-US` or a voice like `nanotts:es-ES`
        + `alt_local_url` If you are connecting to a local network's
           speech server using a different computer, you might need to use
           a different url."""
        if alt_local_url.startswith("http"):
            self.url = alt_local_url
        if (
            int(platform.python_version_tuple()[0]) < 3
            or int(platform.python_version_tuple()[1]) < 8
        ):
            self.ok = False
            return self.ok

        if len(self.voice_id) != 0:
            self.help_url = self.url
            self.help_icon = (
                "/usr/share/icons/HighContrast/scalable/actions/system-run.svg"
            )
            return True
        # format of json dictionary item: ''
        # "voice" or "language and region"
        _lang1 = iso_lang.lower()
        # concise language
        _lang2 = iso_lang.lower().split("-")[0].split("_")[0]
        if not _lang2 in ["de", "en", "es", "fr", "it"]:
            # nanotts is unsupported
            self.vmodels.append("espeak")
        if vox in self.vmodels and len(vox) != 0:
            # Test a specific model
            self.vmodels = [vox]
        try:
            response = urllib.request.urlopen(
                "".join([self.url, "/api/voices?language=", _lang2])
            )
            data_response = response.read()
            self.data = json.loads(data_response)
        except urllib.error.URLError:
            _eurl = self.url
            if self.is_x86_64:
                print(
                    f"""
[OpenTTS](https://github.com/synesthesiam/opentts#)
can synthesize speech privately using <{_eurl}>."""
                )
            self.ok = False
            return False
        except:  # [AttributeError, TimeoutError]:
            # catching classes that do not inherit from BaseException is not allowed
            self.ok = False
            return False
        if len(self.data) == 0:
            return False
        # Find the first voice that meets the criteria. See the
        # swagger API documentation at <http://0.0.0.0:5500/openapi/>.
        self.accept_voice.extend(netcommon.spd_voice_list(0, 200, ["female", "male"]))
        for _locale_lang in ["locale", "language"]:
            for _item in self.data:
                if bool(self.data[_item]["multispeaker"]) and iso_lang.startswith("en"):
                    _voice_ids = self.data[_item]["speakers"]
                    _speaker_prefix = "#"
                else:
                    _voice_ids = [""]
                    _speaker_prefix = ""
                for _speaker in _voice_ids:
                    if self.data[_item]["tts_name"] in self.vmodels:
                        full_name = "".join(
                            [
                                self.data[_item]["tts_name"],
                                ":",
                                self.data[_item]["name"],
                                _speaker_prefix,
                                _speaker,
                            ]
                        )
                        if full_name not in self.full_names:
                            self.accept_voice.append(full_name)
                            if _lang1 in self.data[_item][_locale_lang]:
                                self.full_names.insert(0, full_name)
                                if self.data[_item]["gender"] in [
                                    "M",
                                    None,
                                    "MF",
                                    "FM",
                                ]:
                                    self.male_names.insert(0, full_name)
                                if self.data[_item]["gender"] in [
                                    "F",
                                    None,
                                    "MF",
                                    "FM",
                                ]:
                                    self.female_names.insert(0, full_name)
                                self.ok = True
                            if _lang2 == self.data[_item][_locale_lang]:
                                self.full_names.insert(0, full_name)
                                if self.data[_item]["gender"] in [
                                    "M",
                                    None,
                                    "MF",
                                    "FM",
                                ]:
                                    self.male_names.insert(0, full_name)
                                if self.data[_item]["gender"] in [
                                    "F",
                                    None,
                                    "MF",
                                    "FM",
                                ]:
                                    self.female_names.insert(0, full_name)

                                self.ok = True
        if len(self.male_names) == 0:
            self.male_names = self.full_names
        if len(self.female_names) == 0:
            self.female_names = self.full_names
        return self.ok

    def try_url_lib(
        self,
        _voice="",
        _text="",
        _url="",
        _vocoder="",
        _denoiser_strength="",
        _ssml="",
        _ok_wait=4,
        _end_wait=10,
        _media_work="",
    ) -> bool:
        """Try getting a sound file using url_lib."""
        _done = False
        if not BASICS_OK:
            return False
        _common = netcommon.LocalCommons()
        _common.set_urllib_timeout(_ok_wait)
        my_url = "".join(
            [
                _url,
                "?voice=",
                urllib.parse.quote(_voice),
                "&vocoder=",
                urllib.parse.quote(_vocoder),
                "&denoiserStrength=",
                str(_denoiser_strength),
                "&ssml=",
                urllib.parse.quote(_ssml),
                "&cache=false&text=",
                urllib.parse.quote(_text),
            ]
        )
        try:
            # GET
            response = urllib.request.urlopen(my_url, timeout=_end_wait)
            with open(_media_work, "wb") as _handle:
                _handle.write(response.read())
            if os.path.isfile(_media_work):
                _done = os.path.getsize(_media_work) != 0
        except (TimeoutError, urllib.error.HTTPError):
            print(
                f"""
OpenTTS cannot provide speech for `{_voice}`.
Check the server settings or use a different voice.
    """
            )
            _done = False
        return _done

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
        ssml=False,
        _denoiser_strength=0.03,
        _ok_wait=20,
        _end_wait=60,
    ) -> bool:
        """Read OpenTTS speech aloud"""
        if not self.ok:
            return False
        if len(self.voice_id) == 0:
            self.voice_id = "nanotts:en-US"
            self.voice_name = ""
        _done = False
        _media_out = ""
        # Determine the output file name
        _media_out = readtexttools.get_work_file_path(_out_path, _icon, "OUT")
        # Determine the temporary file name
        _media_work = os.path.join(tempfile.gettempdir(), "opentts.wav")
        if os.path.isfile(_media_work):
            os.remove(_media_work)
        if len(_out_path) == 0 and bool(_post_process):
            if readtexttools.handle_sound_playing(_media_work):
                readtexttools.unlock_my_lock(self.locker)
                return True
            elif os.path.isfile(readtexttools.get_my_lock(self.locker)):
                readtexttools.unlock_my_lock(self.locker)
                return True
        _voice = self.voice_id
        if self.debug and 1:
            print(["`OpenTTSClass` > ` `read`", "Request `_voice`: ", _voice])
        if bool(self.add_pause) and not ssml:
            for _symbol in self.pause_list:
                if _symbol in _text:
                    _text = _text.translate(self.add_pause).replace(".;", ".")
                    break
        _vocoder = "low"
        if self.is_x86_64:
            _vocoder = "medium"
        _ssml = "false"
        if ssml:
            _ssml = "true"
        _url = "".join([self.url, "/api/tts"])
        _text = readtexttools.local_pronunciation(
            _iso_lang, _text, "default", "OPENTTS_USER_DIRECTORY", False
        )[0]

        readtexttools.lock_my_lock(self.locker)
        _tries = 0
        _no = "0" * 10
        if ssml:
            _items = [_text]
        elif self.common.is_ai_developer_platform():
            _items = self.common.big_play_list(_text, _iso_lang.split("-")[0])
        elif len(_text.splitlines()) == 1 or len(_text) < self.max_chars:
            _items = [_text]
        elif self.common.verify_spacy(_iso_lang.split("-")[0]):
            _items = self.common.big_play_list(_text, _iso_lang.split("-")[0])
        else:
            _items = [_text]
        for _item in _items:
            if not self.ok:
                return False
            if not os.path.isfile(readtexttools.get_my_lock(self.locker)):
                print("[>] Stop!")
                self.ok = False
                return True
            elif len(_item.strip(" ;.!?\n")) == 0:
                continue
            elif "." in _media_out and _tries != 0:
                _ext = os.path.splitext(_media_out)[1]
                _no = readtexttools.prefix_ohs(_tries, 10, "0")
                _media_out = _media_out.replace(f".{_ext}", f"_{_no}.{_ext}")
            _tries += 1
            _done = self.try_url_lib(
                _voice,
                _item,
                _url,
                _vocoder,
                _denoiser_strength,
                _ssml,
                _ok_wait,
                _end_wait,
                _media_work,
            )
            if not os.path.isfile(readtexttools.get_my_lock(self.locker)):
                print("[>] Stop")
                return True
            if _done:
                self.common.do_net_sound(
                    _info,
                    _media_work,
                    _icon,
                    _media_out,
                    _audible,
                    _visible,
                    _writer,
                    _size,
                    _post_process,
                    False,
                )
            else:
                break
        self.ok = _done
        if not _done:
            print(self.common.generic_problem)
        readtexttools.unlock_my_lock(self.locker)
        return _done
