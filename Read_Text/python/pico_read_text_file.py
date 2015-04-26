#!/usr/bin/env python
# -*- coding: UTF-8-*-
from __future__ import (absolute_import, division, print_function, unicode_literals)
'''
Pico
====

Reads a text file using pico2wave and a media player.

The SVOX Pico engine is a software speech synthesizer for German, English (GB
and US), Spanish, French and Italian.

SVOX produces a clear and distinct speech output made possible by the use of
Hidden Markov Model (HMM) algorithms.

[SVOX Pico manual](http://www.sephidev.net/external/svox/pico_resources/docs/SVOX_Pico_Manual.pdf)

Install `pico2wave` using a package manager to install the following packages:

    libttspico0
    libttspico-utils
    libttspico-data

Due to license restrictions,the packages are formally part of Debian's 
non-free category rather than Debian proper ("main"). The packages are also
available in Ubuntu's multiverse repository.

If you are using this extension to create still frame videos you need ffmpeg or avconv. 
Webm is the recommended video format. If you are creating a long video, be patient. 
It can take a long time for the external program to render the video.
  
Read Selection... Dialog setup:
-------------------------------

External program: 

    /usr/bin/python 

Command line options (default): 

    "(PICO_READ_TEXT_PY)" --language=(SELECTION_LANGUAGE_CODE) "(TMP)"

or (save as a .wav file in the home directory): 

     "(PICO_READ_TEXT_PY)" --language=(SELECTION_LANGUAGE_CODE) --output "(HOME)(NOW).wav" "(TMP)"

See the manual page for `pico2wave` for more detailed information

[Read Text Extension](http://sites.google.com/site/readtextextension/)

Copyright (c) 2011 - 2015 James Holgate

'''
import getopt,sys,codecs,os,platform,readtexttools

def usage():
  sA = ' ' + os.path.split(sys.argv[0])[1]
  print ("")
  print ("Reads a text file using pico2wave and a media player.")
  print ("")
  print ("Usage")
  print((sA+' "input.txt"'))
  print((sA+' --language [de|en|en-GB|es|fr|it] "input.txt"'))
  print((sA+' --visible "false" "input.txt"'))
  print((sA+' --rate 80% --pitch 80% "input.txt"'))
  print((sA+' --output "output.wav" "input.txt"'))
  print((sA+' --output "output.[m4a|mp2|mp3|ogg]" "input.txt"'))
  print((sA+' --output "output.[avi|webm]" --image "input.[png|jpg]" "input.txt"'))
  print((sA+' --audible "false" --output "output.wav" "input.txt"'))
  print ("")

def picoread(sTXT,sLANG,sVISIBLE,sAUDIBLE,sTMP0,sIMG1,sB,sART):
  '''
  sTXT - Actual text to speak. The file must be written as utf-8.
  sLANG - Supported two or four letter language code - defaults to US English
  sVISIBLE- Use a graphical media player,or False for a command line media player
  sTMP0 - Name of desired output file
  sAUDIBLE - If false, then don't play the sound file
  sIMG1 - a .png or .jpg file is required if we are making a movie, otherwise it is ignored.
  sB - Track name or title
  sART - Artist or author
  '''
  sOUT1=""
  if sLANG[:2].lower()=="de":
    s="de-DE"
  elif sLANG[:2].lower()=="en":
    if sLANG[-2:].upper() in "AU;BD;BS;GB;GH;HK;IE;IN;JM;NZ;PK;SA;TT":
      s="en-GB"
    else:
      s="en-US"
  elif sLANG[:2].lower()=="es":
    s="es-ES"
  elif sLANG[:2].lower()=="fr":
    s="fr-FR"
  elif sLANG[:2].lower()=="it":
    s="it-IT"
  else:
    s="en-US"
  # Determine the output file name
  sOUT1=readtexttools.fsGetSoundFileName(sTMP0,sIMG1,"OUT")
  # Determine the temporary file name
  sTMP1=readtexttools.fsGetSoundFileName(sTMP0,sIMG1,"TEMP")

  # Some apps throw an error if we try to overwrite a file, so delete old versions
  if os.path.isfile(sTMP1):
    os.remove(sTMP1)
  if os.path.isfile(sOUT1):
    os.remove(sOUT1)
  try:
    if "windows" in platform.system().lower():
      sCommand=readtexttools.getWinFullPath("opt/picosh.exe")
      if "de" in s.lower():
        s1=sCommand+ ' –v de-DE_gl0 "' + sTXT+'" "'  + sTMP1 + '"'
      else: # Pico for Windows defaults to British English
        s1=sCommand+ ' "' + sTXT+'" "'  + sTMP1 + '"'
    else:
      sCommand='pico2wave'
      s1=sCommand+' -l '+s+' -w "'+sTMP1+'" '+sTXT 
    readtexttools.myossystem(s1)
    readtexttools.ProcessWaveMedia(sB,sTMP1,sIMG1,sOUT1,sAUDIBLE,sVISIBLE,sART)
  except (IOError):
    print ('I was unable to read!')
    usage()
    sys.exit(2)

def main():
  sLANG="en-US"
  sWAVE=""
  sVISIBLE=""
  sAUDIBLE=""
  sTXT=""
  sRATE="100%"
  sPITCH="100%"
  sIMG1=""
  sTIT=""
  sART=""
  sFILEPATH=sys.argv[-1]
  if os.path.isfile(sFILEPATH):
    try:
      opts,args=getopt.getopt(sys.argv[1:],"hovalrpitn",["help","output=","visible=","audible=","language=","rate=","pitch=","image=","title=","artist="])
    except (getopt.GetoptError):
      # print help information and exit
      print((str(err))) # will print something like "option -a not recognized"
      usage()
      sys.exit(2)
    for o,a in opts:
      if o in ("-h","--help"):
        usage()
        sys.exit(0)
      elif o in ("-o","--output"):
        sWAVE=a
      elif o in ("-v","--visible"):
        sVISIBLE=a
      elif o in ("-a","--audible"):
        sAUDIBLE=a
      elif o in ("-l","--language"):
        sLANG=a
      elif o in ("-r","--rate"):
        sRATE=a
      elif o in ("-p","--pitch"):
        sPITCH=a
      elif o in ("-i","--image"):
        sIMG1=a
      elif o in ("-t","--title"):
        sTIT=a
      elif o in ("-n","--artist"):
        sART=a
      else:
        assert False,"unhandled option"
    try:
      oFILE=codecs.open(sFILEPATH,mode='r',encoding='utf-8')
    except (IOError):
      print ('I was unable to open the file you specified!')
      usage()
    else:
      sTXT=oFILE.read()
      oFILE.close()
      if len(sTXT) != 0:
        sTXT=readtexttools.cleanstr(sTXT)
        sA="' <speed level="+'"'+sRATE+'"><pitch level='+'"'+sPITCH+'"> ' +sTXT+"</pitch></speed>'"
        sB=readtexttools.checkmyartist(sART)
        sC=readtexttools.checkmytitle(sTIT,"pico")
        picoread(sA,sLANG,sVISIBLE,sAUDIBLE,sWAVE,sIMG1,sC,sB)
  else:
    print ('I was unable to find the file you specified!') 
  sys.exit(0)

if __name__=="__main__":
  main()
