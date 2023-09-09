#!/usr/bin/env python
# -*- coding: UTF-8-*-
import os
import platform
import tempfile
try:
    import urllib
    import json
    BASICS_OK = True
except ImportError:
    BASICS_OK = False
import netcommon
import readtexttools


class RhvoiceLocalHost(object):
    """[Rhvoice-rest](https://hub.docker.com/r/aculeasis/rhvoice-rest) is
    a docker image that allows Linux users to use speech synthesis (text
    to speech) while running Read Text Extension in a protected container like
    a snap or a flatpak. It provides a `localhost` http server to convert text
    that you select to speech. Docker images come with all the necessary files
    and settings packaged in a tamper-resistant container.

    This Rhvoice docker container can read English, Esperanto, Georgian, Kyrgyz,
    Macedonian, Portuguese, Russian, Tatar and Ukrainian.

    The `rhvoice` libraries are enabled by electing to install it on a
    supported platform. Read the documentation for help installing the
    libraries or to help with troubleshooting if the tools do not work
    when using your Linux package manager.

    The following notice should be displayed in a dialog when users click
    `About...` or the equivalent in their language when this class is enabled.

    The main library is distributed under LGPL v2.1 or later. But it relies on
    MAGE for better responsiveness. MAGE is distributed under GPL v3 or later,
    so the combination is under GPL v3 or later. If you want to use the library
    in your program under GPL v2 or LGPL, compile the library without MAGE.

    The following restrictions apply to some of the voices:

    All voices from RHVoice Lab's site are distributed under the Creative
    Commons Attribution-NonCommercial-NoDerivatives 4.0 International Public
    License.

    The licenses for other optional third party voices are available at GitHub:

    <https://github.com/RHVoice/RHVoice/blob/master/doc/en/License.md>

    The contents of this resource are not affiliated with, sponsored by, or
    endorsed by RHVoice Lab nor does the documention represent the views or
    opinions of RHVoice Lab or RHVoice Lab personnel.

    The creators of the rhvoice libraries are the originators of the libraries
    enabling the `RhVoiceClass` class.

    See:

    * <https://github.com/RHVoice/RHVoice>
    * <https://github.com/RHVoice/RHVoice/issues>
    * <https://rhvoice.org/>"""

    def __init__(self) -> None:
        """The docker image doesn't expose details of the directory structure
        to the localhost API, so functions in the parent that rely on a specific
        file path do not work."""
        _common = netcommon.LocalCommons()
        self.locker = _common.locker
        self.common = _common
        self.add_pause = _common.add_pause
        self.pause_list = _common.pause_list
        self.base_curl = _common.base_curl
        self.debug = _common.debug
        self.url = "http://0.0.0.0:8080"  # localhost port 8080
        self.help_icon = _common.help_icon
        self.help_heading = "Rhvoice Rest"
        self.help_url = "https://github.com/Aculeasis/rhvoice-rest/"
        self.audio_format = ["wav", "mp3", "opus", "flac"][0]
        self.input_types = ["TEXT"]
        self.accept_voice = [
            "",
            "all",
            "auto",
            "child_female`",
            "child_male1",
            "rhvoice",
            "localhost",
            "docker",
            "local_server",
        ]
        self.ok = False
        self.voice = ""
        self.female = 2
        self.male = 1
        self.checked_lang = ""
        # This is a list for testing if the API fails. Normally, using
        # the json data at <http://0.0.0.0:8080/info> enables updates
        # and forks of the original docker image to use current data.
        # As of 2023.01,18 the API `country` field might not reflect
        # the accent of the named speaker.
        # [lang | lang-region], ['male' | 'female'], name
        self.checklist = [["zzy", "male", "_no_name"]]

        self.verified_voices = []
        self.length_scales = [
            [320, 289, "---------|", 100],
            [288, 257, "--------|-", 95],
            [256, 225, "-------|--", 85],
            [224, 193, "------|---", 75],
            [192, 161, "-----|----", 65],
            [160, 127, "----|----", 50],
            [128, 97, "---|-----", 35],
            [96, 66, "--|------", 20],
            [64, 33, "-|-------", 10],
            [32, 0, "|--------", 0],
        ]

    def update_rhvoice_checklist(self) -> list:
        """Create a list table in the same format as `self.checklist`
        using a json data adapted from the rhvoice-rest API.

        See: <https://www.iso.org/obp/ui/#iso:code:3166:UA>"""
        _url = "".join([self.url, "/info"])
        _default_list = self.checklist
        try:
            response = urllib.request.urlopen(_url)
            data_response = response.read()
            data = json.loads(data_response)
        except urllib.error.URLError:
            self.ok = False
            return _default_list
        except AttributeError:
            try:
                response = urllib.urlopen(_url)
                data_response = response.read()
                data = json.loads(data_response)
            except [AttributeError, urllib.error.URLError]:
                self.ok = False
                return _default_list
        except:
            return _default_list
        voice_lib = data["rhvoice_wrapper_voices_info"]
        key_list = []
        return_list = []
        self.accept_voice.extend(
            netcommon.spd_voice_list(0, 100, ["female", "male"]))
        for _item in voice_lib:
            key_list.append(_item)
            self.accept_voice.append(_item)
            self.verified_voices = key_list
        try:
            for _key in key_list:
                _iso = "".join(
                    [voice_lib[_key]["lang"], "-", voice_lib[_key]["country"]])
                for iso_c in [["-NaN", ""], ["-UK", "-UA"]]:
                    _iso = _iso.replace(iso_c[0], iso_c[1])
                return_list.append([
                    _iso, voice_lib[_key]["gender"],
                    voice_lib[_key]["name"].lower()
                ])
        except KeyError:
            return _default_list
        self.checklist = return_list
        self.ok = True
        return self.checklist

    def language_supported(self,
                           _iso_lang="en-US",
                           alt_local_url="") -> bool:
        """Is the language or voice supported in rhvoice rest?
        + `iso_lang` can be in the form `en-US` or `en`."""
        _found_name = ""
        if alt_local_url.startswith("http"):
            self.url = alt_local_url
        if self.ok:
            return self.ok
        if (int(platform.python_version_tuple()[0]) < 3
                or int(platform.python_version_tuple()[1]) < 8):
            self.ok = False
            return self.ok
        if not bool(self.verified_voices):
            self.update_rhvoice_checklist()
            if not bool(self.verified_voices):
                self.ok = False
                return False
        self.ok = False
        for _search in [_iso_lang.lower(), _iso_lang.split("-")[0].lower()]:
            for item in self.checklist:
                if item[0].lower().startswith(_search):
                    self.checked_lang = item[0]
                    self.ok = True
                    break
            if len(self.checked_lang) != 0:
                break
        if len(self.checked_lang) != 0:
            for item in self.checklist:
                if bool(self.common.debug):
                    print(item)
                if item[2] == _iso_lang.lower():
                    self.checked_lang = item[0]
                    self.ok = True
                    break
        if self.ok:
            help_heading = self.help_heading
            help_url = self.help_url
            print(f"""
Checking {help_heading} voices for `{_iso_lang}`
========================================

<{help_url}>
""")
        return self.ok

    def rhvoice_voice(self,
                      _voice="female1",
                      _iso_lang="en-US",
                      _prefer_gendered_fallback=True) -> str:
        """If the Rhvoice API includes the voice description, return a
        rhvoice voice description like `cmu-bdl-hsmm`, otherwise return
        `''`."""
        if len(_voice) == 0:
            return ""
        if not bool(self.verified_voices):
            self.update_rhvoice_checklist()
            if not bool(self.verified_voices):
                self.ok = False
                return ""
        _voice = _voice.lower()
        if _voice in self.verified_voices:
            return _voice
        _found_locale = self.checked_lang
        if len(_found_locale) == 0:
            _found_locale = readtexttools.default_lang().replace("_", "-")
        _found_locale = _found_locale.split("-")[0].split("_")[0]
        matches = []
        _add_name = ""
        gendered_fallback = ""
        last_match = ""
        i_lang = 0
        i_gender = 1
        i_name = 2
        for _row in self.checklist:
            try:
                if _row[i_lang].startswith(_found_locale):
                    last_match = _row[i_name]
                    for _standard in [
                            _row[i_gender],
                            "".join(["child_", _row[i_gender]]),
                    ]:
                        _add_name = ""
                        if _voice.startswith(_standard):
                            _add_name = last_match
                            break
                if len(_add_name) != 0 and _add_name not in matches:
                    matches.append(_add_name)
                    if len(gendered_fallback) == 0:
                        gendered_fallback = last_match
            except IndexError:
                break
        for i in range(0, len(matches)):
            if _voice.endswith(str(i + 1)):
                return matches[i]
        if _prefer_gendered_fallback:
            if len(gendered_fallback) != 0:
                return gendered_fallback
        return last_match

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
        _vox="female1",
        _ok_wait=4,
        _end_wait=30,
    ) -> bool:
        """Read text using <https://hub.docker.com/r/aculeasis/rhvoice-rest>"""
        if not self.ok:
            return False
        _media_out = ""
        _done = False
        # Determine the output file name
        _media_out = readtexttools.get_work_file_path(_out_path, _icon, "OUT")
        # Determine the temporary file name
        _media_work = os.path.join(tempfile.gettempdir(), "Rhvoice-rest.wav")
        if len(_out_path) == 0 and bool(_post_process):
            if readtexttools.handle_sound_playing(_media_work):
                readtexttools.unlock_my_lock(self.locker)
                return True
            elif os.path.isfile(readtexttools.get_my_lock(self.locker)):
                readtexttools.unlock_my_lock(self.locker)
                return True
        if bool(self.add_pause):
            for _symbol in self.pause_list:
                if _symbol in _text:
                    _text = _text.translate(self.add_pause).replace(".;", ".")
                    break
        if os.path.isfile(_media_work):
            os.remove(_media_work)
        _view_json = self.debug and 1
        response = readtexttools.local_pronunciation(_iso_lang, _text,
                                                     "rhvoice",
                                                     "RHVOICE_USER_DIRECTORY",
                                                     _view_json)
        _text = response[0]
        if _view_json:
            print(response[1])
        _length_scale = 50
        for _item in self.length_scales:
            if not _speech_rate > _item[0] and not _speech_rate < _item[1]:
                _length_scale = _item[3]
                break
        _length_scale = str(_length_scale)
        _url1 = self.url
        _url = f"{_url1}/say"
        _audio_format = self.audio_format
        _voice = self.rhvoice_voice(_vox, _iso_lang, True)
        if BASICS_OK:
            # Not all Rhvoice voices use ascii. i. e.: Portuguese
            # q_voice=let%C3%ADcia
            q_voice = urllib.parse.quote(_voice)
            _body_data = (
                f"format={_audio_format}&rate={_length_scale}&pitch=50&volume=50&voice={q_voice}&text="
            )
            # _method = "GET"
            _strips = "\n .;"
            self.common.set_urllib_timeout(_ok_wait)
            _tries = 0
            readtexttools.lock_my_lock(self.locker)
            _no = "0" * 10
            # Rhvoice has low latency, so using `spacy` to divide text into sentences
            # might degrade performance. Use `splitlines()`
            if self.common.ai_developer_platforms:
                _items = _text.splitlines()
            else:
                _items = [_text]
            for _item in _items:
                if not os.path.isfile(readtexttools.get_my_lock(self.locker)):
                    print("[>] Stop!")
                    return True
                if len(_item.strip(_strips)) == 0:
                    continue
                elif "." in _media_out and _tries != 0:
                    _ext = os.path.splittext(_media_out)[1]
                    _no = readtexttools.prefix_ohs(_tries, 10, "0")
                    _media_out = _media_out.replace(
                        f".{_ext}", f"_{_no}.{_ext}")
                _item = "\n".join(["", _item.strip(_strips), ""])
                # The API uses GET and a `text` argument for text

                q_text = urllib.parse.quote(_item)
                my_url = f'{_url}?{_body_data}"{q_text}"'
                try:
                    # See: <https://docs.python.org/3/library/urllib.request.html>
                    # See also: `/usr/lib/python3.xx/urllib/request.py
                    req = urllib.request.Request(my_url)
                    resp = urllib.request.urlopen(req)
                    response_content = resp.read()
                    with open(_media_work, "wb") as f:
                        f.write(response_content)
                    if os.path.isfile(_media_work):
                        _done = os.path.getsize(_media_work) != 0
                except:
                    _done = False
                    break
                if not _done:
                    readtexttools.unlock_my_lock(self.locker)
                    return False

                if not os.path.isfile(readtexttools.get_my_lock(self.locker)):
                    print("[>] Stop")
                    return True
                retval = self.common.do_net_sound(
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
        readtexttools.unlock_my_lock(self.locker)
        return retval
