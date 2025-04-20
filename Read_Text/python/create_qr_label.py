"""
QR Code
=======

Encode text in a QR Code image file (png).

QR Code uses square patterns to encode characters in an image.
Readers are available in many mobile phone platforms.

You can use QR Code images to facilitate inventory, track shipments,
record web addresses or make electronic business cards (vcards).

**Tip**: For most consumer cameras or phones, keep the length
of the selection as small as possible. Use less than 800 characters.

Requires python 3.8 or newer.

Use a system package manager:

    apt-get install python3-pil python3-qrcode

or install `qrcode` as a local user:

    pip3 install qrcode
    pip3 install Pillow

QR Code is registered trademark of DENSO WAVE INCORPORATED in the
following countries: Japan, United States of America, Australia and
Europe.

* [python qrcode](https://pypi.org/project/qrcode/)
* [zbar](http://zbar.sourceforge.net/)
* [QuickChart.io](https://github.com/typpo/quickchart) code uses the
GNU Affero General Public License v3.0 license, which is displayed at
[GitHub](https://raw.githubusercontent.com/typpo/quickchart/master/LICENSE).

Read Selection... Dialog setup:
-------------------------------

External program:

        /usr/bin/python

Command line options (default size):

        "(CREATE_QR_LABEL_PY)" --output "(HOME)(NOW).png" "(TMP)"

or (large size):

        "(CREATE_QR_LABEL_PY)" --size 12 --output "(HOME)(NOW).png"

or (high error correction):

        "(CREATE_QR_LABEL_PY)" --level H --output "(HOME)(NOW).png"

See the manual page for `qrencode` for more detailed information.

[Read Text Extension](http://sites.google.com/site/readtextextension/)

Copyright (c) 2010 - 2025 James Holgate
"""

import os
import sys
import readtexttools
from urllib.parse import quote

try:
    import codecs
    import getopt
    import webbrowser
except (ImportError, AssertionError, AttributeError):
    pass
try:
    from qrcode.image.pil import PilImage

    IMAGE_OK = True
except ImportError:
    IMAGE_OK = False
try:
    import qrcode
except ImportError:
    if len(readtexttools.find_local_pip("qrcode")) != 0:
        sys.path.append(readtexttools.find_local_pip("qrcode"))
        try:
            import qrcode
        except:
            print(
                """
A python tool cannot find a library that it
needs to create a QR code. Try 

    pip3 install qrcode
    pip3 install Pillow
"""
            )


def usage():  # -> None
    """Show help text"""
    try:
        sA = os.path(sys.argv[0])[1]
    except TypeError:
        sA = "create_qr_label.py"
    print(
        """QR Code
=======

Encode text in a QR Code image (png). Requires `qrcode`.

    pip3 install qrcode
    pip3 install Pillow

Usage
-----

    {0} [--size nn] [--level L|M|Q|H] \\ 
    --fill "0,0,0", --background "255,255,255" \\
    --output "output.png" "input.txt"

`--size` is the pixel size of each little square. 
`--level` is the level of error correction - low to high. 
`--fill` is the foreground color
`--background` is the background color

See <https://pypi.org/project/qrcode/> for more information.

Copyright notice
----------------

*QR Code* is registered trademark of DENSO WAVE INCORPORATED
in the following countries: Japan, United States of America,
Australia and Europe. """.format(
            sA
        )
    )


def rgb_to_tuple(_color="", fallback="black"):  # -> str / tuple
    """Checks an rgb string and converts it to a rgb tuple
    if possible, otherwise the returns a fallback string."""
    if not bool(fallback):
        fallback = "black"
    if not bool(_color):
        return fallback.lower()
    if "," in _color:
        try:
            return eval(readtexttools.safechars(_color))
        except (NameError, SyntaxError):
            return fallback.lower()
    return fallback.lower()


def qrencode(
    _content="", _image_out="", _size="3", _level="L", _fill_color="", _back_color=""
):  # -> bool
    """
    Display a barcode of the selected text

    * _content - the text to display
    * _image_out - the output file
    * _size - The dimension of each QR Code square
    * _level - The degree of redundant data for error correction
    """
    if not bool(_size):
        _size = "3"
    _fill_color = rgb_to_tuple(_fill_color, "black")
    _back_color = rgb_to_tuple(_back_color, "white")
    _checked_size = 3
    for i in range(31):
        if _size == str(i + 1):
            _checked_size = i + 1
            break
    if not _level in ["L", "M", "Q", "H"]:
        _level = "L"
    _content = _content.strip()
    _image_out = _image_out.strip()
    try:
        correction_level = [
            {"_switch": "L", "_int_level": qrcode.constants.ERROR_CORRECT_L},  # 1
            {"_switch": "M", "_int_level": qrcode.constants.ERROR_CORRECT_M},  # 0
            {"_switch": "Q", "_int_level": qrcode.constants.ERROR_CORRECT_Q},  # 3
            {"_switch": "H", "_int_level": qrcode.constants.ERROR_CORRECT_H},
        ]  # 2
        _error_correct = 0

        for i in range(len(correction_level)):
            if correction_level[i]["_switch"].upper() == _level:
                _error_correct = correction_level[i]["_int_level"]
                break
        qr = qrcode.QRCode(
            version=None,
            error_correction=_error_correct,
            box_size=_checked_size,
            border=5,
        )

        qr.add_data(_content)
        qr.make(fit=True)
        img = qr.make_image(fill_color=_fill_color, back_color=_back_color)
        img.save(_image_out)
        if os.path.isfile(_image_out):
            readtexttools.show_with_app(_image_out)
            return True
        return False
    except ValueError:
        qrencode(_content, _image_out, _size, _level, "black", "white")
    except NameError:
        usage()
        _content = quote(_content)
        _url = "https://quickchart.io/qr?size=350&amp;text={}".format(_content)
        _msg = """<{}>""".format(_url)
        if not readtexttools.pop_message(
            "`qrcode` missing. `pip3 install qrcode[pil]`",
            _msg,
            5000,
            readtexttools.net_error_icon(),
            1,
        ):
            readtexttools.show_with_app(_url)
        return False
    except Exception:
        try:
            webbrowser.open(_url)
        except [AttributeError, TypeError]:
            readtexttools.web_info_translate(
                "Exception - `qrcode`, `Pillow` or `webbrowser` failure", "en"
            )


def main():  # -> NoReturn
    """Get information for the QR code program"""
    _size = "3"
    _level = "M"
    _image_out = ""
    _fill_color = "0, 0, 0"  # `black` `rgb(0, 0, 0)`
    _back_color = "255, 255, 255"  # `white` `rgb(255, 255, 255)`

    try:
        _image_out = os.path.join(readtexttools.get_temp_prefix(), "rte-qr-code.png")
    except:
        _image_out = ""
    _text_file_in = sys.argv[-1]
    if os.path.isfile(_text_file_in):
        if sys.argv[-1] == sys.argv[0]:
            usage()
            sys.exit(0)
        try:
            opts, args = getopt.getopt(
                sys.argv[1:],
                "oslfbh",
                ["output=", "size=", "level=", "fill=", "background=", "help"],
            )
        except getopt.GetoptError:
            # print help information and exit:
            print("option was not recognized")
            usage()
            sys.exit(2)
        for o, a in opts:
            if o in ("-o", "--output"):
                _image_out = a
            elif o in ("-s", "--size"):
                _size = a
            elif o in ("-l", "--level"):
                _level = a
            elif o in ("-f", "--fill"):
                _fill_color = a
            elif o in ("-b", "--background"):
                _back_color = a
            elif o in ("-h", "--help"):
                usage()
                sys.exit(0)
            else:
                assert False, "unhandled option"
        if not os.path.isfile(_text_file_in):
            usage()
            sys.exit(0)
        _file_handle = codecs.open(_text_file_in, mode="r", encoding="utf-8")
        _content = _file_handle.read()
        _file_handle.close()
        qrencode(_content, _image_out, _size, _level, _fill_color, _back_color)
    else:
        print("I was unable to find the file you specified!")
    sys.exit(0)


if __name__ == "__main__":
    main()
