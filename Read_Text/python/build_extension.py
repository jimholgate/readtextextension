"""Compress a directory, omitting platform specific autogenerated directories"""

import argparse
import hashlib
import json
import os
import zipfile
from datetime import datetime


ACTION = "Build Read Text Extension"
PACKAGE = "read_text"


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


def zip_directory(
    folder_path: str = "~/project",
    zip_name: str = "~/project.zip",
    omit_list: list = [".DS_Store", "__pycache__", "__MACOSX"],
) -> bool:
    """Zip a directory, omitting platform specific autogenerated directories"""
    if len(zip_name) == 0 or len(folder_path) == 0:
        return False
    try:
        zip_name = os.path.expanduser(zip_name)
        folder_path = os.path.expanduser(folder_path)
        os.makedirs(os.path.dirname(zip_name), exist_ok=True)
        if not os.path.isdir(folder_path):
            return False
        with zipfile.ZipFile(
            zip_name, "w", zipfile.ZIP_DEFLATED, compresslevel=9
        ) as zipf:
            for root, dirs, files in os.walk(folder_path):
                # Exclude omit_list directories
                dirs[:] = [d for d in dirs if os.path.join(root, d) not in omit_list]
                for file in files:
                    file_path = os.path.join(root, file)
                    # Exclude omit_list files
                    list_dir = root.split(os.path.sep)
                    if list_dir[len(list_dir) - 1] not in omit_list:
                        zipf.write(file_path, os.path.relpath(file_path, folder_path))
        return os.path.isfile(zip_name)
    except IOError:
        pass
    return False


def make_json_str(
    base_name: str = "reader.zip",
    date_time: str = "",
    size_bytes: int = 0,
    md5_digest: str = "00000000000000000000000000000000",
) -> str:
    """Return a JSON string with the provided values."""
    data = {
        base_name: {
            "date_time": date_time,
            "size_bytes": size_bytes,
            "md5_digest": md5_digest,
        }
    }
    json_str = json.dumps(data, indent=4)
    return json_str


def save_text(_file_path: str = "", _content: str = "") -> bool:
    """Save text content to a UTF-8 File"""
    try:
        with open(_file_path, "w", encoding="utf-8") as f:
            f.write(_content)
    except Exception as e:
        print(f"""There was an error saving a file: {e}""")
    return os.path.isfile(_file_path)


def main() -> None:
    """Give options for compressing a directory"""
    skip_list = [
        ".DS_Store",
        "__pycache__",
        "__MACOSX",
        ".git",
        ".svn",
        ".hg",
        "node_modules",
        "dist",
        ".idea",
        ".vscode",
        "*.pyc",
        "*.o",
        "*.a",
        "*.so",
        "*.dll",
        "*.dylib",
        "*.log",
        "*.tmp",
        "*.temp",
        "*.swp",
        "Dockerfile",
        "docker-compose.yml",
    ]
    _default = os.path.dirname(os.path.dirname(__file__))
    _date_time = datetime.now()
    _alt = ""
    if os.path.splitext(_default)[0][-1] not in "0123456789":
        # i.e. : `a` for Apache; `b` for Beta ...
        _alt = os.path.splitext(_default)[0][-1]
    parser = argparse.ArgumentParser(
        description="Compress a directory into a zip file."
    )
    parser.add_argument(
        "-d",
        "--directory",
        default=_default,
        help="The directory to compress (default: parent of the current directory)",
    )
    parser.add_argument(
        "-j", "--json", action="store_true", help="Save a JSON fingerprint."
    )
    parser.add_argument(
        "-o",
        "--output",
        default=os.path.join(
            os.path.expanduser("~"),
            _date_time.strftime(f"{PACKAGE}_%Y.%m.%d_%H.%M{_alt}.oxt").lower(),
        ),
        help=f"The output zip file name (default: {PACKAGE}_YYYY.MM.DD_HH.MM{_alt}.oxt in the user home directory)",
    )
    parser.add_argument(
        "-s",
        "--skip",
        default=",".join(skip_list),
        help=f"""A comma separated list of the directories and files to skip  (default: {",".join(skip_list)}""",
    )
    args = parser.parse_args()
    directory_to_compress = args.directory
    archive_output_name = args.output
    skip_list = args.skip.replace(" ", "").split(",")
    base_name = os.path.basename(archive_output_name)
    print(
        f"""
{ACTION}
{(len(ACTION)) * "="}
    
* directory_to_compress : "{directory_to_compress}"
* archive_output_name   : "{archive_output_name}"
"""
    )
    if zip_directory(directory_to_compress, archive_output_name, skip_list):
        _json = make_json_str(
            base_name,
            _date_time.strftime("%Y.%m.%d_%H:%M:%S.%f"),
            os.path.getsize(archive_output_name),
            calculate_md5(archive_output_name),
        )
        print(
            f"""Result
------

"{PACKAGE.replace("_", " ").capitalize()}" was archived in `{os.path.split(archive_output_name)[0]}`.

Fingerprint
-----------

```
{_json}
```
"""
        )
    if args.json:
        save_text(f"""{archive_output_name}.json""", _json)


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
