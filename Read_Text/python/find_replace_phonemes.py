#!/usr/bin/env python3
# -*- coding: UTF-8-*-
import readtexttools
import getopt
import os
import sys


def usage():  # -> None
    '''Show usage'''
    print('''
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

MacOS 13 and MaryTTS can use a subset of the International Phonetic Alphabet.
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

''')


def main():  # -> NoReturn
    '''Replaces mispronounced words with phonemes'''
    _file_out = ''
    _output_type = [0, 1][0]  # Selector [text, confirmed json]
    _language = 'en-CA'
    _my_dir = 'macos_say'
    _user_dir = 'READ_JSON_USER_DIRECTORY'
    _import_meta = readtexttools.ImportedMetaData()
    _text_file_in = sys.argv[-1]
    if os.path.isfile(_text_file_in):
        if sys.argv[-1] == sys.argv[0]:
            usage()
            sys.exit(0)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "holmu", [
                "help", "output=", "language=", "model=", "user_environ_dir="
            ])
        except getopt.GetoptError:
            # print help information and exit:
            print("option was not recognized")
            usage()
            sys.exit(2)
        for o, a in opts:
            if o in ("-h", "--help"):
                usage()
                sys.exit(0)
            elif o in ("-o", "--output"):
                _file_out = a
            elif o in ("-l", "--language"):
                _language = a
            elif o in ("-m", "--model"):
                _my_dir = a
            elif o in ("-u", "--user_environ_dir"):
                _user_dir = a
            else:
                assert False, "unhandled option"
        if not os.path.isfile(_text_file_in):
            usage()
        if os.path.splitext(_file_out)[1] in ['.json', '.js']:
            _output_type = [0, 1][1]
        _content2 = readtexttools.local_pronunciation(
            _language,
            readtexttools.strip_mojibake(
                _language, _import_meta.meta_from_file(_text_file_in, False),
                False), _my_dir, _user_dir, True)
        if not bool(_file_out):
            _file_out = _text_file_in
        if os.path.splitext(_file_out)[1] in ['.json', '.js']:
            _output_type = [0, 1][1]
            print(_content2[1])  # json table
        readtexttools.write_plain_text_file(_file_out, _content2[_output_type],
                                            'utf-8')
    else:
        print('I was unable to find the file you specified!')
    sys.exit(0)


if __name__ == "__main__":
    main()
