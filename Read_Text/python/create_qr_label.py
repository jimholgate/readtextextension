#!/usr/bin/env python
# -*- coding: UTF-8-*-
'''
To encode the text in a QR Code image file (png).

QR Code uses square patterns to encode characters in an image.
Readers are available in many mobile phone platforms. For Linux, 
use zbar. Zbar is an open source toolkit that can decode QR code
images (zbarimg) and scan QR codes with a webcam (zbarcam).
You can use QR Code images to facilitate inventory, track shipments,
record web addresses or make electronic business cards (vcards).

Tip: For most consumer cameras or phones, keep the length
of the selection as small as possible. Use less than 800 characters.

Install qrencode using a package manager or build it from source.

QR Code is registered trademark of DENSO WAVE INCORPORATED in the 
following countries: Japan, United States of America, Australia and Europe.
  
Read Text Extension for OpenOffice.org (for Linux) :
  See: http://sites.google.com/site/readtextextension/
  Tools > Add-Ons > Read Selection... Dialog setup:
  External program: /usr/bin/python
  Command line: "(CREATE_QR_LABEL_PY)" --output "(HOME)(NOW).png" "(TMP)"
  Option (huge): "(CREATE_QR_LABEL_PY)" --size 12 --output "(HOME)(NOW).png" "(TMP)"
  Option (tiny): "(CREATE_QR_LABEL_PY)" --size 1 --output "(HOME)(NOW).png" "(TMP)"
  Option (high error correction): "(CREATE_QR_LABEL_PY)" --level H --output "(HOME)(NOW).png" "(TMP)" 
  See the manual page for qrencode for more detailed information.
Copyright (c) 2011 James Holgate

'''
import getopt, sys, os, readtexttools

def usage():
  sA = ' ' + os.path.split(sys.argv[0])[1]
  print ("")
  print ("Usage")
  print (sA + ' [--size nn] [--level L|M|Q|H] --output "output.png" "input.txt"')
  print (' --size is pixel size of each little square')
  print (' --level is level of error correction - lowest to highest')
  print ("")

def qrencode(sTXT,sOUT1,sSIZE,sLEVEL):
  if sSIZE == "":
    sSIZE = "3"
  if sLEVEL == "":
    sLEVEL = "L"
  #Use cat to send literal text to qrencode...
  try: 
    s1 = 'cat "' + sTXT + '" | qrencode -s ' + sSIZE + ' -l ' + sLEVEL + ' -o "' + sOUT1 + '" '
    print s1
    readtexttools.myossystem(s1)
    #Display the image
    readtexttools.ShowWithApp(sOUT1)
  except IOError, err:
    print 'I was unable to use cat with qrencode!'
    print str(err)
    usage()
    sys.exit(2)

def main():
  sSIZE=""
  sLEVEL=""
  sOUT1=readtexttools.getTempPrefix()+"-qr-code.png"
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hosl", ["help", "output=", "size=","level="])
  except getopt.GetoptError, err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
      sys.exit(0)
    elif o in ("-o", "--output"):
      sOUT1=a
    elif o in ("-l", "--level"):
      sLEVEL=a
    elif o in ("-s", "--size"):
      sSIZE=a
    else:
      assert False, "unhandled option"
  sTXT=sys.argv[-1]
  qrencode(sTXT,sOUT1,sSIZE,sLEVEL)
  sys.exit(0)

if __name__ == "__main__":
  main()
