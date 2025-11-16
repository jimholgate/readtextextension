#!/usr/bin/env python
# -*- coding: UTF-8-*-
"""Common tools for network and neural speech synthesis clients"""

import io
import math
import os
import time
import wave

try:
    import unicodedata
except ImportError:
    pass

try:
    import platform
except AssertionError:
    pass

try:
    import re
except AssertionError:
    pass

try:
    import socket
except ImportError:
    pass
import sys
import readtexttools

if os.name != "nt":
    import pwd
    import grp

try:
    import shutil
except (ImportError, AssertionError):
    try:
        from distutils.spawn import find_executable
    except Exception as e:
        print("Exception", e)

if os.name == "nt":
    try:
        import winsound
    except ImportError:
        pass

NET_SERVICE_LIST = [
    "AUTO",
    "NETWORK",
    "GTTS",
    "MARYTTS",
    "MIMIC",
    "OPENTTS",
    "PIPER",
    "RHVOICE",
    "TTS",
]


def which(app_name):  # -> str
    """Given a string that's the name of a program, returns the path if the
    program is within one of the directories identified in the system `PATH`
    collection, otherwise returns `""`."""
    try:
        retstr = shutil.which(app_name)
        if retstr:
            return str(retstr)
        return ""

    except NameError:
        try:
            retstr = find_executable(app_name)
            if retstr:
                return str(retstr)

        except NameError:
            pass

    return ""


def hardlink_or_copy(src, dst, overwrite=False, preserve_metadata=True):  # -> str
    """
    Try to create a hard link from dst → src on Windows/POSIX.
    Falls back to copying when hard-linking isn't supported (e.g., cross-device).

    Returns one of: "hardlink", "copy", "exists", or "skipped".
    """
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)

    if not os.path.isfile(src):
        raise FileNotFoundError("Source file not found: {}".format(src))

    # Already exists?
    if os.path.exists(dst):
        try:
            if os.path.samefile(src, dst):
                return "skipped"  # already the same file
        except Exception:
            pass
        if not overwrite:
            return "exists"
        os.unlink(dst)

    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)

    try:
        if os.name == "nt":
            # Check drive letters — must match
            s_drive, _ = os.path.splitdrive(src)
            d_drive, _ = os.path.splitdrive(dst)
            if s_drive.lower() != d_drive.lower():
                raise OSError("EXDEV: different drives")

        os.link(src, dst)

        # Verify same inode/device (or NTFS record)
        s_stat, d_stat = os.stat(src), os.stat(dst)
        if (s_stat.st_dev, s_stat.st_ino) != (d_stat.st_dev, d_stat.st_ino):
            os.unlink(dst)
            raise OSError("Hard link verification failed")

        return "hardlink"

    except Exception:
        # Fallback: copy
        if preserve_metadata:
            shutil.copy2(src, dst)
        else:
            shutil.copyfile(src, dst)
        return "copy"


def have_gpu(_test="Radeon"):  # -> bool
    """If the system can detect the specified GPU string, return `True`,
    otherwise return `False`"""
    _test_app = "lspci"
    if not readtexttools.have_posix_app(_test_app, False):
        return False
    _imported_meta = readtexttools.ImportedMetaData()
    return (
        _test.lower()
        in _imported_meta.execute_command("{0} | grep VGA").format(_test_app).lower()
    )


def spd_voice_list(_min=0, _max=100, _roots=None):  # -> list[str]
    """Return a list in the form `['female0', 'male0', 'female1' ...]`"""
    retval = []
    if not _roots:
        _roots = ["female", "male"]
    for _digit in range(_min, _max + 1):
        for _root in _roots:
            retval.append("".join([_root, str(_digit)]))
    return retval


def index_number_to_list_item(_vox_number=0, _list=None):  # -> str
    """Return a specific voice_id using vox_number as an index in the list.
    Handle out of range numbers using a modulus (`int % len(_list)`) value."""
    try:
        if not bool(_list):
            return ""
        if not _vox_number > len(_list) - 1:
            return _list[_vox_number]
        return _list[(_vox_number % abs(len(_list)))]
    except ZeroDivisionError:
        return _list[0]
    except [IndexError, TypeError]:
        pass
    return ""


def speech_wpm(_percent="100%"):  # -> int
    """
    _percent - rate expressed as a percentage.
    Use '100%' for default rate of 160 words per minute (wpm).
    Returns rate between 20 and 640.
    """
    _calc_product = 0
    _result = 0
    _minimum = 20
    _maximum = 640
    _normal = 160
    _p_cent = ""

    try:
        if "%" in _percent or "percent" in _percent:
            _p_cent = readtexttools.safechars(_percent, "1234567890.")
            _calc_product = float(_p_cent) if "." in _p_cent else int(_p_cent) / 100
            _result = math.ceil(_calc_product * _normal)
        else:
            _calc_product = float(_percent) if "." in _percent else int(_percent)
            _result = math.ceil(_calc_product)
    except (TypeError, ValueError):
        return _normal
    if _result == 0:
        return _normal
    elif _result <= _minimum:
        return _minimum
    elif _result >= _maximum:
        return _maximum
    return _result


class UserPermissions(object):
    """Manage options according to the group that the user belongs to"""

    def __init__(self):  # -> None
        """Record tokens to minimize code execution"""
        self.ok = False
        self.ok_group = ""

    def _is_member_of(self, groups_to_check):  # -> bool
        """
        Return True if the current user belongs to any of the groups
        listed in groups_to_check (case-insensitive check).

        Args:
            groups_to_check (list): A list of group name strings
                                    (e.g., ["sudo", "admin", "staff", "readtextadmin"]).

        Returns:
            bool: True if current user belongs to any listed group, False otherwise.
        """
        if os.name == "nt":
            try:
                import winreg

                def can_you_install_via_store():
                    """Check if store is disabled by machine or user policy."""
                    policy_paths = [
                        (
                            winreg.HKEY_LOCAL_MACHINE,
                            "\\".join(
                                ["SOFTWARE", "Policies", "Microsoft", "WindowsStore"]
                            ),
                        ),
                        (
                            winreg.HKEY_CURRENT_USER,
                            "\\".join(
                                ["SOFTWARE", "Policies", "Microsoft", "WindowsStore"]
                            ),
                        ),
                    ]

                    for hive, path in policy_paths:
                        try:
                            with winreg.OpenKey(hive, path) as key:
                                value, _ = winreg.QueryValueEx(
                                    key, "RemoveWindowsStore"
                                )
                                if value == 1:
                                    return False
                        except (FileNotFoundError, OSError):
                            # Key or value doesn't exist (policy not set)
                            continue

                    # Check if OS is a Windows Server edition
                    try:
                        with winreg.OpenKey(
                            winreg.HKEY_LOCAL_MACHINE,
                            "\\".join(
                                [
                                    "SOFTWARE",
                                    "Microsoft",
                                    "Windows NT",
                                    "CurrentVersion",
                                ]
                            ),
                        ) as key:
                            product_name, _ = winreg.QueryValueEx(key, "ProductName")
                            if "Server" in product_name:
                                return False
                    except (FileNotFoundError, OSError):
                        # Couldn't determine OS type; assume client Windows
                        pass

                    return True

                return can_you_install_via_store()

            except (AssertionError, TypeError):
                return False
        else:
            uid = os.getuid()
            user_name = pwd.getpwuid(uid).pw_name
            user_groups = [g.gr_name for g in grp.getgrall() if user_name in g.gr_mem]
            # Also add the user's primary group.
            primary_gid = os.getgid()
            primary_group = grp.getgrgid(primary_gid).gr_name
            user_groups.append(primary_group)
            # Do a case-insensitive comparison.
            user_groups = [x.lower() for x in user_groups]
            for group in groups_to_check:
                if group.lower() in user_groups:
                    self.ok_group = group.lower()
                    self.ok = True
                    return True
            self.ok = False
            return False

    def is_staff_or_admin(self):  # -> bool
        """
        Return True if the user is considered staff or an admin.

        On Unix-like systems, perform this check based on membership in
        one of the groups in the list ["sudo", "admin", "staff", "readtextadmin", "wheel"].
        On Windows, fall back on the standard administrator check.

        Returns:
            bool: True if the user is in one of the designated groups
            or is admin on Windows.
        """
        if self.ok:
            return True
        the_groups = ["sudo", "admin", "staff", "readtextadmin", "wheel"]
        return self._is_member_of(the_groups)

    def specific_staff_or_admin_group(self):  # -> str
        """If a posix user is in `["sudo", "admin", "staff", "readtextadmin", "wheel"]`
        return the name of the group, otherwise if a Windows user is  an
        administrator, return `"nt_admin"`, otherwise return `""`."""
        if self.ok:
            if self.ok_group:
                return self.ok_group
        if self.is_staff_or_admin():
            self.ok = True
        return self.ok_group


def get_wav_duration(path):  # -> float
    """
    Checks the specified audio file and returns its length in seconds.

    Parameters
    ----------
    file_path : str
        Path to the audio file to check. Should point to a .wav file
        accessible from the local filesystem.

    Returns
    -------
    float
        Length of the file in seconds. A return value of `0.0` indicates that:
            - the file does not exist,
            - is not a valid .wav file, or
            - could not be processed/read successfully.

    Notes
    -----
    This function is intended for validation and quick diagnostics,
    allowing callers to detect missing or unreadable files without
    raising exceptions.
    """
    try:
        with wave.open(path, "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return frames / float(rate)
    except Exception as e:
        print("[!] Could not read WAV duration: ", e)
        return 0.0


def play_with_winsound(_media_work="", lock_path=""):  # -> bool
    """    Play a WAV file asynchronously on Windows, with optional early stop control.

    Parameters
    ----------
    _media_work : str, optional
        Path to the .wav file to play. Must exist locally and be a valid WAV file.
        Defaults to an empty string, which will cause the function to return False.
    lock_path : str, optional
        Path to a "lock file" whose continued existence allows playback to proceed.
        If provided and the file is deleted during playback, the audio stops early.

    Returns
    -------
    bool
        True  – Playback worked successfully (and ran to completion or was stopped early).\\
        False – Playback could not be started, or playback could not be stopped.
    """
    # NOTE: `future` and `threads` did not work in testing on Windows, so the script
    # falls back to using a timer and an asynchronous call to winsound.
    if os.name != "nt":
        return False

    if not os.path.isfile(str(lock_path)):
        lock_path = readtexttools.get_my_lock()

    _, _ext = os.path.splitext(_media_work)
    if _ext.lower() != ".wav":
        return False

    try:
        duration = get_wav_duration(_media_work)
        if not duration:
            return False
        elapsed = 0.0
        if os.path.exists(lock_path):
            winsound.PlaySound(_media_work, winsound.SND_FILENAME | winsound.SND_ASYNC)
            print(
                "[>] Python `winsound` playing `{0}`".format(
                    os.path.basename(_media_work)
                )
            )

        while elapsed < duration:
            time.sleep(0.2)
            elapsed += 0.2
            if lock_path and not os.path.exists(lock_path):
                print(
                    "[>] Python `winsound` stopping `{0}`".format(
                        os.path.basename(_media_work)
                    )
                )
                break

        # Always purge at the end
        winsound.PlaySound(None, winsound.SND_PURGE)
        readtexttools.unlock_my_lock(lock_path)
        return True

    except Exception as e:
        print("Exception:", e)
        return False


def is_voice_id_formatted_for_speechd(voice_id=""):  # -> bool
    """
    Returns `True` if the voice_id contains only letters (A-Za-z) and `_`. If
    digits appear, they occur only at the end of the string.
    Examples:
        MALE1
        CHILD_MALE
        female2
        Child_fEMALE
    """
    try:
        # Pattern explanation:
        #   ^[A-Za-z_]+      -> One or more letters or underscores at the start.
        #   (?:[0-9]+)?$     -> Optionally, one or more digits at the very end,
        #   and nothing else.
        pattern = re.compile(r"^[A-Za-z_]+(?:[0-9]+)?$")
        return pattern.fullmatch(voice_id) is not None
    except Exception as e:
        print("Exception in `re`; falling back to `set`: {0}".format(e))
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
        return all(char in allowed for char in voice_id)


class LocalCommons(object):
    """Shared items for local speech servers"""

    def __init__(self):  # -> None
        self.debug = [0, 1, 2, 3][0]
        self.default_lang = readtexttools.default_lang()
        self.default_extension = ".wav"
        self.help_icon = "/usr/share/icons/HighContrast/32x32/apps/web-browser.png"
        self.length_scales = [
            [320, 304, "---------|", 0.50],
            [303, 289, "---------|", 0.525],
            [288, 272, "--------|-", 0.55],
            [271, 257, "--------|-", 0.585],
            [256, 240, "-------|--", 0.62],
            [239, 225, "-------|--", 0.665],
            [224, 208, "------|---", 0.71],
            [207, 193, "------|---", 0.77],
            [192, 176, "-----|----", 0.83],
            [175, 161, "-----|----", 0.915],
            [160, 160, "-----|----", 1.00],  # default
            [159, 143, "---|-----", 1.037],
            [142, 128, "---|-----", 1.15],
            [127, 118, "---|-----", 1.20],
            [117, 110, "---|-----", 1.25],
            [109, 103, "---|-----", 1.375],
            [102, 97, "---|-----", 1.50],
            [96, 81, "--|------", 1.58],
            [80, 66, "--|------", 1.66],
            [64, 49, "-|-------", 2.00],
            [48, 33, "-|-------", 2.50],
            [32, 16, "|--------", 3.75],
            [15, 8, "|--------", 4.375],
            [7, 0, "|--------", 5.00],
        ]
        self.spd_fm = [
            "female1",
            "female2",
            "female3",
            "female4",
            "female5",
            "female6",
            "female7",
            "female8",
            "female9",
            "child_female",
            "child_female1",
        ]
        self.spd_m = [
            "male1",
            "male2",
            "male3",
            "male4",
            "male5",
            "male6",
            "male7",
            "male8",
            "male9",
            "child_male",
            "child_male1",
        ]
        self.pause_list = [
            "(",
            "\n",
            "\r",
            "\u2026",
            "\u201c",
            "\u2014",
            "\u2013",
            "\u00a0",
        ]
        self.rhasspy_fm = [
            "eva_k",
            "hokuspokus",
            "kerstin",
            "rebecca_braunert_plunkett",
            "blizzard_fls",
            "blizzard_lessac",
            "cmu_clb",
            "cmu_eey",
            "cmu_ljm",
            "cmu_lnh",
            "cmu_rms",
            "cmu_slp",
            "cmu_slt",
            "ek",
            "harvard",
            "judy_bieber",
            "kathleen",
            "ljspeech",
            "southern_english_female",
            "karen_savage",
            "siwis",
            "lisa",
            "nathalie",
            "hajdurova",
        ]
        self.ai_developer_platforms = [
            "alma",
            "centos",
            "darwin",
            "debian",
            "fedora",
            "raspbian",
            "rhel",
            "sles",
            "ubuntu",
            "preempt_dynamic",
        ]
        try:
            self.add_pause = str.maketrans(
                {
                    "\n": ";\n",
                    "\r": ";\r",
                    "(": " ( ",
                    "\u201c": "\u201c;",
                    "\u2026": "\u2026;",
                    "\u2014": "\u2014;",
                    "\u2013": "\u2013;",
                    "\u00a0": " ",
                }
            )
        except AttributeError:
            self.add_pause = None
        try:
            self.base_curl = str.maketrans(
                {
                    "\\": " ",
                    '"': '\\"',
                    """
""": """\
""",
                    "\r": " ",
                }
            )
        except AttributeError:
            self.base_curl = None
        self.is_x86_64 = sys.maxsize > 2**32
        self.locker = "net_speech"
        self.generic_problem = """The application cannot load a sound file.
Your computer might be missing a required library, or an operation might have
taken too long."""
        if readtexttools.using_container(False):
            self.generic_problem = """The container application cannot load
a sound file. It might be missing a required library or an operation might
have taken too long."""
        self.last_lang = None
        self.patterns = None

    def is_ai_developer_platform(self):  # -> bool
        """Does the platform include options for docker, podman, system
        contributor or non-free components for some ai models?
        """
        # i. e.: Darwin, NT, Docker container, Debian or other modern
        # enterprise compatible platform?
        if os.name == "nt":
            return True
        if os.name == "posix":
            try:
                _uname_ver = platform.uname().version
            except (AttributeError, NameError, TypeError):
                try:
                    _importmeta = readtexttools.ImportedMetaData()
                    _uname_ver = _importmeta.execute_command("uname -a")
                except Exception as e:
                    print("Exception:  ", e)
                    return False
            for _item in self.ai_developer_platforms:
                if _item.lower() in _uname_ver.lower():
                    return True
        return False

    def set_urllib_timeout(self, _ok_wait=4):  # -> bool
        """Try to set sockets timeout before transfering a file using
        `urllib`.
        https://docs.python.org/3/howto/urllib2.html#sockets-and-layers"""
        try:
            socket.setdefaulttimeout(_ok_wait)
        except:
            return False
        return True

    def rate_to_rhasspy_length_scale(self, _speech_rate=160):  # -> list
        """Look up a Rhasspy or Mimic3 length scale appropriate for requested
        `_speech rate`. Rates have discreet steps. In English, a common speech
        rate is about 160 words per minute, but individuals vary widely. Some
        voices do not sound good with an altered rate."""
        _length_scale = 1
        _length_bar = ""
        for _item in self.length_scales:
            if not _speech_rate > _item[0] and not _speech_rate < _item[1]:
                _length_scale = _item[3]
                _length_bar = _item[2]
                break
        return [_length_scale, _length_bar]

    def ssml_xml(
        self, _text="", _voice="en_UK/apope_low", _speech_rate=160, _xml_lang="en-US"
    ):  # -> str
        """Change the speed that a reader reads plain text aloud using
        w3.org `SSML`. The reader should use standard XML conventions like
        `&amp;`, `&gt;` and `&lt;`.  Mimic3 supports a subset of SSML.
        Not all models support SSML prosody rate.

        <https://www.w3.org/TR/speech-synthesis11/ >"""
        _xmltransform = readtexttools.XmlTransform()
        _text = _xmltransform.clean_for_xml(_text, False)
        _xml_lang = _xml_lang.replace("_", "-")
        try:
            # 160 wpm (Words per minute) yields 100% prosody rate
            if _speech_rate < 40:
                _speech_rate = 40
            _rate = "".join([str(int(_speech_rate / 1.6)), "%"])
        except [AttributeError, TypeError]:
            _rate = "100%"
        return """<?xml version="1.0"?>en
<speak version="1.1" xmlns="http://www.w3.org/2001/10/synthesis"
xml:lang="{0}">
<p>
<prosody rate="{1}"><voice name="{2}" languages="{3}" required="languages">
{4}</voice></prosody></p></speak>""".format(
            _xml_lang, _rate, _voice, _xml_lang, _text
        )

    def do_net_sound(
        self,
        _info="",
        _media_work="",
        _icon="",
        _media_out="",
        _audible="true",
        _visible="false",
        _writer="",
        _size="600x600",
        _post_process="",
        handle_unlock=False,
    ):  # -> bool
        """Play `_media_work` or export it to `_media_out` format."""
        # use `getsize` to ensure that python waits for file to finish download
        if not os.path.isfile(_media_work):
            return False
        if os.path.getsize(os.path.realpath(_media_work)) == 0:
            time.sleep(2)
        if os.path.isfile(_media_work) and _post_process in [
            "process_audio_media",
            "process_wav_media",
        ]:
            if os.path.getsize(os.path.realpath(_media_work)) == 0:
                print("Unable to write media work file.")
                return False
            # NOTE: Calling process should unlock_my_lock()
            # In a loop, this would cause the voice to continue.
            if handle_unlock:
                readtexttools.unlock_my_lock()

            # if not readtexttools.lax_bool(_visible) and not len(_media_out) == 0:
            #     if play_with_winsound(_media_work, readtexttools.get_my_lock()):
            #         return True

            readtexttools.process_wav_media(
                _info,
                _media_work,
                _icon,
                _media_out,
                _audible,
                _visible,
                _writer,
                _size,
            )
            return True
        return False

    def flatpak_package_play_command(
        self, app_signature="com.mikeasoft.pied"
    ):  # -> str
        """If your posix os has a flatpak package with a matching signature,
        then return the command to run the application, otherwise return `""`

        NOTE: If the extension is running in a Flatpak container, it will
        not find the system `/usr/bin/flatpak` program because it only has
        access to system resources included in the Flatpak container.
        """
        if len(app_signature.split(".")) < 2:
            return ""
        if not os.path.isfile("/usr/bin/flatpak"):
            return ""
        _imported_meta = readtexttools.ImportedMetaData()
        if "\t{0}\t".format(app_signature) in _imported_meta.execute_command(
            "flatpak list"
        ):
            return "flatpak run {0}".format(app_signature)
        return ""

    def winsound_purge(self):
        """Stop playing a wave audio file."""
        if not os.name == "nt":
            return True
        try:
            winsound.PlaySound(None, winsound.SND_PURGE)
            time.sleep(0.5)
            return True
        except Exception as e:
            print("Exception:  ", e)
            return False


def get_host_ip():  # -> str
    """Connect to a public IP (Google DNS) without sending data
    to reliably determine the machine's IP address."""
    _local_commons = LocalCommons()
    _local_commons.set_urllib_timeout(2)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        _local_commons.set_urllib_timeout(4)
        return ip
    except Exception:
        _local_commons.set_urllib_timeout(4)
        return "127.0.0.1"  # Fallback if offline


def main():  # -> None
    """Print Info"""
    print(
        """Common Network Tools
====================

* Common tools for network and neural speech synthesis clients
* Access using class `LocalCommons()`

{0}
""".format(
            os.path.abspath(__file__)
        )
    )
    for _engine in NET_SERVICE_LIST:
        print("* {0}".format(_engine))


if __name__ == "__main__":
    main()
