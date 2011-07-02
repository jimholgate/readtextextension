#!/usr/bin/env python
# -*- coding: UTF-8-*-
'''
Reads a text file using pico2wave and a media player.

The SVOX Pico engine is a software speech synthesizer for German,English (GB
 and US),Spanish,French and Italian.

SVOX produces a clear and distinct speech output made possible by the use of
Hidden Markov Model (HMM) algorithms.

See: http://www.sephidev.net/external/svox/pico_resources/docs/SVOX_Pico_Manual.pdf

Install pico2wave using a package manager to install the following packages:

libttspico0
libttspico-utils
libttspico-data

If you are using this extension to create still frame videos you need ffmpeg. Webm is the  
recommended video format. If you are creating a long video, be patient. It can take a long
time for the external program to render the video.

Due to license restrictions,the packages are formally part of Debian's 
non-free category rather than Debian proper ("main"). The packages are also
available in Ubuntu's multiverse repository.

Read Text Extension 0.7.8 or newer dialog:
  Read with an external program: 
    /usr/bin/python
  Normal Command line options: 
    "(PICO_READ_TEXT_PY)" --language=(SELECTION_LANGUAGE_CODE) "(TMP)"
  Command line option to save as a .wav file: 
    "(PICO_READ_TEXT_PY)" --language=(SELECTION_LANGUAGE_CODE) --output "(HOME)(NOW).wav" "(TMP)"

Copyright (c) 2011 James Holgate
'''
import getopt,sys,codecs,os,platform,readtexttools

def usage():
  sA = ' ' + os.path.split(sys.argv[0])[1]
  print ("")
  print ("Reads a text file using pico2wave and a media player.")
  print ("")
  print ("Usage")
  print (sA+' "input.txt"')
  print (sA+' --language [de|en|en-GB|es|fr|it] "input.txt"')
  print (sA+' --visible "false" "input.txt"')
  print (sA+' --rate 80% --pitch 80% "input.txt"')
  print (sA+' --output "output.wav" "input.txt"')
  print (sA+' --output "output.[m4a|mp2|mp3|ogg]" "input.txt"')
  print (sA+' --output "output.[avi|webm]" --image "input.[png|jpg]" "input.txt"')
  print (sA+' --audible "false" --output "output.wav" "input.txt"')
  print ("")

def picoread(sTXT,sLANG,sVISIBLE,sAUDIBLE,sTMP0,sIMG1,sB):
  '''
  sTXT - Text to speak
  sLANG - Supported two or four letter language code - defaults to US English
  sVISIBLE- Use a graphical media player,or False for a command line media player
  sTMP0 - Name of desired output file
  sAUDIBLE - If false, then don't play the sound file
  sIMG1 - a .png or .jpg file is required if we are making a movie, otherwise it is ignored.
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
    readtexttools.ProcessWaveMedia(sB,sTMP1,sIMG1,sOUT1,sAUDIBLE,sVISIBLE)
  except IOError,err:
    print 'I was unable to read!'
    print str(err)
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
  try:
    opts,args=getopt.getopt(sys.argv[1:],"hovalrpi",["help","output=","visible=","audible=","language=","rate=","pitch=","image="])
  except getopt.GetoptError,err:
    # print help information and exit
    print str(err) # will print something like "option -a not recognized"
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
    else:
      assert False,"unhandled option"
  try:
    sFILEPATH=sys.argv[-1]
    oFILE=codecs.open(sFILEPATH,mode='r',encoding=sys.getfilesystemencoding())
  except IOError:
    print 'I was unable to open the file you specified!'
    usage()
  else:
    sTXT=oFILE.read().replace(u" '",u" ‘").replace(u"'",u"’").replace(u' "',u" “").replace(u'"',u'”')
    oFILE.close()
    sA="' <speed level="+'"'+sRATE+'"><pitch level='+'"'+sPITCH+'"> ' +sTXT.encode( "utf-8" )+"</pitch></speed>'"
    sB=sTXT.encode('ascii','replace')
    if len(sB) > 29: # limit of title length.
      sC=sTXT[:26].encode( "utf-8" )+'...'
    else:
      sC=sTXT[:29].encode( "utf-8" )
    picoread(sA,sLANG,sVISIBLE,sAUDIBLE,sWAVE,sIMG1,sC)
    sys.exit(0)

if __name__=="__main__":
  main()
