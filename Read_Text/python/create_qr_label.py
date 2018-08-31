#!/usr/bin/env python
# -*- coding: UTF-8-*-
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals
                        )
'''
QR Code
=======

Encode text in a QR Code image file (png).

QR Code uses square patterns to encode characters in an image.
Readers are available in many mobile phone platforms. For Linux,
use zbar. Zbar is an open source toolkit that can decode QR code
images (zbarimg) and scan QR codes with a webcam (zbarcam).
You can use QR Code images to facilitate inventory, track shipments,
record web addresses or make electronic business cards (vcards).

**Tip**: For most consumer cameras or phones, keep the length
of the selection as small as possible. Use less than 800 characters.

Install qrencode using a package manager or build it from source.

QR Code is registered trademark of DENSO WAVE INCORPORATED in the
following countries: Japan, United States of America, Australia and
Europe.

[qrencode](http://fukuchi.org/works/qrencode/)
[zbar](http://zbar.sourceforge.net/)

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

Copyright (c) 2010 - 2018 James Holgate

'''
import getopt
import os
import sys
import readtexttools


def usage():
    sA = ' ' + os.path.split(sys.argv[0])[1]
    print ("\n\nQR Code")
    print ("=======\n")
    print ("Encode text in a QR Code image (png). Requires `qrencode`.\n")
    print ("Usage")
    print ("-----\n")
    print(('    '+sA + ' [--size nn] [--level L|M|Q|H] \ '))
    print(('      --output "output.png" "input.txt"\n'))
    print ('`--size` is the pixel size of each little square. ')
    print ('`--level` is the level of error correction - low to high. \n')
    print ('See the manual page for `qrencode` for more information.\n')
    print ("Copyright notice")
    print ("----------------\n")
    print ('*QR Code* is registered trademark of DENSO WAVE INCORPORATED')
    print (' in the following countries: Japan, United States of')
    print (' America, Australia and Europe. \n')


def qrencode(sTXT, sOUT1, sSIZE, sLEVEL):
    '''
    Display a barcode of the selected text
      sTXT - the text to display
      sOUT - the output file
      sSIZE - The dimension of each qr code square
      sLEVEL - The degree of redundant data for error correction
    '''
    if sSIZE == "":
        sSIZE = "3"
    if sLEVEL == "":
        sLEVEL = "L"
    # Use cat to send literal text to qrencode...
    try:
        s1 = 'cat "' + sTXT + '" | qrencode -s ' + sSIZE + ' -l ' + sLEVEL
        s1 = s1 + ' -o "' + sOUT1 + '" '
        print (s1)
        readtexttools.myossystem(s1)
        # Display the image
        readtexttools.ShowWithApp(sOUT1)
    except (IOError):
        print ('I was unable to use cat with qrencode!')
        usage()
        sys.exit(2)


def main():
    sSIZE = ""
    sLEVEL = ""
    sOUT1 = ""

    try:
        sOUT1 = readtexttools.getTempPrefix()+"-qr-code.png"
    except:
        sOUT1 = ""
    sTXT = sys.argv[-1]
    if os.path.isfile(sTXT):
        if sys.argv[-1] == sys.argv[0]:
            usage()
            sys.exit(0)
        try:
            opts, args = getopt.getopt(sys.argv[1:],
                                       "hosl",
                                       ["help",
                                        "output=",
                                        "size=",
                                        "level="]
                                       )
        except (getopt.GetoptError):
            # print help information and exit:
            print ("option was not recognized")
            usage()
            sys.exit(2)
        for o, a in opts:
            if o in ("-h", "--help"):
                usage()
                sys.exit(0)
            elif o in ("-o", "--output"):
                sOUT1 = a
            elif o in ("-l", "--level"):
                sLEVEL = a
            elif o in ("-s", "--size"):
                sSIZE = a
            else:
                assert False, "unhandled option"
        if (os.path.isfile('/usr/bin/qrencode') !=
                os.path.isfile('/usr/bin/python')):
            usage()
        else:
            qrencode(sTXT, sOUT1, sSIZE, sLEVEL)
    else:
        print ('I was unable to find the file you specified!')
    sys.exit(0)


if __name__ == "__main__":
    main()
