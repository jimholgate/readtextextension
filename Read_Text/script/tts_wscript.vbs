'VBS Script for Read Text Extension by James Holgate
'Standard: "(TTS_WSCRIPT_VBS)" "(TMP)"
'1: "(TTS_WSCRIPT_VBS)" /voice:"Microsoft Anna" /rate:-3 "(TMP)"
'2: "(TTS_WSCRIPT_VBS)" /language:"(SELECTION_LANGUAGE_CODE)" "(TMP)"
'3: "(TTS_WSCRIPT_VBS)" /language:"(SELECTION_LANGUAGE_CODE)" /soundfile:"(HOME)(NOW).wav" "(TMP)"
'Use "http://www.apple.com/itunes/" to add mp3, m4a and aif items to an iTunes library and home directory
'4: "(TTS_WSCRIPT_VBS)" /language:"(SELECTION_LANGUAGE_CODE)" /soundfile:"(HOME)(NOW).mp3" "(TMP)"
'5: "(TTS_WSCRIPT_VBS)" /language:"(SELECTION_LANGUAGE_CODE)" /soundfile:"(HOME)(NOW).m4a" "(TMP)"
'6: "(TTS_WSCRIPT_VBS)" /language:"(SELECTION_LANGUAGE_CODE)" /soundfile:"(HOME)(NOW).aif" "(TMP)"

Const ForReading=1
Const ForWriting=3 
Const AUDIO_FORMAT=34 ' (16 bit mono 44.100 KHz). 
  'Common formats: 8 (8 KHz 8-bit mono), 16 (16 KHz 8-bit mono)
  '35 (44 KHz 16-bit Stereo), 65 (GSM 8 KHz), 66 (GSM 11 KHz)

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
  ' Play ogg encoded sound files with firefox, chrome or chromium
  ' oggenc.exe or oggenc2.exe makes an ogg file in the specified location
  ' The ogg converter program must be installed in C:\opt\.
  ' oggenc2 encoder - http://www.rarewares.org/ogg-oggenc.php
  ' Players and plugins - http://www.vorbis.com/setup_windows/
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
 'kill wavfile
  Set fso = CreateObject("Scripting.FileSystemObject")
  Set aFile = fso.GetFile(wavfile)
  aFile.Delete
End Sub

Sub wav2flac (wavfile,outfile,sMyWords)
  ' Play flac encoded sound files http://flac.sourceforge.net/links.html#software
  ' Players and plugins - http://flac.sourceforge.net/
  ' On Error Resume Next
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
 'kill wavfile
  Set fso = CreateObject("Scripting.FileSystemObject")
  Set aFile = fso.GetFile(wavfile)
  aFile.Delete
End Sub

Sub wav2m4a (wavfile,outFile,sMyWords)
  ' Play mp4 AAC encoded sound files with most music players
  ' neroAacEnc.exe makes an mp4 file in the specified location
  ' The mp4 converter program must be installed in C:\opt\
  ' Script doesn't set file metatags, but you can use the 
  ' neroAacTag.exe tagging program. See:
  ' http://www.nero.com/enu/downloads-nerodigital-nero-aac-codec.php
  'On Error Resume Next
  if fbFileExists("C:\opt\neroAacEnc.exe") then
    sPpath="C:\opt\neroAacEnc.exe"
    sPname="neroAacEnc.exe:"
  elseif fbFileExists("C:\opt\faac.exe") then
    sPpath="C:\opt\faac.exe"
    sPname="faac.exe:"
  else
    exit sub
  end if        
  ' Last chance to cancel or rename the file. This option is silent,
  ' so script reminds you that you are creating a file.
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
 'kill wavfile
  Set fso = CreateObject("Scripting.FileSystemObject")
  Set aFile = fso.GetFile(wavfile)
  aFile.Delete
End Sub

Sub wav2mp3 (wavfile,outFile,sMyWords)
  ' Play mp3 compatible encoded sound files with most music players
  ' lame.exe makes an mp3 compatible file in the specified location
  ' The mp3 converter program must be installed in C:\opt\
  ' Script doesn't set file metatags. See:
  ' http://www.rarewares.org/mp3-lame-bundle.php
  On Error Resume Next
  if fbFileExists("C:\opt\lame.exe") then
    sPpath="C:\opt\lame.exe"
    sPname="lame.exe:"
  else
    exit sub
  end if        
  ' Last chance to cancel or rename the file. This option is silent,
  ' so script reminds you that you are creating a file.
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
 'kill wavfile
  Set fso = CreateObject("Scripting.FileSystemObject")
  Set aFile = fso.GetFile(wavfile)
  aFile.Delete
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
    Usage "Get / Téléchargez: http://www.apple.com/itunes/" & chr(10) & chr(10) & "Did not find a supported iTunes version / On n'a pas trouvé une version actuelle d'iTunes" & chr(10)
    Wscript.Exit(0)
  End If
  set encoderCollection = iTunesApp.Encoders
  oldEncoder=iTunesApp.CurrentEncoder 
  Select Case strExt(sOut2file)
    Case ".m4a",".aac"
      set encoder=encoderCollection.ItemByName("AAC Encoder")
    Case ".aif",".aiff"
      set encoder=encoderCollection.ItemByName("AIFF Encoder")
    Case Else
      set encoder=encoderCollection.ItemByName("MP3 Encoder")
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
 'kill wavfile
  Set fso = CreateObject("Scripting.FileSystemObject")
  Set aFile = fso.GetFile(wavfile)
  aFile.Delete
End Sub

Function fbFileExists(sfilespec)
   Dim fso
   Set fso = CreateObject("Scripting.FileSystemObject")
   fbFileExists = (fso.FileExists(sfilespec))
End Function

Function AddLanguageCodes(s1,s4)
  s1=Lcase(s1)
  s2=""

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
    if canUseSpeechXML Then
      s2=""
    else
      s2="9" 'en if XP (5.1) can`t tell language.
    end if
  End Select
  If s2="" Then ' With Sapi 5.3 and above we try ISO language code
    s3="<?xml version=" & Chr(34) & "1.0" & Chr(34) & "?>"
    s3=s3 & " <speak version=" & Chr(34) & "1.0" & Chr(34) & " xmlns=" & Chr(34) & "http://www.w3.org/2001/10/synthesis" & Chr(34)
    s3=s3 & " xmlns:xsi=" & Chr(34) & "http://www.w3.org/2001/XMLSchema-instance" & Chr(34)
    s3=s3 & " xsi:schemaLocation=" & Chr(34) & "http://www.w3.org/2001/10/synthesis"
    s3=s3 & " http://www.w3.org/TR/speech-synthesis/synthesis.xsd" & Chr(34) & " xml:lang=" & Chr(34)
    s3=s3 & s1
    s3=s3 & Chr(34) & "> "
    s3=s3 & s4
    s3=s3 & "</speak>"
  Else
    s3="<speak><lang langid=" & Chr(34)
    s3=s3 & s2
    s3=s3 & Chr(34) & "> "
    s3= s3 & s4
    s3=s3 & " </lang></speak>" 
  End if
  AddLanguageCodes=s3
End Function

Sub SayIt(s1,sRate,sVoice)
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
    Loop Until Sapi.WaitUntilDone(1)
    Set Sapi=Nothing 
  End If
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
    If fs.FileExists(sFileName) Then fs.DeleteFile sFileName
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
    end if
  End If
End Sub

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
      select case left(lcase(sLanguage),2)
        Case "de"
          s1="Las ein paar Worte..."
        Case "es"
          s1="Introduzca algunas palabras ..."
        Case "fr"
          s1="Tapez quelques mots..."
        Case "pt"
          s1="Tipo de poucas palavras..."
        Case else
          s1="Enter a few words..."
      end Select
      s2=InputBox(s1,"tts_wscript.vbs",s0)
    Case Else
      Set objFSO=CreateObject("Scripting.FileSystemObject")
      Set objText=objFSO.OpenTextFile(s0,ForReading)
      s2=objText.ReadAll
      objText.Close
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

main
