#!/usr/bin/env python
# -*- coding: UTF-8-*-
"""
Piper TTS
=========

This client reads a text file aloud using `piper-tts`.

Piper TTS is a fast, private local neural text to speech engine.
Users can create or refine voice models based on a recording of
a voice.

This client uses the piper engine to read text aloud using Read
Text Extension with your office program.

* [Piper samples](https://rhasspy.github.io/piper-samples/)
* [Instructions](https://github.com/rhasspy/piper)
* [Download voices](https://huggingface.co/rhasspy/piper-voices/tree/main/)

Read Selection... Dialog setup:
-------------------------------

External program:

    /usr/bin/python3

Use the first available voice.

    "(PIPER_READ_TEXT_PY)"  --rate 100% --language (SELECTION_LANGUAGE_CODE) "(TMP)"

Use a particular model (`auto5`) and speaker (`45`):

    "(PIPER_READ_TEXT_PY)" --voice auto5#45 --rate 75% --language (SELECTION_LANGUAGE_CODE) "(TMP)"

Quick start
-----------

If you are not online, then you cannot download voice models or configuration
files. Once they are installed, piper handles speech locally.

Install the following packages:

    python3-pipx
    espeak-ng-data

Review the [voice model samples](https://rhasspy.github.io/piper-samples/).

The first time you use this client, it will set up a directory to store
piper voice models (`onnx`) and configuration files (`json`). 

`~/.local/share/piper-tts/piper-voices`

Read the `README` file in the directory for the next steps to complete
the installation using voice models for your language and region.

Final steps
-----------

To enhance the functionality, speed and stability of `piper-tts`
you can create a symbolic link at `~/.local/bin/piper-cli` targeting
the most recent binary `piper` executable program included in the 
[piper archive](https://github.com/rhasspy/piper#installation) for your
computer's specific processor type. For example, `piper_amd64.tar.gz`. 

    ln -s -T ~/.local/share/piper-tts/piper/piper ~/.local/bin/piper-cli

System-wide installation
------------------------

If you want every account on a single computer to have access to `piper`
then locate the contents of `piper_amd64.tar.gz` or the equivalent for
your computer architecture in a directory that every account has read access
to and link the `piper` application from the  archive to a location that is
in every user's `PATH` environment. For example,

    sudo ln -s -T /opt/piper-tts/piper/piper /usr/local/bin/piper

If this piper client does not find user installed models and configuration
files, it looks for global models and configuration files in:

    /usr/local/share/piper-voices

Users can access the model in the directory from the client dialog using:

    "(PIPER_READ_TEXT_PY)" --voice auto0#0 --rate 100% --language (SELECTION_LANGUAGE_CODE) "(TMP)"

If your Linux distribution includes packages to link `speech-dispatcher`
with `piper-tts`, then you can configure the `speech-dispatcher` platform
to use `piper-tts`:

    "(SPD_READ_TEXT_PY)" --language "(SELECTION_LANGUAGE_CODE)" "(TMP)"

[Read Text Extension](http://sites.google.com/site/readtextextension/)

Copyright (c) 2023 James Holgate
"""
import codecs
import json
import os
import sys
import getopt
import urllib

import find_replace_phonemes
import netcommon
import readtexttools


class PiperTTSClass(object):
    """Piper TTS class"""

    def __init__(self):  # -> None
        """Initialize data."""
        _common = netcommon.LocalCommons()
        self.default_lang = _common.default_lang
        self.concise_lang = self.default_lang.split("_")[0]
        self.tested_model = ""
        self.untested_model = ""
        self.tested_phrase = ""
        self.sample_model = "en_GB-vctk-medium"
        self.sample_phrase = "A rainbow is a meteorological phenomenon."
        # Is huggingface.co blocked in your region? Add a tested
        # model and sample phrase here so you don't need to go online.
        self.pip_checked_models = [
            [self.sample_model, self.sample_phrase],
            [
                "de_DE-thorsten-medium",
                "Der Regenbogen ist ein atmosphärisch-optisches Phänomen.",
            ],
            ["en_US-arctic-medium", self.sample_phrase],
            ["es_ES-davefx-medium", "Un arco iris es un fenómeno óptico."],
            ["fr_FR-upmc-medium", "Un arc-en-ciel est un phénomène optique."],
            [
                "uk_UA-ukrainian_tts-medium",
                "Весе́лка, також ра́йдуга оптичне явище в атмосфері.",
            ],
            ["zh_CN-huayan-medium", "师傅，你是做什么工作的"],
        ]
        self.instructions = ""
        self.quick_start = ""
        self.app = "piper"
        # Use a complete path for a local installation because the local user
        # might not have added `~/.local/bin/` to their `PATH` environment.
        _app_path = ""
        for _app in ["piper-cli", "piper"]:
            for _item in [
                f"~/.local/bin/{_app}",
                f"~/.local/share/piper-tts/{_app}/{_app}",
            ]:
                _path = os.path.expanduser(_item)
                if os.path.isfile(_path):
                    _app_path = _path
                    break
            if len(_app_path) != 0:
                self.app = _app_path
                break
        self.sample_uri = ""
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
        self.app_locker = readtexttools.get_my_lock(self.locker)
        self.default_extension = _common.default_extension
        self.voice_name = ""
        self.lang = ""
        self.model = ""
        self.piper_voice_dir = ""
        for _piper_dir in [
            "~/.local/share/piper-tts/piper-voices",
            "~/.local/share/piper/piper-voices",
            "~/.local/share/piper-voices",
            "~/piper-voices",
            "~/Downloads/piper-voices",
            readtexttools.linux_machine_dir_path("piper-voices"),
        ]:
            if os.path.isdir(os.path.expanduser(_piper_dir)):
                self.piper_voice_dir = os.path.expanduser(_piper_dir)
                break
        self.espeak_ng_dir = ""
        for espeak_ng_dir in [
            "~/.local/share/piper-tts/piper/espeak-ng-data",
            "~/.local/share/piper-tts/espeak-ng-data",
            "~/.local/share/piper/espeak-ng-data",
            "~/espeak-ng-data",
            "~/Downloads/espeak-ng-data",
            readtexttools.linux_machine_dir_path("espeak-ng-data"),
        ]:
            if os.path.isdir(os.path.expanduser(espeak_ng_dir)):
                self.espeak_ng_dir = os.path.expanduser(espeak_ng_dir)
                break
        self.j_key = ""
        self.j_lang = ""
        self.j_concise_lang = ""
        self.j_model = ""
        self.j_quality = ""
        self.j_path = ""
        self.speaker_id_map_keys = []
        self.dataset = ""
        self.phoneme_type = ""
        self.sample_rate = 22050
        self.noise_scale = 0.667
        self.length_scale = 1
        self.noise_w = 0.8
        self.voice_count = 0
        self.use_specific_onnx_path = ""
        self.use_specific_onnx_voice_no = 0
        self.meta = readtexttools.ImportedMetaData()

    def usage(self, _help=""):  # -> None
        """Usage"""
        cmd = "python3 piper_read_text.py"
        _file = "'<text_path.txt>'"
        if len(_help) != 0:
            cmd = "\"(PIPER_READ_TEXT_PY)\""
            _file = "\"(TMP)\""
        cmd_break = "\\"
        print(
            f"""
Piper TTS
=========

Piper TTS is a fast, private local neural text to speech engine.
This client uses the piper engine to read text aloud using Read
Text Extension with your office program.
{_help}
Use
===

Use the first available voice.

    {cmd} --language en-GB --rate 100% {_file}

Use a particular model (`auto5`) and speaker (`45`):

    {cmd} --language en-GB --voice auto5#45 --rate 75% {_file}

If you specify a voice name for one language model, other language
models will use the first voice in the model's index. For example,
if your preferred voice from the `de_DE-thorsten_emotional-medium`
model is `amused`, you would use:

    {cmd} --language de-DE {cmd_break}
        --voice de_DE-thorsten_emotional-medium#amused {_file}

You can still use French with a model like `fr_FR-upmc-medium`. When
speaking French with this model, it now uses the first voice in the list
(i.e.: `fr_FR-upmc-medium#jessica`) because it did not find `amused`
in the French language model.

You can use a piper `onnx` and `json` model package in a local 
user directory that you specify:

    {cmd} --voice='</path/to/myvoice.onnx>#4' {_file}

The `voices.json` file for piper contains no gender information, so
the application will use the same voice index for 'auto', 'child', female'
and 'male'.

* [Piper samples](https://rhasspy.github.io/piper-samples/)
* [Instructions](https://github.com/rhasspy/piper)
* [Download voices](https://huggingface.co/rhasspy/piper-voices/tree/main/)
"""
        )

    def get_quickstart_info(self):  # -> str
        """Set `self.quick_start` and return concise setup information."""
        _use_phrase = self.sample_phrase
        if len(self.tested_phrase) != 0:
            _use_phrase = self.tested_phrase
        _use_model = self.sample_model
        if len(self.tested_model) != 0:
            _use_model = self.tested_model
        self.quick_start = f"""
Quickstart
==========

    pipx upgrade-all
    pipx install piper-tts
    pipx ensurepath

Before using this piper client, verify that the piper program works by
testing it with a command from the piper-tts
[website](https://github.com/rhasspy/piper) using the same models that you
want to use with this client. If you are using the `python-pipx` version of
`piper`, using these commands trigger a download of configuration and data
files that contain between 60 - 100 GB of data depending on the model.

    sudo apt-get install espeak-ng-data
    cd ~/.local/share/piper-tts/piper-voices
    echo '{_use_phrase}' | \\
        ~/.local/bin/piper --model {_use_model} \\
        --output-raw | \\
        aplay -r 22050 -f S16_LE -t raw -

You can audition this and other piper speech models at the
[Piper Voice Samples](https://rhasspy.github.io/piper-samples/)
webpage. Once you have chosen a model, the page displays a download
[link](https://huggingface.co/rhasspy/piper-voices/tree/main/)
for the `MODEL_CARD`, `.onnx` model and `.json` configuration files. Click the
download links and store them in your voices directory at
`~/.local/share/piper-tts/piper-voices`. The binary version of piper from
[github](https://github.com/rhasspy/piper) is current.

The features of the python version of `piper` can vary depending on the
version of python and the libraries that are supplied by your distribution.
Therefore, some models that work with the binary version of `piper` might
not work with the python version.
"""
        return self.quick_start

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
            for _ignore in ["_script", "~"]:
                if self.concise_lang.startswith(_ignore):
                    self.ok = False
                    return self.ok
            self.ok = True
            return True
        else:
            for _file in os.listdir(self.piper_voice_dir):
                if _file.startswith(self.concise_lang):
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
                    # de_DE-thorsten_emotional-medium
                    self.j_key = data[_item]["key"]
                    self.j_lang = data[_item]["language"]["code"]  # de_DE
                    # de
                    self.j_concise_lang = data[_item]["language"]["family"]
                    self.j_model = data[_item]["name"]  # thorsten_emotional
                    self.j_quality = data[_item]["quality"]  # medium
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
                                if len(self.sample_uri) == 0:
                                    self.untested_model = self.j_key
                                    self.sample_uri = "/".join(
                                        [
                                            "https://rhasspy.github.io/piper-samples/samples",
                                            self.j_concise_lang,
                                            self.j_lang,
                                            self.j_model,
                                            self.j_quality,
                                            "sample.txt",
                                        ]
                                    )
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
        _model = ""
        _model_list = self._model_path_list(self.lang, self.model, _extension)
        _uri = f"{self.voice_url}/{self.concise_lang}"
        if len(_model_list) == 0:
            print("-" * 79)
            print(
                f"""
INFO: Piper TTS is missing `{self.lang}` `.json` and `.onnx` files.
<{self.piper_voice_dir}>

[Get piper-voices](https://huggingface.co/rhasspy/piper-voices/tree/main)"""
            )
            readtexttools.pop_message(self.help_heading, _uri, 8000, self.help_icon)
        _voice_name_base = self.voice_name.split("#")[0]
        os_sep = os.sep
        for _path in _model_list:
            if _path.endswith(f"{os_sep}{_voice_name_base}.{_extension}"):
                _model = _path
                break
        if len(_model) == 0:
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
                    self.dataset = data["dataset"]
                    self.phoneme_type = data["phoneme_type"]
                    for _key in data["speaker_id_map"].keys():
                        self.speaker_id_map_keys.append(_key)
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
            if _vox_number <= _list_size - 1:
                return _vox_number
            return _vox_number % abs(_list_size)
        except (ZeroDivisionError, IndexError, TypeError):
            pass
        return 0

    def _use_espeak_data_dir(self):  # -> bool
        """If the application publishes a major version greater than `0`
        or is an ELF binary return `True` otherwise return `False`"""
        if len(self.espeak_ng_dir) == 0:
            return False
        real_app = ""
        if os.sep in self.app:
            real_app = os.path.realpath(self.app)
            if "ELF" in self.meta.execute_command(f"file {real_app}"):
                return True
        try:
            return (
                int(
                    "".join(
                        ["0", self.meta.execute_command(f"{self.app} --version")]
                    ).split(".", maxsplit=1)[0]
                )
                != 0
            )
        except ValueError:
            return False

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
            _vox_split = _vox.split("#")[1]
            self._check_voice_request(0, self._model_voice_info(_model))
            if _vox_split in self.speaker_id_map_keys:
                voice_no = 0
                for _index in range(len(self.speaker_id_map_keys)):
                    if _vox_split.lower() == self.speaker_id_map_keys[_index].lower():
                        voice_no = _index
                        break
            else:
                voice_no = int(readtexttools.safechars(_vox_split, "1234567890"))
        except (ValueError, IndexError):
            voice_no = 0
        voice_no = self._check_voice_request(voice_no, self._model_voice_info(_model))

        _outer = f" --output-raw | aplay -r {self.sample_rate} -f S16_LE -t raw -"
        # NOTE: change `_outer` if saving mp3 output; post-process wav file.
        if os.path.isfile(self.app_locker):
            readtexttools.unlock_my_lock(self.locker)
            for _app in ["aplay", "piper", "piper-cli"]:
                readtexttools.killall_process(_app)
            return True
        else:
            readtexttools.lock_my_lock(self.locker)
        _model = _model.split("#")[0]
        _cuda = ""
        if netcommon.have_gpu("nvidia"):
            _cuda = " --cuda "
        _espeak_switch = ""
        _esp_warning = ""
        if self._use_espeak_data_dir():
            _espeak_switch = f" --espeak_data '{_espeak_data}'"
        elif self.phoneme_type not in ["espeak"]:
            try:
                _model_n = os.path.split(_model)[1]
            except IndexError:
                _model_n = self.dataset
            _esp_warning = f"""
WARNING: This version of `{self.app}` might not
support the `{self.phoneme_type}` phoneme type so the `{_model_n}`
model might not work. If there is a problem, try updating the model or
install the binary version.
"""
        speaker_switch = "' "
        if voice_no != 0:
            speaker_switch = "".join(["' --speaker ", str(voice_no)])
        if os.path.isfile(_model):
            _json_c = f"{_model}.json"
            if os.path.isfile(_config):
                _json_c = _config

            _command = "".join(
                [
                    "cat '",
                    _text_file,
                    f"' | {self.app}",
                    _cuda,
                    _espeak_switch,
                    " --noise_scale ",
                    str(self.noise_scale),
                    " --noise_w ",
                    str(self.noise_w),
                    " --length_scale ",
                    str(_length_scale),
                    " --model '",
                    _model,
                    "' --config '",
                    _json_c,
                    speaker_switch,
                    _outer,
                ]
            )
            _name_key = "None"
            if self.debug == 0:
                _variant = str(voice_no)
                _name_key = self.dataset
                try:
                    if len(self.speaker_id_map_keys) != 0:
                        _name_key = self.speaker_id_map_keys[voice_no]
                except IndexError:
                    pass
                print(
                    f"""
Piper TTS
=========

* Language:  `{self.concise_lang}`
* Model:  `{_onnx}`
* Requested Language:  `{_iso_lang}`
* Requested Model:  `{_vox}`
* Speaker #: `{_variant}`
* Speaker Name: `{_name_key}`
* Speaker Count:  `{self.voice_count}`
* Speech Rate:  `{_speech_rate}`
{_esp_warning}
[About Piper TTS]({self.help_url})
[Piper Voices]({self.voice_url})
"""
                )
            else:
                print(_command)
            _response = os.system(_command)
            readtexttools.unlock_my_lock(self.locker)
            return _response == 0
        return False

    def load_instructions(self, verbose=True):  # -> str
        """Return installation instructions"""
        _quick_start = ""
        if verbose:
            for suggested in self.pip_checked_models:
                for _test in [self.default_lang, self.concise_lang]:
                    if suggested[0].startswith(_test):
                        self.tested_model = suggested[0]
                        self.tested_phrase = suggested[1]
                        break
                if len(self.tested_model) != 0:
                    break
            if len(self.tested_model) == 0:
                self.tested_model = self.sample_model
                try:
                    self.common.set_urllib_timeout(4)
                    response = urllib.request.urlopen(self.sample_uri)
                    self.tested_phrase = (
                        response.read().decode("utf-8").strip().replace("'", "\\'")
                    )
                    self.tested_model = self.untested_model
                except (TimeoutError, ValueError):
                    pass
                if len(self.tested_phrase) == 0:
                    self.tested_phrase = self.sample_phrase
            _quick_start = self.get_quickstart_info()
        self.instructions = f"""
Summary
=======

* Install the piper application
* Download the current `voices.json` configuration file
* Download voice `onnx` and `json` files for the model or models
  that you need and place them in the appropriate directory.

Installation
============
{_quick_start}
### python-pipx

To [install](https://github.com/rhasspy/piper#running-in-python)
using `pipx`, you need the `python3-pipx` python package.

    pipx upgrade-all
    pipx install piper-tts
    pipx ensurepath

Some platforms might show an error when attempting to use the library because
they use an incompatible version of one or more of python's support libraries
or the system architecture is incompatible with `piper-tts`. In this case, a
binary package compatible with your computer's architecture might work.

Currently, the python library version of the piper command line interface
displays no information about the audio stream. 

### Binary package

The piper-tts pip library distribution helps you to install voices easily.
However, this client works faster and more predictably with the newest
piper-tts binary package from the github website.

The python binary supports Debian stable (x86-64), Fedora Workstation
(x86-64) and Ubuntu LTS (x86-64). If you use the binary package, you
must include the path to `piper` in your `PATH` environment or create a
symbolic link to the program path in a directory that is included in your
`PATH` environment.

Download the [piper archive](https://github.com/rhasspy/piper#installation)
and extract the contents to the `~/.local/share/piper-tts` directory,
so that a piper executable is located at `~/.local/share/piper-tts/piper`.
This client assumes that the location of the `piper` executable is in your
system path. If `~/.local/share/bin` is in your path, then the simplest
way to enable the piper command is to create a symbolic link to the file.

    ln -s -T ~/.local/share/piper-tts/piper/piper ~/.local/bin/piper-cli

This link command uses a distinct name for the application so that the
link does not overwrite a link to a python script of the same name.
The binary version of piper displays information about the audio stream
in the terminal window.

Download models and configuration files
---------------------------------------

### Samples and json configurations download

This is optional. You can set up the standard release directory structure
for all sample voice mp3 files, json configuration files, notes, utility
scripts, and placeholders for onnx file data using git.

    cd "~/.local/share/piper-tts/piper-voices"
    git clone https://huggingface.co/rhasspy/piper-voices

This method of replicating the developer configuraton setup includes plain
text placeholders for the onnx binary files that work with piper-tts. You
can activate a voice model by replacing the text placeholder with the
the actual onnx file from the web site.

#### Placeholder

The placeholder is a text file that contains the version, verification
checksum and size of the onnx file.
https://huggingface.co/rhasspy/piper-voices/raw/main/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx

#### Actual file:

The linked file is a binary file that piper-tts can use to generate speech.
https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx

Local voices
------------
This client looks for voices in several directories. To create a directory in
the recommended location, enter:

    mkdir -p "~/.local/share/piper-tts/piper-voices"
    cd "~/.local/share/piper-tts/piper-voices"

Download the `voices.json` configuration file and place it in the root of this
new directory.

    wget -O "~/.local/share/piper-tts/piper-voices/voices.json" \\
        https://huggingface.co/rhasspy/piper-voices/raw/main/voices.json

Within the new `piper-voices` directory, you can add valid `onnx` and `json`
files from your provider or the official piper-tts voices
[repository](https://huggingface.co/rhasspy/piper-voices). The
[`voices.json`](https://huggingface.co/rhasspy/piper-voices/raw/main/voices.json)
file includes information about the files, including their relative location.

    "files": {{
        "fr/fr_FR/siwis/low/fr_FR-siwis-low.onnx": {{
            "size_bytes": 28130791,
            "md5_digest": "fcb614122005d70f27e4e61e58b4bb56"
        }},
        "fr/fr_FR/siwis/low/fr_FR-siwis-low.onnx.json": {{
            "size_bytes": 5950,
            "md5_digest": "54392cc51bd08e8aa6270302e9d0180b"
        }}, ... }}

Using the example, `fr_FR-siwis-low.onnx` is located on the server at:

<https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/low/fr_FR-siwis-low.onnx>

The `fr_FR-siwis-low.onnx.json` configuration is located on the server at:

<https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/low/fr_FR-siwis-low.onnx.json>

This client looks for the local resources in these directories:

    ~/.local/share/piper-tts/piper-voices/fr/fr_FR/siwis/low/
    ~/.local/share/piper-tts/piper-voices/
    ~/piper-voices/

Place `fr_FR-siwis-low.onnx` and `fr_FR-siwis-low.json` in one of these
directories.

Espeak-ng data
--------------

Some voices might require voice data from the `espeak-ng` package.

### Debian family

    sudo apt-get install espeak-ng-data

### Fedora family

    sudo dnf install espeak-ng-data

### Optimize voice assets

If you add or erase directories with voice assets, or modify configuration
parameters, you can regenerate the local `voices.json` file with a [python
script](https://huggingface.co/rhasspy/piper-voices/tree/main/_script)
included on the huggingface website.

    python3 '($HOME)/.local/share/piper-tts/piper-voices/_script/voicefest.py'

Piper voices have a trade-off between latency and quality. Piper supports
four quality levels:

* `x_low` - 16Khz audio, 5-7M params
* `low` - 16Khz audio, 15-20M params
* `medium` - 22.05Khz audio, 15-20M params
* `high` - 22.05Khz audio, 28-32M params

Some models contain multiple speakers. The quality of one of the speakers
could be less than it would be using a single speaker model. Contributors
and researchers record samples under different conditions, so some voices
might have issues irrespective of these quality levels like background
noise and distortion.

Piper TTS status
----------------

If you open the office application in Linux using a command window, then
the window will display the current status.

* Language:  `en`
* Model:  `en_GB-vctk-medium`
* Requested Language:  `en-CA`
* Requested Model:  `en_GB-vctk-medium#p316`
* Speaker #: `47`
* Speaker Name: `p316`
* Speaker Count:  `109`
* Speech Rate:  `160`

Links
-----

* [About Piper TTS](https://github.com/rhasspy/piper)
* [Piper samples](https://rhasspy.github.io/piper-samples/)
* [Piper Voices](https://huggingface.co/rhasspy/piper-voices/tree/main)
* [Thorsten Müller - Piper Voice Training](https://www.youtube.com/watch?v=b_we_jma220)
    """
        return self.instructions


def main():  # -> NoReturn
    """Use Piper TTS speech synthesis for supported languages."""
    _piper_tts = PiperTTSClass()
    if not sys.version_info >= (3, 6) or not os.name in ["posix"]:
        print("Your system does not support the piper python tool.")
        _piper_tts.usage()
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
        _piper_tts.usage()
        sys.exit(0)
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "hclrv", ["help", "config", "language=", "rate=", "voice="]
        )
    except getopt.GetoptError:
        # print help information and exit
        print("option -a not recognized")
        _piper_tts.usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            _piper_tts.usage()
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
        _dir = os.path.expanduser("~/.local/share/piper-tts/piper-voices/")
        _data = ""
        if not os.path.isdir(_dir):
            os.makedirs(_dir)
            try:
                _piper_tts.common.set_urllib_timeout(4)
                response = urllib.request.urlopen(_piper_tts.json_url)
                _data = response.read().decode("utf-8")
            except TimeoutError:
                pass
            if len(_data) != 0:
                readtexttools.write_plain_text_file(
                    f"{_dir}voices.json", _data, "utf-8"
                )
            readtexttools.write_plain_text_file(
                f"{_dir}README.md", _piper_tts.load_instructions(True), "utf-8"
            )
            readtexttools.show_with_app(_dir)
        _piper_tts.usage(_piper_tts.get_quickstart_info())
        sys.exit(0)
    # WPM = Approximate Words per minute if in English or a similar idiom'
    find_replace_phonemes.fix_up_text_file(
        _text_file_in, "", _iso_lang, _piper_tts.local_dir, "PIPER_USER_DIRECTORY"
    )
    _piper_tts.read(
        _text_file_in, _iso_lang, _config, netcommon.speech_wpm(_percent_rate)
    )
    if _piper_tts.debug != 0:
        print(_piper_tts.load_instructions(True))
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
# This piper client does not automatically download voice models(`onnx`)
# or piper model configuration files (`json`). It does download a document
# enumerating the currently available voice models (`voices.json`).
#
# Copyright (c) 2023 James Holgate
