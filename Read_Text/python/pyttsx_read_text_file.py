#!/usr/bin/env python
# -*- coding: UTF-8-*-
r"""
Pyttsx
======

Read a plain text file in Windows using the Python `pyttsx` speech package.

  +  Designed for reading text aloud with the Windows SAPI5 system.
  +  For other systems, read the
     [documentation](https://github.com/parente/pyttsx)
     for `pyttsx`.

Windows
-------
  1.  Install [Python 2.x](http://www.python.org/).
  2.  Install [Python extensions for 
        Windows](http://sourceforge.net/projects/pywin32/files/).
  3.  Install the [pyttsx
      1.0](http://pypi.python.org/pypi/pyttsx/1.0)
      package.
      

Windows settings
----------------

1. Using [Read 
   Text](http://sites.google.com/site/readtextextension/)
   extension, choose *Tools > Add-Ons > Read Selection...*
2. In the dialogue, enter the following information:
   +  **External program**\
      `"C:\Program Files\Python\python.exe"` **or**\
      `"C:\Program Files\Python\pythonw.exe"`
   +  **Command line options**\
      `"(HOME)Downloads\read_text_file.py" "(TMP)"` **or**\
      `"(HOME)Downloads\read_text_file.py" --voice "Microsoft Sam" "(TMP)"`

Copyright
---------

`pyttsx_read_text_file.py` copyright (c) 2010 - 2018 James Holgate

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import codecs
import getopt
import os
import sys

try:
    import pyttsx
except ImportError:
    pass


def usage():
    sA = "    `" + os.path.split(sys.argv[0])[1]
    print(
        """
Pyttsx Read Text
================

Reads a text file using the Windows `pyttsx` library.

Usage
-----

* To say the text with a specific voice  
  {0} --voice "xxxxxx" "TextFile.txt"`
* To say the text with the default voice  
  {0} "TextFile.txt"`
* To say the text slower  
  {0} --rate "-20" "TextFile.txt"`
* To say the text faster  
  {0} --rate "20" "TextFile.txt"`)""".format(sA)
    )


def read_string_aloud(_name="", _rate=0, speechString=""):
    """
    Says speechString, using the default voice or _name voice
    Positive _rate is faster; Negative _rate is slower
    """
    try:
        dummy = bool(pyttsx)
    except NameError:
        print("FAIL: The `pyttsx` python library is not available.")
        usage()
        sys.exit(2)
    try:
        engine = pyttsx.init()
        engine.setProperty("rate", engine.getProperty("rate") + int(_rate))
    except Exception:
        print("I did not understand the rate!")
        usage()
        sys.exit(2)
    voices = engine.getProperty("voices")
    for voice in voices:
        if voice.name == _name:
            engine.setProperty("voice", voice.id)
            break
    engine.say(speechString)
    engine.runAndWait()


def main():  # -> NoReturn
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vrh", ["voice=", "rate=", "help"])
    except getopt.GetoptError:
        # print help information and exit:
        print("option -a not recognized")
        usage()
        sys.exit(2)
    _name = ""
    _rate = 0
    for o, a in opts:

        if o in ("-v", "--voice"):
            _name = a
        elif o in ("-r", "--rate"):
            _rate = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"
    try:
        f = codecs.open(sys.argv[-1], mode="r", encoding=sys.getfilesystemencoding())
    except IOError:
        print("I was unable to open the file you specified!")
        usage()
    else:
        s = f.read()
        f.close()
        read_string_aloud(_name, _rate, s)
        sys.exit(0)


if __name__ == "__main__":
    main()
