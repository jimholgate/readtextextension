#!/usr/bin/env python3
# -*- coding: UTF-8-*-
"""Module supporting a simple speech synthesis server using the
[Rhasspy Piper TTS
server](https://github.com/rhasspy/piper/blob/master/src/python_run/README_http.md)
"""

import os
import tempfile

try:
    import urllib

    BASICS_OK = True
except ImportError:
    BASICS_OK = False
import netcommon
import readtexttools
import piper_read_text


class RhasspyPiperClass(object):
    """On 2023-12-21 synesthesiam (Michael Hansen) committed
    <https://github.com/rhasspy/piper/commit/2fa4c2c13933c1f6b8d87e34d12788ca8e6d073b>
    See: https://raw.githubusercontent.com/rhasspy/piper/master/src/python_run/piper/http_server.py
    See: https://github.com/rhasspy/piper/blob/master/src/python_run/README_http.md
    See: https://www.youtube.com/watch?v=pLR5AsbCMHs

    `(venv)`
    `python -m piper.http_server --model ~/pathto/en_US-lessac-medium.onnx`

    `* Serving Flask app 'http_server'`
    `* Debug mode: off`
    `INFO:werkzeug:WARNING: This is a development server. Do not use it in a`
    `production deployment. Use a production WSGI server instead.`

    `* Running on all addresses (0.0.0.0)`
    `* Running on http://127.0.0.1:5000`
    `* Running on http://192.168.0.108:5000`"""

    def __init__(self) -> None:
        """No User interface, so just submit plain text to get a WAVE audio file."""
        _common = netcommon.LocalCommons()
        self.locker = _common.locker
        self.common = _common
        self.add_pause = _common.add_pause
        self.pause_list = _common.pause_list
        self.debug = _common.debug
        self.url = "http://127.0.0.1:5000"  # Default URL port 5000
        self.help_heading = "Rhasspy Piper Server"
        self.help_url = (
            "https://github.com/rhasspy/piper/blob/master/src/python_run/README_http.md"
        )
        self.audio_format = ["wav"][0]
        self.input_types = ["TEXT"]
        self.local_dir = "default"

        self.accept_voice = [
            "",
            "all",
            "auto",
            "child_female`",
            "child_male1",
            "female",
            "male",
            "piper",
            "rhasspy",
            "localhost",
            "local_server",
        ]
        self.ok = False

    def ping_local_server(
        self, local_server: str = "http://127.0.0.1:5000?text=0"
    ) -> bool:
        """If local_server returns a file of length not equal to zero, then
        return `True`, but if the value is zero or there is an error, return
        `False`"""
        if not BASICS_OK:
            return False
        try:
            # See: <https://docs.python.org/3/library/urllib.request.html>
            # See also: `/usr/lib/python3.xx/urllib/request.py
            req = urllib.request.Request(local_server)
            resp = urllib.request.urlopen(req)
            response_content = resp.read()
            return len(response_content) != 0
        except:
            # bare-except because qualifying it causes an error on some
            # platforms.
            return False

    def language_supported(
        self, _iso_lang: str = "en-US", alt_local_url: str = ""
    ) -> bool:
        """Rhasspy Piper server only serves one model at a time, and this
        client cannot tell what language the server is serving. Therefore,
        the client assumes that you use the language of your system locale.
        and returns `True` if the requested language matches the system
        language locale.

        `iso_lang` can be in the form `en-US` , "en_US`. or `en`."""
        if alt_local_url.startswith("http"):
            self.url = alt_local_url
        if self.ok:
            return self.ok
        if BASICS_OK:
            _piper_tts = piper_read_text.PiperTTSClass()
            test_locale = _piper_tts.py_locale()
            base_locale = test_locale.split("_")[0]
            base_lang = _iso_lang.split("-")[0].split("_")[0]
            if base_locale == base_lang:
                self.ok = self.ping_local_server(f"{self.url}?text=0")
        return self.ok

    def read(
        self,
        _text: str = "",
        _iso_lang: str = "en-US",
        _visible: str = "false",
        _audible: str = "true",
        _out_path: str = "",
        _icon: str = "",
        _info: str = "",
        _post_process: str = "",
        _writer: str = "",
        _size: str = "600x600",
        _speech_rate: int = 160,
        _vox: str = "auto",
        _ok_wait: int = 4,
        _end_wait: int = 30,
    ) -> bool:
        """Read text using Rhasspy Piper speech synthesis server"""
        if not self.ok:
            return False
        _piper_tts = piper_read_text.PiperTTSClass()
        _media_out = ""
        _done = False
        # Determine the output file name
        _media_out = readtexttools.get_work_file_path(_out_path, _icon, "OUT")
        # Determine the temporary file name
        _media_work = os.path.join(tempfile.gettempdir(), "Rhasspy-Piper.wav")
        if len(_out_path) == 0 and bool(_post_process):
            if readtexttools.handle_sound_playing(_media_work):
                readtexttools.unlock_my_lock(self.locker)
                return True
            elif os.path.isfile(readtexttools.get_my_lock(self.locker)):
                readtexttools.unlock_my_lock(self.locker)
                return True
        if bool(self.add_pause):
            if any(_symbol in _text for _symbol in self.pause_list):
                _text = _text.translate(self.add_pause).replace(".;", ".")
        if os.path.isfile(_media_work):
            os.remove(_media_work)
        _view_json = self.debug and 1
        response = readtexttools.local_pronunciation(
            _iso_lang, _text, _piper_tts.local_dir, "PIPER_USER_DIRECTORY", _view_json
        )
        _text = response[0]
        if _view_json:
            print(response[1])
        if BASICS_OK:
            _body_data = "text="
            # _method = "GET"
            _strips = "\n .;"
            self.common.set_urllib_timeout(_ok_wait)
            _tries = 0
            readtexttools.lock_my_lock(self.locker)
            _no = "0" * 10
            if self.common.ai_developer_platforms:
                _items = _text.splitlines()
            else:
                _items = [_text]
            help_heading = self.help_heading
            help_underscore = len(help_heading) * "="
            print(
                f"""
{help_heading}
{help_underscore}

Server running on: <{self.url}>

[{help_heading}]({self.help_url})
"""
            )
            for _item in _items:
                if not self.ok:
                    return False
                if not os.path.isfile(readtexttools.get_my_lock(self.locker)):
                    print("[>] Stop!")
                    self.ok = False
                    return True
                if len(_item.strip(_strips)) == 0:
                    continue
                if "." in _media_out and _tries != 0:
                    _ext = os.path.splitext(_media_out)[1]
                    _no = readtexttools.prefix_ohs(_tries, 10, "0")
                    _media_out = _media_out.replace(f".{_ext}", f"_{_no}.{_ext}")
                _item = "\n".join(["", _item.strip(_strips), ""])
                # The API can use GET and a `text` argument for text
                q_text = urllib.parse.quote(_item)
                _url = self.url
                my_url = f'{_url}?{_body_data}"{q_text}"'
                try:
                    # See: <https://docs.python.org/3/library/urllib.request.html>
                    # See also: `/usr/lib/python3.xx/urllib/request.py
                    req = urllib.request.Request(my_url)
                    resp = urllib.request.urlopen(req)
                    response_content = resp.read()
                    with open(_media_work, "wb") as _handle:
                        _handle.write(response_content)
                    if os.path.isfile(_media_work):
                        _done = os.path.getsize(os.path.realpath(_media_work)) != 0
                except:
                    # bare-except because qualifying it causes an error on some
                    # platforms.
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
