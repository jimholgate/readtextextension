import netcommon
import os
import platform
import readtexttools

try:
    import requests

    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False
import tempfile

try:
    import urllib

    BASICS_OK = True
except ImportError:
    BASICS_OK = False


class MaryTtsClass(object):
    """MaryTTS
=======

You can use `synesthesiam/docker-marytts` text to speech localhost
http server for 8 languages. You can find other docker containers that can
use the same application program interface with a different selection of
voices, speech technology, and language options. For example,
[Larynx MaryTTS Compatible API](https://github.com/rhasspy/larynx#marytts-compatible-api)

Default MaryTts server: <http://0.0.0.0:59125>

[About MaryTts...](https://github.com/synesthesiam/docker-marytts)

MyCroft AI Mimic TTS
====================

"A fast local neural text to speech engine for Mycroft"

Check the release status of the API for Mimic before using it. By default the
application shares the same address and port as MaryTTS so do not run them at
the same time using the same URL and port.

    mkdir -p "${HOME}/.local/share/mycroft/mimic3"
    chmod a+rwx "${HOME}/.local/share/mycroft/mimic3"
    docker run \
        -it \
        -p 59125:59125 \
        -v "${HOME}/.local/share/mycroft/mimic3:/home/mimic3/.local/share/mycroft/mimic3" \
        'mycroftai/mimic3'

Set the Docker container restart policy to "always"

* [Mimic TTS](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mimic-tts/mimic-3)
* [GitHub](https://github.com/MycroftAI/mimic3)
"""

    def __init__(self):  # -> None
        """Initialize data. See
        <https://github.com/synesthesiam/docker-marytts>"""
        _common = netcommon.LocalCommons()
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
        self.pause_list = _common.pause_list
        self.add_pause = _common.add_pause
        self.base_curl = _common.base_curl
        self.is_x86_64 = _common.is_x86_64
        self.is_mimic = False
        self.max_chars = 360

    def marytts_xml(self, _text="", _speech_rate=160):  # -> str
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
        return (
            """<?xml version="1.0" encoding="UTF-8"?>
<maryxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns="http://mary.dfki.de/2002/MaryXML" version="0.4" xml:lang="en-US"><p>
<prosody rate="%(_rate)s">%(_text)s</prosody></p></maryxml>"""
            % locals()
        )

    def language_supported(self, iso_lang="en-US", alt_local_url=""):  # -> bool
        """Is the language or voice supported?
        + `iso_lang` can be in the form `en-US` or `en`.
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
                    # catching classes that do not inherit from BaseExceptions
                    # is not allowed.
                    response = urllib.urlopen("".join([self.url, dir_search]))
                    _locales = str(response.read(), "utf-8")
                except AttributeError:
                    self.ok = False
        if len(_locales) == 0:
            self.ok = False
            return False
        # Find the first voice that meets the criteria. If found, then
        # return `True`, otherwise return `False`.
        self.accept_voice.extend(netcommon.spd_voice_list(
            0, 100, ["female", "male"])
        )
        self.ok = False
        if "/" in _locales:
            # i. e.: `en_UK/apope_low` for mimic vs. `cmu-rms-hsmm` for MaryTTS
            self.is_mimic = True
            self.local_dir = "mimic"
            self.input_types = ["TEXT", "SSML"]
            for _test in [_lang1, _lang2]:
                for _row in _locales.splitlines():
                    if _row.startswith(_test):
                        self.ok = True
                        self.voice_locale = _test
                        break
                if self.ok:
                    break
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
                    if self.is_mimic:
                        # The default Mimic voice uses this locale
                        self.voice_locale = "en_UK"
                    else:
                        self.voice_locale = "en_GB"
                else:
                    self.voice_locale = "en_US"
            else:
                self.voice_locale = _lang2.lower()
        return self.ok

    def marytts_voice(
        self, _voice="", _iso_lang="en-US", _prefer_gendered_fallback=True
    ):  # -> str
        """If the MaryTTS API includes the voice description, return a
        marytts voice description like `cmu-bdl-hsmm`, otherwise return
        `''`."""
        if len(_voice) == 0:
            return ""
        try:
            response = urllib.request.urlopen("".join([self.url, "/voices"]))
            _voices = str(response.read(), "utf-8")
        except urllib.error.URLError:
            if self.is_mimic:
                print(
                    """Requested [Mimic 3](https://github.com/MycroftAI/mimic3#mimic-3)
                It did not respond correctly."""
                )
            else:
                print(
                    """Requested [docker-marytts](https://github.com/synesthesiam/docker-marytts)
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
        matches = []
        last_match = ""
        gendered_fallback = ""
        if _voice not in self.accept_voice:
            return last_match
        _neutral_voice_count = 0
        if self.is_mimic:
            _neutral_voice_count = 1
        for _tester in _voice_list:
            _row = _tester.split(" ")
            _add_name = ""
            try:
                if _row[1].startswith(_locale):
                    last_match = _row[0]
                    _row2 = _row[2]
                    if _row2 in ["male", "female"]:
                        for _standard in [
                            _row2,
                            "".join(["child_", _row2]),
                            "auto",
                        ]:
                            if _voice.startswith(_standard):
                                _add_name = last_match

                        if len(_add_name) != 0:
                            if _row2 == "male":
                                matches.append(_add_name)
                            else:
                                matches.insert(0, _add_name)
                    else:
                        # Unknown gender, so alternate adding the voice to
                        # the beginning and the end of the list so MALE[1|2|3]
                        # and FEMALE[1|2|3] are different voices if available.
                        _neutral_voice_count += 1
                        if _neutral_voice_count % 2 == 1:
                            matches.append(last_match)
                        else:
                            matches.insert(0, last_match)
                if len(gendered_fallback) == 0:
                    gendered_fallback = last_match
            except IndexError:
                continue
        if "male" in _voice:
            if not _neutral_voice_count in [0, 1]:
                print(
                    """\nNOTICE: The current voice models do not identify
voices by gender so the gender might be wrong."""
                )
        _vox_number = int("".join(["0", readtexttools.safechars(_voice, "1234567890")]))
        # When you just want a list of indices, it is faster to to use len()
        for i in range(0, len(matches)):
            if _vox_number % len(matches) == i + 1:
                return matches[i]
        if _prefer_gendered_fallback:
            if len(gendered_fallback) != 0:
                return gendered_fallback
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
    ):  # -> bool
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
        if self.is_mimic:
            request_params = {
                "text": _text,
                "voice": _mary_vox,
                "ssml": _ssml,
                "lengthScale": _length_scale,
            }
            # Note: 2013-03 Mimic switches are similar to Larynx.
            # This app uses a subset to maximize MaryTTS compatibility.
            # The Mimic defaults work well as-is.
            # 'api/tts?text=' + encodeURIComponent(text) +
            # '&voice=' + encodeURIComponent(voice) +
            # '&noiseScale=' + encodeURIComponent(noiseScale) +
            # '&noiseW=' + encodeURIComponent(noiseW) +
            # '&lengthScale=' + encodeURIComponent(lengthScale) +
            # '&ssml=' + encodeURIComponent(ssml) +
            # '&audioTarget=' + encodeURIComponent(audioTarget)
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
    ):  # -> bool
        """Try getting a sound file using url_lib."""
        _done = False
        if not BASICS_OK:
            return False
        self.common.set_urllib_timeout(_ok_wait)
        q_text = urllib.parse.quote(_text.strip(";\n"))
        if self.is_mimic:
            if _mary_vox.count("/") == 0:
                _mary_vox = "en_UK/apope_low"
            _mary_vox = urllib.parse.quote(_mary_vox)
            _ssml = urllib.parse.quote(_ssml)
            my_url = (
                "%(_url)s?text=%(q_text)s&voice=%(_mary_vox)s&ssml=%(_ssml)s&lengthScale=%(_length_scale)s"
                % locals()
            )
            try:
                # GET
                response = urllib.request.urlopen(my_url, timeout=(_end_wait))
                with open(_media_work, "wb") as f:
                    f.write(response.read())
                if os.path.isfile(_media_work):
                    _done = os.path.getsize(_media_work) != 0
            except:
                pass
        else:
            if len(_mary_vox) == 0:
                vcommand = ""
            else:
                _mary_vox = urllib.parse.quote(_mary_vox)
                vcommand = "&VOICE=%(_mary_vox)s" % locals()
            _body_data = (
                "AUDIO=%(_audio_format)s&OUTPUT_TYPE=%(_output_type)s&INPUT_TYPE=%(_input_type)s&LOCALE=%(_found_locale)s%(vcommand)s&INPUT_TEXT="
                % locals()
            )
            my_url = '%(_url)s?%(_body_data)s"%(q_text)s"' % locals()
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
    ):  # -> bool
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
        if self.is_mimic:
            _media_work = os.path.join(tempfile.gettempdir(), "Mimic3.wav")
            _user_env = "MIMIC_TTS_USER_DIRECTORY"
        else:
            _media_work = os.path.join(tempfile.gettempdir(), "MaryTTS.wav")
            _user_env = "MARY_TTS_USER_DIRECTORY"
        if os.path.isfile(_media_work):
            os.remove(_media_work)
        if len(_out_path) == 0 and bool(_post_process):
            if readtexttools.handle_sound_playing(_media_work):
                readtexttools.unlock_my_lock("mary")
                return True
            elif os.path.isfile(readtexttools.get_my_lock("mary")):
                readtexttools.unlock_my_lock("mary")
                return True
        if bool(self.add_pause) and not ssml:
            for _symbol in self.pause_list:
                if _symbol in _text:
                    _text = _text.translate(self.add_pause).replace(".;", ".")
                    break
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
        elif self.is_mimic:
            if ssml:
                _input_type = self.input_types[3]
                if "</speak>" not in _text:
                    _text = self.common.ssml_xml(
                        _text, _mary_vox, _speech_rate, _iso_lang
                    )
            else:
                _input_type = self.input_types[0]
            _length_scale = self.common.rate_to_rhasspy_length_scale(_speech_rate)[0]
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
        if self.is_mimic:
            _url = "".join([_url1, "/api/tts"])
            _ssml = "0"
            if ssml:
                _ssml = "1"
            if len(_mary_vox) == 0:
                _mary_vox = "en_UK/apope_low"
            _title = """Mycroft AI Mimic-3            
=================="""
            _preload = _mary_vox.split("#")[0]
            _added_info = (
                """Preload voice command
---------------------

    mimic3-server --preload-voice %(_preload)s

Help
----

[Mimic-3](https://github.com/MycroftAI/mimic3#mimic-3)"""
                % locals()
            )

        print(
            """
%(_title)s
* Audio: `%(_audio_format)s`
* Input Type: `%(_input_type)s`
* Speech Rate: `%(_speech_rate)s`
* Locale: `%(_found_locale)s`
* Mapped Voice : `%(_vox)s`
* Output Type: `%(_output_type)s`
* Server URL: `%(_url1)s`
* Voice : `%(_mary_vox)s`

%(_added_info)s
"""
            % locals()
        )
        if _input_type != self.input_types[0]:
            # Don't split XML code
            _items = [_text]
        elif self.common.is_ai_developer_platform():
            _items = self.common.big_play_list(_text, _iso_lang.split("-")[0])
        elif len(_text.splitlines()) == 1 or len(_text) < self.max_chars:
            _items = [_text]
        elif self.common.verify_spacy(_locale.split("_")[0]):
            # Split by sentence (`spacy`) or paragraph (`splitline()`)
            _items = self.common.big_play_list(_text, _locale.split("_")[0])
        else:
            _items = [_text]
        _tries = 0
        readtexttools.lock_my_lock("mary")
        _no = "0" * 10
        for _item in _items:
            if not os.path.isfile(readtexttools.get_my_lock("mary")):
                print("[>] Stop!")
                return True
            elif len(_item.strip(" ;.!?\n")) == 0:
                continue
            elif "." in _media_out and _tries != 0:
                _ext = os.path.splittext(_media_out)[1]
                _no = readtexttools.prefix_ohs(_tries, 10, "0")
                _media_out = _media_out.replace(
                    ".%(_ext)s" % locals(), "_%(_no)s.%(_ext)s" % locals()
                )
            _tries += 1
            _done = self._try_requests(
                _mary_vox,
                _audio_format,
                _output_type,
                _input_type,
                _found_locale,
                _item,
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
                    _item,
                    _ssml,
                    _length_scale,
                    _url,
                    _ok_wait,
                    _end_wait,
                    _media_work,
                )
            if not os.path.isfile(readtexttools.get_my_lock("mary")):
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
        readtexttools.unlock_my_lock("mary")
        return _done
