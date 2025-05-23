﻿#!/usr/bin/env python3
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

Update the Piper TTS model folder and find local voice models.

    "(PIPER_READ_TEXT_PY)" --update "True" --language (SELECTION_LANGUAGE_CODE) "(TMP)"

Use the first available voice.

    "(PIPER_READ_TEXT_PY)" --language (SELECTION_LANGUAGE_CODE) "(TMP)"

Use a particular model (`auto5`) and speaker (`45`):

    "(PIPER_READ_TEXT_PY)" --voice auto5#45 --rate 75% --language (SELECTION_LANGUAGE_CODE) "(TMP)"

Install piper-tts
=================

If you are not online, then you cannot download voice models or
configuration files. Once they are installed, piper handles speech locally.

Pied (Linux)
------------

[Pied](https://pied.mikeasoft.com/) uses a simple graphical interface to
install and manage text-to-speech Piper voices for use with Linux Speech
Dispatcher on supported architectures and distributions.

### Update System Resources

Make sure that you have a version of the Read Text Extension published
later than September 3, 2024. You can find the most recently published
site from your office application's extension download site. 

### FlatPak preparation

[Flatpak](https://flatpak-docs.readthedocs.io/en/latest/) is an application
distribution tool system  where the system can isolate program resources that
are not deemed necessary. In the case of the LibreOffice Flatpak, the system
blocks access to the system `speechd` speech synthesis daemon.

LibreOffice can use Piper in place of `speechd` if you install the `ffmpeg`
package to make Piper streamed speech playback possible. Some versions of Linux
require enabling a `contributor` or `non-free` repository to install `ffmpeg`,
but Ubuntu and Mint both include the required repository unless you disable it.

Check that you have a recent version of [ffmpeg](https://ffmpeg.org/) and
[Flatpak](https://flatpak-docs.readthedocs.io/en/latest/). If you use
a Mint or Ubuntu compatible distribution you can check this with:

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install --upgrade flatpak
sudo apt-get install --upgrade ffmpeg
```

Check that your system has the most recent version of LibreOffice Flatpak:

```
flatpak list
flatpak search org.libreoffice.LibreOffice
```

If the `flatpak list` command does not include `org.libreoffice.LibreOffice`
in the results then install it.

```
sudo flatpak install org.libreoffice.LibreOffice
```

If the version is not current, then update it.

```
sudo flatpak update org.libreoffice.LibreOffice
```

Your system menu might not update immediately unless you log out then log in
again.

### Pied (Linux)

[Pied](https://pied.mikeasoft.com/) uses a simple graphical interface to install
and manage text-to-speech Piper voices for use with Linux Speech Dispatcher on
supported architectures and distributions.

On many modern Linux desktop distributions, Pied is available directly using the
Flatpak or Snap *Software* store applicaiton. 

### What if the *Software* Application Does Not List Pied?

If your computer supports it, you can find "Pied" in the *Software* application
and install it with the click of a button.

Otherwise, if you are using an Enterprise Linux distribution, you can install
Pied on supported architectures using a series of commands in a `bash` terminal.

1. **Add the Flathub Repository**: Open your terminal and run the following
   command to add the Flathub repository:
    
    ```
    sudo flatpak remote-add --if-not-exists \
        flathub https://flathub.org/repo/flathub.flatpakrepo
    ```
    
2. **Install the Required Runtime**: Install the required runtime by running:
    
    ```
    sudo flatpak install flathub org.freedesktop.Platform//24.08
    ```

3. **Get the Installer**: Download the most recent Pied Flatpak installer from
   the [Pied website](https://pied.mikeasoft.com/).  
   
4. **Install the Application**: Install `com.mikeasoft.pied` using the following
   command:
    
    ```
    sudo flatpak install ~/Downloads/com.mikeasoft.pied.flatpak
    ```

### Can I install Pied locally without using `sudo`?

1. Download the latest Pied archive file from the [Pied Github release
   page](https://github.com/Elleo/pied/releases) (For example, 
   `pied-0.2.1-x86_64.tar.gz`) and extract it into a local directory.
2. Run the `pied` program by double-clicking the `pied` program using 
   the Linux distributions **Files** browser.

Binary release (Linux)
----------------------

The binary release is available for several platforms and it is fast.

The most recent binary `piper` executable program included in a 
[piper archive](https://github.com/rhasspy/piper/releases/latest) for your
computer's specific processor type. For example, `piper_linux_x86_64.tar.gz`
works with `x86_64` processors using a Linux desktop.

For example, for the `piper_linux_x86_64` 2023.11.14-2 Linux release, install
the following packages:

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

Python client (Linux pipx)
--------------------------

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

Python (developer)
------------------

[Github](https://github.com/rhasspy/piper?tab=readme-ov-file#installation)
installation notes have information about installing the full package. As a
developer you can create and edit piper models and run piper as a home network
[web](https://github.com/rhasspy/piper/blob/master/src/python_run/README_http.md)
service.

Audition and download a voice model
-----------------------------------

You can check the voice models online.

Review the [voice model samples](https://rhasspy.github.io/piper-samples).

The first time you use this client, it will set up a directory to store
piper voice models (`onnx`) and configuration files (`json`). For Linux,
it uses:

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

The following command returns the `speech-dispatcher` to the defaults. It
does not erase Piper models or Piper configuration files.

    (RESET)

To reenable Pied, simply open the Pied application, select a voice, then
click *Apply*.

[Read Text Extension](http://sites.google.com/site/readtextextension/)

Copyright (c) 2025 James Holgate
"""


import codecs
import os
import random
import stat
import sys
import time
import urllib
import warnings

try:
    import getopt
except (ImportError, AssertionError, AttributeError):
    exit()

try:
    import json
except (ImportError, AssertionError):
    pass

try:
    import locale
except (ImportError, AssertionError):
    pass

try:
    import platform
except (ImportError, AssertionError):
    pass

import build_extension
import find_replace_phonemes
import netcommon
import readtexttools

VLC_WINDOWS_INFO = """
# VLC

> VLC is a free and open source cross-platform multimedia player and framework
> that plays most multimedia files as well as DVDs, Audio CDs, VCDs, and
> various streaming protocols.

-- [VLC: Official site]((https://www.videolan.org))

If you are using PiperTTS on Windows without installing VLC , it can
take a few moments before your computer starts playing Piper speech.
If you are using PiperTTS using a compatibility layer capable of 
running Windows applications on a POSIX-compliant operating system,
you **REQUIRE** the Windows desktop version of VLC to stream piper
audio.

To enable fast and free audio streaming for Windows Piper TTS, use
VideoLAN [VLC Media Player Desktop](https://www.videolan.org)"""


class PiperTTSClass(object):
    """Piper TTS class"""

    def __init__(self) -> None:
        """Initialize data."""
        _common = netcommon.LocalCommons()
        self.machine = ""
        try:
            self.machine = platform.uname().machine
        except (AttributeError, NameError, TypeError):
            _meta = readtexttools.ImportedMetaData()
            self.machine = _meta.execute_command("uname -m")
        self.app_data = ".local"
        self.last_onnx_md5 = ""
        self.piper_minimum_dictionary = {
            "GB-jenny_dioco-medium": {
                "key": "en_GB-jenny_dioco-medium",
                "name": "jenny_dioco",
                "language": {
                    "code": "en_GB",
                    "family": "en",
                    "region": "GB",
                    "name_native": "English",
                    "name_english": "English",
                    "country_english": "Great Britain",
                },
                "quality": "medium",
                "num_speakers": 1,
                "speaker_id_map": {},
                "files": {
                    "en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx": {
                        "size_bytes": 63201294,
                        "md5_digest": "d08f2f7edf0c858275a7eca74ff2a9e4",
                    },
                    "en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx.json": {
                        "size_bytes": 4895,
                        "md5_digest": "e999a9c0aa535fb42e43b04cebcd65d2",
                    },
                    "en/en_GB/jenny_dioco/medium/MODEL_CARD": {
                        "size_bytes": 298,
                        "md5_digest": "ff351d05502764d5b4a074e0648e9434",
                    },
                },
                "aliases": [],
            }
        }
        self.default_lang = _common.default_lang
        self.concise_lang = self.default_lang.split("_")[0]
        self.tested_model = ""
        self.untested_model = ""
        self.tested_phrase = ""
        self.update_request = False
        self.sample_model = "en_GB-jenny_dioco-medium"
        for _item in self.piper_minimum_dictionary:
            if len(self.piper_minimum_dictionary[_item]["key"]) != 0:
                self.sample_model = self.piper_minimum_dictionary[_item]["key"]
                break
        self.sample_phrase = "A rainbow is a meteorological phenomenon."
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
        # environment.  Some app installer platforms use `piper` to refer
        # to a gaming mouse setup program. We check alternatives before
        # testing `piper`.
        # See: [GitHub](https://github.com/libratbag/piper).
        app_list = ["piper-cli", "piper-tts", "piper"]
        if os.name in ["nt"]:
            self.app = "piper.exe"
            _extension_table = readtexttools.ExtensionTable()
            for _item in app_list:
                _app = _extension_table.win_search(f"piper-tts{os.sep}piper", _item)
                if len(_app) != 0:
                    self.app = _app
                    break
        else:
            _app_path = ""
            for _app in app_list:
                for _item in [
                    f"~/.local/bin/{_app}",
                    f"~/.local/share/piper-tts/{_app}/{_app}",
                    f"~/.local/share/pied/common/{_app}/{_app}",
                    f"~/snap/pied/common/{_app}/{_app}",
                    f"~/.var/app/com.mikeasoft.pied/data/pied/piper/{_app}",
                    f"~/.local/share/pied/piper/piper",
                    f"/usr/local/lib/piper/{_app}",
                    f"/usr/local/share/piper/{_app}",
                    f"/usr/lib/piper/{_app}",
                    f"/usr/share/piper/{_app}",
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
        self.sample_webpage = "https://rhasspy.github.io/piper-samples"
        self.json_url_alt = f"{self.sample_webpage}/voices.json"
        self.json_url_wyoming = "https://raw.githubusercontent.com/rhasspy/wyoming-piper/master/wyoming_piper/voices.json"
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
        self.pied_list = []
        self.pied_voice_dir_list = [
            "~/snap/pied/common/models",
            "~/.var/app/com.mikeasoft.pied/data/pied/models",
            f"~/{self.app_data}/share/pied/common/models",
        ]
        self.piper_voice_dir_list = [
            f"~/{self.app_data}/share/piper-tts/piper-voices",
            f"~/{self.app_data}/share/piper/piper-voices",
            f"~/{self.app_data}/share/piper-voices",
            f"~/{self.app_data}/share/pied/common/models",
            "~/snap/pied/common/models",
            "~/.var/app/com.mikeasoft.pied/data/pied/models",
            "~/.local/share/pied/models",
            "~/piper-voices",
            "/opt/piper-voices",
            "/opt/piper-tts/piper-voices",
            "/usr/local/lib/piper",
            "/usr/local/share/piper",
            "/usr/lib/piper",
            "/usr/share/piper",
            readtexttools.linux_machine_dir_path("piper-voices"),
            readtexttools.linux_machine_dir_path("piper-tts/piper-voices"),
        ]
        espeak_ng_data_list = [
            self.app.replace("piper", "espeak-ng-data"),
            f"~/{self.app_data}/share/piper-tts/piper/espeak-ng-data",
            f"~/{self.app_data}/share/piper-tts/espeak-ng-data",
            f"~/{self.app_data}/share/piper/espeak-ng-data",
            f"~/{self.app_data}/share/pied/piper/espeak-ng-data",
            "~/snap/pied/common/piper/espeak-ng-data",
            "~/.var/app/com.mikeasoft.pied/data/pied/piper/espeak-ng-data",
            "~/.local/share/pied/piper/espeak-ng-data",
            "~/espeak-ng-data",
            "~/Downloads/espeak-ng-data",
            "/opt/piper-tts/piper-tts/piper/espeak-ng-data",
            "/usr/local/lib/piper/espeak-ng-data",
            "/usr/lib/piper/espeak-ng-data",
            readtexttools.linux_machine_dir_path("piper-tts/piper/espeak-ng-data"),
            readtexttools.linux_machine_dir_path("espeak-ng-data"),
        ]
        if os.name == "nt":
            self.app_data = "AppData\\Roaming"
            _prog_search = os.path.split(self.app)[0]
            self.piper_voice_dir_list = [
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
        for _piper_dir in self.piper_voice_dir_list:
            if not _piper_dir in self.pied_voice_dir_list:
                if os.path.isdir(os.path.expanduser(_piper_dir)):
                    self.piper_voice_dir = os.path.expanduser(_piper_dir)
                    break
        if len(self.piper_voice_dir) == 0:
            try:
                new_dir = os.path.expanduser(self.piper_voice_dir_list[0])
                os.makedirs(new_dir)
            except (OSError, PermissionError):
                pass
            if os.path.isdir(new_dir):
                self.piper_voice_dir = new_dir
        self.json_file = os.path.join(self.piper_voice_dir, "voices.json")
        self.model_file = os.path.join(self.piper_voice_dir, "models.txt")
        self.md5sum = ""
        self.espeak_ng_dir = ""
        for espeak_ng_dir in espeak_ng_data_list:
            if os.path.isdir(os.path.expanduser(espeak_ng_dir)):
                self.espeak_ng_dir = os.path.expanduser(espeak_ng_dir)
                break

        self.j_key = ""
        self.j_key_list = []
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
        # To hide the VLC interface, use the `--intf dummy` switch
        self.vlc_intfs = ["--intf dummy ", ""]
        self.use_specific_onnx_path = ""
        self.use_specific_onnx_voice_no = 0
        self.meta = readtexttools.ImportedMetaData()
        self.work_file = os.path.join(readtexttools.get_temp_prefix(), "piper-tts.wav")

    def usage(self, _help: str = "") -> None:
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

    def pretty_json_write(
        self, data: any = None, _json_file: str = "", iso_lang: str = "en-US"
    ) -> bool:
        """Use `json.dumps` to verify the format and convert the data to a
        JSON string in human readable format.
        """
        b_done = False
        if len(_json_file) == 0:
            return b_done
        if bool(data):
            try:
                json_string = json.dumps(data, ensure_ascii=False, indent=4)
                with codecs.open(_json_file, "w", "utf-8") as f:
                    f.write(json_string)
                    b_done = True
            except (UnicodeDecodeError.TypeError, OSError, LookupError):
                pass
        if not b_done:
            if not os.path.isfile(self.app_locker):
                readtexttools.pop_message(
                    self.help_heading,
                    "No voice model found",
                    8000,
                    self.help_icon,
                    2,
                    iso_lang,
                )
        return b_done

    def get_valid_qualities(self) -> list:
        """Determine valid qualities based on machine type and GPU
        availability."""
        if self.machine in ["x86_64", "amd64", "x64"]:
            if any(netcommon.have_gpu(_gpu) for _gpu in ["intel", "nvidia", "ryzen"]):
                return ["high", "medium", "low", "x_low"]
            return ["medium", "low", "x_low"]
        elif self.machine in ["arm64", "aarch64", "arm64-darwin"]:
            return ["high", "medium", "low", "x_low"]
        return ["low", "x_low"]

    def unlink_bad_posix_symbolic_link(
        self, _dest: str = "", filter_qualities: bool = False
    ) -> str:
        """If `os.name == 'nt'` always return `realpath`. Otherwise...

        Is `_dest` a real path? Return `_dest` without checking
        the `filter_qualities`.

        Is `_dest` a symbolic link? Unlink it if it is invalid.

        If `filter_qualities` equals `True` return the real path
        if it meets the quality criteria. Otherwise, return the
        real path if the symbolic link points to a valid path.

        If there's no valid link, or there's an error, return `""`
        """
        if os.name == "nt":
            return os.path.realpath(_dest)
        try:
            if _dest == os.path.realpath(_dest):
                return _dest
        except TypeError:
            return ""
        try:
            if not os.path.islink(_dest) or not os.path.exists(os.readlink(_dest)):
                os.unlink(_dest)
                return ""
            if not filter_qualities:
                return os.path.realpath(_dest)
            # Define valid qualities based on machine type and GPU availability
            _valid_qualities = self.get_valid_qualities()
            _test_str = _dest.replace(os.path.expanduser("~"), "~", 1)
            if any(
                f"{os.sep}{quality}{os.sep}" in _test_str
                for quality in _valid_qualities
            ):
                return os.path.realpath(_dest)
        except (OSError, TypeError):
            pass
        return ""

    def onnx_file_data_from_voices_json(
        self, _query: str = "en_GB-jenny_dioco-medium", file_data: str = "md5_digest"
    ) -> str:
        """
        Returns the expected `md5_digest` or `size_bytes` of a voice data
        package from `voices.json` based on a query term.
        """
        if os.sep in _query:
            _query = os.path.splitext(os.path.basename(_query))[0]
        if len(_query) == 0:
            return ""
        if not os.path.isfile(self.json_file):
            return ""
        if not file_data in ["md5_digest", "size_bytes"]:
            file_data = "md5_digest"
        try:
            with codecs.open(
                self.json_file, mode="r", encoding="utf-8", errors="replace"
            ) as file_obj:
                data = json.load(file_obj)
        except (PermissionError, FileNotFoundError, json.JSONDecodeError):
            return ""
        for item in data.values():
            _alias = "-".join([item["name"], item["quality"]])
            if item["aliases"]:
                _alias = item["aliases"][0]
            for field in [item["key"], _alias, item["name"]]:
                if _query == field:
                    # Construct the ONNX path and fetch the MD5 digest
                    _onnx_path = "/".join(
                        [
                            item["language"]["family"],
                            item["language"]["code"],
                            item["name"],
                            item["quality"],
                        ]
                    )
                    _onnx_file = f"{item['key']}.onnx"
                    return (
                        item["files"]
                        .get(f"{_onnx_path}/{_onnx_file}", {})
                        .get(file_data, "")
                    )
        return ""

    def link_home_dir_list(self, all_dir_list=None, _iso_lang: str = "en-US") -> bool:
        """Where onnx.json files exist in a posix home directory and files
        with the same name are not filed using the extension directory with
        a voices.json file, then link the home onnx.json and onnx files in
        the standard directory. Graphical Piper manager applications like the
        [Pied](https://pied.mikeasoft.com/) installer app might not store
        MODEL_CARD files in a standardized directory, so this client tries
        to download them for your reference into the client directory."""
        if not os.name == "posix" or not bool(all_dir_list):
            return False
        _dest_dir = ""
        retval = False
        _env_lang = _iso_lang.replace("-", "_")
        _concise_lang = _env_lang.split("_")[0]
        try:
            for _lang in [
                _env_lang,
                _concise_lang,
            ]:
                for _a_dir in all_dir_list:
                    if not os.path.exists(_a_dir):
                        continue
                    try:
                        files = os.listdir(_a_dir)
                        for _file in files:
                            if _file.startswith(_lang):
                                if _file.endswith(".onnx"):
                                    _file, _ext = os.path.splitext(_file)
                                    self.pied_list.append(os.path.join(_a_dir, _file))
                    except FileNotFoundError:
                        _file = ""
            if not bool(self.pied_list):
                return False
        except TypeError:
            return False

        _data = None
        _json_file = self.json_file
        if os.path.exists(_json_file):
            try:
                with codecs.open(
                    _json_file, mode="r", encoding="utf-8", errors="replace"
                ) as file_obj:
                    data = json.load(file_obj)
            except:
                return False
        try:
            if not data:
                return False
        except UnboundLocalError:
            return False
        for _extension in [".onnx.json", ".onnx", ""]:
            try:
                for _item in data:
                    for _file_path in self.pied_list:
                        _key = data[_item]["key"]
                        if _key in _file_path:
                            _source = f"{_file_path}{_extension}"
                            _dest_dir = os.path.join(
                                self.piper_voice_dir,
                                data[_item]["language"]["family"],
                                data[_item]["language"]["code"],
                                data[_item]["name"],
                                data[_item]["quality"],
                            )
                            if not os.path.isdir(_dest_dir):
                                os.makedirs(_dest_dir)
                            _dest = os.path.join(_dest_dir, f"{_key}{_extension}")
                            filter_qualities = True
                            # Remove an invalid symbolic link. Filter qualities by GPU and machine.
                            if (
                                len(
                                    self.unlink_bad_posix_symbolic_link(
                                        _dest, filter_qualities
                                    )
                                )
                                == 0
                            ):
                                continue
                            if not os.path.isfile(_dest):
                                if os.path.isdir(_dest_dir):
                                    if os.access(_dest_dir, os.W_OK):
                                        try:
                                            if not os.path.exists(_source):
                                                continue
                                            elif os.path.exists(_dest):
                                                continue
                                            elif (
                                                os.path.getsize(
                                                    os.path.realpath(_source)
                                                )
                                                < 20
                                            ):
                                                # Don't link to an invalid file.
                                                continue
                                            if _extension == ".onnx":
                                                real_md5 = (
                                                    build_extension.calculate_md5(
                                                        os.path.realpath(_source)
                                                    )
                                                )
                                                _path_ref = "/".join(
                                                    [
                                                        data[_item]["language"][
                                                            "family"
                                                        ],
                                                        data[_item]["language"]["code"],
                                                        data[_item]["name"],
                                                        data[_item]["quality"],
                                                    ]
                                                )
                                                json_md5 = data[_item]["files"][
                                                    f"{_path_ref}/{_key}{_extension}"
                                                ]["md5_digest"]
                                                if not real_md5 == json_md5:
                                                    print(
                                                        f"""WARNING: 
=======

Your local copy of `{_key}{_extension}` failed the `md5_sum` check.
Consider deleting it and downloading it again."""
                                                    )
                                                    continue
                                            os.symlink(_source, _dest)
                                            print(
                                                f"\nSymbolic link created from `{_source}` to `{_dest}`"
                                            )
                                            if _extension in [".onnx"]:
                                                do_pop_message = True
                                                # If the network works, get the MODEL_CARD
                                                _dir = self.retrieve_model(
                                                    _key, "", do_pop_message
                                                )
                                                if len(_dir) == 0:
                                                    # Failed to download, so show link to `_dest_dir`
                                                    readtexttools.pop_message(
                                                        self.help_heading,
                                                        _dest_dir,
                                                        5000,
                                                        self.help_icon,
                                                        1,
                                                        self.py_locale(),
                                                    )
                                            retval = True
                                        except OSError as e:
                                            print(
                                                f"\nCannot link `{_source}` to `{_dest}`: \n{e}"
                                            )
                                            retval = False
            except (KeyError, SyntaxError):
                return False
        return retval

    def language_supported(self, iso_lang: str = "en-GB", vox: str = "auto") -> bool:
        """Check to see if the language is available"""
        if len(self.espeak_ng_dir) == 0:
            return False
        if len(self.piper_voice_dir) == 0:
            return False
        model_test = vox.split("#")[0]
        if model_test.startswith("~"):
            model_test = os.path.expanduser(model_test)
        if os.path.isfile(f"{model_test}.json"):
            if os.path.isfile(model_test):
                # Check if the real size is smaller than the expected size,
                # i. e.: Check the `onnx` file is corrupt or if it is a text
                # file placeholder.
                if os.path.getsize(
                    os.path.realpath(model_test)
                ) < self.onnx_file_data_from_voices_json(model_test, "size_bytes"):
                    self.ok = False
                    return self.ok
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
        self.voice = int(
            "".join(["0", readtexttools.safechars(vox.split("#")[0], "1234567890")])
        )
        self.voice_name = vox
        self.concise_lang = iso_lang.split("_")[0].split("-")[0]
        self.lang = iso_lang.replace("-", "_")
        _dir_list = os.listdir(self.piper_voice_dir)
        if self.concise_lang in _dir_list:
            if any(
                self.concise_lang.startswith(_ignore)
                for _ignore in ["_script", "~", "."]
            ):
                return self.ok
        retval = False
        if any(_dir.startswith(self.concise_lang) for _dir in _dir_list):
            retval = True
            if self.pied_and_piper_directories_exist():
                pied_model_path = self.pied_model_path()
                for file_name in os.listdir(pied_model_path):
                    for _test in [self.voice_name, self.lang, self.concise_lang]:
                        if file_name.startswith(_test) and file_name.endswith(".onnx"):
                            model_test = os.path.join(pied_model_path, file_name)
                            if build_extension.calculate_md5(
                                os.path.realpath(model_test)
                            ) == self.onnx_file_data_from_voices_json(
                                model_test, "md5_digest"
                            ):
                                all_dir_list = [self.pied_model_path()]
                                self.ok = True
                                self.link_home_dir_list(all_dir_list, self.lang)
                                if not os.path.isfile(self.json_file):
                                    print(
                                        f"""Failed to link `{file_name}` to `{self.piper_voice_dir}`
 
        
The extension needs to download the current `voices.json` data
for currently supported models, including data to check the
integrity of each model.

You can force the application to download it by using a command
that includes the `--update True` option.

    "(PIPER_READ_TEXT_PY)" --update True --language (SELECTION_LANGUAGE_COUNTRY_CODE) "(TMP)" """
                                    )
        self.ok = retval
        return self.ok

    def model_path_list(
        self, iso_lang: str = "en-GB", _vox: str = "", extension: str = "onnx"
    ) -> list:
        """Check the directories for language models, and if found return
        the results in a list.
        """
        # NOTE: We use data that we can determine using the model key, so
        # we don't know whether a particular model is compatible with the
        # current version of piper, or whether the files' checksums match.
        _json_file = self.json_file
        _found_models = []
        _common = netcommon.LocalCommons()
        if os.path.exists(_json_file):
            with codecs.open(
                _json_file, mode="r", encoding="utf-8", errors="replace"
            ) as file_obj:
                data = json.load(file_obj)
        else:
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
                    self.help_heading, _json_file, 8000, self.help_icon, 1, iso_lang
                )
                self.ok = False
                sys.exit(0)
        if not self.pretty_json_write(data, _json_file, iso_lang):
            _warning = f"WARNING: Missing {self.help_heading} File!"
            underline = len(_warning) * "="
            print(
                f"""
{_warning}
{underline}

The {self.help_heading} client could not find a `.json` configuration file in
the `piper-tts` models directory.

    {_json_file}

Attempting to do a generic on-line configuration. If you have custom piper
voice models, then the generic json configuration will not recognize them.

<{self.json_url}>"""
            )
        # Use an English voice if a voice model is not available. This
        # is a common best practice for internationalization. The
        # client communicates that the program works, but you can tell
        # that the system currently lacks the requested voice model.
        # <https://learn.microsoft.com/en-us/windows-hardware/customize/desktop/unattend/microsoft-windows-international-core-uilanguagefallback>
        _match_lang = iso_lang.split("_")[0].split("-")[0]
        _description_list = [
            iso_lang.replace("-", "_"),
            _match_lang,
            "zzy_AQ",
        ]
        available_language = ""
        for description in _description_list:
            try:
                for _item in data:
                    if description == "zzy_AQ" and len(_found_models) == 0:
                        _description = "en"
                        available_language = data[_item]["language"]["name_english"]
                    else:
                        _description = description
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
                                filter_qualities = False
                                # There is no need to know the unlink result.
                                self.unlink_bad_posix_symbolic_link(
                                    self.j_path, filter_qualities
                                )
                                # We need to confirm that items are not
                                # onnx placeholders that only contain
                                # brief ASCII text.
                                if os.path.isfile(self.j_path):
                                    if (
                                        os.path.getsize(os.path.realpath(self.j_path))
                                        > 1000
                                    ):
                                        _found_models.append(self.j_path)
                self._update_model_doc()
            except IndexError:
                pass

        if len(available_language) != 0:
            _download_msg = readtexttools.translate_ui_element(
                iso_lang, "Download a compatible voice model"
            )
            help_heading = self.help_heading
            _web_page = self.sample_webpage
            if "/pied/" in self.espeak_ng_dir:
                help_heading = "Pied"
                _web_page = "https://pied.mikeasoft.com/"
            if not os.path.isfile(self.app_locker):
                readtexttools.pop_message(
                    f"{help_heading} ({iso_lang}) : {_download_msg}",
                    f"""{_web_page}""",
                    5000,
                    self.help_icon,
                    1,
                    iso_lang,
                )

        return _found_models

    def model_path(self, _extension: str = "onnx") -> str:
        """piper-tts models usually have two essential files with `.json` and
        `.onnx` extensions. If `model.[json | .onyx]` is in an expected
        directory, return the path, otherwise return `''`"""
        if len(self.use_specific_onnx_path) != 0:
            return self.use_specific_onnx_path
        if not os.path.isdir(self.piper_voice_dir):
            return ""
        _model = ""
        _model_list = self.model_path_list(self.lang, self.model, _extension)
        _uri = f"{self.voice_url}/{self.concise_lang}"
        if len(_model_list) == 0:
            print("-" * 79)
            print(
                f"""
INFO: Piper TTS cannot find `{self.lang}` `.json` and `.onnx` files.
<{self.json_file}>

<{_uri}>

[Get piper-voices]({self.hug_url}/tree/main)"""
            )
            if not os.path.isfile(self.app_locker):
                readtexttools.pop_message(
                    self.help_heading, _uri, 8000, self.help_icon, 1, self.concise_lang
                )
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
            return os.path.realpath(_model)
        self.ok = False
        return ""

    def py_locale(self, default_locale: str = "en-US") -> str:
        """Try to get the python default locale in using `en_US` format."""
        if os.name == "nt":
            try:
                # New in Python 3.11
                return locale.normalize(locale.getlocale()).split(".")[0]
            except AttributeError:
                warnings.filterwarnings("ignore", category=DeprecationWarning)
            # `getdefaultlocale()` is scheduled for removal in python
            # 3.15.
            try:
                return locale.getdefaultlocale()[0]
            except AttributeError:
                pass
            # Let's assume that piper's ["language"]["name_english"]
            # uses the same language names as the `nt` operating system.
            # We can only reliably resolve it to the base language code
            # known as the `family`. (`de`. `es`, `en`, `fr` ...)
            _json_file = self.json_file
            try:
                with codecs.open(
                    _json_file, mode="r", encoding="utf-8", errors="replace"
                ) as file_obj:
                    data = json.load(file_obj)
                    test_locale = locale.getlocale()[0].split("(")[0].strip()
                    for _item in data:
                        if test_locale.startswith(
                            data[_item]["language"]["name_english"]
                        ):
                            return data[_item]["language"]["family"]
                pass
            except:
                pass
        else:
            try:
                # New in Python 3.11
                return locale.normalize(locale.getlocale()).split(".")[0]
            except AttributeError:
                try:
                    warnings.filterwarnings("ignore", category=DeprecationWarning)
                    return locale.getlocale()[0]
                except AttributeError:
                    pass
        return default_locale

    def _update_model_doc(self) -> bool:
        """
        Updates the model file with new content from `self.j_key_list`.
        Returns `True` if the update was successful, `False` otherwise.
        """
        try:
            _new_model_content = (
                "\n".join(map(str, self.j_key_list)).strip() if self.j_key_list else ""
            )
            _old_model_content = ""
            if _new_model_content:
                if os.path.isfile(self.model_file):
                    try:
                        with codecs.open(
                            self.model_file, "r", encoding="utf-8"
                        ) as file_read:
                            _old_model_content = file_read.read().strip()
                    except Exception as e:
                        print(f"Error reading file: {e}")
                        return False
                if _new_model_content != _old_model_content:
                    try:
                        with codecs.open(
                            self.model_file, "w", encoding="utf-8"
                        ) as file_write:
                            file_write.write(_new_model_content)
                    except Exception as e:
                        print(f"Error writing file: {e}")
                        return False  # Failed to write new content
            return True
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    def _model_voice_info(self, _model: str = "") -> int:
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

    def pied_model_path(self) -> str:
        """Return model path if using a pied speech manager is available for
        a platform that supports pied on current flatpak or snap applications,
        otherwise return `""`."""
        if os.name == "posix":
            for _path in self.pied_voice_dir_list:
                if os.path.isdir(os.path.expanduser(_path)):
                    return os.path.expanduser(_path)
        return ""

    def _check_voice_request(self, _vox_number: int = 0, _list_size: int = 0) -> str:
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
                    if watermark in self.meta.execute_command(
                        f"file {os.path.realpath(real_app)}"
                    ):
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
        self,
        speaker: str = "en_GB-jenny_dioco-medium",
        home: str = "",
        do_pop_message: bool = True,
    ) -> str:
        """Download remote voice MODEL_CARD, onnx and json model files. Returns
        the directory containing the resources if successful, or else `""`."""
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
        if not os.path.isfile(self.app_locker):
            do_pop_message = False
        lang = lang_locale.split("_", maxsplit=1)[0]
        piper_file = ""
        _count = 1
        _extensions = ["MODEL_CARD", ".onnx.json", ".onnx"]
        s_count_total = str(len(_extensions))
        pied_model_path = self.pied_model_path()
        for _end in _extensions:
            pied_test = ""
            try:
                if "." in _end:
                    piper_file = f"{lang_locale}-{name}-{quality}{_end}"
                    if os.path.isfile(os.path.join(pied_model_path, piper_file)):
                        pied_test = os.path.join(pied_model_path, piper_file)
                else:
                    piper_file = _end
                    pied_test = ""
                home_file = os.path.join(
                    self.piper_voice_dir, lang, lang_locale, name, quality, piper_file
                )
                if self.onnx_file_data_from_voices_json(
                    pied_test, "md5_digest"
                ) == build_extension.calculate_md5(pied_test):
                    # Create a symbolic link to a file downloaded using the
                    # `pied`` piper-tts configuration program.
                    try:
                        os.symlink(pied_test, home_file)
                        if os.path.islink(home_file):
                            continue
                    except:
                        pass

                _rname = urllib.parse.quote(name)
                _rpiper_file = urllib.parse.quote(piper_file)
                remote_file = f"{home}{lang}/{lang_locale}/{_rname}/{quality}/{_rpiper_file}?download=true"
                if bool(self.debug):
                    print(
                        f"""`retrieve_model`
#######################################
home_file = {home_file}

remote_file = {remote_file}                
                
"""
                    )
                if os.path.isfile(home_file):
                    continue
                print(f"Requesting `{piper_file}`")
                urllib.request.urlretrieve(
                    remote_file,
                    home_file,
                )
                print(f"Retrieved `{piper_file}`")
                if do_pop_message:
                    s_count = str(_count)
                    _dots = _count * "…"
                    help_heading = self.help_heading
                    msg = f"""🌐 huggingface.co ⇒ 💻 : Piper `{piper_file}`
({s_count}/{s_count_total}) {_dots}"""
                    if piper_file == _end:
                        help_heading = f"{self.help_heading} [ 🛈 `{name}`]"
                        msg = remote_file
                    readtexttools.pop_message(
                        help_heading,
                        msg,
                        16000,
                        self.help_icon,
                        1,
                        lang,
                    )
                _count += 1
            except (TimeoutError, ValueError, urllib.error.URLError):
                pause_time = random.uniform(3, 8)
                time.sleep(pause_time)
                continue
            except OSError as e:
                print(f"OSError downloading `{piper_file}`: {e}")
                return ""
        return os.path.split(home_file)[0]

    def _get_outer_play_code(self, _text_file: str = "", _onnx: str = "") -> str:
        """Return a string with a valid posix command if a given streamer
        works, otherwise `""`."""
        _outer = ""
        _commons = "-autoexit -hide_banner -loglevel info -nostats"
        _gstreamer_out = "".join(
            [
                f"fdsrc ! audio/x-raw,format=S16LE,rate={self.sample_rate},",
                "channels=1 ! autoaudiosink",
            ]
        )
        _vlc_out = "".join(
            [
                f"""--meta-title "{self.help_heading} : {_onnx}" """,
                """--audio-visual visualizer --effect-list spectrometer """,
                """--demux=rawaud --rawaud-channels 1 --rawaud-samplerate """,
                f"""{self.sample_rate} - vlc://quit """,
            ]
        )
        _ffplay_out = "".join(
            [
                f"""-f s16le -ar {self.sample_rate}  -window_title " """,
                f"▶ {self.help_heading} : {_onnx} | 🛑 ",
                readtexttools.translate_ui_element(
                    readtexttools.default_lang(), "Stop"
                ),
                f""" ⌨ [ESC]" {_commons} -x 800 -y 24 -i -""",
            ]
        )
        try:
            # If system command `killall` is available, then hide the player window UI.
            if os.system(f"command -v killall > /dev/null") == 0:
                _ffplay_out = f"-f s16le -ar {self.sample_rate} {_commons} -nodisp -i -"
                _vlc_out = f"""--intf dummy --demux=rawaud --rawaud-channels 1 --rawaud-samplerate {self.sample_rate} - vlc://quit"""
        except (OSError, TypeError):
            pass
        _posix_play_apps = [
            [
                "aplay",
                f"-r {self.sample_rate} -f S16_LE -t raw -",
            ],
            [
                "paplay",
                f"--playback --raw --channels 1 --format s16le --rate {self.sample_rate} -",
            ],
            [
                "pw-cat",
                f"--playback --channels 1 --format s16 --rate {self.sample_rate} -",
            ],
            [
                "play",  # SoX - Sound eXchange
                f"-r {self.sample_rate} -c 1 -b 16 -e signed-integer -t raw -",
            ],
            [
                "gst-launch-1.0",
                _gstreamer_out,
            ],
            [
                "vlc",
                _vlc_out,
            ],
            [
                "ffplay",
                _ffplay_out,
            ],
        ]
        if ".var" in os.path.realpath(__file__):
            # With flatpak instances, the `kill` command does not work.
            # However, an application like `ffplay`, which can show
            # a player window that you can close, allows you to stop
            # playback by httting the [ESC] key to dismiss the window.
            _posix_play_apps = [
                [
                    "ffplay",
                    _ffplay_out,
                ],
                [
                    "gst-launch-1.0",
                    _gstreamer_out,
                ],
            ]
        for test_app, test_outer in _posix_play_apps:
            try:
                if os.system(f"command -v {test_app} > /dev/null") == 0:
                    _outer = f" --output-raw < {_text_file} | {test_app} {test_outer}"
                    break
            except (OSError, TypeError):
                continue
        return _outer

    def _supported_player_list(self) -> list:
        """If the client can access a compatible posix system sound player,
        then return the player in a list, otherwise return `[]`."""
        _programs = []
        for _program in [
            "aplay",
            "pw-cat",
            "ffplay",
            "gst-launch-1.0",
            "paplay",
            "play",
        ]:
            if os.path.isfile(os.path.join("usr", "bin", _program)):
                _programs.append(_program)
        return _programs

    def _vlc_app(self) -> list:
        """Return a list i. e.: `[_vlc="/pathto/vlc", _force_player=True]`
        * item 0 is host system path or `""` if it cannot be found.
        * item 1 is whether to choose `vlc` executable over a system player
          in all cases."""
        _extension_table = readtexttools.ExtensionTable()
        if os.name == "nt":
            _vlc = _extension_table.win_search("vlc", "vlc")
            _force_player = len(_vlc) != 0
            return (_vlc, _force_player)
        _vlc = ""
        _force_player = False
        # A Ubuntu VLC snap is sandboxed, so this client cannot use it.
        # Check only custom installed paths.
        vlc_list = [
            ["/usr/local/bin/vlc", False],
            ["/opt/vlc/bin/vlc", False],
        ]
        if not os.path.isdir("/snapd"):
            vlc_list = vlc_list + [
                ["/Applications/VLC.app/Contents/MacOS/VLC", True],
                ["/usr/bin/vlc", False],
            ]
        for _check_vlc in vlc_list:
            if os.path.isfile(_check_vlc[0]):
                _vlc = _check_vlc[0]
                _force_player = _check_vlc[1]
                break
        if len(_vlc) == 0:
            if len(self._supported_player_list()) == 0:
                if len(_extension_table.vlc) != 0:
                    _vlc = _extension_table.vlc
                    _force_player = True
        return (_vlc, _force_player)

    def read(
        self,
        _text_file: str = "",
        _iso_lang: str = "en-GB",
        _config: str = "",
        _speech_rate: int = 160,
        _player: int = 1,
    ) -> bool:
        """Read speech aloud"""
        _extension_table = readtexttools.ExtensionTable()
        _meta = readtexttools.ImportedMetaData()

        _length_scale = self.length_scale  # Fallback rate
        if _speech_rate != 160:
            _length_scale = self.common.rate_to_rhasspy_length_scale(_speech_rate)[0]
            self.length_scale = _length_scale
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
        _onnx = os.path.splitext(os.path.basename(_model))[0]
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
        _vlc = ""
        _force_player = False
        _vlc_vis = "--audio-visual visualizer --effect-list "
        _vlc_demux = (
            "--demux=rawaud --rawaud-channels 1 --rawaud-samplerate 22050 - vlc://quit"
        )
        for _frame in [
            "--meta-title PiperTTS",
            f'--meta-title "PiperTTS : {_onnx}#{voice_no}"',
            f'-f --meta-title "PiperTTS : {_onnx}#{voice_no}"',
        ]:
            for _xtra in [
                "scope",
                "spectrometer",
                "spectrum",
                "vuMeter",
            ]:
                self.vlc_intfs.append(f"{_frame} {_vlc_vis}{_xtra} ")
        if _player >= len(self.vlc_intfs):
            _player = random.randint(2, len(self.vlc_intfs) - 1)
        _vlc, _force_player = self._vlc_app()
        if len(_vlc) != 0 and (bool(_player) or _force_player):
            if bool(_player):
                _ui = self.vlc_intfs[_player]
            else:
                _ui = self.vlc_intfs[0]
            _outer = f" --output-raw < {_text_file} | {_vlc} {_ui}{_vlc_demux}"
        else:
            if os.name == "posix":
                _outer = self._get_outer_play_code(_text_file, _onnx)
                if len(_outer) == 0:
                    return False
        _demo_warning = ""
        if os.name == "nt":
            _vlc, _force_player = self._vlc_app()
            if len(_vlc) == 0:
                _demo_warning = """
        @
       / \\
      /@@@\\
     /     \\    <https://videolan.org>
    /@@@@@@@\\
   /         \\
 @@@@@@@@@@@@@@@\\
 
Windows needs the desktop version of the VideoLAN VLC Media Player to stream
Piper TTS text. By using Piper's ability to stream audio to a media player
directly without saving a `.wav` audio file to your computer's storage, your
computer can start reading quickly with large or small selections of text."""
                _work_file = _extension_table.add_quotes_if_needed(
                    self.work_file.replace(".txt", ".json")
                )
                _outer = f""" --output_file {_work_file} """
            else:
                _ui = self.vlc_intfs[_player]
                _outer = f" --output-raw < {_text_file} | {_vlc} {_ui}{_vlc_demux}"
        if os.path.isfile(self.app_locker):
            readtexttools.unlock_my_lock(self.locker)
            if len(_vlc) != 0:
                app_list = ["vlc", "piper", "piper-cli", "VLC"]
                if os.name == "nt":
                    app_list = ["VLC.EXE", "PIPER.EXE"]
            else:
                base_list = self._supported_player_list()
                app_list = base_list + [
                    "piper",
                    "piper-cli",
                ]
                if os.name == "nt":
                    app_list = ["SOX.EXE", "PIPER.EXE"]
            print(f"[ > ] {self.help_heading} stopping...")
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
reinstall an up-to-date binary version of Piper.
"""
        speaker_switch = ""
        if os.path.isfile(self.work_file):
            os.remove(self.work_file)
        if voice_no > self.voice_count - 1:
            voice_no = 0
        if voice_no != 0:
            speaker_switch = "".join([" --speaker ", str(voice_no).strip()])
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
            _variant = str(voice_no)
            if self.debug == 0:
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


    {_command}
"""
                )
            else:
                print(self.j_key_list)
                print(_command)

            self._update_model_doc()
            if os.name in ["posix"]:
                _response = os.system(_command)
            elif os.name in ["nt"]:
                if len(_vlc) != 0:
                    _response = os.system(_command)
                else:
                    _json_tools = readtexttools.JsonTools()
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
                        if os.path.getsize(os.path.realpath(self.work_file)) == 0:
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
        self,
        _dir: str = "",
        _voice: str = "",
        _sub_dirs: bool = True,
        do_pop_message: bool = True,
    ) -> bool:
        """Download the most recent `voices.json` file, and if `_sub_dirs` is
        `True` then add new model subdirectories to the local model
        directory."""
        if not os.path.isdir(_dir):
            if len(_dir) == 0:
                return False
            os.makedirs(_dir)
        if not os.path.isfile(self.app_locker):
            do_pop_message = False
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
            data = json.loads(data_response)
            if not self.pretty_json_write(data, self.json_file, self.concise_lang):
                return False
        else:
            return False
        readtexttools.write_plain_text_file(
            os.path.join(_dir, "README.md"), self.load_instructions(True), "utf-8"
        )
        if _sub_dirs:
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
                                    self.help_heading,
                                    _uri,
                                    8000,
                                    self.help_icon,
                                    1,
                                    data[_item]["language"]["code"],
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
            if len(piper_file) != 0:
                print(
                    f"""Please wait
===========

It takes a few moments to retrieve the piper voice model
`{piper_file}` from <{self.hug_url}> """
                )
            _dir = self.retrieve_model(piper_file, "", do_pop_message)
            if len(_dir) != 0:
                readtexttools.show_with_app(_dir)
        return os.path.isfile(self.json_file)

    def load_instructions(self, verbose: bool = True) -> str:
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

    def pied_and_piper_directories_exist(self) -> bool:
        """If a pied directory exists, and a local piper directory has been
        configured, then return `True`. The `voices.json` file has data that
        reflects the current status of the current voice model repository,
        whereas the pied program reflects the status at the time of the
        application's most recent update."""
        if len(self.pied_model_path()) == 0:
            return False
        if os.path.isdir(self.piper_voice_dir):
            return any(
                file_name == "_scripts"
                for file_name in os.listdir(self.piper_voice_dir)
            )
        return False

    def get_checked_pied_onnx(self, _lang: str = "en-GB") -> str:
        """Given an iso language description, check for a suitable onnx
        file in a local pied resource directory. Return a usable
        file path if it checks out as valid or `""` if it does not."""
        if len(self.pied_model_path()) == 0:
            return ""
        if len(_lang) < 2:
            return ""
        _iso_lang = _lang.split(".")[0]
        for _pair in [
            ["-", "_"],
            ["en_UK", "en_GB"],
            ["uk_UK", "uk_UA"],
        ]:
            _iso_lang = _iso_lang.replace(_pair[0], _pair[1])
        pied_model_path = self.pied_model_path()
        for _test in [_iso_lang, _iso_lang.split("_")[0]]:
            for file_name in os.listdir(pied_model_path):
                if file_name.startswith(_test) and file_name.endswith(".onnx"):
                    _found_file = os.path.join(pied_model_path, file_name)
                    if os.path.isfile(_found_file):
                        if not os.path.islink(_found_file):
                            if self.onnx_file_data_from_voices_json(
                                _found_file, "md5_digest"
                            ) == build_extension.calculate_md5(_found_file):
                                return _found_file
        return ""

    def do_update(self) -> bool:
        """"""
        _backup = f"{self.json_file}.bak"
        _update_msg = self.sample_webpage
        if os.name == "nt":
            _update_msg = "Download a compatible voice model"
        if not os.path.isfile(self.app_locker):
            readtexttools.pop_message(
                self.help_heading,
                _update_msg,
                6000,
                self.help_icon,
                1,
                self.concise_lang,
            )
        # `True`, `Yes`, `1`, `-1`
        good_response = False
        _dir = self.piper_voice_dir
        if not os.path.isdir(_dir):
            try:
                os.makedirs(_dir)
                self.pretty_json_write(
                    self.piper_minimum_dictionary,
                    self.json_file,
                    "en-GB",
                )
            except (OSError, PermissionError):
                print("Failed to create a `Piper_TTS` client directory.")
                exit()
            self.common.set_urllib_timeout(4)
        for json_url in [
            self.json_url,
            self.json_url_alt,
            self.json_url_wyoming,
        ]:
            try:
                response = urllib.request.urlopen(json_url)
                if os.path.isfile(self.json_file):
                    if os.path.isfile(_backup):
                        os.remove(_backup)
                    os.rename(self.json_file, _backup)
                self.update_request = True
                self.json_url = json_url
                good_response = True
                break
            except (TimeoutError, ValueError, urllib.error.URLError):
                print(
                    f"""The `Piper_TTS` client failed to connect.
    <{json_url}>"""
                )
                return False
            except OSError as e:
                print(
                    f"""OSError downloading `{self.json_file}`: {e}
    <{json_url}>"""
                )
                return False
            except Exception:
                print(f"Error resolving `{json_url}`")
                return False
        if os.path.isfile(_backup):
            if not os.path.isfile(self.json_file):
                os.rename(_backup, self.json_file)
        if not good_response:
            if not os.path.isfile(self.app_locker):
                readtexttools.pop_message(
                    self.help_heading,
                    "The `Piper_TTS` client failed to connect.",
                    8000,
                    self.help_icon,
                    2,
                    self.concise_lang,
                )
            return False
        return True

    def is_macos(self):
        """Is this a MacOS computer?"""
        try:
            if os.name == "posix":
                if os.uname().sysname.lower() in ["darwin"]:
                    return True
        except AttributeError:
            pass
        return False

    def piper_main(
        self,
        _text_file_in: str = "",
        _do_update: bool = False,
        _iso_lang: str = "en-US",
        _config: str = "",
        _player: int = 0,
        _percent_rate: str = "100%",
        _voice: str = "AUTO0#0",
    ) -> bool:
        """Execute Piper TTS speech synthesis for supported languages
        and return `True` if successful."""
        all_dir_list = [self.piper_voice_dir]
        if _do_update:
            self.do_update()
        if len(_iso_lang) == 0:
            if "_" in _voice and len(_voice.split("-")) == 3:
                _iso_lang = _voice.split("-", maxsplit=1)[0].replace("_", "-")
            else:
                _iso_lang = "en-US"
        if not os.path.isfile(self.json_file):
            self.model_path_list(self.lang, self.model, ".onnx")
        for _a_dir in all_dir_list:
            if os.path.isfile(os.path.join(_a_dir, "voices.json")):
                _use_dir = _a_dir
                break
        if not os.path.isfile(self.model_file):
            self._update_model_doc()
        if self.link_home_dir_list(all_dir_list, _iso_lang):
            print(
                """The Piper TTS client linked to newly installed Piper
    voice model resources."""
            )
        if len(_use_dir) == 0 or self.update_request:
            update_pop_msg = os.name == "posix"
            if os.path.isfile(self.app_locker):
                update_pop_msg = False
            update_sub_dirs = True
            self.update_local_model_dir(
                _use_dir, _voice, update_sub_dirs, update_pop_msg
            )
        if not self.language_supported(_iso_lang, _voice):
            if not self.update_request:
                if os.path.isfile(self.app_locker):
                    os.path.remove(self.app_locker)
                elif not self.is_macos():
                    readtexttools.pop_message(
                        f"{self.help_heading} ({_iso_lang})",
                        "The Piper_TTS client cannot find a compatible voice model for your language.",
                        5000,
                        self.help_icon,
                        1,
                        self.py_locale(),
                    )
                return False
        if _text_file_in.startswith("~"):
            _text_file_in = os.path.expanduser(_text_file_in)
        if not os.path.isfile(_text_file_in):
            return False
        if sys.argv[-1] == sys.argv[0]:
            self.usage()
            return False
        find_replace_phonemes.fix_up_text_file(
            _text_file_in,
            "",
            _iso_lang,
            self.local_dir,
            "PIPER_USER_DIRECTORY",
            False,
        )
        self.read(
            _text_file_in,
            _iso_lang,
            _config,
            netcommon.speech_wpm(_percent_rate),
            _player,
        )
        if self.debug != 0:
            print(self.load_instructions(True))
        return True


def main() -> None:
    """Use Piper TTS speech synthesis for supported languages."""
    _piper_tts = PiperTTSClass()
    if not sys.version_info >= (3, 6) or not os.name in ["nt", "posix"]:
        print("Your system does not support the piper python tool.")
        _piper_tts.usage()
        sys.exit(0)
    _do_update = False
    _percent_rate = "100%"
    _iso_lang = ""
    _config = ""  # model json path (defaults to onnx path + .json suffix)
    _voice = "AUTO0#0"
    # _use_dir = ""
    _player = 0
    if os.name == "nt":
        _player = 0
    _text_file_in = sys.argv[-1]
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "uclprvh",
            ["update=", "config=", "language=", "player=", "rate=", "voice=", "help"],
        )
    except getopt.GetoptError:
        # Show help information and exit
        print("option -a not recognized")
        _piper_tts.usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-u, --update"):
            if readtexttools.lax_bool(a):
                _do_update = True
        elif o in ("-l", "--language"):
            _iso_lang = a
            if _iso_lang.startswith("zxx"):
                _iso_lang = "en-US"
                default_lang = readtexttools.default_lang().replace("_", "-")
                if _piper_tts.language_supported(default_lang):
                    _iso_lang = default_lang
        elif o in ("-c", "--config"):
            if a.startswith("~"):
                a = os.path.expanduser(a)
            if os.path.isfile(a):
                _config = a
        elif o in ("-p", "--player"):
            try_player = _player
            try:
                try_player = int(a)
            except (TypeError, ValueError):
                try_player = _player
            if try_player > _player:
                _player = try_player
        elif o in ("-r", "--rate"):
            _percent_rate = a
        elif o in ("-v", "--voice"):
            _voice = a
        elif o in ("-h", "--help"):
            _piper_tts.usage()
            sys.exit(0)
        else:
            assert False, "unhandled option"
    _piper_tts.piper_main(
        _text_file_in, _do_update, _iso_lang, _config, _player, _percent_rate, _voice
    )


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
# Copyright (c) 2025 James Holgate
