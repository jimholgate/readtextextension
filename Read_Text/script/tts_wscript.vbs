 '' Script for Read Text Extension
 '' ==============================
 '' 
 '' Reads a text file aloud or saves sound to a file.
 '' 
 '' This script uses the Windows speech application programming
 '' interface (`SAPI`). Depending on the version and locale of 
 '' Windows, voices in different languages may be available.
 ''   
 '' Read Selection... Dialog setup:
 '' -------------------------------
 '' 
 '' External program: 
 '' 
 ''     C:\Windows\SysWOW64\wscript.exe
 '' 
 '' Command line options (default): 
 '' 
 ''     "(TTS_WSCRIPT_VBS)" "(TMP)"
 '' 
 '' or (save as a .wav file in the home directory): 
 '' 
 ''     "(TTS_WSCRIPT_VBS)" /soundfile:"(HOME)(NOW).wav" "(TMP)"
 '' 
 '' or (use a named voice)
 '' 
 ''     "(TTS_WSCRIPT_VBS)" /voice:"Microsoft Hazel Desktop - English (Great Britain)" "(TMP)"
 '' 
 '' or (read a little slower)
 '' 
 ''     "(TTS_WSCRIPT_VBS)" /rate:-3 "(TMP)"
 '' 
 '' or (change voice by language)
 '' 
 ''     "(TTS_WSCRIPT_VBS)" /language:"(SELECTION_LANGUAGE_COUNTRY_CODE)" "(TMP)"
 '' 
 '' **Note**: Selecting this option doesn't work with the SAPI
 '' speech synthesizer if you haven't installed a voice in the
 '' language.
 '' 
 '' Optional formats
 '' ----------------
 '' 
 '' ###Flac
 '' 
 '' Play flac encoded sound files using a player or plugin 
 '' 
 ''  * Install `flac.exe` in `C:\opt\`
 ''  * [flac encoder](http://flac.sourceforge.net/links.html#software)
 ''  * [Players and plugins](http://flac.sourceforge.net/)
 '' 
 '' ###iTunes
 '' 
 '' Use [iTunes](http://www.apple.com/itunes/) to add m4a and aif 
 '' items to an iTunes library and home directory.
 '' 
 ''     "(TTS_WSCRIPT_VBS)" /language:"(SELECTION_LANGUAGE_CODE)" /soundfile:"(HOME)(NOW).m4a" "(TMP)"
 ''     "(TTS_WSCRIPT_VBS)" /language:"(SELECTION_LANGUAGE_CODE)" /soundfile:"(HOME)(NOW).aif" "(TMP)"
 '' 
 '' ###Lame
 '' 
 '' Play mp3 compatible encoded sound files with most music players
 '' Use `lame.exe` to make an mp3 compatible file.
 '' 
 ''  * Install `lame.exe` in `C:\opt\`
 ''  * [Lame encoder](http://www.rarewares.org/mp3-lame-bundle.php)
 '' 
 '' ###Nero
 '' 
 '' Play m4a AAC encoded sound files with most music players
 '' Use `neroAacEnc.exe` to make an m4a file.
 '' 
 ''  * Install `neroAacEnc.exe` in `C:\opt\`
 ''  * The `neroAacTag.exe` program adds tags.
 ''  * [Nero m4a encoder](http://www.nero.com/enu/downloads-nerodigital-nero-aac-codec.php)
 '' 
 '' ###Ogg
 '' 
 '' Play ogg encoded sound files with firefox, chrome or chromium.
 '' Use `oggenc.exe` or `oggenc2.exe` to make an ogg file 
 '' 
 ''  * The ogg converter program must be installed in `C:\opt\`.
 ''  * [oggenc2 encoder](http://www.rarewares.org/ogg-oggenc.php)
 ''  * [Players and plugins](http://www.vorbis.com/setup_windows/)
 '' 
 '' [Read Text Extension](http://sites.google.com/site/readtextextension/)
 '' 
 '' Copyright (c) 2011 - 2015 James Holgate

Const ForReading=1
Const ForWriting=3 
Const AUDIO_FORMAT=34 ' (16 bit mono 44.100 KHz). 
  'Common formats: 8 (8 KHz 8-bit mono), 16 (16 KHz 8-bit mono)
  '35 (44 KHz 16-bit Stereo), 65 (GSM 8 KHz), 66 (GSM 11 KHz)
Const APP_SIGNATURE="ca.bc.vancouver.holgate.james.readtextextension"

Sub Usage(s1)
  s1=s1 & chr(10)
  s1=s1 & chr(10)
  s1=s1 & "tts_wscript.vbs [/language:" & chr(34) & "xxx" & chr(34) & " | /voice:" & chr(34) & "xxx" & chr(34) & "] [/rate:"
  s1=s1 & "nn] [/soundfile:" & chr(34) & "c:\xxx.wav" & chr(34) & "] " & chr(34) & "filename.txt" & chr(34) & "" & chr(10)
  s1=s1 & chr(10)
  s1=s1 & "/language:" & chr(34) & "en" & chr(34) & " - Language option" & chr(10)
  s1=s1 & "/voice:" & chr(34) & "Microsoft Anna" & chr(34) & " - Voice option" & chr(10)
  s1=s1 & "/rate:-3 - Minimum -10 & Maximum 10" & chr(10)
  s1=s1 & "/soundfile:" & chr(34) & "C:\xxx.wav" & chr(34) & " - sound file path (optional)" & chr(10)
  s1=s1 & chr(34) & "filename.txt" & chr(34) & " Text Document to read"
  msgBox s1, 0,"Read Text Extension"
End Sub

Function strExt(sA)
  strExt = LCase(Mid(sA,InStrRev(sA,".")))
End Function

Function canUseSpeechXML
  canUseSpeechXML=False
  Set SystemSet = GetObject("winmgmts:").InstancesOf ("Win32_OperatingSystem") 
  for each System in SystemSet 
    VerBig = Left(System.Version,3)
    if CLng(VerBig) > 5.1 Then
      canUseSpeechXML=True
    End if
  next
End Function

Sub wav2ogg (wavfile,oggFile,sMyWords)
  ' On Error Resume Next
  if fbFileExists("C:\opt\oggenc2.exe") then
    sPpath="C:\opt\oggenc2.exe"
    sPname="oggenc2.exe:"
  elseif fbFileExists("C:\opt\oggenc.exe") then
    sPpath="C:\opt\oggenc.exe"
    sPname="oggenc.exe:"
  else
    exit sub
  end if   
   s2=InputBox(sPname,"Read Text",oggFile)
  if len(s2) > 0  then
    Dim WshShell, oExec
    Set WshShell = CreateObject("WScript.Shell")
    sa=sPpath & " --quiet -o " & chr(34) & s2 & chr(34) & " " & chr(34) & wavfile & chr(34)
    Set oExec = WshShell.Exec(sA)
    Do While oExec.Status = 0
       WScript.Sleep 100
    Loop
  end if
 
  fbKillFile wavfile
End Sub

Sub wav2flac (wavfile,outfile,sMyWords)
  if fbFileExists("C:\opt\flac.exe") then
    sPpath="C:\opt\flac.exe"
    sPname="flac.exe:"
  else
    exit sub
  end if   
   s2=InputBox(sPname,"Read Text",outfile)
  if len(s2) > 0  then
    Dim WshShell, oExec
    Set WshShell = CreateObject("WScript.Shell")
    sa=sPpath & " -f -o " & chr(34) & s2 & chr(34) & " " & chr(34) & wavfile & chr(34)
    Set oExec = WshShell.Exec(sA)
    Do While oExec.Status = 0
       WScript.Sleep 100
    Loop
  end if
 
  fbKillFile wavfile
End Sub

Sub wav2m4a (wavfile,outFile,sMyWords)
  if fbFileExists("C:\opt\neroAacEnc.exe") then
    sPpath="C:\opt\neroAacEnc.exe"
    sPname="neroAacEnc.exe:"
  elseif fbFileExists("C:\opt\faac.exe") then
    sPpath="C:\opt\faac.exe"
    sPname="faac.exe:"
  else
    exit sub
  end if        
  s2=InputBox(sPname,"Read Text",outFile)
  if len(s2) > 0  then
    Dim WshShell, oExec
    Set WshShell = CreateObject("WScript.Shell")
    if sPname="neroAacEnc.exe:" then
      sa=sPpath & " -if " & chr(34) & wavfile & chr(34) & " -of " & chr(34) & s2 & chr(34)
    else 'faac.exe
      sa=sPpath & " -o " & chr(34) & s2 & chr(34) & " " & chr(34) & wavfile & chr(34)
    end if
    Set oExec = WshShell.Exec(sA)
    Do While oExec.Status = 0
       WScript.Sleep 100
    Loop
  end if
 
  fbKillFile wavfile
End Sub

Sub wav2mp3 (wavfile,outFile,sMyWords)
  On Error Resume Next
  if fbFileExists("C:\opt\lame.exe") then
    sPpath="C:\opt\lame.exe"
    sPname="lame.exe:"
  else
    exit sub
  end if        
  s2=InputBox(sPname,"Read Text",outFile)
  if len(s2) > 0  then
    Dim WshShell, oExec
    Set WshShell = CreateObject("WScript.Shell")
    'We need to use the --quiet switch, or lame gets stuck in the loop
    sa=sPpath & " --quiet -V2 " & chr(34) & wavfile & chr(34) & " " & chr(34) & s2 & chr(34)
    Set oExec = WshShell.Exec(sA)
    Do While oExec.Status = 0
       WScript.Sleep 100
    Loop
  end if
 
  fbKillFile wavfile
End Sub

Sub wav2iTunes (wavfile,sOut2file,sMyWords)
'iTunes makes a mp3, aac or m4a in the iTunes Music Library 
'then wav2iTunes copies the mp3 to specified location
  On Error Resume Next
  set iTunesApp = WScript.CreateObject("iTunes.Application")
  vers = iTunesApp.Version
  Dim Reg1
  Set Reg1 = new RegExp
  Reg1.Pattern = "^10"
  if not (Reg1.Test(vers)) Then
    Usage "Get: http://www.apple.com/itunes/" & chr(10) & chr(10) & "Did not find a supported iTunes version" & chr(10)
    Wscript.Exit(0)
  End If
  set encoderCollection = iTunesApp.Encoders
  oldEncoder=iTunesApp.CurrentEncoder 
  Select Case strExt(sOut2file)
    Case ".mp3"
      set encoder=encoderCollection.ItemByName("MP3 Encoder")
    Case ".aif",".aiff"
      set encoder=encoderCollection.ItemByName("AIFF Encoder")
    Case Else ' ".m4a",".aac"
      set encoder=encoderCollection.ItemByName("AAC Encoder")
  end Select
  iTunesApp.CurrentEncoder = encoder
  set fso = CreateObject("Scripting.FileSystemObject")  
  set opStatus = iTunesApp.ConvertFile(wavfile)
  while opStatus.InProgress
    WScript.Sleep 1000
  wend
  WScript.Sleep 1000 'Make sure itunes is done
  iTunesApp.CurrentEncoder=oldEncoder
  opStatus.Tracks.Item(1).Composer="sites.google.com/site/readtextextension"
  opStatus.Tracks.Item(1).Artist="sites.google.com/site/readtextextension"
  opStatus.Tracks.Item(1).Album="Read Text Extension"
  opStatus.Tracks.Item(1).Genre="Speech"
  opStatus.Tracks.Item(1).Name=ltrim(rtrim(left(left(sMyWords,instr(sMyWords,chr(10))-2),30)))
  opStatus.Tracks.Item(1).Lyrics=sMyWords
  opStatus.Tracks.Item(1).Year=Year(Now)

  set outfile=fso.GetFile(opStatus.Tracks.Item(1).Location)
  outfile.copy (sOut2file)

  fbKillFile wavfile
End Sub

Function fbFileExists(sfilespec)
   Dim fso
   Set fso = CreateObject("Scripting.FileSystemObject")
   fbFileExists = (fso.FileExists(sfilespec))
End Function

Function fbKillFile(sfilespec)
   Dim fso
   Set fso = CreateObject("Scripting.FileSystemObject")
   If fso.FileExists(sfilespec) Then
     fso.DeleteFile sfilespec
   End If
   fbKillFile = not(fso.FileExists(sfilespec))
End Function

Function AddLanguageCodes(s1,s4)
  s1=Lcase(s1)
  if canUseSpeechXML Then
    ' With Sapi 5.3 and above we use the ISO language code
    s3="<?xml version=" & Chr(34) & "1.0" & Chr(34) & "?>"
    s3=s3 & " <speak version=" & Chr(34) & "1.0" & Chr(34) & " xmlns=" & Chr(34) & "http://www.w3.org/2001/10/synthesis" & Chr(34)
    s3=s3 & " xmlns:xsi=" & Chr(34) & "http://www.w3.org/2001/XMLSchema-instance" & Chr(34)
    s3=s3 & " xsi:schemaLocation=" & Chr(34) & "http://www.w3.org/2001/10/synthesis"
    s3=s3 & " http://www.w3.org/TR/speech-synthesis/synthesis.xsd" & Chr(34) & " xml:lang=" & Chr(34)
    s3=s3 & s1
    s3=s3 & Chr(34) & "> "
    s3=s3 & s4
    s3=s3 & "</speak>"
  else
    ' XP  Sapi 5.1- we look up the Microsoft language code
    Select Case s1
    Case "en"
      s2="409"
    Case "en-us","","zxx"
      s2="409"
    Case "en-gb","en-vg","en-io","en-gg"
      s2="809"
    Case "en-au"
      s2="c09"
    Case "en-bz"
      s2="2809"
    Case "en-ca"
      s2="1009"
    Case "en-bs"
      s2="2409"
    Case "en-hk"
      s2="3c09"
    Case "en-in"
      s2="4009"
    Case "en-id"
      s2="3809"
    Case "en-ie"
      s2="1809"
    Case "en-jm"
      s2="2009"
    Case "en-my"
      s2="4409"
    Case "en-nz"
      s2="1409"
    Case "en-ph"
      s2="3409"
    Case "en-sg"
      s2="4809"
    Case "en-za"
      s2="1c09"
    Case "en-tt"
      s2="2c09"
    Case "en-zw"
      s2="3009"
    Case "fr-be"
      s2="80c"
    Case "fr-ca"
      s2="c0c"
    Case "fr-cg"
      s2="240c"
    Case "fr-ch"
      s2="100c"
    Case "fr-ci"
      s2="300c"
    Case "fr-cm"
      s2="2c0c"
    Case "fr-fr","fr"
      s2="40c"
    Case "fr-ht"
      s2="3c0c"
    Case "fr-lu"
      s2="140c"
    Case "fr-ma"
      s2="380c"
    Case "fr-mc"
      s2="180c"
    Case "fr-ml"
      s2="340c"
    Case "fr-re"
      s2="200c"
    Case "fr-sn"
      s2="280c"
    Case "it","it-it"
      s2="410"
    Case "de-at"
      s2="c07"
    Case "de-ch"
      s2="807"
    Case "de-de","de"
      s2="407"
    Case "de-li"
      s2="1407"
    Case "de-lu"
      s2="1007"
    Case "es-es","es"
      s2="c0a"
    Case "es-ar"
      s2="2c0a"
    Case "es-bo"
      s2="400a"
    Case "es-cl"
      s2="340a"
    Case "es-co"
      s2="240a"
    Case "es-cr"
      s2="140a"
    Case "es-do"
      s2="1c0a"
    Case "es-ec"
      s2="300a"
    Case "es-sv"
      s2="440a"
    Case "es-gt"
      s2="100a"
    Case "es-hn"
      s2="480a"
    Case "es-mx"
      s2="80a"
    Case "es-ni"
      s2="4c0a"
    Case "es-pa"
      s2="180a"
    Case "es-py"
      s2="3c0a"
    Case "es-pe"
      s2="280a"
    Case "es-pr"
      s2="500a"
    Case "es-us"
      s2="540a"
    Case "es-uy"
      s2="380a"
    Case "es-ve"
      s2="200a"
    Case "ru","ru-ru"
      s2="419" 
    Case "hi","hi-in"
      s2="439"
    Case "af","af-za"
      s2="436"
    Case "ar-sa","ar"
      s2="401"
    Case "ar-dz"
      s2="1401"
    Case "ar-bh"
      s2="3c01"
    Case "ar-eg"
      s2="c01"
    Case "ar-iq"
      s2="801"
    Case "ar-jo"
      s2="2c01"
    Case "ar-kw"
      s2="3401"
    Case "ar-lb"
      s2="3001"
    Case "ar-ly"
      s2="1001"
    Case "ar-ma"
      s2="1801"
    Case "ar-om"
      s2="2001"
    Case "ar-qa"
      s2="4001"
    Case "ar-sy"
      s2="2801"
    Case "ar-tn"
      s2="1c01"
    Case "ar-ae"
      s2="3801"
    Case "ar-ye"
      s2="2401"
    Case "eu","eu-fr","eu-es"
      s2="42D"
    Case "bg","bg-bg"
      s2="402"
    Case "ca","ca-es"
      s2="403"
    Case "cs","cs-cz"
      s2="405"
    Case "cy","cy-uk","cy-gb"
      s2="452"
    Case "da","da-dk"
      s2="406"
    Case "et","et-ee"
      s2="425"
    Case "fi","fi-fi"
      s2="40b"
    Case "ka","ka-ge"
      s2="437"
    Case "hl","hl-gr"
      s2="408"
    Case "he","he-il"
      s2="40d"
    Case "hr","hr-hr"
      s2="41a"  
    Case "hu","hu-hu"
      s2="40e"
    Case "is","is-is"
      s2="40f"
    Case "ga","ga-ie"
      s2="83c"  
    Case "gd","gd-uk","gd-gb"
      s2="43c"
    Case "id","id-id"
      s2="421"
    Case "ja","ja-jp"
      s2="411"
    Case "ko","ko-kp","ko-kr"
      s2="412"
    Case "ms","ms-sg","ms-my","ms-id","ms-bn"
      s2="43E"
    Case "mo-mn","mo"
      s2="850"
    Case "nl","nl-nl"
      s2="413"
    Case "nl","nl-be"
      s2="813"
    Case "no","no-no","nb","nb-no"
      s2="414"
    Case "nn","nn-no"
      s2="814"
    Case "pl","pl-pl"
      s2="415"
    Case "pt-br"
      s2="416"
    Case "pt-pt","pt"
      s2="816"
    Case "ro","ro-ro"
      s2="418" 
    Case "sk","sk-sk"
      s2="41b"
    Case "sl","sl-si"
      s2="424"
    Case "sv","sv-se"
      s2="41D"
    Case "th","th-th"
      s2="41E"
    Case "tl","tl-ph"
      s2="464"
    Case "tr","tr-tr"
      s2="41f"
    Case "uk","uk-ua"
      s2="422"
    Case "vi","vi-vn"
      s2="42a"
    Case "zh","zh-cn"
      s2="804"
    Case "zh-tw"
      s2="404"
    Case "zh-hk"
      s2="c04"
    Case "zh-sg"
      s2="1004"
    Case "zh-mo"
      s2="1404"
    Case Else
      s2="9" 'en if XP (5.1) can`t tell language.
    End Select
    s3="<speak><lang langid=" & Chr(34)
    s3=s3 & s2
    s3=s3 & Chr(34) & "> "
    s3= s3 & s4
    s3=s3 & " </lang></speak>" 
  End If
  AddLanguageCodes=s3
End Function

Sub PopMsgBox(sMsg,sHead,sTitle)
  Set objFSO=CreateObject("Scripting.FileSystemObject")
  Dim WshShell, oExec
  Set WshShell = CreateObject("WScript.Shell")
  Set WshEnv = WshShell.Environment("Process")
  tempFolder = WshEnv("TEMP")
  ' write temporary file
  outFile = tempFolder & "\read-text-advisory.hta"
  Set objFile = objFSO.CreateTextFile(outFile,True)
  s1 = "<html><head><script> window.resizeTo(600,180);setTimeout(function(){window.close();}, 5000);</script><HTA:APPLICATION ID=""objReadTextDialog"" APPLICATIONNAME=""Read Text Dialog"" SCROLL=""no"" SINGLEINSTANCE=""yes"" CAPTION=""yes"" SHOWINTASKBAR=""no"" maximizeButton=""no"" minimizeButton=""no""><link rel=""stylesheet"" type=""text/css"" href=""res://ieframe.dll/ErrorPageTemplate.css"" /><meta http-equiv=""Content-Type"" content=""text/html; charset=UTF-8"" /><title>"& sTitle & "</title></head><body onkeydown=""window.close();"" onclick=""window.close();"" ><table width=""500"" cellpadding=""0"" cellspacing=""0"" border=""0""><tr><td id=""infoIconAlign"" width=""60"" align=""left"" valign=""top"" rowspan=""2""><img src=""" & fLogoSrc & """ id=""infoIcon"" alt=""Info icon""></td><td id=""mainTitleAlign"" valign=""middle"" align=""left"" width=""*""><h1 id=""mainTitle"">"& sHead & "</h1>"& sMsg & "</td></tr><tr height = ""60""><td id=""infoIconAlign2"" rowspan=""2""></td><td id=""mainTitleAlign2"" valign=""bottom"" align=""left"" width=""*""></td></tr></table></body></html>"
  objFile.Write s1
  objFile.Close
  ' show message
  Set oExec = WshShell.Exec("mshta.exe " & outFile)
  Do While oExec.Status = 0
    WScript.Sleep 100
  Loop
  fbKillFile outFile
End Sub

Sub SayIt(s1,sRate,sVoice)
  Set objFSO=CreateObject("Scripting.FileSystemObject")
  Dim WshShell, oExec
  Set WshShell = CreateObject("WScript.Shell")
  Set WshEnv = WshShell.Environment("Process")
  tempFolder = WshEnv("TEMP")
  userid = WshEnv("USERNAME")
  ' write temporary file
  outFile = tempFolder & "\" & APP_SIGNATURE & "." & userid & ".lock"
  If fbFileExists (outFile) Then 
    fbKillFile outFile
  Else
    Set objFile = objFSO.CreateTextFile(outFile,True)
    objFile.Write APP_SIGNATURE
    objFile.Close
    Set Sapi=Wscript.CreateObject("SAPI.SpVoice")
    If Sapi Is Nothing Then
      Usage "FAILED Sapi.SpVoice creation. SAPI ne pouvait pas créer une voix."
    Else
      n=0
      While n<Sapi.GetVoices.Count
        If instr(Lcase(Sapi.GetVoices.Item(n).GetDescription),Lcase(sVoice)) > 0 Then
          Set Sapi.Voice=Sapi.GetVoices.Item(n)
          n=Sapi.GetVoices.Count
        Else
          n=n+1
        End If
      WEnd
      Sapi.Rate=int(sRate)
      Sapi.Speak "",1
      Sapi.Speak s1,3
      Do
        WScript.Sleep 100
      Loop Until Sapi.WaitUntilDone(1) or (objFSO.FileExists(outFile) = false)
      Set Sapi=Nothing 
    End If
  End If
  fbKillFile outFile
End Sub

Sub WriteIt(s1,sRate,sVoice,sFileName, sMyWords,sLibre)
  Set fs=CreateObject("Scripting.FileSystemObject") 
  Set Sapi=Nothing
  Set Sapi=Wscript.CreateObject("SAPI.SpVoice")
  If Sapi Is Nothing Then
    Usage "FAILED Sapi.SpVoice creation. SAPI ne pouvait pas créer une voix."
  Else
    n=0
    While n<Sapi.GetVoices.Count
      If instr(Lcase(Sapi.GetVoices.Item(n).GetDescription),Lcase(sVoice)) > 0 Then
        Set Sapi.Voice=Sapi.GetVoices.Item(n)
        n=Sapi.GetVoices.Count
      Else
        n=n+1
      End If
    WEnd
    Sapi.Rate=int(sRate)
    If fbFileExists (sFileName) Then 
      fbKillFile sFileName
    End If
    sFileNameExt=strExt(sFileName)
    Select Case sFileNameExt
      Case ".mp3",".m4a",".aac",".aif",".aiff"
        sWavename=sFileName & ".wav"
        sItunesName=sFileName
        sLibreName=""
      Case ".ogg",".flac"
        sWavename=sFileName & ".wav"
        sItunesName=""
        sLibreName=sFileName
      Case Else
        sWavename=sFileName
        sItunesName=""
        sLibreName=""
    End Select
    Set ss=CreateObject("Sapi.SpFileStream") 
    ss.Format.Type = AUDIO_FORMAT
    ss.Open sWaveName,ForWriting,False 
    Set Sapi.AudioOutputStream=ss 
    Sapi.Speak s1
    Set Sapi=Nothing 
    ss.Close 
    Set ss = Nothing
    If sItunesName <> "" and Lcase(sLibre)<>"true" then
      wav2iTunes sWaveName,sItunesName,sMyWords
    ElseIf sFileNameExt= ".ogg" then
      wav2Ogg sWaveName,sLibreName,sMyWords
    ElseIf sFileNameExt= ".flac" then
      wav2Flac sWaveName,sLibreName,sMyWords
    ElseIf sFileNameExt= ".m4a" then
      wav2m4a sWaveName,sItunesName,sMyWords
    ElseIf sFileNameExt= ".mp3" then
      wav2mp3 sWaveName,sItunesName,sMyWords
    End If
  End If
  if fbFileExists(sFileName) then
    PlaySound "C:\Windows\Media\notify.wav"
    sLang = GetLocale()
    PopMsgBox sFileName, "Read Text : " & fsDone (sLang), "Read Text"
  End If
End Sub

function fsDone (b)
' b - the language name or decimal LCID of a culture group. Returns the word "Done"
' http://0xcc.net/jsescape/ 
' http://www.microsoft.com/resources/msdn/goglobal/default.mspx
' MSDN lists the LCID Culture identifiers in hexidecimal, but VBA needs decimal codes.

  Select Case b
  Case "af", "1078"
    a1 = "Klaar"
  Case "bg", "1026"
    a1 = "&#1043;&#1086;&#1090;&#1086;&#1074;&#1086;"
  Case "ca", "1027"
    a1 = "Finalitzada"
  Case "cs", "1029"
    a1 = "&#68;&#111;&#107;&#111;&#110;&#269;&#101;&#110;&#111;"
  Case "da","1030"
    a1 = "&#102;&#230;&#114;&#100;&#105;&#103;"
  Case "de", "1031", "3079", "5127", "4103", "2055"
    a1 = "Beendet"
  Case "el", "1032"
    a1 = "&#927;&#955;&#959;&#954;&#955;&#951;&#961;&#974;&#952;&#951;&#954;&#949;"
  Case "en", "3081", "10249", "4105", "9225", "2057", "16393", "6153", "8201", "5129", "13321", "7177", "11273", "1033", "12297"
    a1 = "Done"
  Case "es","11274", "16394", "13322", "9226", "5130", "7178", "12298", "17418", "4106", "18442", "2058", "19466", "6154", "15370", "10250", "20490", "1034", "14346", "8202"
    a1 = "Finalizado"
  Case "fr", "3084", "1036", "2060", "11276","9228","12300","5132","13324", "6156", "14348", "10252", "4108", "7180"
    a1 = "Terminé"
  Case "et", "1061"
    a1 = "&#76;&#245;&#112;&#101;&#116;&#97;&#115;"
  Case "fi", "1035"
    a1 = "Valmiit"
  Case "ga", "2108"
    a1 = "Críochnaithe"
  Case "hi", "1081"
    a1 = "&#2360;&#2350;&#2366;&#2346;&#2381;&#2340;"
  Case "hu", "1038"
    a1 = "Kész"
  Case "id", "1057"
    a1 = "Selesai"
  Case "is", "1039"
    a1 = "&#108;&#111;&#107;&#105;&#240;"
  Case "it", "1040", "2064"
    a1 = "Terminato"
  Case "ja", "1041"
    a1 = "&#23436;&#25104;"
  Case "ko", "1042"
    a1 = "&#50756;&#47308;"
  Case "lv", "1062"
    a1 = "Pabeigts"
  Case "lt", "1063"
    a1 = "Baigta"
  Case "mt", "1082"
    a1 = "Lest"
  Case "nl", "1043"
    a1 = "Voltooid"
  Case "pl", "1045"
    a1 = "Zakonczono"
  Case "pt", "1046", "2072"
    a1 = "Concluído"
  Case "ro", "1048"
    a1 = "&#238;&#110;&#99;&#101;&#116;&#97;&#116;"
  Case "ru", "1049", "2073"
    a1 = "&#1047;&#1072;&#1074;&#1077;&#1088;&#1096;&#1077;&#1085;&#1086;"
  Case "sk", "1051"
    a1 = "&#68;&#111;&#107;&#111;&#110;&#269;&#101;&#110;&#233;"
  Case "sl", "1060"
    a1 = "&#75;&#111;&#110;&#269;&#97;&#110;&#111;"
  Case "sv", "2077", "1053"
    a1 = "Slutfört"
  Case "sr", "3098", "2074"
    a1 = "&#1047;&#1072;&#1074;&#1088;&#1096;&#1077;&#1085;&#1086;"
  Case "tl", "fil", "1124"
    a1 = "Tapos"
  Case "tr", "1055"
    a1 = "Bitirdi"
  Case "uk", "1058"
    a1 = "&#1047;&#1072;&#1074;&#1077;&#1088;&#1096;&#1077;&#1085;&#1086;"
  Case "zh-TW", "1028"
    a1 = "&#2360;&#2350;&#2366;&#2346;&#2381;&#2340;"
  Case "zh", "2052", "3076", "5124", "4100"
    a1 = "&#2360;&#2350;&#2366;&#2346;&#2381;&#2340;"
  Case Else '"en" English (default)
    a1 = "Done"
  End Select
  fsDone = a1
end function

Function PlaySound(sURL)
  ' http://stackoverflow.com/questions/22367004/vbs-play-sound-with-no-dialogue
  Dim b1
  Dim o1
  if fbFileExists(sURL) then
    b1 = true
    Set o1 = CreateObject("WMPlayer.OCX")
    o1.URL = sURL
    o1.controls.play 
    While o1.playState <> 1
      WScript.Sleep 100
    Wend
    o1.close
  else
    b1 = false
  end if
  PlaySound = b1
End Function


Function fLogoSrc
  ' Read Text logo base 64 encoded data
  fLogoSrc = "data:image/png;base64,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"
End function

Sub main()
  On Error Resume Next
  'Decode the named arguments...
  sVoice=WScript.Arguments.Named.Item("voice")
  srate=WScript.Arguments.Named.Item("rate")
  sLanguage=WScript.Arguments.Named.Item("language")
  sLibre=WScript.Arguments.Named.Item("use-optional-app")
  If sLibre="" Then
    sLibre=WScript.Arguments.Named.Item("libre") 'depreciated
  End If
  sOutFile=WScript.Arguments.Named.Item("soundfile")
  If sOutFile="" Then
    sOutFile=WScript.Arguments.Named.Item("wavefile") 'depreciated
  End If
  s0=WScript.Arguments.Unnamed.Item(0)
  Select case s0
    Case "-h","--help","/h","-?"
      Usage "Help"
      WScript.Exit(0)
    Case "" 
      s0=Year(Date) & "-" & Month(Date) & "-" & Day(Date) &", " & FormatDateTime(now,4)
      select case GetLocale()
        Case "de", "1031", "3079", "5127", "4103", "2055"
          s1="Las ein paar Worte..."
        Case "en-CA", "4105"
          s1="Excuse me... I need to check something. Could you please type in some text?"
        Case "es","11274", "16394", "13322", "9226", "5130", "7178", "12298", "17418", "4106", "18442", "2058", "19466", "6154", "15370", "10250", "20490", "1034", "14346", "8202"
          s1="Introduzca algunas palabras ..."
        Case "fr", "3084", "1036", "2060", "11276","9228","12300","5132","13324", "6156", "14348", "10252", "4108", "7180"
          s1="Tapez quelques mots..."
        Case "pt", "1046", "2072"
          s1="Tipo de poucas palavras..."
        Case else
          s1="Enter a few words..."
      end Select
      s2=InputBox(s1,"Locale: " & GetLocale(),s0)
    Case Else
        s2=getTextFileContent(s0,"UTF-8")
        If Err <> 0 Then
          Usage Err.Number & " -- " &  Err.Description & " -- " & s0
          Wscript.Exit(0)
        End If
  End Select
  If sLanguage = "" then
    s1=s2
  Else 
    s1=AddLanguageCodes(sLanguage,s2)  
  End If
  If sOutFile="" Then
    sayIt s1,sRate,sVoice
  Else
    writeIt s1,sRate,sVoice,sOutFile,s2,sLibre
  End if
End Sub


Function getTextFileContent (strFileName, strCharSet)
  ' Stefan Thelenius "VBScript: Reading text files" Friday, 11 April 2008
  ' Accessed September 11, 2013.
  ' http://abouttesting.blogspot.ca/2008/04/vbscript-reading-text-files.html
  Const adTypeBinary = 1 'not used
  Const adTypeText = 2
  'Set default CharSet
  If strCharSet = "" Then strCharSet = "ASCII"
  ' *** CharSets ***
  '    Windows-1252
  '    Windows-1257
  '    UTF-16
  '    UTF-8
  '    UTF-7
  '    ASCII
  '    X-ANSI
  '   iso-8859-2
  Set objStreamFile = CreateObject("Adodb.Stream")
  With objStreamFile
    .CharSet = strCharSet
    .Type= adTypeText
    .Open
    .LoadFromFile strFileName
    getTextFileContent = .readText
    .Close
  End With
  Set objStreamFile = Nothing
End Function

Function readFile(s0)
      readFile=getTextFileContent (s0,"UTF-8")
End Function

main
