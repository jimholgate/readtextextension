#!/usr/bin/env python3
# -*- coding: UTF-8-*-
"""Module supporting a local speech synthesis server using a python virtual
environment.

+ [Rhasspy Piper TTS
server](https://github.com/rhasspy/piper/blob/master/src/python_run/README_http.md)
* [Piper 1 GPL HTTP
API](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/API_HTTP.md)
"""
APP_DESCRIPTION = r"""---
title: "Using piper-server"
author: "James Holgate"
date: "2025.08.21"
language: "en-CA"
---

# Using the piper-tts client.

Make sure that your server is running. If you installed it with python pip, then
you can find detailed information with a command like this (replacing `py` with
the actual python command for your platform...)

```Powershell
py - m piper.http_server -h
```

The specific file locations will vary according to your setup and platform.
Here is an example:

```Powershell
py -m piper.http_server --model en_GB-jenny_dioco-medium --speaker 0 --data-dir "$env:USERPROFILE\AppData\Roaming\piper-tts\piper-server\models"
```

With “Enable Experimental Features” enabled in LibreOffice, enter the path to
Python in the **Command** dialog option. For example:

```
C:\Program Files\LibreOffice\program\python.exe
```

In the **Command Line Options**, enter or select:

```
"(NETWORK_READ_TEXT_PY)" --language (SELECTION_LANGUAGE_CODE) "(TMP)"
```

You can test whether the server works with the Read Text Extension using your
local machine’s IP address (replace the address below with your actual IP):

```
"(NETWORK_READ_TEXT_PY)" --url "http://192.168.0.105:5000" --language (SELECTION_LANGUAGE_CODE) "(TMP)"
```

# Network Overview

Piper server won't work on all computers, and the methods will vary depending
on the platform. These instructions are descriptive, not perscriptive.

**Note:** How well this runs depends on your device and home network.  
Some networks block peer-to-peer connections for security reasons.  
If you’re on Windows, try Docker or Podman with a Linux WSL setup,  
or run Piper-TTS on another Linux computer in your network for smoother
performance.

# Installing Piper-TTS on Linux

Installing Python packages locally with `python3-pip` on Debian systems may
trigger errors due to environment restrictions, like an "externally-managed
environment" warning. While workarounds exist, they can lead to unpredictable
behavior when packages are updated.

A more stable and portable solution is to use `podman` or `docker` to run
`piper-server`. This approach provides an isolated environment, consistent
behavior across different Linux distributions.

The default `piper-tts` installation does not include all the libraries needed
to run the Piper HTTP server. You’ll need to install it using `piper-tts[http]`
instead of `piper-tts`. 

You can find out more at the HTTP API page on
[GitHub](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/API_HTTP.md)

## Prerequisites

Before you begin, make sure you have:

- A system that can run `podman` or `docker`  
- A user in the `sudo` or `wheel` group
- An active internet connection

### Make a home network piper-server using pipx

Use this method on a computer that stays at home.

```bash
pipx install piper-tts && pipx inject piper-tts flask
pipx ensurepath
mkdir -p ~/.var/app/com.mikeasoft.pied/data/pied/models
cd ~/.var/app/com.mikeasoft.pied/data/pied/models
~/.local/pipx/venvs/piper-tts/bin/python3 -m piper.download_voices \
    en_GB-jenny_dioco-medium

~/.local/pipx/venvs/piper-tts/bin/python3 \
    -m piper.http_server \
    --data-dir ~/.var/app/com.mikeasoft.pied/data/pied/models \
    --model en_GB-jenny_dioco-medium \
    --speaker 0
```

## 1. Install Podman or Docker

- Use podman and install piper-tts as a user with the minimum permission to
  restrict the piper-server to the host computer.
- Update package lists and install a container management tool. Debian, Red
  Hat and related derivatives include `podman` in their normal repositories.
  
If you are using a Debian derivative, use `apt-get`.

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install podman
```
On current releases of Red Hat derivatives, `podman` tools are installed
by default. 

---

## 2. Install Piper-TTS Server

Podman can use a short `Dockerfile` script to install and activate the piper-tts server.

```Dockerfile
FROM python:3.11-slim

# Create a non-root user and models directory
RUN groupadd --system piper && \
    useradd  --system --gid piper --home-dir /home/piper piper && \
    mkdir -p /models && \
    chown -R piper:piper /models

# Switch to piper, set up paths
USER piper
ENV HOME=/home/piper
ENV PATH="${HOME}/.local/bin:${PATH}"
WORKDIR /home/piper

# Upgrade pip inside the container's user environment
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Piper-TTS & Flask into ~/.local
RUN pip install --no-cache-dir piper-tts flask

# Download your model into /models
ARG MODEL=en_GB-jenny_dioco-medium
RUN python3 -m piper.download_voices ${MODEL} --download-dir /models

EXPOSE 5000

CMD ["python3", "-m", "piper.http_server", \
     "--host", "0.0.0.0", \
     "--port", "5000", \
     "--data-dir", "/models", \
     "--model", "en_GB-jenny_dioco-medium", \
     "--speaker", "0", \
     "--length_scale", "1", \
     "--noise_scale", "0.667", \
     "--noise_w", "0.8"]
```

Name the file `Dockerfile` (no extension) and install into a new blank
directory. In the terminal, use the `cd` command to change to that directory
before creating the `piper-tts` container.

**Note the "." at the end of the podman command below.**

```bash
cd '~/podman_piper-tts'
podman build -t piper-tts .
```

## 3. Use the server with a single voice model right away.

The `Dockerfile` installer recipe included a step to install an English voice
by default. The most recent version of `piper-server` also serves other voices
in a directory that you specify. This example uses the `flatpak` version of
the Pied speech manager models directory as a source of additional voice\
models and configuration files. 

```bash
mkdir -p ~/.var/app/com.mikeasoft.pied/data/pied/models
cd ~/.var/app/com.mikeasoft.pied/data/pied/models
podman run -d \
  --name piper-tts \
  -p 5000:5000 \
  -v ~/.var/app/com.mikeasoft.pied/data/pied/models:/models:Z \
  piper-tts
```

## 4. Check the HTTP Server

You can check the available addresses for the piper-tts server service using
the log command.

```bash
podman logs -f piper-tts
```

The log output shows that the server is listening at `http://127.0.0.1:5000/`.
If the server is configured to do so, the server is also listening at the
computer's home IP address or a private address in the case of restricted
permission settings. If the server has permission, then the address allows
other machines on the same home network to access the service.

You can tell which voice models that a  piper client on your computer can
access by opening your browser and pasting <http://127.0.0.1:5000/voices>
into the address bar.

Also check whether you can read the available voices on other computers in
your home network by browsing to the second address shown in the server
terminal window.

If you use the extension on another computer on your home network, and the
server permissions allow it, you can access the home server by specifying
the specific address of the piper-server in the main dialog.

For example, using Avahi to define a local service name:

```
"(NETWORK_READ_TEXT_PY)" --url "http://piper.local:5000" --language (SELECTION_LANGUAGE_COUNTRY_CODE) "(TMP)"
```


## 5. Test the Server

Use `curl` or any HTTP client to synthesise speech:

```bash
curl -X POST -H 'Content-Type: application/json' \
     -d '{ "text": "Hello from Piper on this computer!" }' \
     -o output.wav http://127.0.0.1:5000
```

Play `output.wav` to confirm everything is working.

---

## 6. Download more Voice Models

If you install Pied using a `flatpak` command, then you can use it to add and
remove voice models in the directory shown above.

The [pied website](https://github.com/Elleo/pied) hosts the latest version/

Otherwise, you can modify the `Dockerfile` to add additional models to the
container.


## Desktop file

You can save a `desktop` file in a local applications settings file to make a
system menu item to start the server.

```ini
[Desktop Entry]
Type=Application
Name=Piper Speech Synthesis
Name[fr]=Synthèse vocale Piper
Name[es]=Síntesis de voz Piper
Name[de]=Piper Sprachsynthese
Name[pt]=Síntese de fala Piper
Name[it]=Sintesi vocale Piper
Name[fi]=Piper-puheentunnistus
Comment=Start the Piper speech synthesis server
Comment[fr]=Démarrer le serveur de synthèse vocale Piper
Comment[es]=Iniciar el servidor de síntesis de voz Piper
Comment[de]=Piper-Sprachsynthese-Server starten
Comment[pt]=Iniciar o servidor de síntese de fala Piper
Comment[it]=Avvia il server di sintesi vocale Piper
Comment[fi]=Käynnistä Piper-puheentunnistuspalvelin
Exec=gnome-terminal -- bash -c 'podman run --network host -v ~/.var/app/com.mikeasoft.pied/data/pied/models:/models:Z piper-tts'
Terminal=true
Icon=/usr/share/icons/gnome/256x256/apps/preferences-desktop-accessibility.png
Categories=Utility;Accessibility;
StartupNotify=true
```
Save it as `~/.local/share/applications/us.synesthesiam.piper-server.desktop`
and set the file to executable.

```bash
chmod +x ~/.local/share/applications/us.synesthesiam.piper-server.desktop
```

On a standard Linux desktop, the new item appears in your normal menu system once 
you log out and log in again.

## Using Python PIP with Windows

This will quickly get you up and running with the piper-tts server API.

You can read a quick summary of the installation process on the OHF-Voice piper
[HTTP API](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/API_HTTP.md)
reference page.

### Why use piper-server with Python instead of the executable program on Windows?

* Manage voice models using the most up-to-date version of piper.
* On some computers, speech starts notably faster.
* Explore the server command parameters to optimize piper for your specific
  architecture and network.
* Depending on your network, you can use text-to-speech via the piper-server
  client on devices that don’t normally support neural voice models.

### Install or update Python

Install a recent version of [Python 3](https://python.org) and follow the
instructions on the website to complete the setup. You can confirm Python
is ready if these commands show version numbers:

```cmd
py --version
pip --version
```

### Install the server

```cmd
py -c "import os; os.makedirs(os.path.expanduser('~/AppData/Roaming/piper-tts/piper-server/models'), exist_ok=True)"
cd %USERPROFILE%\AppData\Roaming\piper-tts\piper-server\models
py -m pip install piper-tts[http]
py -m piper.download_voices en_GB-jenny_dioco-medium
```

### Run the server

You can use the classic command prompt program:

```cmd
py -m piper.http_server -h
py -m piper.http_server --model en_GB-jenny_dioco-medium --speaker 0 --data-dir "%USERPROFILE%\AppData\Roaming\piper-tts\piper-server\models"
```

Use Powershell for cleaner looking output:

```powershell
py -m piper.http_server --model en_GB-jenny_dioco-medium --speaker 0 --data-dir "$env:USERPROFILE\AppData\Roaming\piper-tts\piper-server\models"
```

Check the installation by opening a web browser and visiting:

<http://127.0.0.1:5000/voices>

If the browser shows a JSON data string, the server is working.

## Conclusion

- You can use a speech server instead of a standard installation to provide
  text to speech service on platforms that do not support piper natively,
  or where system policies do not allow a program extension to start another
  program.
- Explore additional command-line options.  
- Piper TTS includes many voice styles and languages. Read the licenses for
  individual models to review the terms.
  """

import os

try:
    import json
    import re
    import tempfile
    import time
    import urllib
    import urllib.request

    # import subprocess
    BASICS_OK = True
except (ImportError, AssertionError):
    BASICS_OK = False

import netcommon
import netsplit
import readtexttools
import piper_read_text
import ping_local_network


class GPLPiperClass(object):
    """
    July 13, 2025. synesthesiam (Michael Hansen) committed an update
    for piper-server that allows users to switch models, speakers and
    other settings.

    NOTE: The new version supports downloading models and
    configuration file using a python piper library.

    * `text` (required) - text to synthesize
    * `voice` (used) - name of voice to use
    * `speaker` (omitted) - name of speaker (Not used)
    * `speaker_id` (used) - speaker# for multi-speaker voices
    * `length_scale` (used) - speaking speed; defaults to 1
    * `noise_scale` (omitted) - speaking variability
    * `noise_w_scale` (omitted) - phoneme width variability

    See:
    <https://github.com/OHF-Voice/piper1-gpl/blob/main/CHANGELOG.md>

        `(venv)`
        `python -m piper.http_server --model ~/pathto/en_US-lessac-medium.onnx`

        `* Serving Flask app 'http_server'`
        `* Debug mode: off`
        `INFO:werkzeug:WARNING: This is a development server. Do not use it in a`
        `production deployment. Use a production WSGI server instead.`

        `* Running on all addresses (0.0.0.0)`
        `* Running on http://127.0.0.1:5000`
        `* Running on http://nnn.nnn.n.nnn:5000`"""

    def __init__(self) -> None:
        """No User web interface, so retrieve a web json file determine the
        settings and available models to create WAVE audio files."""
        _common = netcommon.LocalCommons()
        self.locker = _common.locker
        self.common = _common
        self.add_pause = _common.add_pause
        self.pause_list = _common.pause_list
        self.debug = _common.debug
        self.url = "http://127.0.0.1:5000"  # Default URL port 5000
        self.workgroup_url = None
        self.workgroup_urls = []
        self.help_heading = "OHF-Voice Piper Server"
        self.wave = "GPL-Piper.wav"
        self.help_url = (
            "https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/API_HTTP.md"
        )
        self.audio_format = ["wav"][0]
        self.input_types = ["TEXT"]
        self.local_dir = "default"
        self.speaker_id_key_list = []

        self.accept_voice = [
            "",
            "all",
            "auto",
            "child_female`",
            "child_male1",
            "female",
            "male",
            "piper",
            "piper-network",
            "ohf-voice",
            "localhost",
            "local_server",
        ]
        self.search_network_voice = ["piper-network"]
        self.ok = False
        self.piper_voice_resource = None
        self.piper_json = None
        self.lengthscale = 1
        self.home_network_scan_disabled = False
        self.host_latency = float(0.0)

    def _piper_server_script_path(self) -> str:
        """Find a `site-packages/http_server.py` piper-server script path if
        it was installed in a local posix directory using `pipx`, otherwise `""`.

        Debian discouaages installing utility programs with pip unless you
        create a virtual environment. If you use `sudo apt-get install pipx`,
        then you can install the program using the instructions shown in
        `APP_DESCRIPTION` above."""
        if not netcommon.which("pipx"):
            return ""

        for piper_exe in ["piper-cli", "piper"]:
            piper_path = os.path.realpath(netcommon.which(piper_exe))
            if f"venvs{os.sep}piper-tts" in piper_path:
                lindex = len(piper_path.split(os.sep))
                base_path = os.sep.join(
                    (piper_path.split(os.sep))[: lindex - 2] + ["lib"]
                )
                pattern = re.compile(r"python\d+.\d+")
                for entry in os.listdir(base_path):
                    full_path = os.path.join(base_path, entry)
                    if os.path.isdir(full_path) and pattern.fullmatch(entry):
                        test_path = os.path.join(
                            full_path, "site-packages", "piper", "http_server.py"
                        )
                        if os.path.isfile(test_path):
                            return test_path
        return ""

    def fetch_with_latency(self, url: str):  # -> [Any | None, float]
        """
        Fetch JSON from `url` and return a tuple of
        (parsed_data, latency_seconds).
        """
        start = time.perf_counter()
        try:
            with urllib.request.urlopen(url) as resp:
                body = resp.read()
            latency = time.perf_counter() - start
            self.host_latency = latency
        except Exception as e:
            print("Exception:  ", e)
            body = None
            latency = self.host_latency

        return body, latency

    def ping_local_server(
        self, local_server: str = "http://127.0.0.1:5000", net_servers=None
    ) -> bool:
        """If local_server returns a file of length not equal to zero, then
        return `True`, but if the value is zero or there is an error, return
        `False`"""

        resp_content_voices = ""
        if not BASICS_OK:
            return False
        _success = False
        last_uri = ""
        error_found = ""
        self.common.set_urllib_timeout(2)  # Load locally hosted json code using GET
        if net_servers:
            if not self.home_network_scan_disabled:
                test_list = net_servers
                if local_server:
                    test_list.append(local_server)
        else:
            test_list = [local_server, self.url] + self.workgroup_urls
        for json_uri in test_list:
            if ":" not in json_uri:
                continue
            json_url = json_uri.split("?")[0].rstrip("/ \n")
            if last_uri == json_url:
                continue
            last_uri = json_url
            json_test = f"""{json_url}/voices"""

            try:
                resp_content_voices, latency = self.fetch_with_latency(json_test)
                self.piper_json = json.loads(resp_content_voices)
                _success = True
                self.url = json_url
                if json_url in self.workgroup_urls:
                    self.workgroup_url = json_url
                break

            except Exception as e:
                self.common.set_urllib_timeout(2)
                _success = False
                error_found = e
        if not _success:
            if local_server not in ["http://127.0.0.1:5000", ""]:
                print(
                    f"""WARNING:
Piper-server cannot connect to the service at {json_test}.

* Check the server by opening the service in your web browser.
* Piper-server does not share your data, but it needs to make a local
  connection to verify what voice models are available and to stream
  the speech from a locally hosted device.
* In some cases, restarting your computer or reinstalling piper-server
  can help.

To access another computer on your local network, specify the address
the address using the `--url "{json_url}"` switch in the
main dialog using the ip address of device running the piper-server.

-----

If you do not know the ip address of the server machine, you can scan your
local network by entering `piper-network` as the voice to use. The time to
complete the the scan depends on the speed and size of your network, and the
success of the scan depends on the security settings of your account, the
device and the network. If the user running a piper-tts server does not
have permission to serve to other computers, then the server sends a
"connection refused" message to the client.

See: <https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/API_HTTP.md>

{self._piper_server_script_path()}

Exception: """,
                    error_found,
                )
            return False
        if self.piper_json:
            self.common.set_urllib_timeout(
                7.0 + latency
            )  # 7 seconds allows time to load a model
            return True
        self.wave = "Rhasspy-Piper.wav"
        self.help_heading = "Rhasspy Piper Server"
        self.help_url = (
            "https://github.com/rhasspy/piper/blob/master/src/python_run/README_http.md"
        )
        return False

    def _try_other_machines(self) -> bool:
        """Look for a piper-tts server on other machines in the network"""
        if self.home_network_scan_disabled:
            return False
        _pinglocal = ping_local_network.PingLocals()
        _custom_ignore = None
        host_list = _pinglocal.valid_local_machine_addresses(_custom_ignore)
        test_list = []
        for home_test in host_list:
            test_list.append(f"http://{home_test}:5000")
        if len(test_list) > 0:
            return self.ping_local_server("http://127.0.0.1:5000", test_list)
        return False

    def speaker_count(self, voice_model: str = "") -> int:
        """Use piper json data to determine the number of speakers. Note that
        the `speaker_id` begins at `0`, so the upper bound of the speaker list
        is the `speaker_count - 1`"""
        if not self.piper_json:
            if not self.ping_local_server():
                if not self._try_other_machines():
                    self.home_network_scan_disabled = True
                    return False
        if not self.piper_json:
            return 0
        if not voice_model:
            return 0
        data = self.piper_json
        for item in data:
            if voice_model.strip() == "-".join(
                [
                    data[item]["language"]["code"],
                    data[item]["dataset"],
                    data[item]["audio"]["quality"],
                ]
            ):
                return data[item]["num_speakers"]
        return 0

    def language_supported(
        self, _iso_lang: str = "en-US", alt_local_url: str = "", _vox=""
    ) -> bool:
        """If the current installation of the Piper server only serves one
        model at a time, then the client assumes you use the language of your
        system locale. and returns `True` if the requested language matches
        the system language locale. If you use a Piper server that supports
        multiple models and voices, then the support extends to the languages
        of the models that you have installed.

        `iso_lang` can be in the form `en-US` , "en_US`. or `en`."""

        if self.ok:
            return self.ok
        if not BASICS_OK:
            return False

        _piper_tts = piper_read_text.PiperTTSClass()
        test_locale = _piper_tts.py_locale()
        base_locale = test_locale.split("_")[0]
        base_lang = _iso_lang.split("-")[0].split("_")[0]
        # Check if this release can use specific models and voices.
        test_url = ""

        if alt_local_url.startswith("http"):
            test_url = alt_local_url
        test_ping = self.ping_local_server(test_url)
        if test_ping:
            self.home_network_scan_disabled = True
        else:
            if not self.home_network_scan_disabled:
                if _vox in self.search_network_voice:
                    test_ping = self._try_other_machines()
                    if not test_ping:
                        self.home_network_scan_disabled = True
                else:
                    self.home_network_scan_disabled = True

        if self.piper_json:
            # concise language
            _lang2 = _iso_lang.lower().split("-")[0].split("_")[0]
            data = self.piper_json
            language_family = ""  # en
            language_model = ""  # en_US-lessac-medium
            self.speaker_id_key_list = []
            for item in data:
                language_family = data[item]["language"]["family"]
                language_model = "-".join(
                    [
                        data[item]["language"]["code"],
                        data[item]["dataset"],
                        data[item]["audio"]["quality"],
                    ]
                )
                if isinstance(language_family, str):
                    if _lang2 == language_family:
                        self.piper_voice_resource = language_model
                        first_value = 0
                        speaker_map = data[item]["speaker_id_map"]
                        if speaker_map:
                            first_value = next(iter(speaker_map.values()))
                            for _key in data[item]["speaker_id_map"].keys():
                                if first_value == 0:
                                    self.speaker_id_key_list.append(_key)
                                else:
                                    self.speaker_id_key_list.insert(0, _key)
                        self.ok = True
                        self.wave = "OHF-Voice.wav"
                        return self.ok

        elif base_locale == base_lang:
            self.ok = test_ping
        return self.ok

    def determine_speaker_id(
        self, vox: str = "en_GB-jenny_dioco-medium#0"
    ) -> tuple[int, str]:
        """Determine `speaker_id` and `speaker_name` from a voice string.

        Examples:
            - "de_DE-thorsten_emotional-medium#4" -> (4, "neutral")
            - "de_DE-thorsten_emotional-medium#neutral" -> (4, "neutral")
            - "MALE4" -> (4, "neutral")

        Parameters:
            vox (str): Model and voice identifier string.

        Returns:
            tuple [ int, str ]: (speaker_id, speaker_name)
                - If a valid number or matching name is found, returns both.
                - If neither matches, returns (0, "")."""
        speaker_name = ""
        speaker_id: int | None = None

        # 1. Numeric ID
        if speaker_id is None and self.speaker_id_key_list:
            try:
                # Extract digits or default to "0"
                digits = "".join(c for c in vox if c.isdigit()) or "0"
                candidate = int(digits)

                # Clamp candidate into [0, len–1]
                max_idx = len(self.speaker_id_key_list) - 1
                candidate = min(max(candidate, 0), max_idx)

                speaker_id = candidate
                speaker_name = self.speaker_id_key_list[candidate]

            except ValueError:
                pass

        # 2. Case-sensitive name match
        if speaker_id is None:
            for idx, name in enumerate(self.speaker_id_key_list or []):
                if f"#{name}" in vox:
                    speaker_id = idx
                    speaker_name = name
                    break

        # 3. Case-insensitive name match
        if speaker_id is None:
            low_vox = vox.lower()
            for idx, name in enumerate(self.speaker_id_key_list or []):
                if f"#{name.lower()}" in low_vox:
                    speaker_id = idx
                    speaker_name = name
                    break

        return (speaker_id or 0, speaker_name)

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
        """Read text using a Piper speech synthesis server"""
        if not self.ok:
            return False
        _piper_tts = piper_read_text.PiperTTSClass()
        _media_out = ""
        speaker_id, speaker_name = self.determine_speaker_id(_vox)
        _done = False
        # Determine the output file name
        _media_out = readtexttools.get_work_file_path(_out_path, _icon, "OUT")
        # Determine the temporary file name
        _media_work = os.path.join(tempfile.gettempdir(), self.wave)

        if len(_out_path) == 0 and bool(_post_process):
            if readtexttools.handle_sound_playing(_media_work):
                self.common.winsound_purge()
                readtexttools.unlock_my_lock(self.locker)
                readtexttools.unlock_my_lock()
                return True

            if os.path.isfile(readtexttools.get_my_lock(self.locker)):
                self.common.winsound_purge()
                readtexttools.unlock_my_lock(self.locker)
                readtexttools.unlock_my_lock()
                return True

        if bool(self.add_pause):
            if any(_symbol in _text for _symbol in self.pause_list):
                _text = _text.translate(self.add_pause).replace(".;", ".")
        if os.path.isfile(_media_work):
            os.remove(_media_work)

        length_scale = 1
        try:
            if _speech_rate < 160 or _speech_rate > 160:
                length_scale, _ = self.common.rate_to_rhasspy_length_scale(
                    _speech_rate
                )
        except Exception as e:
            print("Exception:  ", e)

        # If the user has not manually edited the lexicon for their language
        # and region, don't alter any pronunciation. Piper voices can include
        # a wide variety of voice models including user generated models.
        # Since voice models with the same and region can use completely
        # novel rules and training data, it's impossible to generalize what
        # speech needs modification.

        if os.path.isfile(
            os.path.join(
                readtexttools.office_user_dir(),
                "config",
                "lexicons",
                "default",
                f"{_iso_lang}_lexicon.json",
            )
        ):
            _view_json = self.debug and 1
            response = readtexttools.local_pronunciation(
                _iso_lang,
                _text,
                _piper_tts.local_dir,
                "PIPER_USER_DIRECTORY",
                _view_json,
            )
            _text = response[0]
            if _view_json:
                print(response[1])

        if BASICS_OK:
            # _method = "GET"
            _strips = "\n .;"
            self.common.set_urllib_timeout(_ok_wait)
            _tries = 0
            readtexttools.lock_my_lock(self.locker)
            _no = "0" * 10
            _netsplitlocal = netsplit.LocalHandler()
            _items = _netsplitlocal.create_play_list(_text, _iso_lang.split("-")[0])
            help_heading = self.help_heading
            help_underscore = len(help_heading) * "="
            help_voice = self.piper_voice_resource
            if not self.piper_json:
                help_voice, _ = _vox.split("#")
            name_line = ""
            if speaker_name:
                name_line = f"""
- Speaker Name: {speaker_name}"""

            print(
                f"""
{help_heading}
{help_underscore}

- Model: {help_voice}#{str(speaker_id)}{name_line}
- Server Latency: {self.host_latency:.4f} sec.
- Speech Rate: {_speech_rate}
- Piper model data (json): <{self.url}/voices>

[{help_heading}]({self.help_url})
"""
            )
            for _item in _items:
                if self.debug:
                    print([_item, len(_item)])
                if not self.ok:
                    return False
                if not os.path.isfile(readtexttools.get_my_lock(self.locker)):
                    print("[>] Stop!")
                    self.ok = False
                    return True
                if len(_item.strip(_strips)) == 0:
                    continue
                if "." in _media_out and _tries != 0:
                    _, _ext = os.path.splitext(_media_out)
                    _no = readtexttools.prefix_ohs(_tries, 10, "0")
                    _media_out = _media_out.replace(f".{_ext}", f"_{_no}.{_ext}")
                _item = "\n".join(["", _item.strip(_strips), ""])
                # The 2025 GPL version of Piper Server supports switches
                # like the command line version. It defaults to a preset
                # language if the requested language is not installed.

                try:
                    my_url = self.url
                    response_content = None
                    eitem = netsplit.normalize_edge_punct(_item)
                    if self.piper_json:
                        payload = {
                            "text": eitem,
                            "voice": self.piper_voice_resource,
                            "speaker_id": speaker_id,
                            "length_scale": length_scale,
                        }
                        data = json.dumps(payload).encode("utf-8")
                        
                        req = urllib.request.Request(
                            my_url,
                            data=data,
                            headers={"Content-Type": "application/json"},
                            method="POST",
                        )
                    
                        with urllib.request.urlopen(req) as resp:
                            response_content = resp.read()
                    else:
                        # Your piper server was updated December 21, 2023,
                        # and you are limited to one voice model and speaker.
                        try:
                            legacy_req = urllib.request.Request(
                                my_url,
                                data=eitem.encode("utf-8"),
                                headers={"Content-Type": "text/plain"},
                                method="POST",
                            )
                            with urllib.request.urlopen(legacy_req) as legacy_resp:
                                response_content = legacy_resp.read()

                        except Exception as e:
                            print(
                                f"Exception: [{self.help_heading}]({self.help_url}) :",
                                e,
                            )
                            self.ok = False
                            return False
                    if response_content:
                        with open(_media_work, "wb") as _handle:
                            _handle.write(response_content)
                    if os.path.isfile(_media_work):
                        _done = os.path.getsize(os.path.realpath(_media_work)) != 0
                except Exception as e:
                    print(
                        f"""{self._piper_server_script_path()}
Exception:  {e}""",
                    )
                    # bare-except because qualifying it causes an error on some
                    # platforms.
                    retval = False
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


# _gplp = GPLPiperClass()
# print(_gplp._piper_server_script_path())
