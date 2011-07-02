#!/usr/bin/env python
# -*- coding: UTF-8-*-
'''
Reads a text file using espeak, mbrola and a media player.

The espeak program is a software speech synthesizer.
The mbrola synthesiser can improve the naturalness of speech. However, it
has licensing restrictions, and is not part of Debian's main repository.
Ubuntu makes mbrola and mbrola voices available in the multiverse repository.

Install mbrola by installing mbrola using your package manager or downloading
the mbrola binary and installing it. Download mbrola voices and copy or link 
the voice files into the appropriate directory. For example:

  /usr/share/mbrola/voices (Linux, OSX)
  C:\Program Files (x86)\eSpeak\espeak-data (Windows 64 bit)
  C:\Program Files\eSpeak\espeak-data (Windows 32 bit)
 
You only need to copy or link to the voices files themselves. 
In April 2011, compatible mbrola voices were: 

  af1, br1, br3, br4, cr1, cz2, de2, de4, de5, de6, de7, en1, 
  es1, es2, fr1, fr4, gr2, hu1, id1, it3, it4, la1, nl2, pl1, 
  pt1, ro1, sw1, sw2, tr1, tr2, us1, us2, us3

See also:  http://espeak.sourceforge.net/mbrola.html and 
http://tcts.fpms.ac.be/synthesis/

About mbrola:

  T. DUTOIT, V. PAGEL, N. PIERRET, F.  BATAILLE,
  O. VAN DER VRECKEN
  "The MBROLA Project: Towards a Set of High-Quality
  Speech Synthesizers Free of Use for
  Non-Commercial Purposes"
  Proc. ICSLP'96, Philadelphia, vol. 3, pp. 1393-1396.

or, for a more general reference to Text-To-Speech synthesis, the book :

  An Introduction to Text-To-Speech Synthesis,
  forthcoming textbook, T. DUTOIT, Kluwer Academic
  Publishers, 1997.

If you are using this extension to create still frame videos you need ffmpeg. 
Webm is the recommended video format. If you are creating a long video, be patient. 
It can take a long time for the external program to render the video.

Read Text Extension 0.7.12 or newer dialog:
  Read with an external program: 
    /usr/bin/python
  Normal Command line options: 
    "(ESPEAK_READ_TEXT_PY)" --language=(SELECTION_LANGUAGE_CODE) "(TMP)"
  Command line option to save as a .wav file: 
    "(ESPEAK_READ_TEXT_PY)" --language=(SELECTION_LANGUAGE_CODE) --output "(HOME)(NOW).wav" "(TMP)"

Copyright (c) 2011 James Holgate
'''
import getopt,sys,codecs,os,platform,readtexttools

def usage():
  sA = ' ' + os.path.split(sys.argv[0])[1]
  print ("")
  print ("Reads a text file using espeak and a media player.")
  print ("")
  print ("Usage")
  print (sA+' "input.txt"')
  print (sA+' --language [de|en|en-GB|es|fr|it] "input.txt"')
  print (sA+' --visible "false" "input.txt"')
  print (sA+' --output "output.wav" "input.txt"')
  print (sA+' --output "output.[m4a|mp2|mp3|ogg]" "input.txt"')
  print (sA+' --output "output.[avi|webm]" --image "input.[png|jpg]" "input.txt"')
  print (sA+' --audible "false" --output "output.wav" "input.txt"')
  print ("")

def espkread(sTXT,sLANG,sVISIBLE,sAUDIBLE,sTMP0,sIMG1,sB):
  '''
  sTXT - Text to speak
  sLANG - Supported two or four letter language code - defaults to US English
  sVISIBLE- Use a graphical media player,or False for a command line media player
  sTMP1 - Name of desired output file
  sAUDIBLE - If false, then don't play the sound file
  sIMG1 - a .png or .jpg file is required if we are making a movie, otherwise it is ignored.
  '''
  sOUT1=""
  if sLANG[:2].lower()=="de":
    s="de"
  elif sLANG[:2].lower()=="en":
    if sLANG[-2:].upper() in "AU;BD;BS;CA;GB;GH;HK;IE;IN;JM;NZ;PK;SA;TT":
      s="en"
    else:
      s="en-us"
  elif sLANG[:2].lower()=="es":
    if sLANG[-2:].upper() in "ES":
      s="es"
    elif sLANG[-2:].upper() in "MX":
      s="es-mx"
    else:
      s="es-la"
  elif sLANG[:2].lower()=="nb": 
    # *Office uses language code for Norwegian Bokmal - nb
    #  NO is the country code for Norway, not an official language code.
    s="no"
  elif sLANG[:2].lower()=="pt":
    if sLANG[-2:].upper() in "PT":
      s="pt-pt"
    else:
      s="pt"
  elif sLANG[:2].lower()=="zh":
    if sLANG[-2:].upper() in "HK;MO":
      # Yue is official language in Hong Kong & Macau
      s="zh-yue"
    else:
      s="zh"
  elif sLANG[:2].lower() in "af;bs;ca;cs;cy;da;de;el;eo;fi;fr;hi;hr;hu;hy;id;is;it;ku;la;lv;mk;nl;pl;ro;ru;sk;sq;sr;sv;sw;ta;tr;vi":
    s=sLANG[:2].lower()
  else:
    s="en"
# Check if an mbrola voice is available for the language, otherwise use the default espeak voice 
# If there are several compatible mbrola voices, this python script will choose the first one. 
# For example: de2 instead of de7
  ambrola = [ 'af1', 'br1', 'br3', 'br4', 'cr1', 'cz2', 'de2', 'de4', 'de5', 'de6', 'de7', 'en1', 'es1', 'es2', 'fr1', 'fr4', 'gr2', 'hu1', 'id1', 'it3', 'it4', 'la1', 'nl2', 'pl1', 'pt1', 'ro1', 'sw1', 'sw2', 'tr1', 'tr2', 'us1', 'us2', 'us3' ]
  aespeak = [ 'af', 'pt', 'pt', 'pt', 'hr', 'cs', 'de', 'de', 'de', 'de', 'de', 'en', 'es', 'es', 'fr', 'fr', 'el', 'hu', 'id', 'it', 'it', 'la', 'nl', 'pl', 'pt-pt', 'ro', 'sv', 'sv', 'tr', 'tr', 'en-us', 'en-us', 'en-us' ]
  sVoice=s # default to standard espeak voice
  for i in range(len(aespeak)):
    # Check voice
    if aespeak[i] == s:
      if "windows" in platform.system().lower():
        if os.path.isfile(os.path.join(os.getenv("ProgramFiles"),"eSpeak/espeak-data/mbrola",ambrola[i])):
          sVoice="mb-"+ambrola[i]
          break
        elif os.getenv("ProgramFiles(x86)"):
          if os.path.isfile(os.path.join(os.getenv("ProgramFiles(x86)"),"eSpeak/espeak-data/mbrola",ambrola[i])):
            sVoice="mb-"+ambrola[i]
            break 
      else:
        if os.path.isfile(os.path.join("/usr/share/mbrola/voices",ambrola[i])) or os.path.isfile(os.path.join("/usr/share/mbrola/",ambrola[i],ambrola[i])):
          sVoice="mb-"+ambrola[i]
          break
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
    # espeak must be in your system's path 
    # for example: /usr/bin/ or /usr/local/bin/
    sCommand="espeak"
    if "windows" in platform.system().lower():
      sCommand=readtexttools.getWinFullPath("eSpeak/command_line/espeak.exe")
    s1='"'+sCommand+'" -v '+sVoice+' -w "'+sTMP1+'" '+sTXT
    readtexttools.myossystem(s1)
    readtexttools.ProcessWaveMedia(sB,sTMP1,sIMG1,sOUT1,sAUDIBLE,sVISIBLE)
  except IOError, err:
    print 'I was unable to use espeak and read text tools!'
    usage()

def main():
  sLANG="en"
  sWAVE=""
  sVISIBLE=""
  sAUDIBLE=""
  sTXT=""
  sIMG1=""
  try:
    opts,args=getopt.getopt(sys.argv[1:],"hovali",["help","output=","visible=","audible=","language=","image="])
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
    sA=' " ' +sTXT.encode( "utf-8" )+'"'
    sB=sTXT.encode('ascii','replace')
    if len(sB) > 29: # limit of title length.
      sC=sTXT[:26].encode( "utf-8" )+'...'
    else:
      sC=sTXT[:29].encode( "utf-8" )
    espkread(sA,sLANG,sVISIBLE,sAUDIBLE,sWAVE,sIMG1,sC)
    sys.exit(0)

if __name__=="__main__":
  main()
