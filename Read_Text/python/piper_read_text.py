#!/usr/bin/env python
# -*- coding: UTF-8-*-
import codecs
import json
import os
import sys
import getopt
import urllib

import find_replace_phonemes
import netcommon
import readtexttools


def usage():
    """Usage"""
    cmd = "python3 piper_read_text.py"
    print(
        f"""Piper TTS
=========

Piper TTS is a fast, private local neural text to speech engine.

    {cmd} --language en-GB --rate 100% '<text_path.txt>'

Use a particular model (`auto5`) and speaker (`45`):

    {cmd} --language en-GB --voice auto5#45 --rate 75% '<text_path.txt>'

Use a piper `onnx` and `json` model package in a local user directory:

    {cmd} --voice='</path/to/myvoice.onnx>#4' '<text_path.txt>'

`piper_read_text.py` supports the languages, voices and features of
the binary `piper-tts` package rather than the python-pip distribution.
The `voices.json` file for piper 1.1.0 contains no gender information, so
the application will use the same voice index for 'auto', 'child', female'
and 'male'.

You must include the path to `piper` in your `PATH` environment.

This python tool will not work if you use pip3 or pipx to install it as a
command line interface for the python pip library. The `piper` symbolic
link would point to a python wrapper with different command line options
than the binary executable has.

* <https://github.com/rhasspy/piper>
* <https://huggingface.co/rhasspy/piper-voices/tree/main/>
"""
    )


class PiperTTSClass(object):
    """Piper TTS
    ============

    "A fast, private local neural text to speech engine"

    If `piper-tts` is not available using your Linux distributions normal
    package manager, then you can install it locally if it there is a version
    that supports your computer architecture. (i. e.
    `sudo apt-get install piper-tts`)

    Local installation
    ------------------

        mkdir -p "${HOME}/.local/share/piper-tts/piper-voices"
        cd "${HOME}/.local/share/piper-tts/piper-voices"

    Download the `voices.json` configuration file and place it in the root of
    this new directory.

        wget https://huggingface.co/rhasspy/piper-voices/raw/main/voices.json

    Within the new `piper-voices` directory, you can add valid `onnx` and
    `json` files from your provider or the official piper-tts voices
    [repository](https://huggingface.co/rhasspy/piper-voices). The
    [voices.json](https://huggingface.co/rhasspy/piper-voices/raw/main/voices.json)
    file includes file checksums and the path within the piper-voices
    directory to place each onnx and json pair of files. i. e.:

        "files": {
            "fr/fr_FR/siwis/low/fr_FR-siwis-low.onnx": {
                "size_bytes": 28130791,
                "md5_digest": "fcb614122005d70f27e4e61e58b4bb56"
            },
            "fr/fr_FR/siwis/low/fr_FR-siwis-low.onnx.json": {
                "size_bytes": 5950,
                "md5_digest": "54392cc51bd08e8aa6270302e9d0180b"
            }, ...
    Using the example, create this directory:

        ${HOME}/.local/share/piper-tts/piper-voices/fr/fr_FR/siwis/low/

    Place the fr_FR-siwis-low.onnx and fr_FR-siwis-low.json in this
    new directory.

    Espeak-ng
    ----------

    Some voices might require voice data from the `espeak-ng` package.

    ### Debian family

        sudo apt-get install espeak-ng-data

    ### Fedora family

        sudo dnf install espeak-ng-data

    Download a [binary release](https://github.com/rhasspy/piper#installation)
    archive and extract the contents to the `~/.local/share/piper-tts` directory,
    so that a piper executable is located at `~/.local/share/piper-tts/piper`.

    This tool assumes that the location of the `piper` executable is in your
    system path. If `~/.local/share/bin` is in your path, then the simplest
    way to enable the piper command is to create a symbolic link to the file.

        ln -s -T '${HOME}/.local/share/piper-tts/piper/piper' '${HOME}/.local/bin/piper'

    This python tool will not work if you use pip3 or pipx to install it as a
    python pip library. The `piper` symbolic link would point to a python wrapper
    with different command line options than the binary executable has.

    ### Optimize voice assets

    If you add or erase directories with voice assets, you can regenerate the
    local `voices.json` file with a python script included on the huggingface
    website.:

        python3 '($HOME)/.local/share/piper-tts/piper-voices/_script/voicefest.py'

    AI voices have a trade-off between latency and quality on low spec machines.
    Medium quality is great for most desktop computers. For small home automation
    computers, Low quality might work better. If you have a computer with a
    compatible high performance graphics card, you might want to choose High quality.

    * [Piper TTS](https://github.com/rhasspy/piper)
    * [Piper TTS voices](https://huggingface.co/rhasspy/piper-voices)"""

    def __init__(self):  # -> None
        """Initialize data."""
        _common = netcommon.LocalCommons()
        self.locker = _common.locker
        self.common = _common
        self.debug = _common.debug
        self.default_extension = _common.default_extension
        self.ok = False
        self.help_icon = _common.help_icon
        self.help_heading = "Piper TTS"
        self.help_url = "https://github.com/rhasspy/piper"
        self.voice_url = "https://huggingface.co/rhasspy/piper-voices/tree/main"
        self.json_url = (
            "https://huggingface.co/rhasspy/piper-voices/raw/main/voices.json"
        )
        self.local_dir = "default"
        self.default_speaker = 0  # All models have at least one voice.
        self.voice = self.default_speaker
        self.app_locker = readtexttools.get_my_lock("lock")

        self.accept_voice = [
            "",
            "all",
            "auto",
            "child_female1",
            "child_male1",
            "piper",
        ]
        self.default_lang = _common.default_lang
        self.default_model = "en_GB-vctk-medium.onnx"
        self.default_extension = _common.default_extension
        self.add_pause = _common.add_pause
        self.voice_name = ""
        self.lang = ""
        self.concise_lang = ""
        self.model = ""
        self.piper_voice_dir = os.path.expanduser(
            "~/.local/share/piper-tts/piper-voices"
        )
        if not os.path.isdir(self.piper_voice_dir):
            self.piper_voice_dir = os.path.expanduser("~/piper-voices")
        if not os.path.isdir(self.piper_voice_dir):
            self.piper_voice_dir = readtexttools.linux_machine_dir_path("piper-voices")
        if not os.path.isdir(self.piper_voice_dir):
            self.piper_voice_dir = os.path.expanduser("~/Downloads/piper-voices")
        if not os.path.isdir(self.piper_voice_dir):
            self.piper_voice_dir = os.path.expanduser("~/")
        self.espeak_ng_dir = os.path.expanduser(
            "~/.local/share/piper-tts/piper/espeak-ng-data"
        )
        if not os.path.isdir(self.espeak_ng_dir):
            self.espeak_ng_dir = os.path.expanduser("~/espeak-ng-data")
        if not os.path.isdir(self.espeak_ng_dir):
            self.espeak_ng_dir = readtexttools.linux_machine_dir_path("espeak-ng-data")
        self.j_key = ""
        self.j_key_list = []
        self.j_lang = ""
        self.j_concise_lang = ""
        self.j_model = ""
        self.j_quality = ""
        self.j_path = ""
        self.j_speaker_list = []
        self.j_data_set = ''
        self.sample_rate = 22050
        self.noise_scale = 0.667
        self.length_scale = 1
        self.noise_w = 0.8
        self.voice_count = 0
        self.use_specific_onnx_path = ""
        self.use_specific_onnx_voice_no = 0
        self.meta = readtexttools.ImportedMetaData()

    def language_supported(self, iso_lang="en-GB", vox="auto"):  # -> bool
        """Check to see if the language is available"""
        model_test = vox.split("#")[0]
        if model_test.startswith("~"):
            model_test = os.path.expanduser(model_test)
        if os.path.isfile(f"{model_test}.json"):
            if os.path.isfile(model_test):
                if "onnx: data" in self.meta.execute_command(f"file '{model_test}'"):
                    self.use_specific_onnx_path = model_test
                    self.lang = iso_lang
                    file_name = os.path.split(model_test)[1]
                    if "-" in file_name:
                        self.concise_lang = file_name.split("_")[0]
                    if "#" in vox:
                        self.use_specific_onnx_voice_no = int(
                            "".join(
                                [
                                    "0",
                                    readtexttools.safechars(
                                        vox.split("#")[1], "1234567890"
                                    ),
                                ]
                            )
                        )
                    self.ok = True
                    return self.ok
            return False
        if len(self.espeak_ng_dir) == 0:
            return False
        if len(self.piper_voice_dir) == 0:
            return False
        self.voice = int(
            "".join(["0", readtexttools.safechars(vox.split("#")[0], "1234567890")])
        )
        self.voice_name = vox
        self.concise_lang = iso_lang.split("_")[0].split("-")[0]
        self.lang = iso_lang.replace("-", "_")
        if self.concise_lang in os.listdir(self.piper_voice_dir):
            for block_list in ["_script", "~"]:
                if self.concise_lang.startswith(block_list):
                    self.ok = False
                    return self.ok
            self.ok = True
            return True
        else:
            for _file in os.listdir(self.piper_voice_dir):
                if _file.startswith(_file):
                    self.ok = True
                    return self.ok
        return False

    def _model_path_list(self, iso_lang="en-GB", _vox="", extension="onnx"):  # -> list
        """Check the directories for language models, and if found return
        the results in a list.
        """
        # NOTE: We use data that we can determine using the model key, so
        # we don't know whether a particular model is compatible with the
        # current version of piper, or whether the files' checksums match.
        _json_file = os.path.join(self.piper_voice_dir, "voices.json")
        _json_tools = readtexttools.JsonTools()
        _found_models = []
        _common = netcommon.LocalCommons()
        if os.path.exists(_json_file):
            with codecs.open(
                _json_file, mode="r", encoding="utf-8", errors="replace"
            ) as file_obj:
                data = json.load(file_obj)
        else:
            _warning = f"WARNING: Missing {self.help_heading} File!"
            underline = len(_warning) * "="
            print(
                f"""
{_warning}
{underline}

The {self.help_heading} client could not find a `.json` configuration file in
the `piper-tts` models directory.

    {_json_file}

Attempting to a generic on-line configuration. If you have custom piper
voice models, then the generic json configuration will not recognize them.

<{self.json_url}>"""
            )
            try:
                _common.set_urllib_timeout(4)
                response = urllib.request.urlopen(self.json_url)
                data_response = response.read()
                data = json.loads(data_response)
            except TimeoutError:
                self.ok = False
                return _found_models
        for _description in [
            iso_lang.replace("-", "_"),
            iso_lang.split("_")[0].split("-")[0],
        ]:
            try:
                for _item in data:
                    self.j_key = _json_tools.sanitize_json(data[_item]["key"])
                    self.j_key_list = self.j_key.split("-")
                    self.j_lang = self.j_key_list[0]
                    self.j_concise_lang = self.j_lang.split("_")[0]
                    self.j_model = self.j_key_list[1]
                    self.j_quality = self.j_key_list[2]
                    for self.j_path in [
                        os.path.join(
                            self.piper_voice_dir,
                            self.j_concise_lang,
                            self.j_lang,
                            self.j_model,
                            self.j_quality,
                            f"{self.j_key}.{extension}",
                        ),
                        os.path.join(self.piper_voice_dir, f"{self.j_key}.{extension}"),
                    ]:
                        if _vox in [self.j_key, self.j_model]:
                            return [self.j_path]
                        elif self.j_lang.startswith(_description):
                            if self.j_path not in _found_models:
                                # We need to confirm that models are not
                                # onnx placeholders that only contain
                                # ASCII text.
                                if os.path.isfile(self.j_path):
                                    if "onnx: data" in self.meta.execute_command(
                                        f"file '{self.j_path}'"
                                    ):
                                        _found_models.append(self.j_path)
            except IndexError:
                pass
        return _found_models

    def model_path(self, _extension="onnx"):  # -> str
        """piper-tts models usually have two essential files with `.json` and
        `.onnx` extensions. If `model.[json | .onyx]` is in an expected
        directory, return the path, otherwise return `''`"""
        if len(self.use_specific_onnx_path) != 0:
            return self.use_specific_onnx_path
        if not os.path.isdir(self.piper_voice_dir):
            return ""
        _model_list = self._model_path_list(self.lang, self.model, _extension)
        _uri = f"{self.voice_url}/{self.concise_lang}"
        if len(_model_list) == 0:
            print(
                f"""Piper TTS
=========

Missing or incompatible `{self.lang}` language `.json` and `.onnx` files for `{self.voice_name}`.

<{self.piper_voice_dir}>

[Get piper-voices]({_uri})."""
            )
            readtexttools.pop_message(
                self.help_heading, _uri, 8000, readtexttools.net_error_icon()
            )
        _model = netcommon.index_number_to_list_item(self.voice, _model_list)

        if os.path.isfile(_model):
            self.ok = True
            return _model
        self.ok = False
        return ""

    def _model_voice_info(self, _model=""):  # -> int
        """Get current info from  the `_model.json` file such as the
        number of speakers and the sample rate.  Edit the named
        json elements for individual voices if needed"""
        _json_file = os.path.join(f"{_model}.json")
        try:
            with codecs.open(
                _json_file, mode="r", encoding="utf-8", errors="replace"
            ) as file_obj:
                data = json.load(file_obj)
                try:
                    self.sample_rate = data["audio"]["sample_rate"]
                    self.noise_scale = data["inference"]["noise_scale"]
                    self.length_scale = data["inference"]["length_scale"]
                    self.noise_w = data["inference"]["noise_w"]
                    self.j_data_set = data["dataset"]

                    for _key in data["speaker_id_map"].keys():
                        self.j_speaker_list.append(_key)
                except KeyError:
                    pass
                self.voice_count = data["num_speakers"]
        except (KeyError, FileNotFoundError):
            self.voice_count = 0
            self.sample_rate = 22050
        return self.voice_count

    def _check_voice_request(self, _vox_number=0, _list_size=0):  # -> str
        """Handle out of range numbers using a modulus (`int % _list_size`)
        value."""
        try:
            if _list_size == 0:
                return 0
            if not _vox_number > _list_size - 1:
                return _vox_number
            return _vox_number % abs(_list_size)
        except (ZeroDivisionError, IndexError, TypeError):
            pass
        return 0

    def read(
        self, _text_file="", _iso_lang="en-GB", _config="", _speech_rate=160
    ):  # -> bool
        """Read speech aloud"""
        _length_scale = self.length_scale  # Fallback rate
        if _speech_rate != 160:
            _length_scale = self.common.rate_to_rhasspy_length_scale(_speech_rate)[0]
        if not self.ok:
            return False
        _espeak_data = self.espeak_ng_dir
        _model_home = self.piper_voice_dir
        if not os.path.isdir(_model_home):
            return False
        if len(self.use_specific_onnx_path) != 0:
            _model = self.use_specific_onnx_path
            _vox = "".join(["onnx#", str(self.use_specific_onnx_voice_no)])
        else:
            _model = self.model_path("onnx")
            _vox = self.voice_name
        _onnx = os.path.splitext(os.path.split(_model)[1])[0]
        voice_no = 0
        if "#" not in _vox:
            _vox = f"{_vox}#0"
        try:
            voice_no = int(_vox.split("#")[1])
        except (ValueError, IndexError):
            voice_no = 0
        voice_no = self._check_voice_request(voice_no, self._model_voice_info(_model))

        _outer = f" --output-raw | aplay -r {self.sample_rate} -f S16_LE -t raw -"
        # NOTE: change `_outer` if saving mp3 output; post-process wav file.
        if os.path.isfile(self.app_locker):
            readtexttools.unlock_my_lock("lock")
            return True
        else:
            readtexttools.lock_my_lock("lock")
        _model = _model.split("#")[0]
        if os.path.isfile(_model):
            _json_c = f"{_model}.json"
            if os.path.isfile(_config):
                _json_c = _config
            _command = "".join(
                [
                    "cat '",
                    _text_file,
                    "' | piper --espeak_data '",
                    _espeak_data,
                    "' --noise_scale ",
                    str(self.noise_scale),
                    " --noise_w ",
                    str(self.noise_w),
                    " --length_scale ",
                    str(_length_scale),
                    " --model '",
                    _model,
                    "' --config '",
                    _json_c,
                    "' --speaker ",
                    str(voice_no),
                    _outer,
                ]
            )
            _name_key = "None"
            if self.debug == 0:
                _variant = str(voice_no)
                _name_key = self.j_data_set
                try:
                    _name_key = self.j_speaker_list[voice_no]
                except IndexError:
                    pass
                print(
                    f"""
Piper TTS
=========

+ Language:  `{self.concise_lang}`
* Model:  `{_onnx}`
* Requested Language:  `{_iso_lang}`
* Requested Model:  `{_vox}`
* Speaker #: `{_variant}`
* Speaker Name: `{_name_key}`
* Speaker Count:  `{self.voice_count}`
* Speech Rate:  `{_speech_rate}`

[About Piper TTS]({self.help_url})
[Piper Voices]({self.voice_url})
"""
                )
            else:
                print(_command)
            _response = os.system(_command)
            readtexttools.unlock_my_lock("lock")
            return _response == 0
        return False


def main():  # -> NoReturn
    """Use Piper TTS speech synthesis for supported languages."""
    _piper_tts = PiperTTSClass()
    if not sys.version_info >= (3, 6) or not os.name in ["posix"]:
        print("Your system does not support the piper python tool.")
        usage()
        sys.exit(0)
    _percent_rate = "100%"
    _iso_lang = "en-GB"
    _config = ""  # model json path (defaults to onnx path + .json suffix)
    try:
        _iso_lang_def = readtexttools.default_lang().replace("_", "-")
    except AttributeError:
        pass
    _voice = "MALE1"
    _text_file_in = sys.argv[-1]
    if _text_file_in.startswith("~"):
        _text_file_in = os.path.expanduser(_text_file_in)
    if not os.path.isfile(_text_file_in):
        sys.exit(0)
    if sys.argv[-1] == sys.argv[0]:
        usage()
        sys.exit(0)
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "hclrv", ["help", "config", "language=", "rate=", "voice="]
        )
    except getopt.GetoptError:
        # print help information and exit
        print("option -a not recognized")
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-l", "--language"):
            _iso_lang = a
        elif o in ("-c", "--config"):
            if a.startswith("~"):
                a = os.path.expanduser(a)
            if os.path.isfile(a):
                _config = a
        elif o in ("-r", "--rate"):
            _percent_rate = a
        elif o in ("-v", "--voice"):
            _voice = a
        else:
            assert False, "unhandled option"
    if not _piper_tts.language_supported(_iso_lang, _voice):
        sys.exit(0)
    # WPM = Approximate Words per minute if in English or a similar idiom'
    find_replace_phonemes.fix_up_text_file(
        _text_file_in, "", _iso_lang, _piper_tts.local_dir, "PIPER_USER_DIRECTORY"
    )
    _piper_tts.read(
        _text_file_in, _iso_lang, _config, netcommon.speech_wpm(_percent_rate)
    )
    sys.exit(0)


if __name__ == "__main__":
    main()

# NOTE: This python code is a client of Piper. There are thousands
# of Piper voices, and the quality of voice samples on which they
# are based can vary.
# 
# With an untested model check if neural voice quality degrades or
# the voice starts "babbling" random sounds with long srings. Check
# short code-like strings like '`eye`, `bye`, `no`, `No`, `null`, `nil`,
# `None`, `don't` and `False`.
#
# This tool does not automatically download voice models(`onnx`) or
# configuration files (`json`).
#
# Copyright (c) 2023 James Holgate
