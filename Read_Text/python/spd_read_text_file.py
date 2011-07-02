#!/usr/bin/env python
# -*- coding: UTF-8-*-
'''
To read a plain text file using speech-dispatcher
  Tip: Before using this script, try out speech-dispatcher using
  Accessories > Terminal (the command line console) with 
    spd-say "Text to say"
  If the sound doesn't work, or it sounds distorted, try killing
  the speech daemon with System Monitor. On Ubuntu, use
    Tools > System > Administration > System Monitor
    Select Processes > speech-dispatcher
    Edit > Kill Process [Ctrl + K]
  Try spd-say again to see if it works. If you are not able get the
  speech dispatcher to work, use festival, pico or espeak instead.
  
Read Text Extension for OpenOffice.org (for Linux) :
  See: http://sites.google.com/site/readtextextension/
  Tools > Add-Ons > Read Selection... Dialog setup:
  External program: /usr/bin/python
  Command line options (default voice): "(SPD_READ_TEXT_PY)" "(TMP)"
  or (specific language): "(SPD_READ_TEXT_PY)" --language "(SELECTION_LANGUAGE_CODE)" --voice "MALE2" "(TMP)"

Copyright (c) 2010-2011 James Holgate
'''
import getopt, sys, codecs

def usage():
  sA = ' ' + os.path.split(sys.argv[0])[1]
  print ("")
  print ("Usage")
  print (sA+' [--output_module="xx"] [--language="xx"] [--voice="xx"] [--rate="nn"] input.txt')
  print ("  Use a specific output module")
  print ('  '+sA+' --output_module "espeak-generic" "TextFile.txt"')
  print ("")
  print ("  Use a specific language - en, fr, es...")
  print ('  '+sA+' --language "fr" "TextFile.txt"')
  print ("")
  print ("  Use a specific voice - MALE1, FEMALE1, MALE2, ... FEMALE3, CHILD_MALE, CHILD_FEMALE")
  print ('  '+sA+' --voice "MALE1" "TextFile.txt"')
  print ("")
  print ("  To say the text slower - minimum -100")
  print ('  '+sA+' --rate "-20" "TextFile.txt"')
  print ("")
  print ("  To say the text faster - maximum 100")
  print ('  '+sA+' --rate "20" "TextFile.txt"')
  print ("")
  print ("  See also: <http://cvs.freebsoft.org/doc/speechd/speech-dispatcher.html>")

def main():
  try:
    import speechd
    client = speechd.SSIPClient('ReadTextExtensionPythonScript')
  except ImportError:
    print 'I did not find the speechd voice synthesis resources!'
    print str(err)
    usage()
    sys.exit(2)  
  try:
    opts, args = getopt.getopt(sys.argv[1:], "holvr", ["help", "output_module=","language=","voice=","rate="])
  except getopt.GetoptError, err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
      sys.exit()
    elif o in ("-o", "--output_module"):
      client.set_output_module(a)
    elif o in ("-l", "--language"): # 2 letters lowercase - fr Français, de Deutsch...
      client.set_language(a[:2].lower())
    elif o in ("-v", "--voice"): # MALE1, MALE2 ...
      client.set_voice(a.upper())
    elif o in ("-r", "--rate"):
      client.set_rate( int(a) )
    else:
      assert False, "unhandled option"
  try:       
    f = codecs.open(sys.argv[-1],mode='r',encoding=sys.getfilesystemencoding())
  except IOError:
    print 'I was unable to open the file you specified!'
    usage()
  else:
    # 2010.11.20 - Ubuntu 10.10 - espeak-mbrola-generic; espeak-generic
    # speechd freezes up with a single quote & says "backslash" for a double quote
    # so we replace these characters with smart quotes in the unicode string
    s = f.read().replace(u"'",u"´").replace(u' "',u" “").replace(u'"',u'”')
    f.close()
    client.set_punctuation(speechd.PunctuationMode.SOME)
    sA=s.encode( "utf-8" )
    client.speak(sA)
    client.close()
    sys.exit(0)

if __name__ == "__main__":
  main()
