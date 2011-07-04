#!/usr/bin/env python
# -*- coding: UTF-8-*-
'''
Read Text Library
Common tools for Read Text Extension
Copyright (c) 2011 James Holgate
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
  print (" Video:")
  print (sA+' --image="poster.png" --sound="poster.wav" --output="poster.webm"')
  print (sA+' --visible="true" --audible="true" --image="poster.png" --sound="poster.wav" --title="Pretty lake" --output="poster.webm"')
  print (" Audio:")
  print (sA+' --sound="poster.wav --output="poster.ogg"')
  print (sA+' --visible="false" --audible="true" --sound="poster.wav" --output="poster.ogg"')
  print ("")

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
    sTMP1=getTempPrefix()+"-speech.wav"
  sTMP1EXT=os.path.splitext(sTMP1)[1].lower()
  sIMG1FILEEXT=os.path.splitext(sIMG1)[1].lower()
  if sTMP1EXT==".mp3":
      if os.path.isfile("/usr/bin/lame") or os.path.isfile(r"C:\opt\lame.exe"): 
        sOUT1=sTMP1
        sTMP1=sOUT1+".wav"
      else:
        # Can't make mp3,so make wav
        sOUT1=sTMP1+".wav"
        sTMP1=sOUT1
  elif sTMP1EXT==".m4a":
      if os.path.isfile("/usr/bin/faac") or os.path.isfile(r"C:\opt\neroAacEnc.exe") or os.path.isfile(r"C:\opt\faac.exe"):
        sOUT1=sTMP1
        sTMP1=sOUT1+".wav"
      else:
        # Can't make m4a,so make wav
        sOUT1=sTMP1+".wav"
        sTMP1=sOUT1
  elif sTMP1EXT==".ogg":
      if os.path.isfile("/usr/bin/oggenc") or os.path.isfile(r"C:\opt\oggenc.exe") or os.path.isfile(r"C:\opt\oggenc2.exe"):
        sOUT1=sTMP1
        sTMP1=sOUT1+".wav"
      else:
        # Can't make ogg,so make wav
        sOUT1=sTMP1+".wav"
        sTMP1=sOUT1
  elif sTMP1EXT==".aif":
      if os.path.isfile("/usr/bin/ffmpeg") or os.path.isfile(r"C:\opt\ffmpeg.exe"):
        sOUT1=sTMP1
        sTMP1=sOUT1+".wav"
      else:
        # Can't make aif, so make wav
        sOUT1=sTMP1+".wav"
        sTMP1=sOUT1
  elif sTMP1EXT==".flac":
      if os.path.isfile("/usr/bin/ffmpeg") or os.path.isfile(r"C:\opt\flac.exe"):
        sOUT1=sTMP1
        sTMP1=sOUT1+".wav"
      else:
        # Can't make flac, so make wav
        sOUT1=sTMP1+".wav"
        sTMP1=sOUT1
  elif sTMP1EXT==".spx":
      if os.path.isfile("/usr/bin/gst-launch") or os.path.isfile("/usr/bin/speexenc"):
        sOUT1=sTMP1
        sTMP1=sOUT1+".wav"
      else:
        # Can't make spx, so make wav
        sOUT1=sTMP1+".wav"
        sTMP1=sOUT1
  elif sTMP1EXT in ".avi;.webm;.m4v;.mov;.mpg;.mp4;.wmv":
      if (os.path.isfile("/usr/bin/ffmpeg") or os.path.isfile(r"C:\opt\ffmpeg.exe")) and sIMG1FILEEXT in ".bmp;.gif;.jpeg;.jpg;.png;.tif;.tiff;.tga;":
        sOUT1=sTMP1
        sTMP1=sOUT1+".wav"
      else:
        # Can't make video,so make wav
        sOUT1=sTMP1+".wav"
        sTMP1=sOUT1
  elif sTMP1EXT==".mp2":
      if os.path.isfile("/usr/bin/twolame") or os.path.isfile("/usr/bin/ffmpeg")or os.path.isfile(r"C:\opt\ffmpeg.exe"):
        sOUT1=sTMP1
        sTMP1=sOUT1+".wav"
      else:
        # Can't make mp2,so make wav
        sOUT1=sTMP1+".wav"
        sTMP1=sOUT1
  if sType1=="TEMP":
    retVal=sTMP1
  else:
    retVal=sOUT1
  return retVal

def ProcessWaveMedia(sB,sTMP1,sIMG1,sOUT1,sAUDIBLE,sVISIBLE):
  '''
  Converts audio file, plays copy and deletes original
  sB is brief title
  sTMP is working file name (wav)
  sIMG1 is image to add to video. Ignored if making audio only
  sOUT1 is output file name.( webm, ogg etc.)
  sAUDIBLE - Do we play the file after conversion?
  sVISIBLE - Do we use a GUI or the console?
  '''
  Wav2Media(sB,sTMP1,sIMG1,sOUT1,sAUDIBLE,sVISIBLE)
  try:
    if sOUT1=='':
      print 'Saved to: '+sTMP1
    else:
      os.remove(sTMP1)
  except OSError, e:
    print ('Could not remove "'+sTMP1+'"')

def Wav2Media(sB,sTMP1,sIMG1,sOUT1,sAUDIBLE,sVISIBLE):
  '''
  Converts audio file and plays copy
  sB is brief title
  sTMP1 is working file name (wav)
  sIMG1 is image to add to video. Ignored if making audio only
  sOUT1 is output file name.( webm, ogg etc.)
  sAUDIBLE - Do we play the file after conversion?
  sVISIBLE - Do we use a GUI or the console?
  '''
  try:
    sTT=sB.replace('"',' ').replace("'"," ")
    sTY=time.strftime("%Y")
    sTA="Read Text Extension"
    sTL="sites.google.com/site/readtextextension"
    sTG="Speech"
    wave_read=wave.open(sTMP1,'r')
    iTIME=math.ceil(wave_read.getnframes()/wave_read.getframerate())+1
    sTIME=repr(iTIME)
    sOUT1EXT=os.path.splitext(sOUT1)[1].lower()
    sTMP1EXT=os.path.splitext(sTMP1)[1].lower()
    sIMG1FILEEXT=os.path.splitext(sIMG1)[1].lower()
    print '-----------------------------------------------------'
    print 'Read Text Extension'
    print ''
    print 'Title: ' + sTT
    print 'Working File Name: ' + sTMP1
    print 'File Name: ' + sOUT1
    print 'Frame rate: ' + repr(wave_read.getframerate())
    print 'Number of frames: ' + repr(wave_read.getnframes())
    print 'Duration in seconds: ' + sTIME
    print '-----------------------------------------------------'
    wave_read.close()
    sFFmeta=''
    if "windows" in platform.system().lower():
      sFFcommand=getWinFullPath("opt/ffmpeg.exe")
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
        if s0=='':
          s0=getWinFullPath("/opt/oggenc.exe")
        s1=s0+' -o "'+sOUT1+'" "'+sTMP1+'"'
        myossystem(s1)
      else:
        s1='oggenc --album "'+sTL+'" --artist "'+sTA+'" --title "'+sTT+'" --genre "'+sTG+'" --date '+sTY+' -o "'+sOUT1+'" "'+sTMP1+'"'
        myossystem(s1)
    elif sOUT1EXT==".m4a":
      if "windows" in platform.system().lower():
        # The programs are supplied in a zip file. To use them in this script, you need to extract them to the directories shown.
        # C:/opt/neroAacEnc.exe
        # See: http://www.nero.com/enu/downloads-nerodigital-nero-aac-codec.php
        s0=getWinFullPath("/opt/neroAacEnc.exe")
        if s0=='':
          s0=getWinFullPath("/opt/faac.exe")
          s1=s0+' -o "'+sOUT1+'" "'+sTMP1+'"'
        else:
          s1=s0+' -if "'+sTMP1+'" -of "'+sOUT1+'"'
        myossystem(s1)
      else:
        s1='faac --album "'+sTL+'" --artist "'+sTA+'" --title "'+sTT+'" --genre "'+sTG+'" --year '+sTY+' -o "'+sOUT1+'" "'+sTMP1+'"'
        myossystem(s1)
    elif sOUT1EXT==".mp3":
      if "windows" in platform.system().lower():
        # The program is supplied in a zip file. To use it in this script, you need to extract it to the directory shown.
        # C:/opt/lame.exe
        #see:  http://www.rarewares.org/mp3-lame-bundle.php
        s0=getWinFullPath("/opt/lame.exe")
        s1=s0+' -V 4 --tl "'+sTL+'" --ta "'+sTA+'" --tt "'+sTT+'" --tg "'+sTG+'" --ty '+sTY+' "'+sTMP1+'" "'+sOUT1+'"'
        myossystem(s1)
      else:
        s1='lame --tl "'+sTL+'" --ta "'+sTA+'" --tt "'+sTT+'" --tg "'+sTG+'" --ty '+sTY+' "'+sTMP1+'" "'+sOUT1+'"'
        myossystem(s1)
    elif sOUT1EXT==".spx":
      # gst-launch is slow to encode... but the file size is very small... gst-launch is a Gstreamer utility
      if os.path.isfile("/usr/bin/speexenc"):
        s1='speexenc --title "'+sTT+'" "'+sTMP1+'" "'+sOUT1+'"'
      else:
        s1='gst-launch filesrc location="'+sTMP1+'" ! decodebin ! speexenc ! oggmux ! filesink location="'+sOUT1+'"'
      myossystem(s1)
    elif sOUT1EXT==".mp2":
      if os.path.isfile("/usr/bin/twolame"):
        s1='twolame "'+sTMP1+'" "'+sOUT1+'"'
      else:
        sFFmeta=' -metadata title="'+sTT+'" -metadata Year="'+sTY+'" -metadata artist="'+sTA+'" -metadata album="'+sTL+'" -metadata genre="'+sTG+'" '
        s1='"'+sFFcommand +'" -i "'+sTMP1+'" '+sFFmeta+' -y "'+sOUT1+'"'
      myossystem(s1)
    elif sOUT1EXT==".aif":
      sFFmeta=' -metadata title="'+sTT+'" -metadata album="'+sTL+'" '
      s1='"'+sFFcommand +'" -i "'+sTMP1+'" '+sFFmeta+' -y "'+sOUT1+'"'
      myossystem(s1)
    elif sOUT1EXT==".flac":
      if "windows" in platform.system().lower():
        # The programs is supplied in a zip file. To use it in this script, you need to extract it to the directory shown.
        # C:/opt/flac.exe
        # See: http://flac.sourceforge.net/
        s0=getWinFullPath("/opt/flac.exe")
        s1=s0+' -f -o "'+sOUT1+'" "'+sTMP1+'"'
        
        myossystem(s1)
      else:
        sFFmeta=' -metadata title="'+sTT+'" -metadata album="'+sTL+'" '
        s1='"'+sFFcommand +'" -i "'+sTMP1+'" '+sFFmeta+' -y "'+sOUT1+'"'
        myossystem(s1)
    elif sOUT1EXT==".avi":
      # The quality isn't as good as webm. Use avi format if you need to edit the video with Windows Movie Maker
      sFFmeta=' -metadata title="'+sTT+'" -metadata comment="'+sTG+' - '+sTL+', '+sTY+'" -metadata artist="'+sTA+'" -metadata genre="'+sTG+'" '
      s1='"'+sFFcommand +'" -loop_input -r 24000/1001 -i "'+sTMP1+'" -f image2 -i "'+sIMG1+'" -t "'+sTIME+'" -vcodec msmpeg4v2 '+sFFmeta+' -y "'+sOUT1+'"'
      myossystem(s1)
    elif sOUT1EXT==".mpg":
      # Use mpg format if you need to make a clip for a DVD -s 720x480
      sFFmeta=' -metadata title="'+sTT+'" '
      s1='"'+sFFcommand +'" -loop_input -r 24000/1001 -i "'+sTMP1+'" -f image2 -i "'+sIMG1+'" -t "'+sTIME+'" -target dvd '+sFFmeta+' -y "'+sOUT1+'"'
      myossystem(s1)
    elif sOUT1EXT==".mp4":
      # For ipod or iphone video library'
      sFFmeta=' -metadata title="'+sTT+'" -metadata Year="'+sTY+'" -metadata artist="'+sTA+'" -metadata album="'+sTL+'" -metadata genre="'+sTG+'" '
      s1='"'+sFFcommand +'" -loop_input -r 24000/1001 -i "'+sTMP1+'" -f image2 -i "'+sIMG1+'" -t "'+sTIME+'" -qmax 5  -aspect 4:3 -s 480x320 '+sFFmeta+' -y "'+sOUT1+'"'
      myossystem(s1)
    elif sOUT1EXT==".webm":
      # Chrome, Firefox (Linux) and totem can open webm directly. Edit webm with openshot or pitivi or upload directly to Youtube.
      sFFmeta=' -metadata title="'+sTT+'" '
      s1='"'+sFFcommand +'" -loop_input -r 30 -i "'+sTMP1+'" -f image2 -i "'+sIMG1+'" -t "'+sTIME+'" -b 3900k  -acodec libvorbis -ab 100k -f webm '+sFFmeta+' -y  "'+sOUT1+'"'
      myossystem(s1)
    else:
      sOUT1=sTMP1
    if sAUDIBLE.lower()=="false":
      print 'Play is set to false, so the file will not play.'
      print "The program saved the file to:  "+sOUT1
    else:
      #Play the file
      if sVISIBLE.lower()=="false" and sTMP1EXT not in ".avi;.flv;.webm;.m4v;.mov;.mpg;.mp4;.wmv":
        PlayWaveInBackground(sOUT1)
      else:
        ShowWithApp(sOUT1)
  
  except IOError,err:
    print >>sys.stderr, "Read Text Tools execution failed"
    print str(err)
    sys.exit(2)

def getTempPrefix():
  '''
  Returns path to temporary directory plus a filename prefix. 
  Need to supply an extension to determine the context - i.e: 
   -sound.wav for sound
   -image.png for image
  '''
  if "windows" in platform.system().lower():
    sOUT1=os.path.join(os.getenv("TMP"),os.getenv("USERNAME"))
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
    s1='open "'+sOUT1+'" '
    myossystem(s1)
  elif "windows" in platform.system().lower():
    # Windows
    os.startfile(sOUT1)
  else:
    if os.path.isfile("/usr/bin/xdg-open"):
      s1='xdg-open "'+sOUT1+'" '
    elif os.path.isfile("/usr/bin/gnome-open"): 
      s1='gnome-open "'+sOUT1+'" '
    elif os.path.isfile("/usr/bin/kde-open"):
      s1='kde-open "'+sOUT1+'" '
    myossystem(s1)

def PlayWaveInBackground(sOUT1):
  '''
  Opens using command line shell
  '''
  if "darwin" in platform.system().lower():
    #MacOS
    s1='afplay "'+sOUT1+'" '
    myossystem(s1)
  elif "windows" in platform.system().lower():
    # Windows
    import winsound
    winsound.PlaySound(sOUT1, winsound.SND_FILENAME|winsound.SND_NOWAIT)
  else:
    if os.path.isfile("/usr/bin/esdplay"):
      s1='esdplay "'+sOUT1+'" '
    elif os.path.isfile("/usr/bin/paplay"):
      s1='paplay "'+sOUT1+'" '
    elif os.path.isfile("/usr/bin/aplay"):
      s1='aplay "'+sOUT1+'" '
    myossystem(s1)

def myossystem(s1):
  '''
  This is equivalent to os.system(s1)
  Replaced os.system(s1) to avoid Windows path errors.
  '''
  if "windows" in platform.system().lower():
    try:
      retcode = subprocess.call(s1, shell=False)
      if retcode < 0:
        print >>sys.stderr, "Process was terminated by signal", -retcode
      else:
        print >>sys.stderr, "Process returned", retcode
    except OSError, e:
      print >>sys.stderr, "Execution failed:", e
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
