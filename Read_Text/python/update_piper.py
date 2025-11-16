#!/usr/bin/env python3
# -*- coding: UTF-8-*-
"""Module to download
[Rhasspy Piper TTS](https://github.com/OHF-Voice/piper1-gpl/)
"""
import os
import subprocess
import tempfile
import zipfile

try:
    import shutil
except (ImportError, AssertionError):
    try:
        from distutils.spawn import find_executable
    except Exception as e:
        print("Exception", e)

try:
    import requests
except (ImportError, AssertionError):
    pass

try:
    import tarfile
except (ImportError, AssertionError):
    pass

try:
    from urllib.request import urlretrieve
except (ImportError, AssertionError):
    try:
        from urllib import urlretrieve
    except Exception as e:
        print("Exception (urllib): ", e)

try:
    from datetime import datetime
    import platform

    BASICS_OK = True
except (ImportError, AssertionError):
    BASICS_OK = False

# Local libraries
import netcommon
import readtexttools
import piper_read_text


def which(app_name):
    """Given a string that's the name of a program, returns the path if the
    program is within one of the directories identified in the system `PATH`
    collection, otherwise returns `""`."""
    return netcommon.which(app_name)

class GetPiperClass:
    """Determine the best download link and fetch the latest Piper release"""

    def __init__(self) -> None:
        """Initialize by fetching the latest release data."""
        self.old_api_url = "https://api.github.com/repos/rhasspy/piper/releases/latest"
        # On `2025-07-10T21:01:19Z`, Mike Hansen (synthesiam) released "OHF-Voice/piper1-gpl"
        # See: <https://github.com/OHF-Voice/piper1-gpl/>

        # On July, 13, 2025, the json API only includes no assets (compiled releases). The
        # source code is available as a `tarball_url` or a `zipball_url`.
        #
        # The new release includes features that extend and change the functions
        # that were in the previous GitHub hosted development package.
        # TODO: If the Windows version of the piper package includes `ffmpeg`, then
        # Windows users might not need to install VLC to get streaming audio playback.
        _common = netcommon.LocalCommons()
        self.api_url = self.old_api_url
        self.gpl_api_url = "https://api.github.com/repos/OHF-Voice/piper1-gpl/releases/latest"
        self.api_urls = [self.gpl_api_url, self.old_api_url]
        self.release = "2023.11.14-2"  # Default fallback
        self.help_heading = "Piper TTS"
        self.help_icon = _common.help_icon
        self.release_data = None
        for api_url in self.api_urls:
            try:
                self.temp_dir = tempfile.gettempdir()
            except NameError:
                self.temp_dir = os.path.join(os.path.expanduser("~"), "temp")
            
            try:
                response = requests.get(api_url, timeout=5)
                response.raise_for_status()
                self.release_data = response.json()
            except NameError:
                try:
                    import urllib
                    import json

                    response = urllib.request.urlopen(api_url)
                    data_response = response.read()
                    self.release_data = json.loads(data_response)
                except:
                    self.release_data = None
            except (requests.exceptions.RequestException, ValueError):
                self.release_data = None
            if self.release_data:
                if len(self.release_data.get("assets", self.release)):
                    if self.release_data.get("name", self.release):
                        self.release = self.release_data.get("name", self.release)
                        self.api_url = api_url
                        break


    def best_piper_tts_download(self) -> dict:
        """Return details of the best Piper TTS download for the current system."""
        if not self.release_data:
            return {"url": "", "size": None, "updated_at": None}

        system = platform.system().lower()
        architecture = platform.machine().lower()

        platform_map = {
            "darwin": "macos",
            "windows": "windows",
            "linux": "linux",
        }
        system = platform_map.get(system, system)

        if system.lower() in ["darwin", "macos"]:
            architecture_map = {
                "arm64": "aarch",
                "x86_64": "x64",
            }
            architecture = architecture_map.get(architecture, architecture)

        # Extract matching asset details in one step
        matching_asset = next(
            (
                asset
                for asset in self.release_data.get("assets", [])
                if asset.get("state") == "uploaded"
                and system in asset["name"]
                and architecture in asset["name"]
            ),
            None,
        )

        if matching_asset:
            return {
                "name": matching_asset.get("name"),
                "url": matching_asset.get("browser_download_url", ""),
                "size": matching_asset.get("size"),
                "updated_at": matching_asset.get("updated_at"),
            }

        return {"name": "", "url": "", "size": None, "updated_at": None}

    def download_file(self, url: str, file_path: str) -> bool:
        """Download a file, using a progress indicator and a resume feature
        if available."""
        _pipertts = piper_read_text.PiperTTSClass()
        success = _pipertts.download_file(url, file_path)
        if success:
            return True
        try:
            urlretrieve(url, file_path)
            return True
        except Exception as e:
            print("Error (`url_retrieve`)", e)
        return False


    def update_path(self, new_path: str="") -> bool:
        """If needed, then add `new_path` to the PATH so that you can start
        a program in the `new_path` without entering the full path. You might
        need to log out and log in again to apply the change."""
        if not os.path.isdir(new_path):
            return False
        if os.name == "nt":
            current_path = os.environ.get("PATH")
            if not new_path in current_path and os.path.isdir(new_path):
                os.environ["PATH"] = ";".join([current_path, new_path])
                if which("setx"):
                    try:
                        subprocess.run(
                            ["setx", "PATH", os.environ["PATH"]], check=False
                            )
                        return True
                    except Exception as e:
                        print("Exception: ", e)
                        return False

        _bashrc = os.path.realpath(os.path.expanduser("~/.bashrc"))
        if not os.path.isfile(_bashrc):
            return False
        new_path = os.path.realpath(os.path.expanduser("~/.local/bin"))
        if not os.path.isdir(new_path):
            return False
        current_path = os.environ.get("PATH")
        if not new_path in current_path and os.path.exists(new_path):
            os.environ["PATH"] = f"{current_path}{os.sep}{new_path}"
        _now = datetime.now()
        str_now = _now.strftime("%Y-%m-%d %H:%M:%S")
        _base_name = os.path.basename(__file__)
        _entry = f"""

# Created by `{_base_name}` on {str_now}
export PATH="$PATH:{new_path}"
"""
        try:
            with open(
                _bashrc, mode="r", encoding="utf-8", errors="replace"
            ) as file_obj:
                _bashrc_text = file_obj.read()
        except (UnicodeDecodeError, PermissionError, FileNotFoundError) as e:
            print(f"Error Reading {_bashrc}: {e}")
            return False
        if f'export PATH="$PATH:{new_path}"' in _bashrc_text:
            return True
        _bashrc_text = f"{_bashrc_text}{_entry}"
        try:
            with open(
                _bashrc, mode="w", encoding="utf-8", errors="replace"
            ) as file_obj:
                file_obj.write(_bashrc_text)
        except (PermissionError, ValueError) as e:
            print(f"Error Writing {_bashrc}: {e}")
            return False
        return True

    def pied_flatpak_run_string(self) -> str:
        """Return a command line string to run Pied if it is available as a
        flatpak, otherwise return `""`.

        **Pied**, like any third party program that modifies local
        speech-dispatcher settings might prevent you being able to read text
        aloud in every program or read more than one language. Firefox's
        **Reader View** might not display the **Read Aloud** icon. You can
        reenable it in Firefox by Disabling `narrate.filter-voices` in
        `about:config`. See <https://github.com/Elleo/pied/issues/23>."""

        _localcommons = netcommon.LocalCommons()
        return _localcommons.flatpak_package_play_command("com.mikeasoft.pied")

    def decompress_archive(self, archive="", extract_to="", check_size=0) -> bool:
        "Decompress archive"
        if not archive:
            return False
        if not extract_to:
            return False
        if not os.path.exists(extract_to):
            try:
                os.makedirs(extract_to)
            except Exception as e:
                print("Exception (makedirs): ", e)
                return False

        _, extension = os.path.splitext(archive)
        if not extension:
            return False
        if not os.path.isfile(archive):
            return False
        if check_size:
            size = os.stat(archive).st_size
            if size not in [check_size, check_size + 1, check_size + 2]:
                return False
        if extension.lower() in [".zip", ".oxt"]:

            try:
                with zipfile.ZipFile(archive, "r") as zip_ref:
                    zip_ref.extractall(extract_to)
                return True

            except:
                return False

        if extension.lower() in [".gz", ".tgz", ".tar"]:
            if platform.system().lower() == "linux":
                if which("tar"):
                    # For large files, using tar is faster than python.
                    cmd = ["tar", "-xf", archive, "-C", extract_to]
                    try:
                        proc = subprocess.Popen(cmd)
                        if proc.wait() != 0:
                            raise subprocess.CalledProcessError(proc.returncode, cmd)
                        return True

                    except Exception as e:
                        print("Exception (`tar`...): ", e)

            try:
                tarmode = "r:*"
                if extension.lower() in [".gz", ".tgz"]:
                    tarmode = "r:gz"
                with tarfile.open(archive, mode=tarmode) as tar:
                    tar.extractall(path=extract_to)
                    return True

            except Exception as e:
                print("Exception (`tar.extractall())`: ", e)

        return False

    def filter_install_piper_request(self) -> bool:
        """Return `True` if either the pied flatpak piper text to speech
        manager or the piper program package itself is installed, in
        which case you do not have to download the piper program package."""
        _piper_tts = piper_read_text.PiperTTSClass()
        local_path = _piper_tts.real_piper_path()
        if local_path:
            return True
        if not self.release_data:
            print(
                """ [Piper][1] is not available to download. Check your network or try again
later.

[1]: {0}
"""
            ).format(self.api_url)
            return False
        iso_lang = readtexttools.default_lang().replace("_", "-")

        if platform.system().lower() == "linux" and platform.machine().lower() in [
            "x86_64"
        ]:
            pied_flatpak = self.pied_flatpak_run_string()
            if len(pied_flatpak) != 0:
                _imported_meta = readtexttools.ImportedMetaData()
                _imported_meta.execute_command(pied_flatpak)
                return True
        if not platform.system().lower() == "windows":
            readtexttools.pop_message(
                "{0} - {1}".format(_piper_tts.help_heading, self.release),
                _piper_tts.help_url,
                8000,
                _piper_tts.help_icon,
                2,
                iso_lang,
            )
        return False

    def piper_local_install_path(self):
        """Choose a local installation path for the Piper package.
        ```
        /piper
            libtashkeel_model.ort
            piper.exe
            *.dll
            /espeak-ng-data
               /lang
               /voices
               *.dict
            /pkgconfig
        ```
        """
        home_path = os.path.expanduser("~")
        if platform.system().lower() == "windows":
            return os.path.join(home_path, "AppData", "Local", "Programs", "piper-tts")
        elif platform.system.lower() == "darwin":
            # "~/Library/Application Support/piper-tts"
            return os.path.join(
                home_path, "Library", "Application Support", "piper-tts"
            )
        else:
            if which("flatpak"):
                return os.path.join(
                    home_path,
                    ".var",
                    "app",
                    "com.mikeasoft.pied",
                    "data",
                    "pied",
                )

            elif which("snap"):
                return os.path.join(
                    home_path,
                    "snap",
                    "pied",
                    "common",
                )

        return os.path.join(
            home_path,
            ".local",
            "share",
            "piper-tts",
        )


def get_piper() -> bool:
    """Check user account permission and whether a version of Piper already
    exists, then quit if it does. Check if a compatible version of piper is
    available online; if not, then quit. Otherwise, try to install it as a
    locally installed program in a conventional directory for utility command
    line programs."""

    if which("piper"):
        return False

    _permissions = netcommon.UserPermissions()
    if not _permissions.is_staff_or_admin():
        print(
            """
"Your administrator needs to grant you staff or administrator rights to
allow you to install `piper` using this tool. Simply put, you can
install this tool on a supported computer platform if you are allowed
to install and remove programs normally on the computer that you are
using."""
        )
        return False
    _get_p = GetPiperClass()
    already_installed = _get_p.filter_install_piper_request()

    if already_installed:
        print("\nPiper is installed.\nExiting...")
        return False
    if not _get_p.release_data:
        print(
            """Data at <{0}> is not available.
Exiting...""".format(
                _get_p.api_url
            )
        )
        return False

    prog_dir = _get_p.piper_local_install_path()
    temp_dir = _get_p.temp_dir
    piper_url = _get_p.best_piper_tts_download()["url"]
    expected_size = _get_p.best_piper_tts_download()["size"]
    if not piper_url:
        return False
    archive_name = _get_p.best_piper_tts_download()["name"]
    try:
        os.makedirs(prog_dir, exist_ok=True)
        os.makedirs(temp_dir, exist_ok=True)
    except Exception as e:
        print("Exception (`os.makedirs`) in `main()`: ", e)
        return False
    if os.path.isdir(_get_p.temp_dir) and os.path.isdir(prog_dir):
        piper_download = os.path.join(temp_dir, archive_name)
        print("""
====================================
Starting Piper TTS installation...
====================================
""")
        print("Expected Size:      ", expected_size)
        print("Downloading from:   ", piper_url)
        print("Downloading to:     ", piper_download)
        # Download an archive to the temporary directory.
        _get_p.download_file(piper_url, piper_download)
        print("Installing:         ", os.path.join(prog_dir, "piper"))
        # Decompress the archive in a local applications directory.
        _get_p.decompress_archive(piper_download, prog_dir, expected_size)
        # Add the piper directory to the operating system environment `PATH`
        if os.path.isdir(os.path.join(prog_dir, "piper")):
            if os.name in ["posix", "nt"]:
                _get_p.update_path(os.path.join(prog_dir, "piper"))
            print("""
====================================
installation completed successfully.
====================================
""")
            return True
        else:
            print("""
====================================
The installation was not completed.
====================================
""")
        return False


def main():
    if get_piper():
        print("\nGot Piper")
    else:
        print("\nDid not update Piper.")
        print(which("piper"), "\n")


if __name__ == "__main__":
    main()
