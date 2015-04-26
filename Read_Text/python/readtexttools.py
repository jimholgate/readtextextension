#!/usr/bin/env python
# -*- coding: UTF-8-*-
from __future__ import (absolute_import, division, print_function, unicode_literals)
'''
Read Text Library
=================

Common tools for Read Text Extension. 

Reads a .wav sound file, converts it and/or plays it with a media player.
  
Usage
-----

Audio: 

    python readtexttools.py --sound="poster.wav" --output="poster.ogg"
    python readtexttools.py --visible="false" --audible="true" --sound="poster.wav" --output="poster.ogg"

Video: 

    python readtexttools.py --image="poster.png" --sound="poster.wav" --output="poster.webm"
    python readtexttools.py --visible="true" --audible="true" --image="poster.png" --sound="poster.wav" --title="Pretty lake" --output="poster.webm"

If the image in the movie is distorted, then the input image may be corrupt or unusable. Images directly 
exported from the office program may not work. Fix the image by opening it with an image editor like `gimp`
and trimming the image so that the proportions match the desired output video proportions. Export the 
trimmed image as a `jpg` or `png` image file.

Experimental issues
-------------------

Experimental codecs might produce bad results. If the command line includes `-strict experimental`, you 
should check the output file on different devices. Python2  still works, but python3 is *strongly*
recommended, especially for using the speech-dispatcher and multilingual (unicode) metadata.

[Read Text Extension](http://sites.google.com/site/readtextextension/)

Copyright (c) 2011 - 2015 James Holgate
'''
import getopt,sys,codecs,os,platform,time,wave,math,subprocess,shlex

def usage():
  '''
  Displays the usage of the included python app "main", which can be used to convert
  wav files to other formats like ogg audio or webm video.
  '''
  sA = ' ' + os.path.split(sys.argv[0])[1]
  print ("")
  print ("Reads a .wav sound file, converts it, and plays copy with a media player.")
  print ("")
  print ("Usage")
  print (" Audio:")
  print((sA+u' --sound="poster.wav" --output="poster.ogg"'))
  print((sA+u' --visible="false" --audible="true" --sound="poster.wav" --output="poster.ogg"'))
  print (" Video:")
  print((sA+u' --image="poster.png" --sound="poster.wav" --output="poster.webm"'))
  print((sA+u' --visible="true" --audible="true" --image="poster.png" --sound="poster.wav" --title="Pretty lake" --output="poster.webm"'))
  print ("")

def fsAppSignature():
  retVal = "ca.bc.vancouver.holgate.james.readtextextension"
  return retVal

def fsAppName():
  retVal = "Read Text"
  return retVal

def fsGetSoundFileName(sTMP1,sIMG1,sType1):
  '''
  Determine the temporary filename or output filename 
  Given the filename sTMP1, returns a temporary filename if sType1 is "TEMP"
  or the output filename if sType1 is anything else. 
  Example: 
  import readtexttools
  # Determine the temporary file name
  sTMP1=readtexttools.fsGetSoundFileName(sTMP1,sIMG1,"TEMP")
  # Determine the output file name
  sOUT1=readtexttools.fsGetSoundFileName(sTMP1,sIMG1,"OUT")
  '''
  sOUT1=""
  if sTMP1=="":
    sTMP1=getTempPrefix()+u"-speech.wav"
  sTMP1EXT=os.path.splitext(sTMP1)[1].lower()
  sIMG1FILEEXT=os.path.splitext(sIMG1)[1].lower()
  if sTMP1EXT==".mp3":
      if os.path.isfile("/usr/bin/lame") or os.path.isfile(r"C:\opt\lame.exe"): 
        sOUT1=sTMP1
        sTMP1=sOUT1+u".wav"
      else:
        # Can't make mp3,so make wav
        sOUT1=sTMP1+u".wav"
        sTMP1=sOUT1
  elif sTMP1EXT==".m4a":
      if os.path.isfile("/usr/bin/faac") or os.path.isfile(r"C:\opt\neroAacEnc.exe") or os.path.isfile(r"C:\opt\faac.exe"):
        sOUT1=sTMP1
        sTMP1=sOUT1+u".wav"
      else:
        # Can't make m4a,so make wav
        sOUT1=sTMP1+u".wav"
        sTMP1=sOUT1
  elif sTMP1EXT==".ogg":
      if os.path.isfile("/usr/bin/oggenc") or os.path.isfile(r"C:\opt\oggenc.exe") or os.path.isfile(r"C:\opt\oggenc2.exe"):
        sOUT1=sTMP1
        sTMP1=sOUT1+u".wav"
      else:
        # Can't make ogg,so make wav
        sOUT1=sTMP1+u".wav"
        sTMP1=sOUT1
  elif sTMP1EXT==".aif":
      if os.path.isfile("/usr/bin/avconv") or os.path.isfile("/usr/bin/ffmpeg") or os.path.isfile(r"C:\opt\ffmpeg.exe"):
        sOUT1=sTMP1
        sTMP1=sOUT1+u".wav"
      else:
        # Can't make aif, so make wav
        sOUT1=sTMP1+u".wav"
        sTMP1=sOUT1
  elif sTMP1EXT==".flac":
      if os.path.isfile("/usr/bin/avconv") or os.path.isfile("/usr/bin/ffmpeg") or os.path.isfile(r"C:\opt\flac.exe"):
        sOUT1=sTMP1
        sTMP1=sOUT1+u".wav"
      else:
        # Can't make flac, so make wav
        sOUT1=sTMP1+u".wav"
        sTMP1=sOUT1
  elif sTMP1EXT in ".avi;.webm;.m4v;.mov;.mpg;.mp4;.wmv":
      if (os.path.isfile("/usr/bin/avconv") or os.path.isfile("/usr/bin/ffmpeg") or os.path.isfile(r"C:\opt\ffmpeg.exe")) and sIMG1FILEEXT in ".bmp;.gif;.jpeg;.jpg;.png;.tif;.tiff;.tga;":
        sOUT1=sTMP1
        sTMP1=sOUT1+u".wav"
      else:
        # Can't make video,so make wav
        sOUT1=sTMP1+u".wav"
        sTMP1=sOUT1
  if sType1=="TEMP":
    retVal=sTMP1
  else:
    retVal=sOUT1
  return retVal

def ProcessWaveMedia(sB,sTMP1,sIMG1,sOUT1,sAUDIBLE,sVISIBLE,sART):
  '''
  Converts audio file, plays copy and deletes original
  sB is brief title
  sTMP is working file name (wav)
  sIMG1 is image to add to video. Ignored if making audio only
  sOUT1 is output file name.( webm, ogg etc.)
  sAUDIBLE - Do we play the file after conversion?
  sVISIBLE - Do we use a GUI or the console?
  '''
  Wav2Media(sB,sTMP1,sIMG1,sOUT1,sAUDIBLE,sVISIBLE,sART)
  try:
    if sOUT1=='':
      print((u'Saved to: '+sTMP1))
    else:
      if os.path.isfile(sTMP1):
        os.remove(sTMP1)
  except (OSError, e):
    print((u'Could not remove "'+sTMP1+u'"'))

def WavtoSeconds(sTMP1):
  '''
  Tells approximately how long a sound in a wav file is in seconds
  as a integer
  '''
  wave_read=wave.open(sTMP1,'r')
  retVal=math.ceil(wave_read.getnframes()//wave_read.getframerate())+1
  wave_read.close()
  return retVal

def Wav2Media(sB,sTMP1,sIMG1,sOUT1,sAUDIBLE,sVISIBLE,sART):
  '''
  Wav2Media
  =========
  
  Converts a wave audio file to another sound or movie format and plays a copy.

      sB is brief title
      sTMP1 is working file name (wav)
      sIMG1 is image to add to video. Ignored if making audio only
      sOUT1 is output file name.( webm, ogg etc.)
      sAUDIBLE - Do we play the file after conversion?
      sVISIBLE - Do we use a GUI or the console?

  '''
  LockMyLock()
  sTT=sB
  iTIME=WavtoSeconds(sTMP1)
  sTIME=repr(iTIME)
  sOUT1EXT=os.path.splitext(sOUT1)[1].lower()
  sTMP1EXT=os.path.splitext(sTMP1)[1].lower()
  sIMG1FILEEXT=os.path.splitext(sIMG1)[1].lower()
  sARTIST = ""
  try:
    sTT=cleanstr(sTT)
    sTY=time.strftime("%Y")
    s1=sART
    if len(s1)==0:
      print(u"No artist name found. Trying system user name.")
    else:
      sARTIST=sART
  except (UnicodeDecodeError):
    sARTIST=fsAppName
    sTT=timefortitle()
    sTL=u"("+fsAppName()+u")"
    sTG="Speech"
    sTY=time.strftime("%Y")
  try:
    sTL=u"("+fsAppName()+u")"
    sTG=u"Speech"
    print (u'-----------------------------------------------------')
    print (fsAppName())
    print (u'')
    print((u'Title: ' + sTT))
    print((u'Working File Name: ' + sTMP1))
    print((u'File Name: ' + sOUT1))
    print((u'Duration in seconds: ' + sTIME))
    print (u'-----------------------------------------------------')
  except (UnicodeDecodeError):
    sARTIST=" "
    sTT=" "
    sTL=" "
    sTG=" "
    sTY=" "
  try:  
    sFFmeta=u''
    if "windows" in platform.system().lower():
      sFFcommand=getWinFullPath("opt/ffmpeg.exe")
    else:
      if os.path.isfile("/usr/bin/avconv"):
        sFFcommand='avconv'
      else:
        sFFcommand='ffmpeg' 
    if sOUT1EXT==".ogg":
      sTY=time.strftime("%Y-%m-%d")
      if "windows" in platform.system().lower():
        # The program is supplied in a zip file. To use it in this script, you need to extract it to the directory shown.
        # C:/opt/oggenc.exe or C:/opt/oggenc2.exe
        # See: http://www.rarewares.org/ogg-oggenc.php for oggenc2.exe 
        # The Ogg sound format is open. Chromium, Firefox, and Google Chrome can play ogg sound files. 
        # You can also get free plugins for Windows Media Player and Apple Quicktime.
        s0=getWinFullPath("/opt/oggenc2.exe")
        if len(s0)==0:
          s0=getWinFullPath("/opt/oggenc.exe")
        s1=s0+u' -o "'+sOUT1+u'" "'+sTMP1+u'"'
        myossystem(s1)
      else:
        try:
          sFFmeta=u'--album "'+sTL+u'" --artist "'+sARTIST+u'" --title "'+sTT+u'" --genre "'+sTG+u'" --year '+sTY+u' -o "'
        except(UnicodeDecodeError):
          sFFmeta=""
        s1=u'oggenc '+sFFmeta+u" "+sOUT1+u'" "'+sTMP1+u'"'
        myossystem(s1)
    elif sOUT1EXT==".m4a":
      if "windows" in platform.system().lower():
        # The programs are supplied in a zip file. To use them in this script, you need to extract them to the directories shown.
        # C:/opt/neroAacEnc.exe
        # See: http://www.nero.com/enu/downloads-nerodigital-nero-aac-codec.php
        s0=getWinFullPath("/opt/neroAacEnc.exe")
        if len(s0)==0:
          s0=getWinFullPath("/opt/faac.exe")
          s1=s0+u' -o "'+sOUT1+u'" "'+sTMP1+u'"'
        else:
          s1=s0+u' -if "'+sTMP1+u'" -of "'+sOUT1+u'"'
        myossystem(s1)
      else:
        try:
          sFFmeta=u'--album "'+sTL+u'" --artist "'+sARTIST+u'" --title "'+sTT+u'" --genre "'+sTG+u'" --year '+sTY+u' -o "'
        except(UnicodeDecodeError):
          sFFmeta=""
        s1=u'faac '+sFFmeta+sOUT1+u'" "'+sTMP1+u'"'
        myossystem(s1)
    elif sOUT1EXT==".mp3":
      if "windows" in platform.system().lower():
        # The program is supplied in a zip file. To use it in this script, you need to extract it to the directory shown.
        # C:/opt/lame.exe
        #see:  http://www.rarewares.org/mp3-lame-bundle.php
        s0=getWinFullPath("/opt/lame.exe")
        s1=s0+u' -V 4 --tl "'+sTL+u'" --ta "'+sARTIST+u'" --tt "'+sTT+u'" --tg "'+sTG+u'" --ty '+sTY+u' "'+sTMP1+u'" "'+sOUT1+u'"'
        myossystem(s1)
      else:
        try:
          sFFmeta = u' --tl "'+sTL+u'" --ta "'+sARTIST+u'" --tt "'+sTT+u'" --tg "'+sTG+u'" --ty "'+sTY+u'" '
        except(UnicodeDecodeError,TypeError):
          sFFmeta=""
        s1= 'lame '+sFFmeta+' "'+sTMP1+'" "'+sOUT1+'"'
        myossystem(s1)
    elif sOUT1EXT==".aif":
      try:
        sFFmeta=u' -metadata title="'+sTT+u'" -metadata album="'+sTL+u'" '
      except(UnicodeDecodeError):
        sFFmeta=""
      s1=u'"'+sFFcommand +u'" -i "'+sTMP1+u'" '+sFFmeta+u' -y "'+sOUT1+u'"'
      print (s1)
      myossystem(s1)
    elif sOUT1EXT==".flac":
      if "windows" in platform.system().lower():
        # The programs is supplied in a zip file. To use it in this script, you need to extract it to the directory shown.
        # C:/opt/flac.exe
        # See: http://flac.sourceforge.net/
        s0=getWinFullPath("/opt/flac.exe")
        s1=s0+u' -f -o "'+sOUT1+u'" "'+sTMP1+u'"'
        myossystem(s1)
      else:
        try:
          sFFmeta=u' -metadata title="'+sTT+u'" -metadata album="'+sTL+u'" '
        except(UnicodeDecodeError):
          sFFmeta=u''
        s1=u'"'+sFFcommand +u'" -i "'+sTMP1+u'" '+sFFmeta+u' -y "'+sOUT1+u'"'
        myossystem(s1)
    elif sOUT1EXT==".webm":
      # Chrome, Firefox (Linux) and totem can open webm directly. Edit webm with openshot or pitivi or upload directly to Youtube.
      # The webm movie format uses Vorbis audio and VP8 video regardless of authoring program or platform.
      try:
        sFFmeta=u' -metadata title="'+sTT+u'" -metadata Year="'+sTY+u'" -metadata artist="'+sARTIST+u'" -metadata album="'+sTL+u'" -metadata genre="'+sTG+u'"'
      except(UnicodeDecodeError):
        sFFmeta=u''
      s1=u'"'+sFFcommand +u'" -i "'+sTMP1+u'" -f image2 -i "'+sIMG1+u'" -t "'+sTIME+u'" -vcodec libvpx -g 120 -lag-in-frames 16 -deadline good -cpu-used 0 -vprofile 0 -qmax 63 -qmin 0 -b:v 768k -acodec libvorbis -ab 112k -ar 44100 -f webm '+sFFmeta+u' -y "'+sOUT1+u'"'
      myossystem(s1)
    else:
      sOUT1=sTMP1
    if sAUDIBLE.lower()=="false":
      print ('Play is set to false, so the file will not play.')
      print(("The program saved the file to:  "+sOUT1))
      if os.path.isfile("/usr/bin/notify-send"):
        s1=u'notify-send "'+fsAppName()+'" "'+sOUT1+u'"'
        myossystem(s1)
    else:
      #Play the file
      if sVISIBLE.lower()=="false" and sTMP1EXT not in ".avi;.flv;.webm;.m4v;.mov;.mpg;.mp4;.wmv":
        PlayWaveInBackground(sOUT1)
      else:
        ShowWithApp(sOUT1)
  except (IOError):
    print (fsAppName()+" Tools execution failed")
    sys.exit(2)
    if os.path.isfile("/usr/bin/notify-send"):
      s1=u'notify-send "'+fsAppName()+'" "python error"'
      myossystem(s1)
  UnlockMyLock()

def cleanstr(sIN):
  '''
  Removes some characters from strings for use in 'song' titles
  '''
  retval=" "
  try:
    retval=sIN
    retval=retval.replace('"',u' ')
    retval=retval.replace("'",u" ")
    retval=retval.replace("\n",u" ")
    retval=retval.replace("\f",u"")
    retval=retval.replace("\r",u"")
    retval=retval.replace("\t",u" ")
  except(UnicodeDecodeError):
    print (retval+" error in readtexttools.cleanstr")
  return retval

def timefortitle():
  '''
  Returns an unambiguous time expression for a title in an international format
  '''
  return time.strftime("%Y-%m-%d_%H:%M:%S-%Z")

def checkmytitle(sTIT,sTOOL):
  '''
  If it is not a working title, replace title
  '''
  sC=sTIT
  try:
    if len(sC)==0:
      sC=sTOOL+u" "+timefortitle()
    else:
      sC=sTIT
  except(UnicodeDecodeError):
    sC=sTOOL+u" "+timefortitle()
  return sC

def checkmyartist(sART):
  '''
  If not a working artist, replaces artist with user name
  '''
  sC=sART
  try:
    if len(sC)==0:
      sC=getMyUserName()
    else:
      sC=sART
  except(UnicodeDecodeError):
    sC=getMyUserName()
  return sC

def LockMyLock():
  s1=getMyLock("lock")
  fileh = open (s1, 'w')
  fileh.write(fsAppSignature())
  fileh.close()

def UnlockMyLock():
  s1=getMyLock("lock")
  if os.path.isfile(s1):
    os.remove(s1)

def getMyLock(sLOCK):
  '''
  Returns path to temporary directory plus a lock file name. Use an value like "lock"
  for sLOCK. You can use more than one lock if you use different values for sLOCK.
  '''
  s1="."+ sLOCK
  if "windows" in platform.system().lower():
    sOUT1=os.path.join(os.getenv("TMP"),fsAppSignature()+u"."+os.getenv("USERNAME")+s1)
  elif "darwin" in platform.system().lower():
    sOUT1=os.path.join(os.getenv("TMPDIR"),fsAppSignature()+u"."+os.getenv("USERNAME")+s1)
  else:
    sOUT1=os.path.join("/tmp",fsAppSignature()+u"."+os.getenv("USER")+s1)
  return sOUT1

def getMyUserName():
  '''
  Returns the user name. Optionally, you can provide a temporary lock.id file 
  for this function to read the artist or author name from and then remove. 
  '''
  if "windows" in platform.system().lower():
    sOUT1=os.getenv("USERNAME")
  elif "darwin" in platform.system().lower():
    sOUT1=os.getenv("USERNAME")
  else:
    sOUT1=os.getenv("USER")
  s1 = getMyLock("lock.id")
  if os.path.isfile(s1):
    f = codecs.open(s1,mode='r',encoding='utf-8')
    sOUT1=f.read()
    f.close()
    os.remove(s1)
  return sOUT1

def getTempPrefix():
  '''
  Returns path to temporary directory plus a filename prefix. 
  Need to supply an extension to determine the context - i.e: 
   -sound.wav for sound
   -image.png for image
  '''
  if "windows" in platform.system().lower():
    sOUT1=os.path.join(os.getenv("TMP"),os.getenv("USERNAME"))
  elif "darwin" in platform.system().lower():
    sOUT1=os.path.join(os.getenv("TMPDIR"),os.getenv("USER"))
  else:
    sOUT1=os.path.join("/tmp",os.getenv("USER"))
  return sOUT1

def getWinFullPath(s1):
  '''
  Copy Windows zipped command-line programs (oggenc.exe, neroAacEnc.exe
  neroAacTag.exe etc.) to "C:/opt". For Windows programs that use an
  installation program (mbrola, espeak etc.), accept the defaults.
  
  Code checks for path in the 64 and 32 bit program directories
  and for a path in the home drive. 
  For example, if s1 is "/opt/oggenc.exe" and Windows is the US
  English locale on a single user computer, the code checks:
    "C:/Program Files/opt/oggenc.exe"
    "C:/Program Files(x86)/opt/oggenc.exe"
    "C:/opt/oggenc.exe"
  '''
  sCommand=''
  if "windows" in platform.system().lower():
    if os.path.isfile(os.path.join(os.getenv("ProgramFiles"),s1)):
      sCommand=os.path.join(os.getenv("ProgramFiles"),s1)
    elif os.getenv("ProgramFiles(x86)"):
      if os.path.isfile(os.path.join(os.getenv("ProgramFiles(x86)"),s1)):
        sCommand=os.path.join(os.getenv("ProgramFiles(x86)"),s1)
    elif os.getenv("HOMEDRIVE"):
      if os.path.isfile(os.path.join(os.getenv("HOMEDRIVE"),s1)):
        sCommand=os.path.join(os.getenv("HOMEDRIVE"),s1)
    else:
      sCommand=''
  return sCommand

def ShowWithApp(sOUT1):
  '''
  Same as double clicking the document - opens in default application
  '''
  if "darwin" in platform.system().lower():
    #MacOS
    s1=u'open "'+sOUT1+u'" '
    myossystem(s1)
  elif "windows" in platform.system().lower():
    # Windows
    os.startfile(sOUT1)
  else:
    if os.path.isfile("/usr/bin/xdg-open"):
      s1=u'xdg-open "'+sOUT1+u'" '
    elif os.path.isfile("/usr/bin/gnome-open"): 
      s1=u'gnome-open "'+sOUT1+u'" '
    elif os.path.isfile("/usr/bin/kde-open"):
      s1=u'kde-open "'+sOUT1+u'" '
    myossystem(s1)

def PlayWaveInBackground(sOUT1):
  '''
  Opens using command line shell
  '''
  if "darwin" in platform.system().lower():
    #MacOS
    s1=u'afplay "'+sOUT1+u'" '
    myossystem(s1)
  elif "windows" in platform.system().lower():
    # Windows
    import winsound
    winsound.PlaySound(sOUT1, winsound.SND_FILENAME|winsound.SND_NOWAIT)
  else:
    if os.path.isfile("/usr/bin/esdplay"):
      s1=u'esdplay "'+sOUT1+u'" '
    elif os.path.isfile("/usr/bin/paplay"):
      s1=u'paplay "'+sOUT1+u'" '
    elif os.path.isfile("/usr/bin/aplay"):
      s1=u'aplay "'+sOUT1+u'" '
    myossystem(s1)

def myossystem(s1):
  '''
  This is equivalent to os.system(s1)
  Replaced os.system(s1) to avoid Windows path errors.
  '''
  s1 = s1.encode("utf-8")
  if "windows" in platform.system().lower():
    try:
      retcode = subprocess.call(s1, shell=False)
      if retcode < 0:
        print ("Process was terminated by signal")
      else:
        print ("Process returned")
    except (OSError, e):
      print ("Execution failed")
  else:
    os.system(s1)

def main():
  '''
  Converts the input wav sound to another format. Ffmpeg
  can convert to a still frame movie if you include an image

  '''
  sLANG=""
  sWAVE=""
  sVISIBLE=""
  sAUDIBLE=""
  sTXT=""
  sIMG1=""
  sOUT1=""
  sB="Video memo"
  try:
    opts,args=getopt.getopt(sys.argv[1:],"hovaist",["help","output=","visible=","audible=","image=","sound=","title="])
  except (getopt.GetoptError):
    # print help information and exit
    print("An option was not recognized")
    usage()
    sys.exit(2)
  for o,a in opts:
    if o in ("-h","--help"):
      usage()
      sys.exit(0)
    elif o in ("-o","--output"):
      sOUT1=a
    elif o in ("-v","--visible"):
      sVISIBLE=a
    elif o in ("-a","--audible"):
      sAUDIBLE=a
    elif o in ("-i","--image"):
      sIMG1=a
    elif o in ("-s","--sound"):
      sWAVE=a
    elif o in ("-t","--title"):
      sB=a
    else:
      assert False,"unhandled option"
  Wav2Media(sB,sWAVE,sIMG1,sOUT1,sAUDIBLE,sVISIBLE)
  sys.exit(0)

if __name__=="__main__":
  main()
