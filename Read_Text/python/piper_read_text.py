#!/usr/bin/env python3
"""Piper TTS is a fast neural text to speech tool."""
APP_DESCRIPTION = r"""
Piper TTS
=========

This client reads a text file aloud using `piper-tts`.

Piper TTS is a fast, private local neural text to speech engine.
Users can create or refine voice models based on a recording of
a voice.

This client uses the piper engine to read text aloud using Read
Text Extension with your office program.

* [Piper samples](https://rhasspy.github.io/piper-samples)
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

Install piper-tts
=================

If you are not online, then you cannot download voice models or configuration
files. Once they are installed, piper handles speech locally.

Binary release (Linux)
----------------------

The binary release is available for several platforms and it is fast.

The most recent binary `piper` executable program included in a 
[piper archive](https://github.com/rhasspy/piper/releases/latest) for your
computer's specific processor type. For example, `piper_linux_x86_64.tar.gz`
works with `x86_64` processors using a Linux desktop.

For example, for the `piper_linux_x86_64` 2023.11.14-2 Linux release, install the following packages:

    python3-pipx
    espeak-ng-data

Use the following commands:

    python3 -c "import os;os.makedirs(os.path.expanduser('~/.local/share/piper-tts/'))"
    python3 -c "from urllib import request;import os;request.urlretrieve(\
        'https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz',\
        os.path.expanduser(\
            '~/piper_linux_x86_64.tar.gz'))"
    tar -xf ~/piper_linux_x86_64 -C ~/.local/share/piper-tts/
    ln -s -T ~/.local/share/piper-tts/piper/piper ~/.local/bin/piper-cli
    pipx ensurepath
    ~/.local/bin/piper-cli --version

Python release (Linux)
----------------------

The python pipx package has higher latency, but the `piper` script simplifies
automating downloading the required `onnx` data and `json` configuration
files. Some Linux platforms use python versions that are incompatible or only
partially compatible with the pipx stable release of `piper-tts`.

Install the following packages:

    python3-pipx
    espeak-ng-data

Then use pipx to install `piper-tts`

    pipx update-all
    pipx install piper-tts
    pipx ensurepath
    piper -h

Audition and download a voice model
-----------------------------------

You can check the voice models online.

Review the [voice model samples](https://rhasspy.github.io/piper-samples).

The first time you use this client, it will set up a directory to store
piper voice models (`onnx`) and configuration files (`json`). 

`~/.local/share/piper-tts/piper-voices`

You can download the voice and configuration files for various languages
and regions following the link on the piper-samples web page.

Automatic Download
------------------

Open the extension main dialog with *Tools  -> Add-ons  -> Read Text...*.
Choose or enter a command line menu item that includes the name of a
valid model and the string `--update True`. For example for the standard
American English (en-US) `lessac` voice model you could use:

    "(PIPER_READ_TEXT_PY)" --update True --voice en_US-lessac-medium "(TMP)"

If you are a developer, you can place your locally developed model directly
in the `~/.local/share/piper-tts/piper-voices` directory. The extension
synchronizes the `voices.json` file each time you automatically download
piper resources, so the extension would not be able to find your local
voice model if you dropped it into a subdirectory that you created manually.

Manual Download
---------------

Move the `onnx` and `json` files to the local `piper-voices` directory.

Read the `README` file in the directory for more information about using voice
models for other languages and regions.

System-wide installation (Linux)
--------------------------------

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
import stat
import sys
import getopt
import urllib

import find_replace_phonemes
import netcommon
import readtexttools

VLC_WINDOWS_INFO = """
# VLC

> VLC is a free and open source cross-platform multimedia player and framework
> that plays most multimedia files as well as DVDs, Audio CDs, VCDs, and
> various streaming protocols.

-- [VLC: Official site]((https://www.videolan.org))

    ██████████████████████████████████████████████████████████████████
    ██████████████████████████████████████████████████████████████████
    ██████████████████████████████████████████████████████████████████
    ██████████████████████████████████████████████████████████████████
    ████████              ██        ████  ██████              ████████
    ████████  ██████████  ████████      ████  ██  ██████████  ████████
    ████████  ██      ██  ████  ██  ██  ████████  ██      ██  ████████
    ████████  ██      ██  ██████    ██  ██    ██  ██      ██  ████████
    ████████  ██      ██  ██████      ██  ██  ██  ██      ██  ████████
    ████████  ██████████  ████  ██  ████████████  ██████████  ████████
    ████████              ██  ██  ██  ██  ██  ██              ████████
    ████████████████████████    ████    ████  ████████████████████████
    ████████    ██    ██  ████  ████  ██      ██  ██████████  ████████
    ████████████        ████████  ████      ██  ██          ██████████
    ████████████████      ████  ████    ██  ████    ██  ████  ████████
    ████████      ████  ████  ████████████████████  ██        ████████
    ████████  ████  ████  ████    ██████      ██  ██████████  ████████
    ████████      ██  ████  ████  ██  ██        ████  ████  ██████████
    ████████    ██████    ████  ████████    ██    ██          ████████
    ████████  ████  ████████    ████  ██  ██    ██  ██    ██  ████████
    ████████  ██  ████    ████          ████          ██    ██████████
    ████████████████████████  ████  ██  ████  ██████  ██    ██████████
    ████████              ████  ████  ██████  ██  ██  ██████  ████████
    ████████  ██████████  ████      ██  ██    ██████  ██████  ████████
    ████████  ██      ██  ██    ██    ██              ████████████████
    ████████  ██      ██  ██  ██  ██  ██████████  ████████    ████████
    ████████  ██      ██  ████      ██    ████  ████          ████████
    ████████  ██████████  ██  ██  ████████  ██████    ██      ████████
    ████████              ██  ██      ██████    ██████  ████  ████████
    ██████████████████████████████████████████████████████████████████
    ██████████████████████████████████████████████████████████████████
    ██████████████████████████████████████████████████████████████████
    ██████████████████████████████████████████████████████████████████

If you are using PiperTTS on Windows without installing VLC , it can
take a few few moments before your computer starts playing Piper speech.

To enable fast and free audio streaming for Windows Piper TTS, use
VideoLAN [VLC Media Player Desktop](https://www.videolan.org)"""


class PiperTTSClass(object):
    """Piper TTS class"""

    def __init__(self) -> None:
        """Initialize data."""
        _common = netcommon.LocalCommons()
        self.default_lang = _common.default_lang
        self.concise_lang = self.default_lang.split("_")[0]
        self.tested_model = ""
        self.untested_model = ""
        self.tested_phrase = ""
        self.update_request = False
        self.sample_model = "en_GB-jenny_dioco-medium"
        self.sample_phrase = "A rainbow is a meteorological phenomenon."
        # Is huggingface.co blocked in your region? Add a tested
        # model and sample phrase here so you don't need to go online.
        self.pip_checked_models = [
            [self.sample_model, self.sample_phrase],
            [
                "de_DE-thorsten-medium",
                "Der Regenbogen ist ein atmosphärisch-optisches Phänomen.",
            ],
            ["en_US-lessac-medium", self.sample_phrase],
            ["es_ES-sharvard-medium", "Un arco iris es un fenómeno óptico."],
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
        # Try to use a complete path for a local installation because the
        # local user might not have added the piper path to their `PATH`
        # environment.
        app_list = ["piper-cli", "piper"]
        if os.name in ["nt"]:
            self.app = "piper.exe"
            _extension_table = readtexttools.ExtensionTable()
            for _item in app_list:
                _app = _extension_table.win_search("piper-tts\\piper", _item)
                if len(_app) != 0:
                    self.app = _app
                    break
        else:
            _app_path = ""
            for _app in app_list:
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
        self.hug_url = "https://huggingface.co/rhasspy/piper-voices"
        self.voice_url = f"{self.hug_url}/tree/main"
        self.json_url = f"{self.hug_url}/raw/main/voices.json"
        self.local_dir = "default"
        self.default_speaker = 0  # All models have at least one voice.
        self.voice = self.default_speaker
        self.app_locker = readtexttools.get_my_lock(self.locker)
        self.default_extension = _common.default_extension
        self.voice_name = ""
        self.lang = ""
        self.model = ""
        self.piper_voice_dir = ""
        self.app_data = ".local"
        piper_voices_list = [
            f"~/{self.app_data}/share/piper-tts/piper-voices",
            f"~/{self.app_data}/share/piper/piper-voices",
            f"~/{self.app_data}/share/piper-voices",
            "~/piper-voices",
            "/opt/piper-voices",
            "/opt/piper-tts/piper-voices",
            readtexttools.linux_machine_dir_path("piper-voices"),
            readtexttools.linux_machine_dir_path("piper-tts/piper-voices"),
        ]
        espeak_ng_data_list = [
            self.app.replace("piper", "espeak-ng-data"),
            f"~/{self.app_data}/share/piper-tts/piper/espeak-ng-data",
            f"~/{self.app_data}/share/piper-tts/espeak-ng-data",
            f"~/{self.app_data}/share/piper/espeak-ng-data",
            "~/espeak-ng-data",
            "~/Downloads/espeak-ng-data",
            "/opt/piper-tts/piper-tts/piper/espeak-ng-data",
            readtexttools.linux_machine_dir_path("piper-tts/piper/espeak-ng-data"),
            readtexttools.linux_machine_dir_path("espeak-ng-data"),
        ]
        if os.name == "nt":
            self.app_data = "AppData\\Roaming"
            _prog_search = os.path.split(self.app)[0]
            piper_voices_list = [
                f"~\\{self.app_data}\\share\\piper-tts\\piper-voices",
                f"~\\{self.app_data}\\piper-tts\\piper-voices",
                f"~\\{self.app_data}\\piper\\piper-voices",
                f"~\\{self.app_data}\\piper-voices",
                "~\\AppData\\Local\\Programs\\piper-tts\\piper-voices",
                "~\\AppData\\Local\\Programs\\piper\\piper-voices",
                "~\\.local\\share\\piper-tts\\piper-voices",
                f"{_prog_search}\\piper-voices",
            ]
            espeak_ng_data_list = [
                self.app.replace("piper.exe", "espeak-ng-data"),
                f"~\\{self.app_data}\\piper-tts\\piper\\espeak-ng-data",
                f"~\\{self.app_data}\\piper\\espeak-ng-data",
                f"~\\{self.app_data}\\espeak-ng\\espeak-ng-data",
                "~\\.local\\share\\piper-tts\\piper\\espeak-ng-data",
                "~\\AppData\\Local\\Programs\\piper\\espeak-ng-data",
                "~\\AppData\\Local\\Programs\\piper-tts\\piper\\espeak-ng-data",
                "~\\AppData\\Local\\Programs\\espeak-ng\\espeak-ng-data",
                f"{_prog_search}\\espeak-ng-data",
            ]
        for _piper_dir in piper_voices_list:
            if os.path.isdir(os.path.expanduser(_piper_dir)):
                self.piper_voice_dir = os.path.expanduser(_piper_dir)
                break
        self.espeak_ng_dir = ""
        for espeak_ng_dir in espeak_ng_data_list:
            if os.path.isdir(os.path.expanduser(espeak_ng_dir)):
                self.espeak_ng_dir = os.path.expanduser(espeak_ng_dir)
                break
        if len(self.espeak_ng_dir) == 0:
            espeak_msg = os.path.expanduser(espeak_ng_data_list[0])
            print(
                f"""
Note
====
                  
The Piper speech client can't find a required resource.

No `espeak-ng-data` directory found at `{espeak_msg}`
"""
            )
        self.j_key = ""
        self.j_key_list = []
        self.j_lang = ""
        self.j_concise_lang = ""
        self.j_model = ""
        self.j_quality = ""
        self.j_path = ""
        self.sample_webpage = "https://rhasspy.github.io/piper-samples"
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
        self.work_file = os.path.join(readtexttools.get_temp_prefix(), "piper-tts.wav")

    def usage(self, _help="") -> None:
        """Usage"""
        cmd = "python3 piper_read_text.py"
        _file = "'<text_path.txt>'"
        if len(_help) != 0:
            cmd = '"(PIPER_READ_TEXT_PY)"'
            _file = '"(TMP)"'
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

    {cmd} --language fr-FR {cmd_break}
        --voice de_DE-thorsten_emotional-medium#amused {_file}

You can use a piper `onnx` and `json` model package in a local 
user directory that you specify:

    {cmd} --voice='</path/to/myvoice.onnx>#4' {_file}

To update the configuration data to include the current list of
online voice models and configuration files, use:

    {cmd} --update True --language en-GB --rate 100% {_file}

The `voices.json` file for piper contains no gender information, so
the application will use the same voice index for 'auto', 'child', female'
and 'male'.

* [Piper samples]({self.sample_webpage})
* [Instructions]({self.help_url})
* [Download voices]({self.hug_url}/tree/main/)

{APP_DESCRIPTION}
"""
        )

    def get_pip_test_text(self) -> str:
        """Set `self.quick_start` and return the string."""
        _use_phrase = self.sample_phrase
        if len(self.tested_phrase) != 0:
            _use_phrase = self.tested_phrase
        _use_model = self.sample_model
        if len(self.tested_model) != 0:
            _use_model = self.tested_model
        self.quick_start = f"""
If you have installed the `piper-tts` library, you can use the
following commands to install specific voice models.

    sudo apt-get install espeak-ng-data
    cd ~/.local/share/piper-tts/piper-voices
    echo '{_use_phrase}' | \\
        ~/.local/bin/piper --model {_use_model} \\
        --output-raw | \\
        aplay -r 22050 -f S16_LE -t raw -

The features of the python version of `piper` can vary depending on the
version of python and the libraries that are supplied by your distribution.
Therefore, some models that work with the binary version of `piper` might
not work with the python version.
"""
        return self.quick_start

    def language_supported(self, iso_lang="en-GB", vox="auto") -> bool:
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
        _dir_list = os.listdir(self.piper_voice_dir)
        self.ok = False
        if self.concise_lang in _dir_list:
            if any(
                self.concise_lang.startswith(_ignore) for _ignore in ["_script", "~"]
            ):
                return self.ok
        self.ok = any(_file.startswith(self.concise_lang) for _file in _dir_list)
        return self.ok

    def _model_path_list(self, iso_lang="en-GB", _vox="", extension="onnx") -> list:
        """Check the directories for language models, and if found return
        the results in a list.
        """
        # NOTE: We use data that we can determine using the model key, so
        # we don't know whether a particular model is compatible with the
        # current version of piper, or whether the files' checksums match.
        _json_file = os.path.join(self.piper_voice_dir, "voices.json")
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
            except (TimeoutError, ValueError):
                self.ok = False
                return _found_models
            except urllib.error.URLError:
                readtexttools.unlock_my_lock(self.locker)
                readtexttools.pop_message(
                    self.help_heading, _json_file, 8000, self.help_icon
                )
                self.ok = False
                sys.exit(0)
        for _description in [
            iso_lang.replace("-", "_"),
            iso_lang.split("_")[0].split("-")[0],
        ]:
            try:
                for _item in data:
                    # de_DE-thorsten_emotional-medium
                    self.j_key = data[_item]["key"]
                    self.j_key_list.append(self.j_key)
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
                                            self.sample_webpage,
                                            self.j_concise_lang,
                                            self.j_lang,
                                            self.j_model,
                                            self.j_quality,
                                            "sample.txt",
                                        ]
                                    )
                                # We need to confirm that items are not
                                # onnx placeholders that only contain
                                # brief ASCII text.
                                if os.path.isfile(self.j_path):
                                    if os.path.getsize(self.j_path) > 1000:
                                        _found_models.append(self.j_path)
            except IndexError:
                pass
        return _found_models

    def model_path(self, _extension="onnx") -> str:
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
INFO: Piper TTS cannot find `{self.lang}` `.json` and `.onnx` files.
<{self.piper_voice_dir}/voices.json>

[Get piper-voices]({self.hug_url}/tree/main)"""
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

    def _model_voice_info(self, _model="") -> int:
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

    def _check_voice_request(self, _vox_number=0, _list_size=0) -> str:
        """Handle out of range numbers using a modulus (`int % _list_size`)
        value."""
        try:
            if _list_size == 0:
                return 0
            if _vox_number >= _list_size - 1:
                return _vox_number
            return _vox_number % abs(_list_size)
        except (ZeroDivisionError, IndexError, TypeError):
            pass
        return 0

    def _use_espeak_data_dir(self) -> bool:
        """If the application publishes a major version higher than `0`
        or is an executable binary return `True` otherwise return `False`"""
        if len(self.espeak_ng_dir) == 0:
            return False
        real_app = ""
        if os.sep in self.app:
            real_app = os.path.realpath(self.app)
            if os.name == "posix":
                for watermark in ["ELF", "64-bit executable"]:
                    if watermark in self.meta.execute_command(f"file {real_app}"):
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

    def retrieve_model(
        self, speaker="en_GB-jenny_dioco-medium", home="", do_pop_message=True
    ) -> str:
        """Download remote voice onnx and json model files. Returns the directory
        containing the onnx and json file if successful, or else `""`."""
        if len(speaker) == 0:
            speaker = "en_GB-jenny_dioco-medium"
        if len(home) == 0:
            home = f"{self.hug_url}/resolve/main/"
        try:
            speaker = speaker.split(".", maxsplit=1)[0]
            lang_locale, name, quality = speaker.split("-")
        except ValueError:
            name = "jenny_dioco"
            quality = "medium"
            lang_locale = "en_GB"
        lang = lang_locale.split("_", maxsplit=1)[0]
        piper_file = ""
        _count = 1
        _extensions = ["onnx.json", "onnx"]
        s_count_total = str(len(_extensions))
        for _end in _extensions:
            try:
                piper_file = f"{lang_locale}-{name}-{quality}.{_end}"
                home_file = os.path.join(
                    self.piper_voice_dir, lang, lang_locale, name, quality, piper_file
                )
                if os.path.isfile(home_file):
                    continue
                print(f"Requesting `{piper_file}`")
                urllib.request.urlretrieve(
                    f"{home}{lang}/{lang_locale}/{name}/{quality}/{piper_file}?download=true",
                    home_file,
                )
                print(f"Retrieved `{piper_file}`")
                if do_pop_message:
                    s_count = str(_count)
                    _dots = _count * "…"
                    readtexttools.pop_message(
                        self.help_heading,
                        f"""🌐 huggingface.co ⇒ 💻 : Piper `{piper_file}`
({s_count}/{s_count_total}) {_dots}""",
                        16000,
                        self.help_icon,
                    )
                _count += 1
            except (TimeoutError, ValueError, urllib.error.URLError):
                return ""
            except OSError as e:
                print(f"OSError downloading `{piper_file}`: {e}")
                return ""
        return os.path.split(home_file)[0]

    def read(
        self, _text_file="", _iso_lang="en-GB", _config="", _speech_rate=160
    ) -> bool:
        """Read speech aloud"""
        _extension_table = readtexttools.ExtensionTable()
        _length_scale = self.length_scale  # Fallback rate
        if _speech_rate != 160:
            _length_scale = self.common.rate_to_rhasspy_length_scale(_speech_rate)[0]
        if not self.ok:
            return False
        _espeak_data = _extension_table.add_quotes_if_needed(self.espeak_ng_dir)
        if not os.path.isdir(self.piper_voice_dir):
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
        _outer = f" --output-raw < {_text_file} | aplay -r {self.sample_rate} -f S16_LE -t raw -"
        _vlc = ""
        _demo_warning = ""
        if os.name == "nt":
            _vlc = _extension_table.win_search("vlc", "vlc")
            if len(_vlc) == 0:
                _demo_warning = """
        @
       / \\
      /@@@\\
     /     \\    <https://videolan.org>
    /@@@@@@@\\
   /         \\
 @@@@@@@@@@@@@@@\\
 
On the Windows NT platform, this client needs VideoLAN VLC Media Player to
stream Piper TTS text. By using Piper's ability to stream audio to a media
player directly without saving a file to your computer's storage, it can
read text quickly and securely with large or small selections of text."""
                _work_file = _extension_table.add_quotes_if_needed(
                    self.work_file.replace(".txt", ".json")
                )
                _outer = f""" --output_file {_work_file} """
            else:
                # To hide the interface, use the `--intf dummy` switch
                _ui = ["--intf dummy ", ""][1]
                _outer = f""" --output-raw < {_text_file} | {_vlc} {_ui}--demux=rawaud --rawaud-channels 1 --rawaud-samplerate 22050 - vlc://quit"""

        if os.path.isfile(self.app_locker):
            readtexttools.unlock_my_lock(self.locker)
            if len(_vlc) != 0:
                app_list = ["vlc", "piper", "piper-cli"]
            else:
                app_list = ["aplay", "piper", "piper-cli"]
            for _app in app_list:
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
            _espeak_switch = f" --espeak_data {_espeak_data}"
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
        speaker_switch = " "
        if os.path.isfile(self.work_file):
            os.remove(self.work_file)
        if voice_no > self.voice_count - 1:
            voice_no = 0
        if voice_no != 0:
            speaker_switch = "".join([" --speaker ", str(voice_no)])
        if os.path.isfile(_model):
            _json_c = f"{_model}.json"
            if os.path.isfile(_config):
                _json_c = _config
            if len(_vlc) != 0 or os.name != "nt":
                _command = "".join(
                    [
                        f"{self.app}",
                        _cuda,
                        _espeak_switch,
                        " --noise_scale ",
                        str(self.noise_scale),
                        " --noise_w ",
                        str(self.noise_w),
                        " --length_scale ",
                        str(_length_scale),
                        " --model ",
                        _model,
                        " --config ",
                        _json_c,
                        speaker_switch,
                        _outer,
                    ]
                )
            else:
                # Windows PowerShell reports `RedirectionNotSupported``
                _command = "".join(
                    [
                        "cat ",
                        _text_file,
                        f" | {self.app}",
                        _cuda,
                        " --json-input ",
                        _espeak_switch,
                        " --noise_scale ",
                        str(self.noise_scale),
                        " --noise_w ",
                        str(self.noise_w),
                        " --length_scale ",
                        str(_length_scale),
                        " --model ",
                        _model,
                        " --config ",
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
{_demo_warning}\

"""
                )
            else:
                print(self.j_key_list)
                print(_command)
            if os.name in ["posix"]:
                _response = os.system(_command)
            elif os.name in ["nt"]:
                if len(_vlc) != 0:
                    _response = os.system(_command)
                else:
                    _json_tools = readtexttools.JsonTools()
                    _meta = readtexttools.ImportedMetaData()
                    _content = _meta.meta_from_file(
                        _text_file, True, "backslashreplace"
                    )
                    _content = _json_tools.sanitize_json(_content)
                    _lcc = "{"
                    _rcc = "}"
                    readtexttools.write_plain_text_file(
                        _text_file, f""" {_lcc} "text": "{_content}" {_rcc} """, "utf-8"
                    )

                    _response = readtexttools.run_powershell(_command.replace('"', "'"))
                    # Closing the PowerShell window stops the speech. The program
                    # waits for a response to keep the window from closing before
                    # the speech output ends.
                    print(_response)
                    if os.path.isfile(self.work_file):
                        print(VLC_WINDOWS_INFO)
                        if os.path.getsize(self.work_file) == 0:
                            return False
                        readtexttools.process_wav_media(
                            "untitled",
                            self.work_file,
                            "",
                            "",
                            "true",
                            "false",
                            "",
                            "600x600",
                        )
            else:
                _response = 1
            readtexttools.unlock_my_lock(self.locker)
            return _response == 0
        return False

    def update_local_model_dir(
        self, _dir="", _voice="", _sub_dirs=True, do_pop_message=True
    ) -> bool:
        """Download the most recent `voices.json` file, and if `_sub_dirs` is
        `True` then add new model subdirectories to the local model
        directory."""
        if not os.path.isdir(_dir):
            if len(dir) == 0:
                return False
            os.makedirs(_dir)
        try:
            self.common.set_urllib_timeout(4)
            response = urllib.request.urlopen(self.json_url)
            data_response = response.read()
            _content = data_response.decode("utf-8")
        except (TimeoutError, ValueError):
            pass
        except urllib.error.URLError:
            readtexttools.unlock_my_lock(self.locker)
            return False
        except OSError as e:
            print(f"OSError downloading `{self.json_url}`: {e}")
        piper_file = ""
        if len(_content) != 0:
            readtexttools.write_plain_text_file(f"{_dir}voices.json", _content, "utf-8")
        readtexttools.write_plain_text_file(
            f"{_dir}README.md", self.load_instructions(True), "utf-8"
        )
        if _sub_dirs:
            data = json.loads(data_response)
            try:
                for _item in data:
                    new_dir = os.path.join(
                        _dir,
                        data[_item]["language"]["family"],
                        data[_item]["language"]["code"],
                        data[_item]["name"],
                        data[_item]["quality"],
                    )
                    if not os.path.isdir(new_dir):
                        print(f"Create directory <{new_dir}>")
                        os.makedirs(new_dir)
                    test_voice = "-".join(
                        [
                            data[_item]["language"]["code"],
                            data[_item]["name"],
                            data[_item]["quality"],
                        ]
                    )
                    if _voice.split("#", maxsplit=1)[0] == test_voice:
                        piper_file = test_voice
                    if self.update_request and len(test_voice) == 0:
                        if self.concise_lang == data[_item]["language"]["family"]:
                            _uri = f"{self.voice_url}/{self.concise_lang}"
                            # NOTE: On free desktop compatible installations
                            # a pop up menu appears with a link to a directory
                            # to download voice resources. Sandboxed releases
                            # of the office suite might not be able to display
                            # system pop ups or download resources from the
                            # Internet.
                            if do_pop_message:
                                readtexttools.pop_message(
                                    self.help_heading, _uri, 8000, self.help_icon
                                )
                            readtexttools.show_with_app(_dir)
                            self.update_request = False
            except IndexError:
                pass
            if not os.path.isdir(os.path.join(_dir, "_scripts")):
                os.makedirs(os.path.join(_dir, "_scripts"))
            for _script in ["voice_names.sh", "voicefest.py"]:
                _script_url = f"{self.hug_url}/raw/main/_script/{_script}"
                _script_path = os.path.join(_dir, "_scripts", _script)
                if not os.path.isfile(_script_path):
                    try:
                        self.common.set_urllib_timeout(4)
                        response = urllib.request.urlopen(_script_url)
                        data_response = response.read()
                        _content = data_response.decode("utf-8")
                        readtexttools.write_plain_text_file(
                            _script_path, _content, "utf-8"
                        )
                        try:
                            os.chmod(_script_path, stat.S_IRWXG)
                        except (FileNotFoundError, PermissionError):
                            pass
                    except (TimeoutError, ValueError, urllib.error.URLError):
                        pass
                    except OSError as e:
                        print(f"OSError downloading `{_script_path}`: {e}")
            print(
                f"""Please wait
===========

It takes a few moments to retrieve the piper voice model
`{piper_file}` from <{self.hug_url}> """
            )
            _dir = self.retrieve_model(piper_file, "", do_pop_message)
            if len(_dir) != 0:
                readtexttools.show_with_app(_dir)
        return os.path.isfile(f"{_dir}voices.json")

    def load_instructions(self, verbose=True) -> str:
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
                except (TimeoutError, ValueError, urllib.error.URLError):
                    pass
                except OSError as e:
                    print(f"OSError downloading `{self.sample_uri}`: {e}")
                if len(self.tested_phrase) == 0:
                    self.tested_phrase = self.sample_phrase
            _quick_start = self.get_pip_test_text()
        self.instructions = f"""
Summary
=======

* Install the piper application
* Download the current `voices.json` configuration file
* Download voice `onnx` and `json` files for the model or models
  that you need and place them in the appropriate directory.

{APP_DESCRIPTION}

Details
=======

python-pipx
-----------

To [install]({self.help_url}#running-in-python) `piper-tts`
using `pipx`, you need the `python3-pipx` and the `espeak-ng-data` packages.

    pipx upgrade-all
    pipx install piper-tts
    pipx ensurepath
    piper -h

Some platforms might show an error when attempting to use the library because
they use an incompatible version of one or more of python's support libraries
or the system architecture is incompatible with `piper-tts`. In this case, a
binary package compatible with your computer's architecture might work.

Currently, the python library version of the piper command line interface
displays no information about the audio stream.
{_quick_start}
Binary package
--------------

The python binary supports Debian stable (x86-64), Fedora Workstation
(x86-64) and Ubuntu LTS (x86-64). If you use the binary package, you
must include the path to `piper` in your `PATH` environment or create a
symbolic link to the program path in a directory that is included in your
`PATH` environment.

Download the [piper archive]({self.help_url}/releases/latest)
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

Create a settings directory manually
------------------------------------

If you are using a version of the office suite with restricted permissions or
a different version of python than the system python, automated installation
of voice model and configuration files might fail.

This client looks for voices in several directories. To create a directory in
the recommended location, enter:

    mkdir -p "~/{self.app_data}/share/piper-tts/piper-voices"
    cd "~/{self.app_data}/share/piper-tts/piper-voices"

Download the `voices.json` configuration file and place it in the root of this
new directory.

    wget -O "~/{self.app_data}/share/piper-tts/piper-voices/voices.json" \\
        {self.hug_url}/raw/main/voices.json

Within the new `piper-voices` directory, you can add valid `onnx` and `json`
files from your provider or the official piper-tts voices
[repository]({self.hug_url}). The
[`voices.json`]({self.hug_url}/raw/main/voices.json)
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

<{self.hug_url}/resolve/main/fr/fr_FR/siwis/low/fr_FR-siwis-low.onnx>

The `fr_FR-siwis-low.onnx.json` configuration is located on the server at:

<{self.hug_url}/resolve/main/fr/fr_FR/siwis/low/fr_FR-siwis-low.onnx.json>

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
parameters, you can regenerate the local `voices.json` file with a python
[script]({self.hug_url}/tree/main/_script)
included on the huggingface website.

    python3 '($HOME)/.local/share/piper-tts/piper-voices/_script/voicefest.py'

Piper voices have a trade-off between latency and quality. Piper supports
four quality levels:

* `x_low` - 16Khz audio, 5-7M params
* `low` - 16Khz audio, 15-20M params
* `medium` - 22.05Khz audio, 15-20M params
* `high` - 22.05Khz audio, 28-32M params

Some models contain multiple speakers. The quality of one of the speakers
could be worse than it would be using a single speaker model. Contributors
and researchers record samples under different conditions, so some voices
might have issues like background noise and distortion irrespective of the
stated quality level.

Git clone
---------

Git is a developer tool to manage computer projects.

### Advantages

* Using Git as an alternative method to set up a developer release directory
  structure will include all sample voice `mp3` files, `json` configuration
  files, notes, utility scripts, and placeholders for `onnx` file data.
* Using this developer version facilitates updating the local `voices.json`
  file so that you can use this piper client with third party.
  voice models and configuration files like ones that you create yourself.
* The git program can help you track changes and undo mistakes in text files.

### Disadvantages

* It will not work as-is because the placeholders are not actual `onnx`
  data files.
* Modifying the git clone might cause problems if you try to push it or
  synchronize it to a public repository.

### Method

    cd "~/{self.app_data}/share/piper-tts/piper-voices"
    git clone {self.hug_url}

This method of replicating the developer configuraton setup includes plain
text placeholders for the `onnx` binary files that work with piper-tts. You
can activate a voice model by replacing the text placeholder with local 
symbolic links to local binary onnx files downloaded from the huggingface.co
web site.

#### Placeholder

The placeholder is a text file that contains the version, verification
checksum and size of the `onnx` file.
{self.hug_url}/raw/main/en/en_GB/vctk/medium/en_GB-vctk-medium.onnx

#### Actual file:

The linked file is a binary file that piper-tts can use to generate speech.
{self.hug_url}/resolve/main/en/en_GB/vctk/medium/en_GB-vctk-medium.onnx

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

* [About Piper TTS]({self.help_url})
* [Piper Samples]({self.sample_webpage})
* [Piper Voices]({self.hug_url}/tree/main)
* [Thorsten Müller - Piper Voice Training](https://www.youtube.com/watch?v=b_we_jma220)
    """
        return self.instructions


def main() -> None:
    """Use Piper TTS speech synthesis for supported languages."""
    _piper_tts = PiperTTSClass()
    _dir = _piper_tts.piper_voice_dir
    _dir_list = [_dir, _piper_tts.piper_voice_dir]
    if not sys.version_info >= (3, 6) or not os.name in ["nt", "posix"]:
        print("Your system does not support the piper python tool.")
        _piper_tts.usage()
        sys.exit(0)
    _percent_rate = "100%"
    _iso_lang = ""
    _config = ""  # model json path (defaults to onnx path + .json suffix)
    _voice = "AUTO0#0"
    _text_file_in = sys.argv[-1]
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "uclrvh",
            ["update=", "config=", "language=", "rate=", "voice=", "help"],
        )
    except getopt.GetoptError:
        # print help information and exit
        print("option -a not recognized")
        _piper_tts.usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-u, --update"):
            if readtexttools.lax_bool(a):
                readtexttools.pop_message(
                    _piper_tts.help_heading,
                    _piper_tts.sample_webpage,
                    8000,
                    _piper_tts.help_icon,
                )
                # `True`, `Yes`, `1`, `-1`
                try:
                    _piper_tts.common.set_urllib_timeout(4)
                    response = urllib.request.urlopen(_piper_tts.json_url)
                    if os.path.isfile(f"{_dir}voices.json"):
                        os.remove(f"{_dir}voices.json")
                        _dir_list = [_dir]
                    _piper_tts.update_request = True
                except (TimeoutError, ValueError, urllib.error.URLError):
                    pass
                except OSError as e:
                    print(f"OSError downloading `{_dir}voices.json`: {e}")
                except Exception:
                    print(f"Error resolving `{_piper_tts.json_url}`")
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
        elif o in ("-h", "--help"):
            _piper_tts.usage()
            sys.exit(0)
        else:
            assert False, "unhandled option"
    use_dir = ""
    if len(_iso_lang) == 0:
        if "_" in _voice and len(_voice.split("-")) == 3:
            _iso_lang = _voice.split("-", maxsplit=1)[0].replace("_", "-")
        else:
            _iso_lang = "en-US"
    for _a_dir in _dir_list:
        if os.path.isfile(os.path.join(_a_dir, "voices.json")):
            use_dir = _a_dir
            break
    if len(use_dir) == 0 or _piper_tts.update_request:
        _piper_tts.update_local_model_dir(use_dir, _voice, True, True)
    if not _piper_tts.language_supported(_iso_lang, _voice):
        if not _piper_tts.update_request:
            sys.exit(0)
    if _text_file_in.startswith("~"):
        _text_file_in = os.path.expanduser(_text_file_in)
    if not os.path.isfile(_text_file_in):
        sys.exit(0)
    if sys.argv[-1] == sys.argv[0]:
        _piper_tts.usage()
        sys.exit(0)
    find_replace_phonemes.fix_up_text_file(
        _text_file_in,
        "",
        _iso_lang,
        _piper_tts.local_dir,
        "PIPER_USER_DIRECTORY",
        False,
    )
    _piper_tts.read(
        _text_file_in, _iso_lang, _config, netcommon.speech_wpm(_percent_rate)
    )
    if _piper_tts.debug != 0:
        print(_piper_tts.load_instructions(True))
    sys.exit(0)


if __name__ == "__main__":
    main()

# NOTE: This python code is a client of Piper. Piper supports many voice
# models from different sources. The quality and quantity of voice samples
# on which they are based can vary.
#
# With an untested model check if neural voice quality degrades or the voice
# starts "babbling" random sounds with long strings. Check short code-like
# strings like '`eye`, `bye`, `no`, `No`, `null`, `nil`, `None`, `don't` and
# `False`.
#
# Copyright (c) 2023 James Holgate
