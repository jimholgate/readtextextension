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
    import json

    BASICS_OK = True
except ImportError:
    BASICS_OK = False


class LarynxClass(object):
    """Larynx is a text to speech local http voice server that a
    Raspberry Pi computer can use with automated devices. Larynx
    can support SSML and codes in plain text strings to suggest
    how to say words and phrases. Check the larynx website shown
    at the end to see what processor platforms that larynx
    officially supports.

    To use the larynx speech synthesis client with this python class,
    you need to initiate `larynx-server`. Depending on how larnyx
    is configured, you might need administrator (`sudo`) access to
    start the server or to let local users start the server.

    This python program uses the larynx web api to read text aloud.

    Before putting larynx into daily use, you should test Layrnx speech
    synthesis using a desktop web browser at a `localhost` url. You
    can test different quality settings to determine the best combination
    of fidelity and low latency on your system.  The recommended setting for
    supported Raspberry Pi computers is currently `0` or `Low Quality`.
    For most consumer computers, the recommended setting is `1` or
    `Medium Quality`.

    If the implementation of dbus allows it, this class displays a
    pop-up menu if you have not created a directory in
    `~/.local/share/larynx/`. If your `larynx-server` is set up to
    allow it, this is the directory where the server stores and reads
    downloaded voices.

    [Default larnyx address](http://0.0.0.0:5002)

    [About Larynx...](https://github.com/rhasspy/larynx)"""

    def __init__(self):  # -> None
        """Initialize data. See
        <https://github.com/rhasspy/larynx#basic-synthesis>"""
        _common = netcommon.LocalCommons()
        self.common = _common
        self.debug = _common.debug
        self.default_extension = _common.default_extension
        self.ok = True
        # This is the default. You can set up Larynx to use a different port.
        self.url = "http://0.0.0.0:5002"  # localhost port 5002
        self.help_icon = _common.help_icon
        self.help_heading = "Rhasspy Larynx"
        self.help_url = "https://github.com/rhasspy/larynx#larynx"
        self.local_dir = os.path.expanduser("~/.local/share/larynx/")
        self.vocoders = None  # ordered fast+normal to slow+high quality
        self.ssmls = [False, True]  # false = TEXT or true = SSML
        self.rate_denominator = 1
        self.length_scales = _common.length_scales
        # A lower speed corresponds to a longer duration.
        # larynx `glow_tts` voices from larynx version 1.1.
        self.accept_voice = [
            "",
            "all",
            "auto",
            "child_female1",
            "child_male1",
            "larynx",
            "localhost",
            "docker",
            "local_server",
        ] + netcommon.spd_voice_list(0, 100, ["female", "male"])
        self.spd_fm = _common.spd_fm
        self.spd_m = _common.spd_m

        # The routine uses the default voice as a fallback. The routine
        # prioritizes a voice that you chose to install.
        self.default_lang = _common.default_lang
        self.default_voice = "mary_ann"
        self.default_extension = _common.default_extension
        # `mary_ann` is the default voice, and it is always installed. It
        # will not appear in a downloaded voices directory. It will always
        # be included in the server's json request response.
        self.larynx_v1 = ["mary_ann"]
        if "_IN" in self.default_lang:
            self.larynx_v1 = ["cmu_aup", "cmu_ksp", "cmu_slp"]
        elif self.default_lang == "en_CA":
            self.larynx_v1 = ["mary_ann", "cmu_jmk"]
        elif self.default_lang == "es_ES":
            self.larynx_v1 = ["carlfm", "karen_savage"]
        elif self.default_lang == "fr_FR":
            self.larynx_v1 = ["gilles_le_blanc", "siwis"]
        elif self.default_lang == "it_IT":
            self.larynx_v1 = ["lisa", "riccardo_fasol"]
        elif self.default_lang not in ["en_PH", "en_US", "es_MX"]:
            self.larynx_v1 = [
                "blizzard_fls",
                "ek",
                "harvard",
                "northern_english_male",
                "scottish_english_male",
                "southern_english_female",
                "southern_english_male",
            ]
        # https://community.rhasspy.org/t/preview-of-new-tts-voices/2556
        self.larynx_fm = _common.rhasspy_fm
        self.larynx_fm.append(self.default_voice)
        self.voice_id = ""
        self.voice_name = ""
        self.pause_list = _common.pause_list
        self.add_pause = _common.add_pause
        self.base_curl = _common.base_curl
        self.is_x86_64 = _common.is_x86_64
        self.max_chars = 360

    def _set_vocoders(self, alt_local_url=""):  # -> bool
        """If the server is running, then get the list of voice coders.
        + `alt_local_url` If you are connecting to a local network's
           larynx server using a different computer, you might need to use
           a different url."""
        if alt_local_url.startswith("http"):
            self.url = alt_local_url
        data = {}
        if bool(self.vocoders):
            return True
        try:
            self.common.set_urllib_timeout(1)
            response = urllib.request.urlopen("".join([self.url, "/api/vocoders"]))
            data_response = response.read()
            data = json.loads(data_response)
        except TimeoutError:
            self.ok = False
            return False
        except urllib.error.URLError:
            self.ok = False
            return False
        except AttributeError:
            try:
                response = urllib.urlopen("".join([self.url, "/api/vocoders"]))
                data_response = response.read()
                data = json.loads(data_response)
            except AttributeError:
                self.ok = False
                return False
            except TimeoutError:
                self.ok = False
                return False
            except urllib.error.URLError:
                self.ok = False
                return False
            except:
                self.ok = False
                return False
        except:
            print(
                """Unknown error while looking up larynx voice encoders.
Try restarting `larynx-server`."""
            )
            return False
        if len(data) == 0:
            return False
        _nsv = ""
        for _jint in range(0, len(data)):
            _nsv = "".join([_nsv, data[_jint]["id"], "\n"])
        self.vocoders = _nsv[:-1].split("\n")
        return True

    def _spd_voice_to_larynx_voice(
        self, _search="female1", larynx_names="mary_ann"
    ):  # -> str
        """Assign a larynx name like `scottish_english_male` to a spd_voice
        like `male1`"""
        if self.debug and 1:
            print(
                ["`LarynxClass` > `_spd_voice_to_larynx_voice`", _search, larynx_names]
            )
        _search = _search.lower().strip("'\" \n")
        if len(_search) == 0:
            return ""
        elif len(larynx_names.strip()) == 0:
            return ""
        # data_list has a minimum of four items.
        # Not using Modulo Operator (`%`)
        _data = 5 * """%(larynx_names)s\n""" % locals()
        _data_list = _data.strip().split("\n")
        _resultat = ""
        count_f = 0
        for count, _item in enumerate(self.spd_m):
            if _item == _search:
                count_f = count
                break
        _voices = ""
        if "female" not in _search:
            for _voice in _data_list:
                if _voice not in self.larynx_fm:
                    _voices = "".join([_voices, _voice, "\n"])
            try:
                _resultat = _voices.strip().split("\n")[count_f]
            except IndexError:
                _resultat = self.voice_name
        if len(_resultat) != 0:
            return _resultat
        count_f = 0
        for count, _item in enumerate(self.spd_fm):
            if _item == _search:
                count_f = count
                break
        _voices = ""
        for _voice in _data_list:
            if _voice in self.larynx_fm:
                _voices = "".join([_voices, _voice, "\n"])
        try:
            _resultat = _voices.strip().split("\n")[count_f]
        except IndexError:
            _resultat = self.voice_name
        return _resultat

    def language_supported(
        self, iso_lang="en-US", alt_local_url="", vox="auto"
    ):  # -> bool
        """Is the language or voice supported?
        + `iso_lang` can be in the form `en-US` or a voice like `eva_k`
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
        if not self._set_vocoders(self.url):
            self.ok = False
            return False
        if len(self.voice_id) != 0:
            self.help_url = self.url
            self.help_icon = (
                "/usr/share/icons/HighContrast/scalable/actions/system-run.svg"
            )
            return True
        # format of json dictionary item: 'de-de/eva_k-glow_tts'
        # "voice" or "language and region"
        _lang1 = iso_lang.lower()
        # concise language
        _lang2 = iso_lang.lower().split("-")[0].split("_")[0]
        data = {}
        try:
            response = urllib.request.urlopen("".join([self.url, "/api/voices"]))
            data_response = response.read()
            data = json.loads(data_response)
        except urllib.error.URLError:
            _eurl = self.url
            if self.is_x86_64:
                print(
                    """
[larynx-server](https://github.com/rhasspy/larynx)
can synthesize speech privately using %(_eurl)s."""
                    % locals()
                )
            self.ok = False
            return False
        except AttributeError:
            try:
                # catching classes that do not inherit from BaseExceptions
                # is not allowed.
                response = urllib.urlopen("".join([self.url, "/api/voices"]))
                data_response = response.read()
                data = json.loads(data_response)
            except Exception:
                try:
                    os.system("larynx-server")
                except OSError:
                    pass
                self.ok = False
                return False
        if len(data) == 0:
            return False
        # Find the first voice that meets the criteria. If found, then
        # return `True`, otherwise return `False`.
        _voice_id = ""
        larynx_names = ""
        for _item in data:
            if data[_item]["downloaded"]:
                self.accept_voice.append(data[_item]["name"])
                if _lang1 in data[_item]["language"]:
                    larynx_names = "".join([larynx_names, "\n", data[_item]["name"]])
                elif _lang2 == data[_item]["language"].split("-")[0].split("_")[0]:
                    larynx_names = "".join([larynx_names, "\n", data[_item]["name"]])
        larynx_names = larynx_names.strip()
        _vox = vox.lower()
        if _vox in larynx_names.split("\n"):
            _verified_name = _vox
        else:
            _verified_name = self._spd_voice_to_larynx_voice(_vox, larynx_names)
        if _verified_name in self.larynx_v1:
            _logo = "".join([" \u263B  (", self.default_lang, ")"])
        else:
            _logo = "".join([" \u263A  (", _lang2, ")"])
        print_url = self.url
        if len(_verified_name) != 0:
            if len(larynx_names) != 0:
                display_names = larynx_names.replace(
                    _verified_name, "%(_verified_name)s %(_logo)s  %(_vox)s" % locals()
                )
                print(
                    """
Loading larynx voices for `%(_lang2)s`
==============================

%(display_names)s

[Larynx server](%(print_url)s)
"""
                    % locals()
                )
            # Check for a specific matching SPD name
            # Search examples - `FEMALE2`, `MALE1`
            for _item in data:
                if data[_item]["name"] == _verified_name:
                    if self.debug and 1:
                        print(
                            [
                                "`LarynxClass` > `language_supported` found: ",
                                data[_item]["name"],
                                "Setting `id` to: ",
                                data[_item]["id"],
                            ]
                        )
                    self.voice_id = data[_item]["id"]
                    self.voice_name = data[_item]["name"]
                    self.ok = True
                    return self.ok
        self.ok = False
        iso_lower = iso_lang.replace("_", "-").lower()
        # Find a voice id that matches Larynx name, id or language
        # Search examples: ``, `AUTO`, `LARYNX`
        for _item in data:
            if data[_item]["downloaded"]:
                for try_lang in [
                    data[_item]["language"],
                    data[_item]["language"].split("-")[0],
                ]:
                    for argument in [_vox, iso_lower, _lang1]:
                        if argument in [
                            try_lang,
                            data[_item]["name"],
                            data[_item]["id"],
                        ]:
                            self.voice_id = data[_item]["id"]
                            self.voice_name = data[_item]["name"]
                            self.ok = True
                            return self.ok
        return self.ok

    def get_voc_type(self, _type="small"):  # -> str
        """Try to get the appropriate voc type for the platform."""
        if not _type in ["small", "medium", "large"]:
            return ""
        for coder in self.vocoders:
            if coder.endswith(_type):
                return coder
        return ""

    def _try_requests(
        self,
        _voice="",
        _text="",
        _url="",
        _vocoder="",
        _denoiser_strength="",
        _noise_scale="",
        _length_scale="",
        _ssml="",
        _ok_wait=4,
        _end_wait=30,
        _media_work="",
    ):  # -> bool
        """Try getting a sound file using requests."""
        _done = False
        if not REQUESTS_OK:
            return False
        try:
            _strips = "\n .;"
            _text = "\n".join(["", _text.strip(_strips), ""])
            response = requests.post(
                _url,
                params={
                    "voice": _voice,
                    "vocoder": _vocoder,
                    "denoiserStrength": _denoiser_strength,
                    "noiseScale": _noise_scale,
                    "lengthScale": _length_scale,
                    "ssml": _ssml,
                },
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
        _voice="",
        _text="",
        _url="",
        _vocoder="",
        _denoiser_strength="",
        _noise_scale="",
        _length_scale="",
        _ssml="",
        _ok_wait=4,
        _media_work="",
    ):  # -> bool
        """Try getting a sound file using url_lib."""
        _done = False
        if not BASICS_OK:
            return False
        self.common.set_urllib_timeout(_ok_wait)
        _vocoder = urllib.parse.quote(_vocoder)
        _voice = urllib.parse.quote(_voice)
        my_url = (
            """%(_url)s?voice=%(_voice)s&vocoder=%(_vocoder)s&denoiserStrength=%(_denoiser_strength)s&noiseScale=%(_noise_scale)s&lengthScale=%(_length_scale)s&ssml=%(_ssml)s"""
            % locals()
        )
        try:
            _strips = "\n .;"
            _text = "\n".join(["", _text.strip(_strips), ""])
            data = _text.encode("utf-8", "ignore")
            req = urllib.request.Request(my_url, data)
            resp = urllib.request.urlopen(req)
            response_content = resp.read()
            with open(_media_work, "wb") as f:
                f.write(response_content)
            if os.path.isfile(_media_work):
                _done = os.path.getsize(_media_work) != 0
        except:
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
        _speech_rate=160,
        quality=1,
        ssml=False,
        _denoiser_strength=0.005,
        _noise_scale=0.667,
        _ok_wait=20,
        _end_wait=60,
    ):  # -> bool
        """
        First, check larynx language support using `def language_supported`.
        Speak text aloud using a running instance of the
        [larynx-server](https://github.com/rhasspy/larynx)
        For most personal computers "highest" quality is too slow for
        real time speech synthesis. Use "standard" or "higher".
        """
        if not self.ok:
            return False
        if len(self.voice_id) == 0:
            self.voice_id = "en-us/mary_ann-glow_tts"
            self.voice_name = "mary_ann"
        _done = False
        if not os.path.isdir(self.local_dir):
            if not readtexttools.is_container_instance():
                readtexttools.pop_message(
                    self.help_heading,
                    "".join(["<", self.help_url, ">"]),
                    8000,
                    self.help_icon,
                    1,
                )
        _media_out = ""
        # Determine the output file name
        _media_out = readtexttools.get_work_file_path(_out_path, _icon, "OUT")
        # Determine the temporary file name
        _media_work = os.path.join(tempfile.gettempdir(), "larynx.wav")
        if os.path.isfile(_media_work):
            os.remove(_media_work)
        if len(_out_path) == 0 and bool(_post_process):
            if readtexttools.handle_sound_playing(_media_work):
                readtexttools.unlock_my_lock("larynx")
                return True
            elif os.path.isfile(readtexttools.get_my_lock("larynx")):
                readtexttools.unlock_my_lock("larynx")
                return True
        _voice = self.voice_name
        if self.debug and 1:
            print(["`LarynxClass` > ` `read`", "Request `_voice`: ", _voice])
        _length_scale = 0.85
        if bool(self.add_pause) and not ssml:
            for _symbol in self.pause_list:
                if _symbol in _text:
                    _text = _text.translate(self.add_pause).replace(".;", ".")
                    break
        try:
            if not self.is_x86_64:
                # Unknown platform - try the fastest setting.
                _vocoder = self.get_voc_type("small")
            elif quality in range(0, len(self.vocoders) - 1):
                # Set manually - I don't know which order the
                # voices are on your platform, so if it does
                # not work as expected, try a different number.
                _vocoder = self.vocoders[quality]
            elif len(_text.split()) < 3:
                # A single word
                self.rate_denominator = 0.85  # speak slower
                _vocoder = self.get_voc_type("large")
            else:
                _vocoder = self.get_voc_type("medium")
            if len(_vocoder) == 0:
                _vocoder = self.vocoders[len(self.vocoders) - 1]
        except IndexError:
            if bool(self.vocoders):
                _vocoder = self.vocoders[len(self.vocoders) - 1]
            else:
                return False
        _ssml = "false"
        if ssml:
            _ssml = "true"
        _url = "".join([self.url, "/api/tts"])
        _rate_length_scale = self.common.rate_to_rhasspy_length_scale(_speech_rate)
        if len(_rate_length_scale[1]) != 0:
            print(
                "".join(
                    [
                        "\nLarynx\n======\n+ tts rate: ",
                        _speech_rate,
                        "\nwpm   20%[",
                        _rate_length_scale[1],
                        "]200%\n+ url: ",
                        self.url,
                        "\n+ voice encoder: ",
                        _vocoder,
                        "\n+ voice id: ",
                        _voice,
                        "\n",
                    ]
                )
            )
        _length_scale = _rate_length_scale[0]
        _length_scale = str(_length_scale / self.rate_denominator)
        _text = readtexttools.local_pronunciation(
            _iso_lang, _text, "larynx", "LARYNX_USER_DIRECTORY", False
        )[0]

        readtexttools.lock_my_lock("larynx")
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
            if not os.path.isfile(readtexttools.get_my_lock("larynx")):
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
                _voice,
                _item,
                _url,
                _vocoder,
                _denoiser_strength,
                _noise_scale,
                _length_scale,
                _ssml,
                _ok_wait,
                _end_wait,
                _media_work,
            )
            if not _done:
                _done = self._try_url_lib(
                    _voice,
                    _item,
                    _url,
                    _vocoder,
                    _denoiser_strength,
                    _noise_scale,
                    _length_scale,
                    _ssml,
                    _ok_wait,
                    _media_work,
                )
            if not os.path.isfile(readtexttools.get_my_lock("larynx")):
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
        readtexttools.unlock_my_lock("larynx")
        return _done
