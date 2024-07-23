#!/usr/bin/env python
# -*- coding: UTF-8-*-
"""Support MaryTTS speech synthesis using a Docker image. This image
features a collection of hidden semi-Markov model (HSMM) voices for
various languages. Latency is low and the models are compact. This
tool uses the same web address as Mimic3 by default, so you can't
run the two localhost servers together using the defaults.

    docker run -it -p 59125:59125 synesthesiam/marytts:latest \
        --voice cmu-bdl-hsmm --voice upmc-pierre-hsmm
    xdg-open http://0.0.0.0:59125

[MaryTSS](https://github.com/synesthesiam/docker-marytts)
"""


import os
import sys
import tempfile

try:
    import requests

    REQUESTS_OK = True
except (AttributeError, ImportError):
    REQUESTS_OK = False
try:
    import urllib

    BASICS_OK = True
except ImportError:
    BASICS_OK = False

import netcommon
import readtexttools


class MaryTtsClass(object):
    """MaryTTS
    =======

    You can use `synesthesiam/docker-marytts` text to speech localhost
    http server for 8 languages. You can find other docker containers that can
    use the same application program interface with a different selection of
    voices, speech technology, and language options.

    Default MaryTts server: <http://0.0.0.0:59125>

    [About MaryTts...](https://github.com/synesthesiam/docker-marytts)"""

    def __init__(self) -> None:
        """Initialize data. See
        <https://github.com/synesthesiam/docker-marytts>"""
        _common = netcommon.LocalCommons()
        self.locker = _common.locker
        self.common = _common
        self.debug = _common.debug
        self.local_dir = "mary_tts"
        self.ok = True
        self.response = ""
        # This is the default. You can set up MaryTts to use a different port.
        self.url = "http://0.0.0.0:59125"  # localhost port 59125
        self.help_icon = _common.help_icon
        self.help_heading = "Rhasspy MaryTTS"
        self.help_url = "https://github.com/synesthesiam/docker-marytts"
        self.audio_format = "WAVE_FILE"
        self.input_types = [
            "TEXT",
            "SIMPLEPHONEMES",
            "SABLE",
            "SSML",
            "APML",
            "EMOTIONML",
            "RAWMARYXML",
        ]
        self.accept_voice = [
            "",
            "all",
            "auto",
            "child_female",
            "child_female1",
            "child_male",
            "child_male1",
            "marytts",
            "mimic",
            "localhost",
            "docker",
            "local_server",
        ]
        self.voice_locale = ""
        self.voice_mimic_locale = ""
        self.pause_list = _common.pause_list
        self.add_pause = _common.add_pause
        self.base_curl = _common.base_curl
        self.is_x86_64 = _common.is_x86_64
        self.max_chars = 180
        self.nogender = "NA"
        self.male = "male"
        self.female = "female"

    def marytts_xml(self, _text="", _speech_rate=160) -> str:
        """Change the speed that MaryTTS reads plain text aloud using
        `RAWMARYXML`. `maryxml` correctly uses standard XML conventions like
        `&amp;`, `&gt;` and `&lt;`, so the characters that they represent use
        corrected XML."""
        _xmltransform = readtexttools.XmlTransform()
        _text = _xmltransform.clean_for_xml(_text, False)
        try:
            # 160 wpm (Words per minute) yields 100% prosody rate
            if _speech_rate < 40:
                _speech_rate = 40
            _rate = "".join([str(int(_speech_rate / 1.6)), "%"])
        except [AttributeError, TypeError]:
            _rate = "100%"
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<maryxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns="http://mary.dfki.de/2002/MaryXML" version="0.4" xml:lang="en-US"><p>
<prosody rate="{_rate}">{_text}</prosody></p></maryxml>"""

    def language_supported(self, iso_lang="en-US", alt_local_url="") -> bool:
        """Is the language or voice supported?
        + `iso_lang` can be in the form `en-US` or `en`.
        + `alt_local_url` If you are connecting to a local network's
           speech server using a different computer, you might need to use
           a different url."""
        if alt_local_url.startswith("http"):
            self.url = alt_local_url
        if sys.version_info < (3, 8):
            self.ok = False
            return self.ok
        if len(self.voice_locale) != 0:
            self.help_url = self.url
            self.help_icon = (
                "/usr/share/icons/HighContrast/scalable/actions/system-run.svg"
            )
            return True
        _lang1 = iso_lang.replace("-", "_")
        # concise language
        _lang2 = _lang1.split("_")[0]
        _locales = ""
        self.common.set_urllib_timeout(1)
        for dir_search in ["/locales", "/voices"]:
            try:
                response = urllib.request.urlopen("".join([self.url, dir_search]))
                _locales = str(response.read(), "utf-8")
            except TimeoutError:
                continue
            except urllib.error.URLError:
                self.ok = False
            except AttributeError:
                try:
                    response = urllib.urlopen("".join([self.url, dir_search]))
                    _locales = str(response.read(), "utf-8")
                except AttributeError:
                    self.ok = False
        if len(_locales) == 0:
            self.ok = False
            return False
        # Find the first voice that meets the criteria. If found, then
        # return `True`, otherwise return `False`.
        self.accept_voice.extend(netcommon.spd_voice_list(0, 100, ["female", "male"]))
        self.ok = False
        if "/" in _locales:
            # i. e.: `en_UK/apope_low` for mimic vs. `cmu-rms-hsmm` for MaryTTS
            return False
        if _lang1 in _locales.split("\n"):
            self.ok = True
            self.voice_locale = _lang1
        elif _lang2 in _locales.split() or _lang2 == "en":
            self.ok = True
            if _lang2 == "en":
                if _lang1[-2:].lower() in [
                    "au",
                    "bd",
                    "bs",
                    "gb",
                    "gh",
                    "hk",
                    "ie",
                    "in",
                    "jm",
                    "nz",
                    "pk",
                    "sa",
                    "tt",
                    "uk",
                ]:
                    self.voice_locale = "en_GB"
                else:
                    self.voice_locale = "en_US"
            else:
                self.voice_locale = _lang2.lower()
                self.voice_mimic_locale = _lang2
        return self.ok

    def _what_gender(self, _voice="male1") -> str:
        """Check the voice for a specific gender"""
        test_voice = _voice.lower()
        for gender in ["female", "male"]:
            for _standard in [gender, "".join(["child_", gender])]:
                if test_voice.startswith(_standard):
                    if gender == "female":
                        return self.female
                    return self.male
        return self.nogender

    def marytts_voice(
        self, _voice="", _iso_lang="en-US", _prefer_gendered_fallback=True
    ) -> str:
        """If the MaryTTS API includes the voice description, return a
        marytts voice description like `cmu-bdl-hsmm`, otherwise return
        `''`."""
        if len(_voice) == 0:
            return ""
        try:
            response = urllib.request.urlopen("".join([self.url, "/voices"]))
            _voices = str(response.read(), "utf-8")
        except urllib.error.URLError:
            help_site = (
                "[docker-marytts](https://github.com/synesthesiam/docker-marytts)"
            )
            print(
                f"""Requested {help_site}
It did not respond correctly."""
            )
            return ""
        except AttributeError:
            try:
                # catching classes that do not inherit from BaseExceptions
                # is not allowed.
                response = urllib.urlopen("".join([self.url, "/voices"]))
                _voices = str(response.read(), "utf-8")
            except AttributeError:
                return ""
        if len(_voices) == 0:
            return ""
        _locale = _iso_lang.replace("-", "_")
        _voice = _voice.lower()
        if _voices.count(_locale) == 0:
            # i. e.: en_AU, en_CA ... en_ZA etc.
            # Disregard the region code and use all voices for the language.
            _locale = _locale.split("_")[0]
        _voice_list = _voices.splitlines()
        for _tester in _voice_list:
            _row = _tester.split(" ")
            if _row[0].count(_voice) != 0:
                self.voice_locale = _row[1]
                return _row[0]
        last_match = ""
        if _voice not in self.accept_voice:
            return last_match
        good_rows = []
        match_found = []
        unmatch_found = []
        for _tester in _voice_list:
            _row = _tester.split(" ")
            is_exact_voice = False
            try:
                is_exact_voice = _row[0].lower() == _voice.lower()
                if _row[1].startswith(_locale) or is_exact_voice:
                    last_match = _row[0]
                    good_rows.append(_row)
            except IndexError:
                continue
        if len(good_rows) == 0:
            return ""
        mary_gender = self._what_gender(_voice)
        for good_row in good_rows:
            gender = good_row[2]
            if gender == mary_gender or is_exact_voice:
                match_found.append(good_row[0])
            else:
                unmatch_found.append(good_row[0])
        if len(match_found) == 0:
            match_found = unmatch_found
        elif not _prefer_gendered_fallback:
            # Allow male1 or no gender as alternate for female2
            # Allow female1 or no gender as alternate for male2
            match_found = match_found.extend(unmatch_found)
        _vox_number = int("".join(["0", readtexttools.safechars(_voice, "1234567890")]))
        best_match = netcommon.index_number_to_list_item(_vox_number, match_found)
        if len(best_match) != 0:
            return best_match
        return last_match

    def _try_requests(
        self,
        _mary_vox="",
        _audio_format="",
        _output_type="",
        _input_type="",
        _found_locale="",
        _text="",
        _ssml="",
        _length_scale=1,
        _url="",
        _ok_wait=4,
        _end_wait=30,
        _media_work="",
    ) -> bool:
        """Try getting a sound file using requests."""
        _done = False
        if not REQUESTS_OK:
            return False
        if len(_mary_vox) == 0:
            request_params = {
                "AUDIO": _audio_format,
                "OUTPUT_TYPE": _output_type,
                "INPUT_TYPE": _input_type,
                "LOCALE": _found_locale,
                "INPUT_TEXT": _text,
            }
        else:
            request_params = {
                "AUDIO": _audio_format,
                "OUTPUT_TYPE": _output_type,
                "INPUT_TYPE": _input_type,
                "LOCALE": _found_locale,
                "VOICE": _mary_vox,
                "INPUT_TEXT": _text,
            }
        _strips = ";\n .;"
        _text = _text.strip(_strips)
        try:
            response = requests.post(
                _url,
                params=request_params,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
                },
                data=_text.encode("utf-8", "ignore"),
                timeout=(_ok_wait, _end_wait),
            )
            with open(_media_work, "wb") as f:
                f.write(response.content)
            if os.path.isfile(_media_work):
                _done = os.path.getsize(_media_work) != 0
        except:
            _done = False
        return _done

    def _try_url_lib(
        self,
        _mary_vox="",
        _audio_format="",
        _output_type="",
        _input_type="",
        _found_locale="",
        _text="",
        _ssml="",
        _length_scale=1,
        _url="",
        _ok_wait=4,
        _end_wait=30,
        _media_work="",
    ) -> bool:
        """Try getting a sound file using url_lib."""
        _done = False
        if not BASICS_OK:
            return False
        self.common.set_urllib_timeout(_ok_wait)
        q_text = urllib.parse.quote(_text.strip(";\n"))
        if len(_mary_vox) == 0:
            vcommand = ""
        else:
            _mary_vox = urllib.parse.quote(_mary_vox)
            vcommand = f"&VOICE={_mary_vox}"
        _body_data = f"AUDIO={_audio_format}&OUTPUT_TYPE={_output_type}&INPUT_TYPE={_input_type}&LOCALE={_found_locale}{vcommand}&INPUT_TEXT="
        my_url = f'{_url}?{_body_data}"{q_text}"'
        try:
            # POST
            # NOTE: Setting a MaryTTS speech rate requires the python
            # `requests` library.
            _strips = "\n .;"
            _text = "\n".join(["", _text.strip(_strips), ""])
            data = {}  # The API uses an `INPUT_TEXT` argument for text
            req = urllib.request.Request(my_url, data)
            resp = urllib.request.urlopen(req)
            response_content = resp.read()
            with open(_media_work, "wb") as f:
                f.write(response_content)
            if os.path.isfile(_media_work):
                _done = os.path.getsize(_media_work) != 0
        except:
            _done = False
        if _done:
            self.ok = True
        else:
            self.ok = False
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
        ssml=False,
        _vox="male1",
        _ok_wait=4,
        _end_wait=30,
    ) -> bool:
        """
        The read tool supports a subset of MaryTTS functions because not
        all voices, languages and synthesisers support all of the features
        of the server.
        """
        if not self.ok:
            return False
        _media_out = ""
        _done = False
        _length_scale = 1
        _ssml = "0"
        # Determine the output file name
        _media_out = readtexttools.get_work_file_path(_out_path, _icon, "OUT")
        # Determine the temporary file name;
        _media_work = os.path.join(tempfile.gettempdir(), "MaryTTS.wav")
        _user_env = "MARY_TTS_USER_DIRECTORY"
        if os.path.isfile(_media_work):
            os.remove(_media_work)
        if len(_out_path) == 0 and bool(_post_process):
            if readtexttools.handle_sound_playing(_media_work):
                readtexttools.unlock_my_lock(self.locker)
                return True
            elif os.path.isfile(readtexttools.get_my_lock(self.locker)):
                readtexttools.unlock_my_lock(self.locker)
                return True
        if bool(self.add_pause) and not ssml:
            if any(_symbol in _text for _symbol in self.pause_list):
                _text = _text.translate(self.add_pause).replace(".;", ".")
        _view_json = self.debug and 1
        _mary_vox = self.marytts_voice(_vox, _iso_lang)
        response = readtexttools.local_pronunciation(
            _iso_lang, _text, self.local_dir, _user_env, _view_json
        )
        _text = response[0]
        if _view_json:
            print(response[1])
        if ssml:
            _input_type = self.input_types[3]
        elif _speech_rate == 160:
            _input_type = self.input_types[0]
        elif not REQUESTS_OK:
            # With `urllib` the tested version of MaryTTS can only use TEXT,
            # not RAWMARYXML
            print(
                """
NOTE: Setting a MaryTTS speech rate requires the python `request` library."""
            )
            _input_type = self.input_types[0]
        else:
            _input_type = self.input_types[6]
            if "</maryxml>" not in _text:
                _text = self.marytts_xml(_text, _speech_rate)
        _url1 = self.url
        _url = "".join([_url1, "/process"])
        _locale = _iso_lang.replace("-", "_")
        _found_locale = "en_US"
        if len(self.voice_locale) != 0:
            _found_locale = self.voice_locale
        _audio_format = self.audio_format
        _output_type = "AUDIO"
        _title = """Docker MaryTTS
=============="""
        _added_info = "[Docker MaryTTS](https://github.com/synesthesiam/docker-marytts)"
        print(
            f"""
{_title}
* Audio: `{_audio_format}`
* Input Type: `{_input_type}`
* Speech Rate: `{_speech_rate}`
* Locale: `{_found_locale}`
* Mapped Voice : `{_vox}`
* Output Type: `{_output_type}`
* Server URL: `{_url1}`
* Voice : `{_mary_vox}`

{_added_info}
"""
        )
        if _input_type != self.input_types[0]:
            # Don't split XML code
            _items = [_text]
        elif len(_text) < self.max_chars:
            _items = [_text]
        else:
            _items = self.common.big_play_list(_text, _iso_lang.split("-")[0])
        _tries = 0
        readtexttools.lock_my_lock(self.locker)
        _no = "0" * 10
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
            _done = self._try_requests(
                _mary_vox,
                _audio_format,
                _output_type,
                _input_type,
                _found_locale,
                _item.strip(),
                _ssml,
                _length_scale,
                _url,
                _ok_wait,
                _end_wait,
                _media_work,
            )
            if not _done:
                _done = self._try_url_lib(
                    _mary_vox,
                    _audio_format,
                    _output_type,
                    _input_type,
                    _found_locale,
                    _item.strip(),
                    _ssml,
                    _length_scale,
                    _url,
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
