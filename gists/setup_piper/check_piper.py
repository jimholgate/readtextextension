"""Install or test `piper-tts` resources on Windows or Linux.
<https://github.com/rhasspy/piper/releases/latest>."""
#########################################
#########################################
PIPER_RELEASE_VERSION = "2023.11.14-2"  #
#########################################
#########################################
ABOUT_PIPER = """

About Piper TTS
===============

**[Piper][1]** is a fast, local neural text to speech system.

On supported platforms Read Text Extension uses a local directory that follows
the format of the online Piper TTS directories. If the program doesn't start
when you type `piper.exe` or `piper-cli` in a command line window, then make
sure the program is in your system's `PATH` and that the machine type of your
computer matches the machine type of the program archive.

Linux
-----

Use your package manager to check if the [`python3-tkinter`][2] library or the
Zenity application is installed to enable the piper installation script dialogs.

To enable a visual user interface for playback, install [`vlc`][3].

Windows
-------

> The legacy console mode is deprecated and no longer being updated.
>
> -- *[Depreciated features in the Windows Client][4]*. Microsoft.
> Accessed January 3, 2024.

PowerShell supersedes the classic console. The safest way to run a [python][5]
script is by opening it in [Visual Studio Code][6] and clicking the "Run"
button. Visual Studio Code will show if it finds any issues.

> VBScript is deprecated. In future releases of Windows, VBScript will
> be available as a feature on demand before its removal from the
> operating system. 
> 
> -- *[Depreciated features in the Windows Client][7]*. Microsoft.
> Accessed January 3, 2024.

Starting with Read Text 0.8.74, the extension uses the LibreOffice and Apache
OpenOffice scripting systems if VBScript is not available. The default behavior
is to hide the setup menu if your Windows computer does not have VBScript. You
can enable alternative scripting methods like python. Use the LibreOffice
*Tools - Options - Advanced* tool and check *Enable Experimental Features*.

The [Rhasspy project][8] released a Windows pre-release of it's Piper TTS
software.

Starting with Read Text 0.8.74, the extension supports it as an experimental
feature in Windows. Install the app with the script, then enable it by going
to  *Tools - Options - Advanced* and selecting *Enable Experimental Features*.

To improve performance and enable a visual user interface for playback,
install the [VideoLAN VLC Media Player][9] desktop application.

(c) 2024, James Holgate.

[License][10]


  [1]: https://github.com/rhasspy/piper
  [2]: https://packages.debian.org/search?keywords=python3-tk
  [3]: https://packages.debian.org/search?keywords=vlc
  [4]: https://learn.microsoft.com/en-us/windows/whats-new/deprecated-features
  [5]: https://www.python.org/downloads/windows/
  [6]: https://code.visualstudio.com/
  [7]: https://learn.microsoft.com/en-us/windows/whats-new/deprecated-features
  [8]: https://github.com/rhasspy/piper
  [9]: https://www.videolan.org
  [10]: https://raw.githubusercontent.com/jimholgate/readtextextension/master/Read_Text/registration/LICENSE
"""

ABOUT_MD5_CHECKSUM = """
About the MD5 Checksum
----------------------

When you download a file, the website often provides an MD5 checksum, which is
like a unique digital fingerprint for that file. If the file is changed in 
any way, the MD5 checksum will also change.

So, if the MD5 checksum of your downloaded file does not match the one from
the website, it could mean:

1. The file was updated: The website might have updated the file after the MD5
   checksum was listed.
2. Download errors: Sometimes, errors can occur during the download process
   that slightly alter the file.
3. Different calculation methods: The MD5 checksum might have been calculated
   differently by the computer program that you are using and the website.
4. New models: For recently created models, there might be more frequent
   updates due to improvements or corrections in the language model. This
   could result in a different MD5 checksum each time you download the file.

A different MD5 checksum does not necessarily mean the file is dangerous. But
it does mean the file might not be exactly what the service intended to
provide. If you have any concerns, you could try deleting the `voices.json`
file, then try downloading the ONNX file that has the wrong checksum later. It
might be good to let the model's creators know that you had a problem.
"""
import argparse
import codecs
import hashlib
import json
import locale
import urllib.request
import os
import platform
import subprocess
import time
import unicodedata
import zipfile

from datetime import datetime, timedelta

try:
    import tkinter as tk
    from tkinter import messagebox
    from tkinter import simpledialog

    GOT_TK = True
except ImportError:
    GOT_TK = False


class ShowDialog:
    def __init__(self):
        """Initializes the ShowDialog class, checks for the availability of tkinter and zenity."""
        if GOT_TK:
            self.root = tk.Tk()
            self.root.withdraw()  # Hide the main window
            self.got_tk = True
        else:
            self.root = None
            self.got_tk = False
        self.got_zenity = False
        if os.path.isfile("/usr/bin/zenity"):
            self.got_zenity = True

    def _zenity(self, type: str = "info", text: str = "", title: str = "Zenity"):
        """Runs a zenity command with the given type, text, and title."""
        if not self.got_zenity:
            return None
        try:
            retval = subprocess.run(
                ["zenity", f"--{type}", f"--text={text}", f"--title={title}"],
                capture_output=True,
                text=True,
            )
            return retval.returncode
        except FileNotFoundError:
            return None

    def _tkinter(self, type: str = "showinfo", text: str = "", title: str = "Tkinter"):
        """Displays a tkinter messagebox with the given type, text, and title."""
        return getattr(messagebox, type)(title, text)

    def showinfo(self, title: str = "Info", text: str = "_showinfo"):
        """Displays an info dialog with the given text and title."""
        if self.got_zenity:
            self._zenity("info", text, title)
        elif self.got_tk:
            self._tkinter("showinfo", text, title)

    def showwarning(self, title: str = "Warning", text: str = "_showwarning") -> None:
        """Displays a warning dialog with the given text and title."""
        if self.got_zenity:
            self._zenity("warning", text, title)
        elif self.got_tk:
            self._tkinter("showwarning", text, title)

    def askyesno(
        self, title: str = "Ask Yes/No", text: str = "_askyesno", default: bool = False
    ) -> bool:
        """Displays a yes/no question dialog with the given text and title,
        returns a boolean based on the user's choice."""
        if self.got_zenity:
            return self._zenity("question", text, title) == 0
        elif self.got_tk:
            return self._tkinter("askquestion", text, title) == "yes"
        return default

    def askstring(
        self,
        title: str = "_ask_string",
        prompt: str = "_prompt",
        initialvalue: str = "_initialvalue",
    ) -> str:
        """Displays a dialog asking for a string input with the given title, prompt, and initial value, returns the user's input."""
        if self.got_zenity:
            result = subprocess.run(
                [
                    "zenity",
                    "--entry",
                    f"--title={title}",
                    f"--text={prompt}",
                    f"--entry-text={initialvalue}",
                ],
                capture_output=True,
                text=True,
            )
            return result.stdout.strip()
        elif self.got_tk:
            return simpledialog.askstring(
                title=title,
                prompt=prompt,
                initialvalue=initialvalue,
            ).strip()
        return initialvalue.strip()


def get_file_text(_file: str = "") -> str:
    """Get the text of a utf-8 file"""
    try:
        with codecs.open(
            _file, mode="r", encoding="utf-8", errors="replace"
        ) as file_obj:
            return file_obj.read()
    except (PermissionError, FileNotFoundError):
        return ""


def check_if_file_is_stale(file_path: str = "", _hour: int = 4) -> bool:
    """Get the modification time of the file. If a file is more than `_hour`
    hours old, or `file_path` is not a valid file, return `True`, otherwise
    `False`. This is to avoid flooding an online resource repeatedly with
    requests for the same file."""
    if not os.path.isfile(file_path):
        return True
    mod_time = os.path.getmtime(file_path)
    current_time = time.time()
    return current_time - mod_time > _hour * 60 * 60


def calculate_md5(file_path: str = "") -> str:
    """Return the hexadecimal MD5 hash of `file_path`. You can verify
    downloads are complete and correct by comparing the stated md5
    checksum to this routine's output"""
    if not os.path.isfile(file_path):
        return ""
    with open(file_path, "rb") as file:
        md5 = hashlib.md5()
        for chunk in iter(lambda: file.read(4096), b""):
            md5.update(chunk)
        return md5.hexdigest()


class GetPiperData:
    """Edit the data to reflect currently available versions"""

    def __init__(self):
        """The default data"""
        # Default release info
        self.release_ver = PIPER_RELEASE_VERSION
        self.changed_status = False
        self.this_machine = platform.machine().lower()
        self.debug = False
        self.quiet = False
        self.client_title = f"Piper TTS Client for {platform.system()}"

        if not bool(GOT_TK):
            self.quiet = True

        # File checking values
        self.file_does_not_exist = 0
        self.file_exists = 1
        self.getsize_not_too_small = 2
        self.getsize_matches = 4
        self.md5_matches = 8

        # System info
        self.program_path = os.path.realpath(
            os.path.expanduser("~/.local/share/piper-tts")
        )
        if bool(os.environ.get("LOCALAPPDATA")):
            self.program_path = os.path.join(
                os.environ.get("LOCALAPPDATA"), "Programs", "piper-tts"
            )
        #        if bool(os.environ.get("WINEHOMEDIR")):
        #            program_path = os.path.join(
        #                os.environ.get("WINEHOMEDIR"), ".local", "share", "piper-tts"
        #            )
        #            if os.path.isdir(program_path):
        #                self.program_path = program_path
        self.data_path = os.path.realpath(
            os.path.expanduser("~/.local/share/piper-tts")
        )
        if bool(os.environ.get("APPDATA")):
            if not os.path.isdir(self.data_path):
                self.data_path = os.path.join(os.environ.get("APPDATA"), "piper-tts")
        self.download_path = os.path.realpath(os.path.expanduser("~/Downloads/"))
        if not os.path.isdir(self.download_path):
            self.download_path = os.path.realpath(os.path.expanduser("~/"))
        self.supported_machines = ["amd64"]
        if self.this_machine in self.supported_machines:
            # Make `.this_machine` the default.
            self.supported_machines = [self.this_machine] + self.supported_machines
        self.file_spec = f"piper_windows_{self.supported_machines[0]}.zip"
        if platform.system() == "Linux":
            self.supported_machines = ["x86_64", "armv7l", "aarch64"]
            if self.this_machine in self.supported_machines:
                # Make `.this_machine` the default.
                self.supported_machines = [self.this_machine] + self.supported_machines
            self.file_spec = f"piper_linux_{self.supported_machines[0]}.tar.gz"
        elif platform.system() == "Darwin":
            exit()
        self.model_dir = os.path.join(self.data_path, "piper-voices")
        self.voices_json_path = os.path.realpath(f"{self.model_dir}/voices.json")

        # Online resources
        self.piper_source = "https://github.com/rhasspy/piper"
        self.piper_voices_url = "https://huggingface.co/rhasspy/piper-voices"
        self.piper_samples_url = "https://rhasspy.github.io/piper-samples/"
        self.voices_json_uri = f"{self.piper_voices_url}/raw/main/voices.json"
        # Default voice model info
        self.key = "en_GB-jenny_dioco-medium"
        self.name_english = "English"
        self.country_english = ""
        self.system_family = "en_GB"
        self.family = self.key.split("_")[0]
        self.code = self.key.split("-")[0]
        self.name = self.key.split("-")[1]
        self.quality = self.key.split("-")[2]
        # On-line Open Neural Network Exchange (ONNX) resources that Piper TTS supports
        _rname = urllib.parse.quote(self.name)
        _rkey = urllib.parse.quote(self.key)
        self.onnx_dir_url = f"{self.piper_voices_url}/resolve/main/{self.family}/{self.code}/{_rname}/{self.quality}/"
        self.onnx_url = f"{self.onnx_dir_url}{_rkey}.onnx"
        self.json_url = f"{self.onnx_dir_url}{_rkey}.onnx.json"
        self.model_card_url = f"{self.onnx_dir_url}MODEL_CARD"
        # A `~/.local` directory to store Piper TTS ONNX resources
        self.onnx_file_base = os.path.join(
            self.model_dir,
            self.family,
            self.code,
            self.name,
            self.quality,
        )
        self.model_card_file = os.path.join(self.onnx_file_base, "MODEL_CARD")
        self.onnx_file = os.path.join(self.onnx_file_base, f"{self.key}.onnx")
        self.json_file = f"{self.onnx_file}.json"
        # Values of ONNX resource settings to be determined from the `voices.json` file.
        # The defaults use a value that never matches a valid value.
        self.onnx_published_size = -1
        self.onnx_md5 = ""
        self.onnx_json_published_size = -1
        self.onnx_json_md5 = ""
        self.model_card_published_size = -1
        self.model_card_md5 = ""
        # Criteria : Prefer a language model with these features:
        #
        # * Medium quality model, if available.
        # * Model has a single voice or one male and one female voice
        # * Plain style for reading - no special effect or novelty characters
        # * Uses a high quality recording of an original reader.
        # * Recent
        # * Public domain or specific permission conditions in license.
        self.piper_localization = [
            [
                "ar_JO-kareem-medium",
                "Arabic",
                "Jordan",
                "",
            ],
            [
                "ca_ES-upc_ona-medium",
                "Catalan",
                "Spain",
                "",
            ],
            [
                "cs_CZ-jirka-medium",
                "Czech",
                "Czech Republic",
                "",
            ],
            [
                "da_DK-talesyntese-medium",
                "Danish",
                "Denmark",
                "",
            ],
            [
                "de_DE-thorsten-medium",
                "German",
                "Germany",
                "",
            ],
            [
                "en_GB-jenny_dioco-medium",
                "English",
                "Great Britain",
                "en_UK",
            ],
            [
                "en_US-lessac-medium",
                "English",
                "United States",
                "",
            ],
            [
                "es_ES-sharvard-medium",
                "Spanish",
                "Spain",
                "",
            ],
            [
                "fi_FI-harri-medium",
                "Finnish",
                "Finland",
                "",
            ],
            [
                "fr_FR-upmc-medium",
                "French",
                "France",
                "",
            ],
            [
                "hu_HU-anna-medium",
                "Hungarian",
                "Hungary",
                "",
            ],
            [
                "is_IS-bui-medium",
                "Icelandic",
                "Iceland",
                "",
            ],
            [
                "ka_GE-natia-medium",
                "Georgian",
                "Georgia",
                "",
            ],
            [
                "lb_LU-marylux-medium",
                "Luxembourgish",
                "Luxembourg",
                "",
            ],
            [
                "ne_NP-google-medium",
                "Nepali",
                "Nepal",
                "",
            ],
            [
                "nl_BE-nathalie-medium",
                "Dutch",
                "Belgium",
                "",
            ],
            [
                "no_NO-talesyntese-medium",
                "Norwegian",
                "Norway",
                "",
            ],
            [
                "pl_PL-darkman-medium",
                "Polish",
                "Poland",
                "",
            ],
            [
                "pt_BR-faber-medium",
                "Portuguese",
                "Brazil",
                "",
            ],
            [
                "ro_RO-mihai-medium",
                "Romanian",
                "Romania",
                "",
            ],
            [
                "ru_RU-irina-medium",
                "Russian",
                "Russia",
                "",
            ],
            [
                "sk_SK-lili-medium",
                "Slovak",
                "Slovakia",
                "",
            ],
            [
                "sr_RS-serbski_institut-medium",
                "Serbian",
                "Serbia",
                "",
            ],
            [
                "sv_SE-nst-medium",
                "Swedish",
                "Sweden",
                "",
            ],
            [
                "sw_CD-lanfrica-medium",
                "Swahili",
                "Democratic Republic of the Congo",
                "",
            ],
            [
                "tr_TR-dfki-medium",
                "Turkish",
                "Turkey",
                "",
            ],
            [
                "uk_UA-ukrainian_tts-medium",
                "Ukrainian",
                "Ukraine",
                "uk-UK",
            ],
            [
                "vi_VN-vais1000-medium",
                "Vietnamese",
                "Vietnam",
                "",
            ],
            [
                "zh_CN-huayan-medium",
                "Chinese",
                "China",
                "yue",
            ],
        ]

    def update_bashrc(self) -> bool:
        """If needed, then add `~/.local/bin` to the Linux PATH so that
        you can run `piper-cli` without including the full path. You might
        need to log out and log in again to apply the change."""
        _bashrc = os.path.realpath(os.path.expanduser("~/.bashrc"))
        if not os.path.isfile(_bashrc):
            return False
        new_path = os.path.realpath(os.path.expanduser("~/.local/bin"))
        if not os.path.isdir(new_path):
            return False
        current_path = os.environ.get("PATH")
        if not new_path in current_path and os.path.exists(new_path):
            os.environ["PATH"] = f"{current_path}{os.pathsep}{new_path}"
        _now = datetime.now()
        str_now = _now.strftime("%Y-%m-%d %H:%M:%S")
        _base_name = os.path.basename(__file__)
        _entry = f"""

# Created by `{_base_name}` on {str_now}
export PATH="$PATH:{new_path}"
"""
        try:
            with codecs.open(
                _bashrc, mode="r", encoding="utf-8", errors="replace"
            ) as file_obj:
                _bashrc_text = file_obj.read()
        except (PermissionError, FileNotFoundError):
            return False
        if f'export PATH="$PATH:{new_path}"' in _bashrc_text:
            return True
        _bashrc_text = f"{_bashrc_text}{_entry}"
        try:
            with codecs.open(
                _bashrc, mode="w", encoding="utf-8", errors="replace"
            ) as file_obj:
                file_obj.write(_bashrc_text)
        except (PermissionError, ValueError):
            return False
        return True

    def _sys_default_locale(self, _default: str = "en_US") -> str:
        """Try to get the system locale; fall back to `_default` posix locale
        code"""
        data = None
        if os.name == "nt":
            # NOTE: NT : locale.getdefaultlocale' is deprecated for py 3.15
            # so we can't find the locale data in the form `fr_CA` directly.
            # Most of the time, using Piper's `voices.json` with
            # `data[_item]["language"]["name_english"]`to determine
            # `data[_item]["language"]["family"]` should work to identify
            #  the locale in Posix format, otherwise, default to the
            # `_default`.
            _win_locale = locale.getlocale()[0]
            if os.path.isfile(self.voices_json_path):
                # Checking the Windows locale value against the `voice.json`
                # file was not tested to work for every locale. Accents in
                # a locale vary depending on the recorded speech sample.
                self._update_local_from_json(_win_locale)
                for _try_locale in [
                    f"""{self.name_english}_{self.country_english}""",
                    self.name_english,
                ]:
                    if _win_locale.startswith(_try_locale):
                        _default = self.family
                        break
            return _default
        try:
            if len(locale.getlocale()[0]) != 0:
                self.system_family = locale.getlocale()[0]
            elif len(locale.getdefaultlocale()[0]) != 0:
                self.system_family = locale.getdefaultlocale()[0]
        except AttributeError:
            try:
                if len(locale.getlocale()[0]) != 0:
                    self.system_family = locale.getlocale()[0]
            except AttributeError:
                self.system_family = _default
        return self.system_family

    def _update_local_from_json(self, _j_key: str = "") -> bool:
        """Find a close message for a string that describes a unique voice
        or language using `_j_key` as a search."""
        data = None
        if os.path.isfile(self.voices_json_path):
            try:
                with codecs.open(
                    self.voices_json_path, mode="r", encoding="utf-8", errors="replace"
                ) as file_obj:
                    data = json.load(file_obj)
            except (PermissionError, FileNotFoundError):
                data = None
        if not bool(data):
            return False
        try:
            for _item in data:
                if _j_key.split(".")[0].split("#")[0] in [
                    data[_item]["key"],
                    f"""{data[_item]["name"]}-{data[_item]["quality"]}""",
                    f"""{data[_item]["language"]["code"]}""",
                    f"""{data[_item]["language"]["code"].replace("_", "-")}""",
                ]:
                    # On-line Open Neural Network Exchange (ONNX) resources that Piper TTS supports
                    # Update URLs and other data using current data from `voices.json`.
                    self.key = data[_item]["key"]
                    self.name_english = data[_item]["language"]["name_english"]
                    self.country_english = data[_item]["language"]["country_english"]
                    self.family = data[_item]["language"]["family"]
                    self.code = data[_item]["language"]["code"]
                    self.name = data[_item]["name"]
                    self.quality = data[_item]["quality"]
                    _rname = urllib.parse.quote(self.name)
                    _rkey = urllib.parse.quote(self.key)
                    self.onnx_dir_url = f"{self.piper_voices_url}/resolve/main/{self.family}/{self.code}/{_rname}/{self.quality}/"
                    self.onnx_url = f"{self.onnx_dir_url}{_rkey}.onnx"
                    self.json_url = f"{self.onnx_dir_url}{_rkey}.onnx.json"
                    self.model_card_url = urllib.parse.quote(
                        f"{self.onnx_dir_url}MODEL_CARD"
                    )

                    self.onnx_file_base = os.path.join(
                        self.model_dir,
                        self.family,
                        self.code,
                        self.name,
                        self.quality,
                    )
                    self.model_card_file = os.path.join(
                        self.onnx_file_base, "MODEL_CARD"
                    )
                    self.onnx_file = os.path.join(
                        self.onnx_file_base, f"""{self.key}.onnx"""
                    )
                    self.json_file = f"{self.onnx_file}.json"
        except IndexError:
            return False
        return True

    def update_locale_preferences(self, model="") -> str:
        """Update some specific locale settings. Return a model `key` string."""
        found_model = ""
        if platform.system() == "Linux":
            self.update_bashrc()
        if len(model.split("_")) == 2 and len(model.split("-")) == 3:
            self.system_family = model.split("_")[0]
        else:
            self.system_family = self._sys_default_locale()
        for _test_locale in [self.system_family, self.system_family.split("_")[0]]:
            for lang_model in self.piper_localization:
                if lang_model[0].startswith(_test_locale):
                    found_model = lang_model[0]
                    break
            if len(found_model) != 0:
                break
        if len(found_model) == 0:
            return self.key
        if self._update_local_from_json(found_model):
            pass
        else:
            self.key = found_model
            self.family = self.key.split("_")[0]
            self.code = self.key.split("-")[0]
            self.name = self.key.split("-")[1]
            self.quality = self.key.split("-")[2]
            self.onnx_file_base = os.path.join(
                self.model_dir,
                self.family,
                self.code,
                self.name,
                self.quality,
            )
        _rname = urllib.parse.quote(self.name)
        _rkey = urllib.parse.quote(self.key)
        self.onnx_url = f"{self.piper_voices_url}/resolve/main/{self.family}/{self.code}/{_rname}/{self.quality}/{_rkey}.onnx"
        self.model_card_url = f"{self.piper_voices_url}/resolve/main/{self.family}/{self.code}/{_rname}/{self.quality}/MODEL_CARD"
        self.onnx_file = os.path.join(self.onnx_file_base, f"{self.key}.onnx")
        self.json_file = f"{self.onnx_file}.json"
        return self.key

    def open_uri(self, _uri: str = "") -> bool:
        """Open a web page or a document with a default application"""
        if os.name == "nt":
            # Windows
            try:
                os.startfile(_uri)
                return True
            except (AttributeError, NameError):
                return False
        else:
            for opener in ["xdg-open", "gnome-open", "kde-open", "open"]:
                if os.path.isfile(os.path.realpath(f"/usr/bin/{opener}")):
                    _open = opener
                    return os.system(f'{_open} "{_uri}"')
        return False

    def get_voices_json(self, _always_update: bool = True) -> bool:
        """`voices.json` includes the currently published voice models and
        characterstics including the path to the models' subdirectories.
        Return `True` if the client can download the file, otherwise
        return `False`."""
        _already_is_file = os.path.isfile(self.voices_json_path)
        if not _always_update and _already_is_file:
            self.changed_status = False
            return True
        try:
            if not os.path.isdir(self.model_dir):
                os.makedirs(self.model_dir, exist_ok=True)
            if os.path.isdir(self.model_dir):
                urllib.request.urlretrieve(self.voices_json_uri, self.voices_json_path)
                if self.debug:
                    print(
                        f"`get_voices_json` - Retrieved `{self.voices_json_uri}`\n"
                        + "*" * 60
                    )
                if os.path.isfile(self.voices_json_path):
                    if os.path.getsize(self.voices_json_path) != 0:
                        return True
        except (TimeoutError, ValueError, FileNotFoundError, OSError):
            print(f"`get_voices_json` Error retrieving `{self.voices_json_uri}`")
        self.changed_status = _already_is_file != os.path.isfile(self.voices_json_path)
        return os.path.isfile(self.voices_json_path)

    def get_piper_and_install(
        self,
        processor_family: str = "",
        file_spec: str = "",
        release_ver: str = "",
        key: str = "",
    ) -> bool:
        """Download required assets to set up piper tts."""
        _showdialog = ShowDialog()
        if len(processor_family) == 0:
            self.update_locale_preferences()
            processor_family = self.supported_machines[0]
        if len(file_spec) == 0:
            self.update_locale_preferences()
            file_spec = self.file_spec
        if len(release_ver) == 0:
            self.update_locale_preferences()
            release_ver = self.release_ver
        if len(key) == 0:
            key = self.key
        elif self.key != key:
            self.key = key
            self.update_locale_preferences()
        app_pack = os.path.join(self.download_path, file_spec)
        if not self.quiet:
            _response1 = _showdialog.askyesno(
                self.client_title,
                f"""This {self.client_title} works best with VLC Media Player.

<https://videolan.org>

Do you want to install the contents of `{file_spec}` locally?""",
            )
            if not _response1:
                if self.debug:
                    print("Cancelling setup.")
                return False
            else:
                if self.debug:
                    print(
                        "`get_piper_and_install` - Starting piper installation\n"
                        + "*" * 10
                        + "-" * 50
                    )
                check_release_ver = _showdialog.askstring(
                    "Piper Version",  # title
                    f"""What version of piper do you want? See:
            
        <{self.piper_source}/releases/latest>""",  # prompt
                    release_ver,  # initialvalue
                )
                if not bool(check_release_ver):
                    return False
                elif (
                    len(check_release_ver) > 9
                    and len(check_release_ver.split(".")) == 3
                ):
                    release_ver = check_release_ver
                else:
                    print("Cancelling setup.")
                    return False
                check_processor_family = _showdialog.askstring(
                    "Piper Processor",  # title
                    "What processor do you use?",  # prompt
                    processor_family,  # initialvalue
                )
                if not bool(check_processor_family):
                    return False
                elif check_processor_family in self.supported_machines:
                    processor_family = check_processor_family
                    file_spec = self.file_spec
                else:
                    print("Cancelling setup.")
                    exit()
        else:
            print(f"Installing the contents of `{file_spec}` to your computer...")

        app_pack = os.path.join(self.download_path, file_spec)
        prog_dir = self.program_path
        new_path = os.path.join(prog_dir, "piper")

        try:
            if not os.path.isfile(app_pack):
                urllib.request.urlretrieve(
                    f"{self.piper_source}/releases/download/{release_ver}/{file_spec}",
                    app_pack,
                )
                if os.path.isfile(app_pack):
                    if os.path.getsize(app_pack) != 0:
                        self.changed_status = True
        except (TimeoutError, ValueError, FileNotFoundError, OSError):
            print(f"`get_piper_and_install` Error retrieving `{file_spec}`")
        if os.path.isfile(file_spec):
            if self.debug:
                print(
                    f"`get_piper_and_install` - Retrieved {file_spec}\n"
                    + "*" * 20
                    + "-" * 40
                )
        try:
            os.makedirs(prog_dir, exist_ok=True)
        except (FileExistsError, PermissionError):
            pass
        if os.path.isfile(app_pack) and os.path.isdir(prog_dir):
            try:
                _lext = os.path.splitext(app_pack)[1].lower()
            except IndexError:
                _lext = ""
            if not os.path.isdir(new_path):
                if _lext in [".zip", ".oxt"]:
                    with zipfile.ZipFile(app_pack, "r") as zip_ref:
                        zip_ref.extractall(prog_dir)
                elif _lext in [".gz", ".tgz", ".tar"]:
                    if not os.path.isdir(new_path):
                        subprocess.run(
                            ["tar", "-xf", app_pack, "-C", prog_dir], check=False
                        )
                        if os.path.isdir(new_path):
                            local_bin = os.path.realpath(
                                os.path.expanduser("~/.local/bin")
                            )
                            try:
                                _piper_bin = os.path.join(prog_dir, "piper", "piper")
                                _piper_link = os.path.join(local_bin, "piper-cli")
                                if not os.path.isfile(_piper_link):
                                    os.symlink(_piper_bin, _piper_link)
                            except (FileExistsError, PermissionError):
                                print(
                                    f"Could not create a symbolic link `{prog_dir}/piper/piper` -> `{local_bin}/piper-cli`"
                                )
                current_path = os.environ.get("PATH")
                if not new_path in current_path and os.path.exists(new_path):
                    os.environ["PATH"] = f"{current_path}{os.pathsep}{new_path}"
                    if os.name == "nt":
                        subprocess.run(
                            ["setx", "PATH", os.environ["PATH"]], check=False
                        )
        if os.path.isdir(new_path):
            if self.debug:
                print(
                    f"`get_piper_and_install` - Unpacked archive to `{prog_dir}`\n"
                    + "*" * 30
                    + "-" * 30
                )
            return True
        return False

    def check_onnx_file_ok(self) -> int:
        """Check the speech model's `.onnx` file and return an integer score
        that indicates how well the file sizes and checksums match.
        * `0` means that there is no local file.
        * `1` means that the download was probably incomplete.
        * `3` means that the download was probably complete.
        * `7` means that the file size equals the `voices.json` specification.
        * `15` means that you can be very confident that the file is good.

        Class operators:
        * `self.file_does_not_exist` = 0
        * `self.file_exists = 1`
        * `self.getsize_not_too_small = 2`
        * `self.getsize_matches = 4`
        * `self.md5_matches = 8`"""

        _counter = self.file_does_not_exist
        if os.path.isfile(self.onnx_file):
            _counter += self.file_exists
        else:
            return _counter
        _real_md5 = calculate_md5(self.onnx_file)
        _real_size = os.path.getsize(self.onnx_file)
        if _real_size >= self.onnx_published_size:
            _counter += self.getsize_not_too_small
        if _real_size == self.onnx_published_size:
            _counter += self.getsize_matches
        if _real_md5 == self.onnx_md5:
            _counter += self.md5_matches
        return _counter

    def downloaded_file_log(self, check_no: int = 0, _header="") -> str:
        """Generate a brief report of the download status of a file that
        we tried to download."""
        if len(_header) == 0:
            _header == "The file"
        _log = ""
        if bool(check_no & self.getsize_matches):
            _log = f"{_log}\n* `{_header}` is exactly the expected size."
        elif bool(check_no & self.getsize_not_too_small):
            _log = f"{_log}\n* `{_header}` is not too small."
        elif bool(check_no & self.file_exists):
            _log = f"{_log}\n* `{_header}` is a file."
        if bool(check_no & self.md5_matches):
            _log = f"{_log}\n* `{_header}` passes the MD5 fingerprint check."
        else:
            _log = f"{_log}\n* `{_header}` failed the MD5 fingerprint check."
        if len(_log) == 0:
            _log = f"{_log}\n* `{_header}` failed to download."
        return f" {_log}"

    def report_onnx_integrity(self) -> str:
        """If the checksum is not correct, then ask whether
        to remove the onnx file."""
        _showdialog = ShowDialog()
        _msg = ""
        _onnx_verified = False
        _update_model = os.path.splitext(os.path.basename(self.onnx_file))[0]
        if os.path.isfile(self.onnx_file):
            check_onnx_file_ok = self.check_onnx_file_ok()
            _onnx_verified = check_onnx_file_ok >= self.md5_matches
            _result = self.downloaded_file_log(
                check_onnx_file_ok, f"{_update_model}.onnx"
            )
            _msg = f"""ONNX file summary
-----------------
{_result}

Details
-------

* self.onnx_published_size :        {self.onnx_published_size}
* os.path.getsize(self.onnx_file) : {os.path.getsize(self.onnx_file)}
* self.onnx_md5 :                   "{self.onnx_md5}"
* calculate_md5(self.onnx_file) :   "{calculate_md5(self.onnx_file)}"
* os.path.dirname(self.onnx_file) : "{os.path.dirname(self.onnx_file)}"
+ self.model_dir :                  "{self.model_dir}"  
"""
        if not _onnx_verified and os.path.isfile(self.onnx_file):
            print(ABOUT_MD5_CHECKSUM)
            if not self.quiet:
                if len(_msg) != 0:
                    if _showdialog.askyesno(f"Delete {self.key}.onnx?", _msg):
                        print("Confirmed delete. Please wait...")
                        if os.path.isfile(self.onnx_file):
                            os.remove(self.onnx_file)
        return _msg

    def get_onnx_data(self, model: str = "") -> bool:
        """Download voice model data. Return `True` if successful."""
        _showdialog = ShowDialog()
        prog_dir = self.program_path

        if len(model) != 0:
            model = self.key
        self.update_locale_preferences(model)
        model_card_file = self.model_card_file
        onnx_file = self.onnx_file
        json_file = self.json_file
        onnx_url = self.onnx_url
        if self.debug:
            print(
                f"""`get_onnx_data`
model : {model}
onnx_file : {onnx_file}
onnx_url : {onnx_url}
self.model_card_file = {self.model_card_file}"""
            )
            exit()
        _installed = True
        for _file in [model_card_file, json_file, onnx_file]:
            if not os.path.isfile(_file):
                _installed = False
                break
        if self.check_onnx_file_ok() == self.file_does_not_exist:
            _installed = False
        if _installed:
            _card_text = get_file_text(model_card_file)
            if not self.quiet:
                _showdialog.showinfo(
                    self.client_title,
                    f"""{_card_text}
## Size

{round(self.onnx_published_size * 0.000001, 1)} MB""",
                )
            else:
                print(_card_text)
            return True
        try:
            if not os.path.isfile(json_file):
                os.makedirs(os.path.dirname(json_file), exist_ok=True)
                urllib.request.urlretrieve(self.json_url, json_file)
                if self.debug:
                    print(
                        f"`get_onnx_data` - Retrieved `{self.json_url}`\n"
                        + "*" * 40
                        + "-" * 20
                    )
                if os.path.isfile(json_file):
                    if os.path.getsize(json_file) != 0:
                        self.changed_status = True
        except (TimeoutError, ValueError, FileNotFoundError, OSError):
            print(f"Error retrieving `{self.json_url}`")
        try:
            if not os.path.isfile(model_card_file):
                os.makedirs(os.path.dirname(model_card_file), exist_ok=True)
                urllib.request.urlretrieve(self.model_card_url, model_card_file)
                if self.debug:
                    print(
                        f"`get_onnx_data` - Retrieved `{self.model_card_url}`\n"
                        + "*" * 45
                        + "-" * 15
                    )
                if os.path.isfile(model_card_file):
                    if os.path.getsize(model_card_file) != 0:
                        self.changed_status = True
        except (TimeoutError, ValueError, FileNotFoundError, OSError):
            print(f"Error retrieving `{self.model_card_url}`")
        _card_text = get_file_text(model_card_file)
        if (not self.quiet) and len(_card_text) != 0:
            if _showdialog.askyesno(
                f"Download {self.key}.onnx?",
                f"""{_card_text}
## Size

{round(self.onnx_published_size * 0.000001, 1)} MB""",
            ):
                print("Confirmed download. Please wait...")
            else:
                return False
        try:
            if bool(self.check_onnx_file_ok() & self.md5_matches):
                if os.path.isfile(onnx_file):
                    if os.path.isfile(f"{onnx_file}.bak"):
                        os.remove(f"{onnx_file}.bak")
                    os.rename(onnx_file, f"{onnx_file}.bak")
            if not os.path.isfile(onnx_file):
                print(
                    f"""
                      
Model Information
-----------------

```
{_card_text}
```

Streaming
---------

On supported platforms, [VideoLAN VLC](https://www.videolan.org/)
can help reduce response time for long texts by acting as a "sink"
for Piper's raw audio "source". On some portable computers, using
a visual media streamer can stop the computer from going to sleep
while audio is streaming.

VLC is very good for streaming Piper raw audio output on the Windows
platform.

More
----

Learn more about Piper TTS.

<{self.piper_source}>

Listen to samples of different voice models.

<{self.piper_samples_url}>

Get VideoLan VLC Media Player

<https://www.videolan.org/>

Downloading ONNX Piper Data
---------------------------
                      
Downloading `{self.key}.onnx` data takes a few moments.
When you see a dialogue, you will be ready to use the voice model.
On Windows, `piper` will be in your system `PATH` when you close
the current console session and restart a new session. On Linux
platforms, this installer creates a link to the program at
`~/.local/bin/piper-cli`. Check your Linux desktop documentation
to find out how to check your system PATH. If you install the
python3 `pipx` version of piper on a Linux platform, then running
`piper` runs the pipx version and `piper-cli` runs the locally
installed command line interface.
"""
                )
                os.makedirs(os.path.dirname(onnx_file), exist_ok=True)
                urllib.request.urlretrieve(onnx_url, onnx_file)
                if self.debug:
                    print(
                        f"`get_onnx_data` - Retrieved `{onnx_url}\n"
                        + "*" * 50
                        + "-" * 10
                    )
                if os.path.isfile(onnx_file):
                    if os.path.getsize(onnx_file) != 0:
                        self.changed_status = True
        except (TimeoutError, ValueError, FileNotFoundError, OSError):
            print(f"Error retrieving `{onnx_url}`")
        _success = False
        for _piper_test in [
            "piper-cli",
            "piper",
            os.path.realpath(
                f"{prog_dir}/piper/piper"
            ),  # Windows, This tool local install
            os.path.realpath(
                os.path.expanduser("~/.local/bin/piper")
            ),  # pipx local library
            os.path.realpath(
                os.path.expanduser("~/.local/bin/piper-cli")
            ),  # link to binary
            os.path.realpath(
                os.path.expanduser("usr/bin/piper")
            ),  # link to systembinary
        ]:
            try:
                _success = bool(subprocess.run([_piper_test, "-h"], check=True))
                break
            except (FileNotFoundError, PermissionError, OSError):
                _success = False

        _msg = f"""{self.client_title} did not work on your computer.

    The application might be corrupt or it might be incompatible with the
    {self.this_machine} computer processor."""
        if not _success:
            if not self.quiet:
                _showdialog.showinfo(
                    self.client_title,
                    _msg,
                )
            else:
                print(_msg)
        _msg = "Finished installing resources to your computer."
        if self.quiet:
            print(_msg)

            return True
        if self.changed_status and _success:
            _showdialog.showinfo(
                self.client_title,
                _msg,
            )
        elif not self.quiet:
            _reply = _showdialog.askyesno(
                self.client_title, "Do you want to view or edit the piper directories?"
            )
            if _reply == True:
                for _directory in [self.program_path, self.model_dir]:
                    if os.path.isdir(_directory):
                        self.open_uri(_directory)
            else:
                print("Edit the directories? You answered No.")
                return False

            if _showdialog.askyesno(
                self.client_title,
                f"Do you want to open <{self.piper_samples_url}>?",
            ):
                self.open_uri(self.piper_samples_url)
        return True

    def create_model_dirs(self) -> bool:
        """Use the voices.json file to update the piper-voices directory"""
        created_new = False
        if not os.path.isfile(self.voices_json_path):
            return False
        try:
            with codecs.open(
                self.voices_json_path, mode="r", encoding="utf-8", errors="replace"
            ) as file_obj:
                data = json.load(file_obj)
        except (PermissionError, FileNotFoundError):
            return False
        try:
            if not bool(data):
                return False
            for _item in data:
                new_dir = os.path.join(
                    self.model_dir,
                    data[_item]["language"]["family"],
                    data[_item]["language"]["code"],
                    data[_item]["name"],
                    data[_item]["quality"],
                )
                if not os.path.isdir(new_dir):
                    _display_dir = new_dir
                    if os.name == "nt":
                        _display_dir = new_dir.unicodedata.normalize(
                            "NFKD", new_dir.encode("ascii", "namereplace").decode()
                        )
                    print(f"Create directory <{_display_dir}>")
                    os.makedirs(new_dir, exist_ok=True)
                    created_new = True
        except (IndexError, OSError):
            return False
        return created_new

    def check_model_key_and_english_str(self, _query: str = "") -> str:
        """Check that that the query term uniquely identifies a voice package
        or that the model name matches a key in the voices.json file."""
        data = None
        ok_field = None
        if not os.path.isfile(self.voices_json_path):
            return ""
        else:
            try:
                with codecs.open(
                    self.voices_json_path, mode="r", encoding="utf-8", errors="replace"
                ) as file_obj:
                    data = json.load(file_obj)
            except (PermissionError, FileNotFoundError):
                data = None
        if bool(data):
            # `"name"` is the model name, not the speaker name.
            # a model can have hundreds of speakers or just one.
            try:
                for _item in data:
                    # `name plus quality specified uniquely identifies a voice, but
                    # just the name does not (i.e. `thorsten-high`, `thorsten-low` etc.)
                    _alias = "-".join([data[_item]["name"], data[_item]["quality"]])
                    _aliases = data[_item]["aliases"]
                    if len(_aliases) != 0:
                        _alias = _aliases[0]
                    for field in [
                        data[_item]["key"],
                        _alias,
                        data[_item]["name"],
                    ]:
                        if _query == field:
                            _win_locale = f"""{data[_item]["language"]["name_english"]}_{data[_item]["language"]["country_english"]}"""
                            # Determine the published file size and a
                            # hexadecimal MD5 hash
                            _onnx_path = "/".join(
                                [
                                    data[_item]["language"]["family"],
                                    data[_item]["language"]["code"],
                                    data[_item]["name"],
                                    data[_item]["quality"],
                                ]
                            )
                            _onnx_file = f"""{data[_item]["key"]}.onnx"""
                            self.onnx_published_size = data[_item]["files"][
                                f"{_onnx_path}/{_onnx_file}"
                            ]["size_bytes"]
                            self.onnx_md5 = data[_item]["files"][
                                f"{_onnx_path}/{_onnx_file}"
                            ]["md5_digest"]
                            self.onnx_json_published_size = data[_item]["files"][
                                f"{_onnx_path}/{_onnx_file}.json"
                            ]["size_bytes"]
                            self.onnx_json_md5 = data[_item]["files"][
                                f"{_onnx_path}/{_onnx_file}.json"
                            ]["md5_digest"]
                            self.model_card_published_size = data[_item]["files"][
                                f"{_onnx_path}/MODEL_CARD"
                            ]["size_bytes"]
                            self.model_card_md5 = data[_item]["files"][
                                f"{_onnx_path}/MODEL_CARD"
                            ]["md5_digest"]

                            # Look through the language data to find items that you might use
                            # to identify a specific voice.
                            if len(_alias) == 0:
                                if os.name == "nt":
                                    _alias = _win_locale
                                else:
                                    _alias = _query
                            # `ok_field `is a list with a length of 4 that follows the data
                            # pattern of `self.piper_localization``. Add the list at the top
                            # of `self.piper_localization`, if it is not one of the presets
                            # for the locale.
                            ok_field = [
                                data[_item]["key"],
                                data[_item]["language"]["name_english"],
                                data[_item]["language"]["country_english"],
                                _alias,
                            ]
                            if ok_field not in self.piper_localization:
                                self.piper_localization = [
                                    ok_field
                                ] + self.piper_localization
                            break
                    if bool(ok_field):
                        break
            except (KeyError, UnboundLocalError):
                ok_field = None
                data = None

        _nstr = NormalizeStr()
        if len(_query) == 0:
            return self.key
        _key = 0
        _language = 1
        _country = 2
        _alt = 3
        s_query = _nstr.normalize_str(_query)
        for _list in self.piper_localization:
            s_key = _nstr.normalize_str(_list[_key])
            s_language = _nstr.normalize_str(_list[_language])
            s_country = _nstr.normalize_str(_list[_country])
            s_alt = _nstr.normalize_str(_list[_alt])
            s_code = s_key.split("-", 1)[0]
            s_family = s_key.split("_", 1)[0]
            list_key = s_key.split("-")
            s_quality = list_key[len(list_key) - 1]
            s_name = list_key[len(list_key) - 2]
            for _test in [
                s_key,
                f"{s_name}{s_quality}" f"{s_language}{s_country}",
                s_language,
                s_code,
                s_alt,
                s_family,
            ]:
                if s_query == _test:
                    # On-line Open Neural Network Exchange (ONNX) resources that Piper TTS supports
                    # Update URLs and other data using current data from `voices.json`.
                    self.key = data[_item]["key"]
                    return _list[_key]
        return ""

    def piper_is_installed(self, _cmd: str = "-h") -> bool:
        """Try running Piper"""
        if len(_cmd) == 0:
            return False
        _checks = [
            "piper.exe",
            "piper-cli",
            os.path.realpath(f"{self.program_path}/piper/piper"),
            "piper",  # The Linux pipx or system packaged version.
        ]
        if os.name == "nt":
            _checks = [
                os.path.realpath(f"{self.program_path}/piper/piper"),
                "piper",
                "piper.exe",
                "piper-cli",
            ]
        for trial in _checks:
            try:
                return bool(subprocess.run([trial, _cmd], check=True))
            except (
                FileNotFoundError,
                PermissionError,
                OSError,
                subprocess.CalledProcessError,
            ):
                continue
        return False


class NormalizeStr:
    """Make it easier to match strings by changing the srring
    to lower case and removing most punctuation and non-print
    characters."""

    def __init__(self):
        """Character translation"""
        try:
            self.remove = str.maketrans(
                {
                    " ": "",
                    ",": "",
                    "\\": "",
                    "{": "",
                    "}": "",
                    '"': "",
                    "@": "",
                    "|": "",
                    "'": "",
                    "%": "",
                    "$": "",
                    "&": "",
                    "^": "",
                    "!": "",
                    "=": "",
                }
            )
        except AttributeError:
            self.remove = None

    def normalize_str(self, _query: str = "") -> str:
        """Standardize user string input"""
        if len(_query) == 0:
            return ""
        _test = _query.lower()
        if self.remove:
            return str(_test.translate(self.remove))
        return ""


def main() -> None:
    """Set default architecture and release with command line arguments."""

    _get_piper = GetPiperData()
    _py3 = "python3"
    if os.name == "nt":
        _py3 = "python.exe"
    _description = f"""Use `{_py3} {os.path.basename(__file__)} --help`.

[Piper]({_get_piper.piper_source})
is a fast and local text to speech system.

This tool downloads the `piper` program package and the language model
resources. Your computer will connect to the Internet.

Downloading resources can take a few moments. Please be patient. On 
supported platforms, a dialog will confirm that the downloads have
completed.

"""
    if platform.system() not in ["Linux", "Windows"]:
        print(
            f"""UNSUPPORTED PLATFORM
====================

This Piper client does not support the {platform.system()} system.

{_description}"""
        )
        exit()
    _time_to_update = check_if_file_is_stale(_get_piper.voices_json_path)
    if not _get_piper.get_voices_json(_time_to_update):
        print(
            f"""The `{_get_piper.voices_json_path}`
settings file is missing or out of date.

The online resource at <{_get_piper.voices_json_uri}>
is unavailable. Check that your computer is on-line or try again later.

{_description}"""
        )
        if not os.path.isfile(_get_piper.voices_json_path):
            print("\n\nExiting...")
            exit()
    onnx_item = _get_piper.update_locale_preferences()
    # Update
    _default_model = _get_piper.check_model_key_and_english_str(onnx_item)
    # Read the command line preferences
    parser = argparse.ArgumentParser(description=_description)
    parser.add_argument(
        "--language_code",
        default="",
        help=f"""Language_code (default: `{_get_piper.name_english}`)
or `<name>-<quality>` (i. e.: `thorsten-medium`)""",
    )
    parser.add_argument(
        "--processor_family",
        default=_get_piper.supported_machines[0],
        help=f"Processor family (default: `{_get_piper.supported_machines[0]}`)",
    )
    parser.add_argument(
        "--release_ver",
        default=_get_piper.release_ver,
        help=f"Release version (default: `{_get_piper.release_ver}`)",
    )
    parser.add_argument(
        "--hide_ui",
        action="store_true",
        help="""Disable tk dialogs, even if python includes the optional
`tkinter` python library.""",
    )
    args = parser.parse_args()
    _get_piper.quiet = args.hide_ui
    file_spec = _get_piper.file_spec
    _update_model = onnx_item
    if len(args.language_code) != 0:
        _update_model = _get_piper.check_model_key_and_english_str(args.language_code)
        _get_piper.key = _update_model
    else:
        _get_piper.key = _default_model
        onnx_item = _get_piper.update_locale_preferences()
    print(
        f"""
Piper Text to Speech Installation
=================================
          
{_description}

First, let's confirm what you want to download.

"""
    )
    print(
        f"""
* [{_get_piper.file_spec}]({_get_piper.piper_source})
* [{_update_model}]({_get_piper.piper_samples_url})
"""
    )
    if not _get_piper.piper_is_installed():
        # Try getting the program and a voice for the requested language voice
        # or the default voice for your language.
        _get_piper.create_model_dirs()
        _get_piper._update_local_from_json()
        if _get_piper.get_piper_and_install(
            args.processor_family, file_spec, args.release_ver, onnx_item
        ):
            _get_piper.get_onnx_data()
    else:
        # You have the program, so get a voice for the requested language voice
        # or the default voice for your language.
        _get_piper.create_model_dirs()
        _get_piper._update_local_from_json()
        _get_piper.get_onnx_data(_update_model)
    print(_get_piper.report_onnx_integrity())


if __name__ == "__main__":
    main()

###############################################################################
# Read Text Extension
#
# Copyright And License
#
# (c) 2024 [James Holgate Vancouver, CANADA](readtextextension(a)outlook.com)
#
# THIS IS FREE SOFTWARE; YOU CAN REDISTRIBUTE IT AND/OR MODIFY IT UNDER THE
# TERMS OF THE GNU GENERAL PUBLIC LICENSE AS PUBLISHED BY THE FREE SOFTWARE
# FOUNDATION; EITHER VERSION 2 OF THE LICENSE, OR(AT YOUR OPTION)ANY LATER
# VERSION.  THIS SCRIPT IS DISTRIBUTED IN THE HOPE THAT IT WILL BE USEFUL, BUT
# WITHOUT ANY WARRANTY; WITHOUT EVEN THE IMPLIED WARRANTY OF MERCHANTABILITY OR
#  FITNESS FOR A PARTICULAR PURPOSE.SEE THE GNU GENERAL PUBLIC LICENSE FOR MORE
# DETAILS.
#
# YOU SHOULD HAVE RECEIVED A COPY OF THE GNU GENERAL PUBLIC LICENSE ALONG WITH
# THIS SOFTWARE; IF NOT, WRITE TO THE FREE SOFTWARE FOUNDATION, INC., 59 TEMPLE
# PLACE, SUITE 330, BOSTON, MA 02111-1307  USA
###############################################################################
