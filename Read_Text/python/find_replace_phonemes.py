#!/usr/bin/env python
# -*- coding: UTF-8-*-
"""Modify strings of text using JSON coded graphemes and phonemes"""


import getopt
import os
import sys
import readtexttools

def usage():  # -> None
    """Show usage"""
    print(
        """
Replace mispronounced words with phonemes
=========================================

Uses a json table to search and replace mispronounce words with a
string in phonemic format. Some speech synthesis voice models
require their own custom code because they interpret written phonemes
differently.

* `-o`, `--output` - the new text file to write. If blank overwrite
  the input file
* `-l`, `--language` - the language in iso format
* `-m`, `--model` - the extension json directory to search
* `-u`, `--user_environ_dir` - an optional user environment string
  to use for the json file search.

Layrnx and MaryTTS can use a subset of the International Phonetic Alphabet.
Enclose the phonetic substring in square brackets.

Legacy speech systems might require plain text or a use a different standard.

MacOS 13 Example
================

In
--

`The Musqueam store at the airport is next to the food court.`

Out
---

`The [mʌskwiaəum] store at the airport is next to the food court.`

See:

* <https://www.internationalphoneticalphabet.org/ipa-chart-audio/index.html>
* <https://aletheiacui.github.io/tutorials/ipa_mac_users.html>

New file
--------

find_replace_phonemes.py --model <model> --output <path-out> --language en-CA <path-in>

Modify file
-----------

find_replace_phonemes.py --model <model> --language en-CA <path-to-file-to-edit>"""
    )


def fix_up_text_file(
    _text_file_in="",
    _file_out="",
    _language="en-CA",
    _my_dir="default",
    _user_dir="SPEECH_USER_DIRECTORY",
    _verbose=False,
):  # -> bool
    """Replace incorrect pronunciations in a UTF-8 text file."""
    _import_meta = readtexttools.ImportedMetaData()
    _output_type = [0, 1, 2][0]
    if not os.path.isfile(_text_file_in):
        return False
    _ext = ""
    if not bool(_file_out):
        _file_out = _text_file_in
    if "." in _file_out:
        _ext = os.path.splitext(_file_out)[1]
    if _ext in [".json", ".js"]:
        _output_type = [0, 1, 2][1]
    elif _ext in [".xml", ".lmxl", ".xpls", ".pls"]:
        _output_type = [0, 1, 2][2]
    _content2 = readtexttools.local_pronunciation(
        _language,
        _import_meta.meta_from_file(_text_file_in, False),
        _my_dir,
        _user_dir,
        True,
        _verbose,
    )
    readtexttools.write_plain_text_file(_file_out, _content2[_output_type], "utf-8")
    return True


def main():  # -> NoReturn
    """Replaces mispronounced words with phonemes"""
    _file_out = ""
    _verbose = False
    # _output_type = [0, 1][0]  # Selector [text, confirmed json]
    _language = "en-CA"
    _my_dir = "macos_say"
    if os.name == "nt":
        _my_dir = "windows_sapi"
    _user_dir = "READ_JSON_USER_DIRECTORY"
    # _import_meta = readtexttools.ImportedMetaData()
    _text_file_in = sys.argv[-1]
    if os.path.isfile(_text_file_in):
        if sys.argv[-1] == sys.argv[0]:
            usage()
            sys.exit(0)
        try:
            opts, args = getopt.getopt(
                sys.argv[1:],
                "olmuvh",
                [
                    "output=",
                    "language=",
                    "model=",
                    "user_environ_dir=",
                    "verbose=",
                    "help",
                ],
            )
        except getopt.GetoptError:
            # print help information and exit:
            print("option was not recognized")
            usage()
            sys.exit(2)
        for o, a in opts:
            if o in ("-o", "--output"):
                _file_out = a
            elif o in ("-l", "--language"):
                _language = a
            elif o in ("-m", "--model"):
                _my_dir = a
            elif o in ("-u", "--user_environ_dir"):
                _user_dir = a
            elif o in ("-v", "--verbose"):
                _verbose = readtexttools.lax_bool(a)
            elif o in ("-h", "--help"):
                usage()
                sys.exit(0)
            else:
                assert False, "unhandled option"
        if not os.path.isfile(_text_file_in):
            usage()
            sys.exit(0)
        if not fix_up_text_file(
            _text_file_in, _file_out, _language, _my_dir, _user_dir, _verbose
        ):
            print("I was unable to find the file you specified!")
    sys.exit(0)


if __name__ == "__main__":
    main()
