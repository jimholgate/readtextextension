'''
'' Read text
'' =========
'' 
'' **Read text** reads text aloud, saves audio files and
'' can use resources from the web based on the selected
'' text.
'' 
'' * Select text.
'' * Click the *Read selection* button.
'' * To read aloud, accept the default in the dialogue, or choose
''   another action from the menus.
'' 
'' Saving files
'' ------------
'' 
'' Windows lets you save sound files in an uncompressed`.wav` format. 
'' To convert `.wav` files to small `.m4a` files that you can share 
'' on most mobile phones, music players and tablets, download 
'' [Nero m4a encoder][1]
'' [1]:http://www.nero.com/enu/downloads-nerodigital-nero-aac-codec.php
'' and save ' `neroAacEnc.exe` and `neroAacTag.exe` in `C:\opt\`
'' The extension adds writing `.m4a` files to the list of options
'' in the dialogue.
'' 
'' Language support
'' ----------------
'' 
'' This script uses the Windows speech application programming
'' interface (`SAPI`). Depending on the version and locale of
'' Windows, voices in different languages may be available.
'' 
'' Examples:
'' ---------
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
''     "(TTS_WSCRIPT_VBS)" /voice:"Microsoft Hortense Desktop - French" "(TMP)"
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
'' ================
'' 
'' ## AAC Encoder
'' 
'' [Nero m4a encoder](http://www.nero.com/enu/downloads-nerodigital-nero-aac-codec.php)
'' is a free command line M4A converter from [Nero](http://www.nero.com).
'' 
'' You can play m4a AAC encoded sound files with most music players.
'' Use `neroAacEnc.exe` to make an m4a file.
'' 
''  * If the directory `C:\opt` doesn't exist, create it. 
''  * Copy `neroAacEnc.exe` to `C:\opt\`
''  * Copy `neroAacTag.exe` to `C:\opt\`
''  * The `neroAacTag.exe` program adds metadata like author, genre, title and year.
''
''     "(TTS_WSCRIPT_VBS)" /use-optional-app:"True" /soundfile:"(HOME)en\(NOW).m4a" "(TMP)"
'' 
'' ## Audacity
'' 
'' [Audacity](http://audacityteam.org/) is a free cross platform audio editor. It can
'' use an [FFmpeg](https://ffmpeg.org/) library to save audio files in different formats.  
'' 
'' ### FFmpeg for Audacity
'' 
'' Windows security policies may prevent you from installing the Audacity FFmpeg converter
'' library using the `ffmpeg-win-2.2.2.exe` installer.  You can install the FFmpeg library
'' by downloading the `ffmpeg-win-2.2.2.zip` archive and copying the contents to a
'' directory that is available to all users.
'' 
'' 1. Log in with an administrator account.
'' 2. Go to the [MP3 for Audacity page](http://lame.buanzo.org/#lamewindl). 
'' 3. Directly underneath "For FFmpeg/LAME on Windows click below:", left-click the link
''   `ffmpeg-win-2.2.2.zip` and save the file anywhere on your computer.
'' 4. Double-click `ffmpeg-win-2.2.2.zip` to open the archive. 
'' 5. If the directory `C:\opt` doesn't exist, create it. Copy the contents of the zip 
''    file to `C:\opt`.
'' 6. Any user can now set up Audacity to use ffmpeg by opening Audacity, then setting 
''    *Edit - Preferences... - Libraries - FFmpeg library* to `C:\opt`.
'' 7. Read text extension now shows .mp3 and .ogg formats as export options.
'' 8. You can use Audacity to add music or special effects to your sound files.
'' 
''     "(TTS_WSCRIPT_VBS)" /use-optional-app:"True" /soundfile:"(HOME)en\(NOW).mp3" "(TMP)"
''     "(TTS_WSCRIPT_VBS)" /use-optional-app:"True" /soundfile:"(HOME)en\(NOW).ogg" "(TMP)"
'' 
'' ## Flac
'' 
'' Makes free lossless audio codec (FLAC) files.
'' 
''  * Install `flac.exe` in `C:\opt\`
''  * [flac encoder](http://flac.sourceforge.net/links.html#software)
''  * [Players and plugins](http://flac.sourceforge.net/)
'' 
''     "(TTS_WSCRIPT_VBS)" /use-optional-app:"True" /soundfile:"(HOME)en\(NOW).flac" "(TMP)"
'' 
'' ## iTunes
'' 
'' **iTunes** is a visual music manager from Apple available at no cost.
'' 
'' Use [iTunes](http://www.apple.com/itunes/) to convert sound files with metadata
'' and album cover art. The first time you use it, iTunes takes a few moments to start.
'' iTunes creates the audio file in it's own directory and signals you with a sound. 
'' Read Text Extension puts a copy in a sound directory in your home directory.
'' 
''     "(TTS_WSCRIPT_VBS)" /language:"en-US" /soundfile:"(HOME)en\(NOW).aif" "(TMP)"
''     "(TTS_WSCRIPT_VBS)" /language:"en-US" /soundfile:"(HOME)en\(NOW).m4a" "(TMP)"
''     "(TTS_WSCRIPT_VBS)" /language:"en-US" /soundfile:"(HOME)en\(NOW).mp3" "(TMP)"
'' 
'' ## Lame
'' 
'' Lame is a free command line file converter.
'' 
'' Play mp3 compatible encoded sound files with most music players
'' Use `lame.exe` to make an mp3 compatible file.
'' 
''  * Install `lame.exe` in `C:\opt\`
''  * [Lame encoder](http://www.rarewares.org/mp3-lame-bundle.php)
'' 
''     "(TTS_WSCRIPT_VBS)" /use-optional-app:"True" /soundfile:"(HOME)en\(NOW).mp3" "(TMP)"
'' 
'' ## Miro Video Converter (FFmpeg)
'' 
'' This is a free visual music and video converter from the Participatory 
'' culture foundation.
'' 
'' Miro Video Converter can convert mp3, ogg and other media using `ffmpeg`
'' Once installed, read text can use FFmpeg to make audio and video media files
'' for cross-platform applications.
'' 
''  * [ffmpeg](https://www.ffmpeg.org)
''  * [Miro formats](http://develop.participatoryculture.org/index.php/ConversionMatrix)
''  * [Miro video converter](http://ftp.osuosl.org/pub/pculture.org/mirovideoconverter/)
''  * [Participatory culture foundation](http://pculture.org/)
'' 
''     "(TTS_WSCRIPT_VBS)" /use-optional-app:"True" /soundfile:"(HOME)en\(NOW).mp3" "(TMP)"
''     "(TTS_WSCRIPT_VBS)" /use-optional-app:"True" /soundfile:"(HOME)en\(NOW).ogg" "(TMP)"
'' 
'' The direct link to the most recent version of Miro Video Converter is at osuosl.org -
'' [`MiroConverterSetup.exe`](http://ftp.osuosl.org/pub/pculture.org/mirovideoconverter/).
'' 
'' ## Ogg
'' 
'' Play ogg encoded sound files with firefox, chrome or chromium.
'' Use `oggenc.exe` or `oggenc2.exe` to make an ogg file
'' 
''  * The ogg converter program must be installed in `C:\opt\`.
''  * [oggenc2 encoder](http://www.rarewares.org/ogg-oggenc.php)
''  * [Players and plugins](http://www.vorbis.com/setup_windows/)
'' 
''     "(TTS_WSCRIPT_VBS)" /use-optional-app:"True" /soundfile:"(HOME)en\(NOW).ogg" "(TMP)"
'' 
'' ----------------------------------------------------------------------------
'' 
'' [Read Text Extension](http://sites.google.com/site/readtextextension/)
'' 
'' Copyright © 2011 - 2015 James Holgate
'''
Const ForReading = 1
Const ForWriting = 3
Const AUDIO_FORMAT = 34  ' (16 bit mono 44.100 KHz).
    ' Common formats: 8 (8 KHz 8-bit mono), 16 (16 KHz 8-bit mono)
    ' 35 (44 KHz 16-bit Stereo), 65 (GSM 8 KHz), 66 (GSM 11 KHz)
Const APP_SIGNATURE = "ca.bc.vancouver.holgate.james.readtextextension"
Const APP_NAME = "Read Text"


Sub Usage(sA)
    '''
    ' Shows usage in a dialog box when the program has a problem parsing a line.
    '''
    s1 = sA & chr(10) & _
            chr(10)& _
            "tts_wscript.vbs [/language:""xxx"" | /voice:""xxx""] [/rate:"& _
            "nn] [/soundfile:""c:\xxx.wav""] ""filename.txt""" & chr(10) & _
            chr(10) & _
            "/language:""fr"" - Language option" & chr(10)& _
            "/voice:""Microsoft Hortense Desktop - French""" & _
            chr(10) & _
            "/rate:-3 - Minimum -10 & Maximum 10" & chr(10) & _
            "/soundfile:""C:\xxx.wav"" - sound file path" & chr(10) & _
            "/imagefile:""C:\xxx.[png|jpg]"" - input png or jpg for album" & _
            " cover" & chr(10) & _
            "/sDimensions = ""400x400"" - suggested album" & _
            " cover size in pixels" & chr(10) & _
            """filename.txt"" Text Document to read (required)"
    msgBox s1, 0, APP_NAME
End Sub


Function EscapeReturnsAndReplaceQuotes(sA)
    '''
    ' Use a normal plain text string to generate a 'lyrics' string
    ' with smart quotes and no carriage returns.
    '''
    Dim s1

    EscapeReturnsAndReplaceQuotes = ""
    ' Not all audio players can show lyrics longer than 1000 characters.
    If len(sA) > 1000 then
	sA = left(sA, 996) & " ..."
    Elseif sA = "" then
        Exit Function
    End if
    s1 = Replace(sA, chr(13), "\n")  ' escaped CR
    s1 = Replace(s1, " """, " “" )  ' SPACE, left double quote
    s1 = Replace(s1, chr(10) & """", chr(10) & "“" )  ' LF, left double quote
    s1 = Replace(s1, chr(9) & """", chr(9) & "“" )  ' TAB, left double quote
    s1 = Replace(s1, "(" & """", "(“" )  ' left (, left double quote
    s1 = Replace(s1, "[" & """", "[“" )  ' left [, left double quote
    s1 = Replace(s1, "*" & """", "*“" )  ' *, left double quote from markdown
    s1 = Replace(s1, "_" & """", "_“" )  ' _, left double quote from markdown
    s1 = Replace(s1, """", "”" )  ' all others, right double quote
    EscapeReturnsAndReplaceQuotes = s1
End Function


Function strExt(sA)
    '''
    ' Given a file path, returns the extension
    '''
    strExt = LCase(Mid(sA,InStrRev(sA,".")))
End Function


Function doExecute(sA, bWaitTilDone)
    '''
    ' Execute a string as a command
    '''
    Dim oExec
    Dim WshShell

    on error resume next
    If Len(sA) > 0  Then
        Set WshShell = CreateObject("WScript.Shell")
        Set oExec = WshShell.Exec(sA)
        If bWaitTilDone then
            Do While oExec.Status = 0
                 WScript.Sleep 100
            Loop
        End If
    End If
    If Err.Number <> 0 Then
        msgBox Err.Description
        doExecute = False
    Else
        doExecute = True
    End If
End Function


Function fbRemoveFile(sfilespec)
    '''
    ' Remove file. Returns true if successful or if no file exists.
    '''
    Dim fso
    Set fso = CreateObject("Scripting.FileSystemObject")
    If fso.FileExists(sfilespec) Then
        fso.DeleteFile sfilespec
    End If
    fbRemoveFile = not(fso.FileExists(sfilespec))
End Function


Function fsMyInputBox(sA)
    '''
    ' Debug or pause execution. Returns string or blank if you click 'Cancel'
    '''
    Dim cr
    Dim s1
    Dim s2
    Dim s3
    Dim s4
    Dim s5

    cr = chr(10)
    s1 = EscapeReturnsAndReplaceQuotes(fsMetaalbum)
    s2 = EscapeReturnsAndReplaceQuotes(fsMetaId)
    s3 = EscapeReturnsAndReplaceQuotes(fsMetagenre)
    s4 = EscapeReturnsAndReplaceQuotes(fsMetatitle)
    s5 = EscapeReturnsAndReplaceQuotes(fsMetatrack)
    fsMyInputBox = InputBox(s1 & cr & s2 & cr & cr & s5 & ". " & s4, s3, sA)
End Function


Function fbFileExists(sfilespec)
    '''
    ' Test if file exists.
    '''
    Dim fso
    If Len(sfilespec) = 0 Then
        fbFileExists = False
    Else
        Set fso = CreateObject("Scripting.FileSystemObject")
        fbFileExists = (fso.FileExists(sfilespec))
    End If
End Function


Function fbIsAppDataFile(sA, bTattle)
    '''
    ' Identify files that shouldn't be manually edited or deleted.
    ' If bTattle is true, then report the bad file path in a dialog
    ' functioning as a msgbox but using an inputbox so that you can
    ' copy the path and check the location in your file browser.
    '''
    Dim a1
    Dim b1
    Dim n
    Dim objFSO
    Dim oExec
    Dim s1
    Dim s2
    Dim WshEnv
    Dim WshShell

    fbIsAppDataFile = False
    Set objFSO=CreateObject("Scripting.FileSystemObject")
    Set WshShell = CreateObject("WScript.Shell")
    Set WshEnv = WshShell.Environment("Process")
    s2 = ""
    s1 = WshEnv("ALLUSERSPROFILE") & chr(10) & _
            WshEnv("APPDATA") & chr(10) & _
            WshEnv("LOCALAPPDATA") & chr(10) & _
            ".oxt" & chr(10) & _
            WshEnv("ProgramData") & chr(10) & _
            WshEnv("ProgramFiles(x86)") & chr(10) & _
            WshEnv("ProgramFiles") & chr(10) & _
            WshEnv("ProgramW6432") & chr(10) & _
            WshEnv("SystemDrive") & "\opt" & chr(10) & _
            WshEnv("SystemRoot") & chr(10) & _
            "uno_packages" & chr(10) & _
            WshEnv("USERPROFILE") & "\opt" & chr(10) & _
            WshEnv("windir")
    a1 = split(s1, (chr(10)))
    If len(sA) > 0 Then
        For n = Lbound(a1) to Ubound(a1)
            If len(a1(n)) > 0 Then
                If Instr(sA, a1(n)) > 0 Then
                    fbIsAppDataFile = True
                    s2 = a1(n)
                    Exit For
                End If
            End if
        Next
    End If
    if fbIsAppDataFile = True and bTattle = True Then
        b1 = InputBox("Restricted path!", APP_NAME, sA)
    end if
End Function


Function canUseSpeechXML
    '''
    ' Can the installed version of SAPI use XML?
    '''
    Dim SystemSet
    Dim VerBig

    canUseSpeechXML = False
    Set SystemSet = GetObject("winmgmts:").InstancesOf("Win32_OperatingSystem")
    for each System in SystemSet 
        VerBig = Left(System.Version,3)
        If CLng(VerBig) > 5.1 Then
            canUseSpeechXML=True
        End If
    next
End Function


Function myOptPath(appName)
    '''
    ' Look in a couple of spots for optional command line converters
    ' * In your home directory in a directory named opt `C:\Users\myName\opt\`
    ' * In opt in the root of your home drive `C:\opt\`
    ' Returns path if found, or "" if not found.
    '''
    Dim wshEnv
    Dim WshShell
    Dim s1
    Dim s2

    Set WshShell = CreateObject("WScript.Shell")
    Set WshEnv = WshShell.Environment("Process")
    myOptPath = ""
    s1 = WshEnv("HOMEDRIVE") & "\opt\" & appName
    s2 = WshEnv("USERPROFILE") & "\opt\" & appName
    If fbFileExists(s1) Then
        myOptPath = s1
    Elseif fbFileExists(s2) Then
        myOptPath = s2
    End If
End Function


Function myAudacityLamePath
    '''
    ' Returns path to lame mp3 converter program.
    '''
    Dim wshEnv
    Dim WshShell
    Dim s1
    Dim s2

    Set WshShell = CreateObject("WScript.Shell")
    Set WshEnv = WshShell.Environment("Process")
    myAudacityLamePath = ""
    s1 = WshEnv("ProgramFiles(x86)") & "\Lame For Audacity\lame.exe"
    s2 = WshEnv("ProgramFiles") & "\Lame For Audacity\lame.exe"
    If fbFileExists(s1) Then
        myAudacityLamePath = s1
    Elseif fbFileExists(s2) Then
        myAudacityLamePath = s2
    End If
End Function


Function wav2ogg(wavfile, outfile, sMyWords)
    '''
    ' Use a downloaded command line program to convert sound file
    '''
    Dim b1
    Dim s1
    Dim s2
    Dim s3
    Dim sMeta
    Dim sLyrics
    Dim sPname
    Dim sPath

    wav2ogg = False
    On Error Resume Next
    s1 = myOptPath("oggenc2.exe") 
    s2 = myOptPath("oggenc.exe")
    sLyrics = ""
    If fbFileExists(s1) Then
        sPpath = s1
        sPname = s1
    Elseif fbFileExists(s2) Then
        sPpath = s2
        sPname = s2
    Else
        Exit Function
    End If
    If sPpath = s1 Then
        s3 = fsVerifiedMetatitle
        If s3 = "" Then
            sMeta = ""
        Else
            sMeta = " --album """ & fsMetaalbum & _
                    """ --artist """ & fsMetaId & _
                    """ --genre """ & fsMetagenre & _
                    """ --title """ & s3 & _
                    """ --tracknum """ & fsMetatrack & _
                    """ "
        End If
        If Len(sMyWords) > 0 Then
             ''''' Not activated if there are no lyrics
             sLyrics = EscapeReturnsAndReplaceQuotes(sMyWords)
             sMeta = sMeta & " --lyrics=""" & sLyrics & """ "
        End If
        sA = sPpath & " """ & wavfile & """ " & sMeta & " --quiet -o """
        sA = sA & outfile & """ " 
    Else
        sA=sPpath & " --quiet -o """ & outfile & """ """ & wavfile & """"
    End If
    s2 = outfile
    If Len(s2) > 0  Then
        ' fsMyInputBox(sA)
        b1 = doExecute(sA, True)
    End If
    If fbFileExists(outfile) Then
        wav2ogg = True
        fbRemoveFile wavfile
    End If
End Function


Function fsVorbisMeta
    '''
    ' [Tag specifications](http://www.xiph.org/vorbis/doc/v-comment.html)
    ' [About flac converter](http://linux.die.net/man/1/flac)
    ' Depending on version of ffmpeg or other player, these tags may be 
    ' ignored.
    '''
    Dim s3

    s3 = fsVerifiedMetatitle
    If s3 = "" Then
    fsVorbisMeta = ""
    Else
        fsVorbisMeta = " -T ALBUM=""" & fsMetaalbum & _
                    """ -T ARTIST=""" & fsMetaId & _
                    """ -T GENRE=""" & fsMetagenre & _
                    """ -T TITLE=""" & s3 & _
                    """ -T TRACKNUMBER=""" & fsMetatrack & _
                    """ "
    End If
End Function


Function wav2flac(wavfile, outfile, sMyWords, sImage)
    '''
    ' Converts wav audio file to free lossless audio codec.
    '''
    Dim b1
    Dim s1
    Dim s2
    Dim s3
    Dim sA
    Dim sMeta

    wav2flac = False
    s1 = myOptPath("flac.exe") 
    If fbFileExists(s1) Then
        sPpath = s1
        sPname = s1
    Else
        Exit Function
    End If
    s2 = outfile
    If Len(sImage) > 0 and fbFileExists(sImage) Then
        s3 = " --picture=""" & sImage & """ " 
    Else
        s3 = ""
    End If
    sMeta = fsVorbisMeta
    If Len(s2) > 0  Then
        sA=sPpath & s3 & sMeta & " -f -o """ & s2 & """ """ & wavfile & """"
        ''''''If Len(fsMyInputBox(sA)) = 0 Then
        ''''''  Exit Function
        ''''''End If
        b1 = doExecute(sA, True)
    End If
    If fbFileExists(outfile) Then
        wav2flac = True
        fbRemoveFile wavfile
    End If
End Function


Function wav2m4a(wavfile, outFile, sMyWords, sImage)
    '''
    ' Use a downloaded command line program to convert sound file.
    '''
    Dim b1
    Dim b2
    Dim s1
    Dim s2
    Dim s3
    Dim s4
    Dim sA
    Dim sPpath
    Dim sPname

    s1 = myOptPath("neroAacEnc.exe") 
    s2 = myOptPath("faac.exe")
    wav2m4a = False
    If fbFileExists(s1) Then
        sPpath = s1
        sPname = s1
    Elseif fbFileExists(s2) Then
        sPpath = s2
        sPname = s2
    Else
        Exit Function
    End If 
    s3 = outFile
    s4 = ""
    If Len(s3) > 0  Then
        If sPname = s1 Then
            sA = sPpath & " -if """ & wavfile & """ -of """ & s3 & """"
            b1 = doExecute(sA, False) 
        Else 'faac.exe
            sA = sPpath & " -o """ & s3 & """ """ & wavfile & """"
            b1 = doExecute(sA, True)
        End If
    End If
    b2 = fbTagM4a(s3, sMyWords, sImage)
    If fbFileExists(s3) Then
        wav2m4a = True
        fbRemoveFile wavfile
    End If
End Function


Function fbTagM4a(s2, sMyWords, sImage)
    '''
    ' Use a downloaded command line program to tag a sound file.
    ' `neroAacEnc` can't process long wav files if the function waits for
    ' the shell result to equal 0.  This dialog shows when the encoder is
    ' running.  While you wait for the file to convert, check the title.  
    ' If you click *Cancel*, the function skips adding metadata. 
    ' If you click *OK* it adds metadata.
    '''
    Dim b1
    Dim s1
    Dim s3
    Dim sMeta

    fbTagM4a = False
    s1 = myOptPath("neroAacTag.exe")
    s3 = fsVerifiedMetatitle
    if s3 = "" then
        exit function
    end if
    If fbFileExists(s1) and fbFileExists(s2) Then
        sMeta = " -meta:album="""& fsMetaalbum & _
                """ -meta:artist=""" & fsMetaId & _
                """ -meta:composer=""" & fsMetaId & _
                """ -meta:comment=""" & "[Nero AAC Encoder](http://www.nero.com)" & _
                """ -meta:genre=""" & fsMetagenre & _
                """ -meta:title=""" & s3 & _
                """ -meta:track=""" & fsMetatrack & _
                """ -meta:year=""" & year(Now) & _
                """ "
        If Len(sImage) > 0 and fbFileExists(sImage) Then
            sMeta = sMeta & "-add-cover:front:""" & sImage & """ "
        End If
        If Len(sMyWords) > 0 Then
             ''''' Not activated if there are no lyrics
             sLyrics = EscapeReturnsAndReplaceQuotes(sMyWords)
             sMeta = sMeta & " -meta:lyrics=""" & sLyrics & """ "
        End If
        sA= s1 &" """ & s2 & """" & sMeta
        ''''''' sTest1 = fsMyInputBox(sA) ''''''debug
        b1 = doExecute(sA, True)
        fbTagM4a = True
    End If
End Function


Function wav2mp3(wavfile, outFile, sImage)
    '''
    ' Use a downloaded command line program to convert sound file.
    '''
    Dim s1
    Dim s2
    Dim s3
    Dim sMeta
    Dim sPath

    wav2mp3 = False
    On Error Resume Next
    s1 = myOptPath("lame.exe")
    If len(s1) = 0 then
        ' Look for lame.exe in the Audacity lame library
        s1 = myAudacityLamePath()
    End If
    If fbFileExists(s1) Then
        sPpath = s1
    Else
        Exit Function
    End If
    s3 = fsVerifiedMetatitle
    If s3 = "" Then
        sMeta = ""
    Else
        sMeta = " --tt """ & s3 & _
                """ --ta """ & fsMetaId & _
                """ --tc """ & "[Lame.exe](http://www.rarewares.org)" & _
                """ --tl """ & fsMetaalbum & _
                """ --ty """ &  Year(Now) & _
                """ --tn """ & fsMetatrack & _
                """ --tg """ & fsMetagenre & _
                """ "
    End If
    If Len(sImage) > 0 and fbFileExists(sImage) Then
        Select Case lcase(strExt(sImage))
        Case ".jpg", ".jpeg", ".png", ".gif"
            sMeta = sMeta & " --ti """ & simage & """ "
        Case Else
        End Select
    End If
    s2 = outFile
    If Len(s2) > 0  Then
        ' We need to use the --quiet switch, or lame gets stuck in the loop.
        sA = sPpath & _
                         sMeta & _
                         " --ignore-tag-errors --quiet -V2 """ & _
                         wavfile & _
                         """ """ & _
                         s2 & _
                         """"
        b1 = doExecute(sA, True)
    End If
    If fbFileExists(outFile) Then
        wav2mp3 = True
        fbRemoveFile wavfile
    End If
End Function


Function fsMetaalbum()
    Dim s1
    Dim s2

    s2 = sLockPath("lock")
    If fbFileExists(s2 & ".album") Then
        s1 = readFile(s2 & ".album")
    Else
        s1 = APP_NAME & " album"
    End If
    fsMetaalbum = EscapeReturnsAndReplaceQuotes(s1)
End Function


Function fsMetagenre()
    Dim s1
    Dim s2

    s2 = sLockPath("lock")
    If fbFileExists(s2 & ".genre") Then
        s1 = readFile(s2 & ".genre")
    Else
        s1 = "Speech"
    End If
    fsMetagenre = EscapeReturnsAndReplaceQuotes(s1)
End Function


Function fsMetaId()
    Dim s1
    Dim s2

    s2 = sLockPath("lock")
    If fbFileExists(s2 & ".id") Then
        s1 = readFile(s2 & ".id")
    Else
        s1 = "sites.google.com/site/readtextextension"
    End If
    fsMetaId = EscapeReturnsAndReplaceQuotes(s1)
End Function


Function fsMetatitle()
    Dim s1
    Dim s2

    s2 = sLockPath("lock")
    If fbFileExists(s2 & ".title") Then
        s1 = readFile(s2 & ".title")
    Else
        s1 = "Untitled"
    End If
    fsMetatitle = EscapeReturnsAndReplaceQuotes(s1)
End Function



Function fsVerifiedMetatitle()
    Dim s1

    s1 = fsMetatitle
    PlaySound "C:\Windows\Media\notify.wav"
    s1 = fsMyInputBox(s1)  
    fsVerifiedMetatitle = EscapeReturnsAndReplaceQuotes(s1)
End Function


Function fsMetatrack
    Dim s1
    Dim s2

    s2 = sLockPath("lock")
    If fbFileExists(s2 & ".track") Then
        s1 = readFile(s2 & ".track")
    Else
        s1 = "1"
    End If
    fsMetatrack = EscapeReturnsAndReplaceQuotes(s1)
End Function

Sub removeMetaFiles()
    Dim a1
    Dim s1
    Dim n

    s1 = sLockPath("lock")
    a1 = split(".album,.genre,.id,.title,.track", ",")
    For n = Lbound(a1) To Ubound(a1)
        fbRemoveFile s1 & a1(n)
    Next
End Sub


Function fsWhereIsFfmpeg()
    '''
    ' If you installed Miro Video Converter in the default location, this
    ' function points to ffmpeg. If you just have ffmpeg, install it or link
    ' to it in `c:\opt\ffmpeg.exe`
    '''
    Dim c1
    Dim c2
    Dim c3
    Dim c4
    Dim c5
    Dim c6
    Dim c7
    Dim c8
    Dim objFSO
    Dim oExec
    Dim retval
    Dim WshEnv
    Dim WshShell

    Set objFSO=CreateObject("Scripting.FileSystemObject")
    Set WshShell = CreateObject("WScript.Shell")
    Set WshEnv = WshShell.Environment("Process")
    c1 = WshEnv("ProgramFiles(x86)")
    c2 = WshEnv("ProgramFiles")
    c3 = "\Participatory Culture Foundation\Miro Video Converter\ffmpeg\ffmpeg.exe"
    c4 = "\Participatory Culture Foundation\Miro\ffmpeg\ffmpeg.exe"
    c5 = WshEnv("HOMEDRIVE") & "\opt\ffmpeg.exe"
    c6 = WshEnv("USERPROFILE") & "\opt\ffmpeg.exe"
    c7 = WshEnv("HOMEDRIVE") & "\opt\avconv.exe"
    c8 = WshEnv("USERPROFILE") & "\opt\avconv.exe"
    retval = ""
    If fbFileExists(c6) Then
        retval = c6
    Elseif fbFileExists(c7) Then
        retval = c7
    Elseif fbFileExists(c8) Then
        retval = c8
    Elseif fbFileExists(c5) Then
        retval = c5
    ElseIf fbFileExists(c1 & c3) Then
        retval = c1 & c3
    ElseIf fbFileExists(c2 & c3) Then
        retval = c2 & c3
    ElseIf fbFileExists(c1 & c4) Then
        retval = c1 & c4
    ElseIf fbFileExists(c2 & c4) Then
        retval = c2 & c4
    Else
        retval = ""
    End If
    fsWhereIsFfmpeg = retval
End Function


Function wav2iTunes(wavfile,sOut2file,sMyWords,sImage, bPlay)
    '''
    ' iTunes makes a mp3, aac or m4a in the iTunes Music Library 
    ' if Length of sOutFile is not zero, Then saves to sOutFile Path
    ' [iTunes Interface Reference][1]
    ' [1]: (http://www.joshkunz.com/iTunesControl/interfaceIiTunes.html)
    '''
    Dim encoder
    Dim encoderCollection
    Dim fso
    Dim myExt
    Dim oldEncoder
    Dim opStatus
    Dim outfile
    Dim Reg1
    Dim s3
    Dim track
    Dim vers

    wav2iTunes = False
    On Error Resume Next
    vers = "Unknown version"
    set iTunesApp = WScript.CreateObject("iTunes.Application.1")
    vers = iTunesApp.Version
    set encoderCollection = iTunesApp.Encoders
    oldEncoder = iTunesApp.CurrentEncoder
    myExt = strExt(sOut2file)
    Select Case myExt
        Case ".mp3"
            set encoder = encoderCollection.ItemByName("MP3 Encoder")
        Case ".aif",".aiff"
            set encoder = encoderCollection.ItemByName("AIFF Encoder")
        Case Else ' ".m4a",".aac", ""
            set encoder = encoderCollection.ItemByName("AAC Encoder")
    End Select
    iTunesApp.CurrentEncoder = encoder
    set fso = CreateObject("Scripting.FileSystemObject")  
    set opStatus = iTunesApp.ConvertFile(wavfile)
    while opStatus.InProgress
        WScript.Sleep 1000
    wend
    WScript.Sleep 1000 'Make sure itunes is done
    iTunesApp.CurrentEncoder=oldEncoder
    s3 = fsVerifiedMetatitle
    If len(s3) > 0 Then
       ' Add metadata
       set track = opStatus.Tracks.Item(1)
       track.Album = fsMetaalbum()
       track.Artist = fsMetaId()
       track.Composer = fsMetaId()
       track.Genre = fsMetagenre()
       track.Lyrics = sMyWords
       track.Name = s3
       track.TrackNumber = fsMetatrack()
       track.Year = Year(Now)
       If Len(sImage) > 0 and fbFileExists(sImage) Then
           track.AddArtworkFromFile(sImage)
       End If
    End If
    set outfile=fso.GetFile(track.Location)
    If Len(sOut2file) > 0 Then 
        outfile.copy(sOut2file)
    End If
    If bplay Then
        track.Play()
    End If
    If Err <> 0 and Err <> 13 Then
        Usage "Did not find a supported iTunes version" & chr(10) & vers & chr(10) & Err.Description
        Wscript.Exit(0)
    Else
        If fbFileExists(outfile) Then
            wav2iTunes = True
            fbRemoveFile wavfile
        End If
    End If
End Function


Function wav2FFmpeg(sWaveName, sOutName, sImage, sDimensions)
    '''
    '' 
    '' wav2FFmpeg
    '' ========
    ''
    '' Converts wav format sound to compressed format optionally
    '' including a picture if supported by the ffmpeg muxer.
    '' returns True if it creates a file; otherwise returns False.
    ''
    ''     sWaveName - the wave sound to convert `input.wav`
    ''     sOutName - the converted file' `output.mp3`
    ''     sImage - a png file to use as a poster `input.png`
    ''       value is ignored for muxers and codecs that don't support it.
    ''     sDimensions - suggested dimensions for video output `400x400`
    ''       value is ignored for audio
    '''  
    Dim b1
    Dim cout2
    Dim cr
    Dim doJob
    Dim doJob1
    Dim doJob2
    Dim ffMeta
    Dim myConverter
    Dim retVal
    Dim sFileNameExt
    Dim sPreProcess

    cr= chr(10)
    wav2FFmpeg = False 'default when exiting Function before creating a file
    doJob = ""
    doJob1 = ""
    doJob2 = ""
    ffMeta = ""
    If Len(sDimensions) = 0 Then
        sDimensions = "400x400"
    End If
    sFileNameExt = strExt(sOutName)

' ###Where's ffmpeg?

    myConverter = fsWhereIsFfmpeg()
    If Len(myConverter) = 0 Then
        exit function
    End If

' ###Which codecs can skip the preflight check?

    Select Case sFileNameExt
        Case ".m4a"
            sPreProcess=""
            sPostProcess= ""
            If fbFileExists("C:\opt\neroAacEnc.exe") Then
             ' Nero is recommended for producing standards compliant m4a output.
             ' [Nero m4a encoder][2]
             ' [2]:(http://www.nero.com/enu/downloads-nerodigital-nero-aac-codec.php)
                 exit function
            End If
        Case ".mp3"
            sPreProcess=""
            sPostProcess= ""
            If fbFileExists("C:\opt\lame.exe") Then
                ' You appear to prefer the lame encoder.
                exit function
            End If
        Case ".aif", ".aiff"
            ' Lossless audio interchange format
            sPreProcess=""
            sPostProcess= ""
        Case ".flac"
            ' Lossless audio format
            ' flac is compressed, but requires a player or plugin
            sPreProcess=""
            sPostProcess= ""
            If fbFileExists("C:\opt\flac.exe") Then
                ' You appear to prefer the flac conversion utility.
                exit function
            End If
        Case ".ogg"
            sPreProcess=""
            sPostProcess= ""
            If fbFileExists("C:\opt\oggenc2.exe") Then
                ' You appear to prefer the oggenc2 conversion utility.
                exit function
            End If
        Case ".webm"
            ' Webm - web media file for Chromium, Google Chrome and Firefox.
            sPreProcess=""
            sPostProcess= ""
        Case ".m4v",".mp4"
            ' uses `-strict experimental`. **Do not enable by default**. 
            ' May produce bad results.
            sPreProcess="preFlightCheck"
            sPostProcess= ""
        Case Else ' ".aac"
            exit function
    End Select

' ###Ffmpeg metadata
'
' A muxer may ignore some or all metadata tags. For example if the format 
' doesn't support a field, ffmpeg ignores the tag.

    ffmeta = " -metadata album=""" & fsMetaalbum & _
            """ -metadata artist=""" & fsMetaId & _
            """ -metadata comment="""& "[FFmpeg](https://www.ffmpeg.org)" & _
            """ -metadata genre="""& fsMetagenre & _
            """ -metadata title=""" & fsMetatitle & _
            """ -metadata track=""" & fsMetatrack & _
            """ -metadata year=""" & Year(Now) & """ "

' ###Default muxer settings
' 
    doJob = """" & myConverter & """ -i """ & sWaveName
    doJob = doJob & """ " & ffmeta & " -y """ & sOutName & """"
    Select Case sFileNameExt
    Case ".mp3"
        ' Name temporary file - something like Filename.mp3.mp3
        cout2 = sOutName & ".mp3"
        doJob = """" & myConverter & """ -i """ & sWaveName & _
                """ " & ffmeta & _
                " -y """ & cout2 & """"
        doJob2 ="""" & myConverter & """ -i """ & cout2 & _
                """ -i """ & sImage & _
                """ -map 0:0 -map 1:0 -c copy" & _
                " -id3v2_version 3 -metadata:s:v" & _
                " title=""Album cover""" & _
                " -metadata:s:v comment=""Cover (Front)""" & _
                " -y """  & _
                sOutName & """"
        If sPreProcess="preFlightCheck" Then
            retval = fsMyInputBox(doJob)
            If Len(retVal) = 0 Then
                exit function
            Else
                doJob = retVal
            End If
        End If
        b1 = doExecute(doJob, True)

        ' Add the image
        If Len(sImage) > 0 and fbFileExists(sImage) Then 
            If sPreProcess="preFlightCheck" or sPreProcess="postFlightCheck" Then
                retval = fsMyInputBox(doJob2)
                If Len(retVal) = 0 Then
                    exit function
                Else
                    doJob2 = retVal
                End If
            End If
            b1 = doExecute(doJob2, True)
        End If

        ' If we succeeded, Then delete the temporary file.
        If fbFileExists(sOutName) Then
            fbRemoveFile(cout2)
        End If
    Case ".m4a",".aac",".aif",".aiff",".ogg",".flac"
        If sPreProcess="preFlightCheck" Then
            retval = fsMyInputBox( doJob )
            If Len(retVal) = 0 Then
                exit function
            Else
                doJob = retVal
            End If
        End If
        b1 = doExecute(doJob, True)
    Case ".webm"
        doJob1 ="""" & myConverter & """ -i """ & sImage & """ -i """ & _
                """ -i """ & sWaveName & _
                """ -vcodec libvpx -g 120 -lag-in-frames 16" & _
                " -deadline good -cpu-used 0 -vprofile 0" & _
                " -qmax 63 -qmin 0 -b:v 768k -acodec libvorbis" & _
                " -ab 112k -ar 44100 -f webm -s """ & _
                sDimensions & """ -y """ &  sOutName & """"
        If sPreProcess="preFlightCheck" Then
            retval = fsMyInputBox( doJob1 )
            If Len(retVal) = 0 Then
                exit function
            Else
                doJob1 = retVal
            End If
        End If
        b1 = doExecute(doJob1, True)
    Case ".m4v" 
        ' -strict experimental may produce bad results...
        cout2 = sWaveName & ".webm"
        doJob1 ="""" & myConverter & """ -i """ & sImage & """ -i """ & _
                sWaveName & """ -vcodec libvpx -g 120" & _
                " -lag-in-frames 16 -deadline good" & _
                " -cpu-used 0 -vprofile 0 -qmax 63 -qmin 0" & _
                " -b:v 768k -acodec libvorbis -ab 112k" & _
                " -ar 44100 -f webm -y """ &  cout2 & """ "
        doJob2 = """" & myConverter & """ -i """ & cout2 & _
                """ -acodec aac -ab 160k -vcodec libx264" & _
                " -preset slow -profile:v baseline -level 30" & _
                " -maxrate 10000000 -bufsize 10000000 -f mp4" & _
                " -threads 0 -strict experimental " & ffmeta & _
                " -y """ & sOutName & """ "
        If sPreProcess="preFlightCheck" or "postFlightCheck" Then
            retval = fsMyInputBox( doJob1 )
            If Len(retVal) = 0 Then
                exit function
            Else
                doJob1 = retVal
            End If
        End If
        b1 = doExecute(doJob1, True)
        WScript.Sleep 500
        If sPreProcess="postFlightCheck" Then
            retval = fsMyInputBox( doJob2 )
            If Len(retVal) = 0 Then
                exit function
            Else
                doJob2 = retVal
            End If
        End If
        b1 = doExecute(doJob2, True)
    Case Else
        doJob = """" & myConverter & """ -i """ & sWaveName
        doJob = doJob & """ -y """ & sOutName & """"
        b1 = doExecute(doJob, True)
    End Select
    If fbFileExists(sOutName) Then
        fbRemoveFile sWaveName
        removeMetaFiles
        wav2FFmpeg = True
    End If
End Function


Function AddLanguageCodes(s1, s4)
    '''
    ' On supported Windows systems, adds standard speech XML.
    ' On legacy Windows systems (XP), adds Microsoft markup.
    '''
    Dim s2
    Dim s3

    s1 = Lcase(s1)
    If canUseSpeechXML Then
        ' With Sapi 5.3 and above we use the ISO language code
        s3 = "<?xml version = ""1.0""?>"
        s3 = s3 & " <speak version = ""1.0"" xmlns ="
        s3 = s3 & " ""http://www.w3.org/2001/10/synthesis"""
        s3 = s3 & " xmlns:xsi = ""http://www.w3.org/2001/XMLSchema-instance"""
        s3 = s3 & " xsi:schemaLocation = ""http://www.w3.org/2001/10/synthesis"
        s3 = s3 & " http://www.w3.org/TR/speech-synthesis/synthesis.xsd"""
        s3 = s3 & " xml:lang = """
        s3 = s3 & s1
        s3 = s3 & """> "
        s3 = s3 & s4
        s3 = s3 & "</speak>"
    Else
        ' XP  Sapi 5.1- we look up the Microsoft language code
        Select Case s1
        Case "en"
            s2 = "409"
        Case "en-us","","zxx"
            s2 = "409"
        Case "en-gb","en-vg","en-io","en-gg"
            s2 = "809"
        Case "en-au"
            s2 = "c09"
        Case "en-bz"
            s2 = "2809"
        Case "en-ca"
            s2 = "1009"
        Case "en-bs"
            s2 = "2409"
        Case "en-hk"
            s2 = "3c09"
        Case "en-in"
            s2 = "4009"
        Case "en-id"
            s2 = "3809"
        Case "en-ie"
            s2 = "1809"
        Case "en-jm"
            s2 = "2009"
        Case "en-my"
            s2 = "4409"
        Case "en-nz"
            s2 = "1409"
        Case "en-ph"
            s2 = "3409"
        Case "en-sg"
            s2 = "4809"
        Case "en-za"
            s2 = "1c09"
        Case "en-tt"
            s2 = "2c09"
        Case "en-zw"
            s2 = "3009"
        Case "fr-be"
            s2 = "80c"
        Case "fr-ca"
            s2 = "c0c"
        Case "fr-cg"
            s2 = "240c"
        Case "fr-ch"
            s2 = "100c"
        Case "fr-ci"
            s2 = "300c"
        Case "fr-cm"
            s2 = "2c0c"
        Case "fr-fr","fr"
            s2 = "40c"
        Case "fr-ht"
            s2 = "3c0c"
        Case "fr-lu"
            s2 = "140c"
        Case "fr-ma"
            s2 = "380c"
        Case "fr-mc"
            s2 = "180c"
        Case "fr-ml"
            s2 = "340c"
        Case "fr-re"
            s2 = "200c"
        Case "fr-sn"
            s2 = "280c"
        Case "it","it-it"
            s2 = "410"
        Case "de-at"
            s2 = "c07"
        Case "de-ch"
            s2 = "807"
        Case "de-de","de"
            s2 = "407"
        Case "de-li"
            s2 = "1407"
        Case "de-lu"
            s2 = "1007"
        Case "es-es","es"
            s2 = "c0a"
        Case "es-ar"
            s2 = "2c0a"
        Case "es-bo"
            s2 = "400a"
        Case "es-cl"
            s2 = "340a"
        Case "es-co"
            s2 = "240a"
        Case "es-cr"
            s2 = "140a"
        Case "es-do"
            s2 = "1c0a"
        Case "es-ec"
            s2 = "300a"
        Case "es-sv"
            s2 = "440a"
        Case "es-gt"
            s2 = "100a"
        Case "es-hn"
            s2 = "480a"
        Case "es-mx"
            s2 = "80a"
        Case "es-ni"
            s2 = "4c0a"
        Case "es-pa"
            s2 = "180a"
        Case "es-py"
            s2 = "3c0a"
        Case "es-pe"
            s2 = "280a"
        Case "es-pr"
            s2 = "500a"
        Case "es-us"
            s2 = "540a"
        Case "es-uy"
            s2 = "380a"
        Case "es-ve"
            s2 = "200a"
        Case "ru","ru-ru"
            s2 = "419" 
        Case "hi", "hi-in"
            s2 = "439"
        Case "af","af-za"
            s2 = "436"
        Case "ar-sa","ar"
            s2 = "401"
        Case "ar-dz"
            s2 = "1401"
        Case "ar-bh"
            s2 = "3c01"
        Case "ar-eg"
            s2 = "c01"
        Case "ar-iq"
            s2 = "801"
        Case "ar-jo"
            s2 = "2c01"
        Case "ar-kw"
            s2 = "3401"
        Case "ar-lb"
            s2 = "3001"
        Case "ar-ly"
            s2 = "1001"
        Case "ar-ma"
            s2 = "1801"
        Case "ar-om"
            s2 = "2001"
        Case "ar-qa"
            s2 = "4001"
        Case "ar-sy"
            s2 = "2801"
        Case "ar-tn"
            s2 = "1c01"
        Case "ar-ae"
            s2 = "3801"
        Case "ar-ye"
            s2 = "2401"
        Case "eu","eu-fr","eu-es"
            s2 = "42D"
        Case "bg","bg-bg"
            s2 = "402"
        Case "ca","ca-es"
            s2 = "403"
        Case "cs","cs-cz"
            s2 = "405"
        Case "cy","cy-uk","cy-gb"
            s2 = "452"
        Case "da","da-dk"
            s2 = "406"
        Case "et","et-ee"
            s2 = "425"
        Case "fi","fi-fi"
            s2 = "40b"
        Case "ka","ka-ge"
            s2 = "437"
        Case "hl","hl-gr"
            s2 = "408"
        Case "he","he-il"
            s2 = "40d"
        Case "hr","hr-hr"
            s2 = "41a"  
        Case "hu","hu-hu"
            s2 = "40e"
        Case "is","is-is"
            s2 = "40f"
        Case "ga","ga-ie"
            s2 = "83c"  
        Case "gd","gd-uk","gd-gb"
            s2 = "43c"
        Case "id","id-id"
            s2 = "421"
        Case "ja","ja-jp"
            s2 = "411"
        Case "ko","ko-kp","ko-kr"
            s2 = "412"
        Case "ms","ms-sg","ms-my","ms-id","ms-bn"
            s2 = "43E"
        Case "mo-mn","mo"
            s2 = "850"
        Case "nl","nl-nl"
            s2 = "413"
        Case "nl","nl-be"
            s2 = "813"
        Case "no","no-no","nb","nb-no"
            s2 = "414"
        Case "nn","nn-no"
            s2 = "814"
        Case "pl","pl-pl"
            s2 = "415"
        Case "pt-br"
            s2 = "416"
        Case "pt-pt","pt"
            s2 = "816"
        Case "ro","ro-ro"
            s2 = "418" 
        Case "sk","sk-sk"
            s2 = "41b"
        Case "sl","sl-si"
            s2 = "424"
        Case "sv","sv-se"
            s2 = "41D"
        Case "th","th-th"
            s2 = "41E"
        Case "tl","tl-ph"
            s2 = "464"
        Case "tr","tr-tr"
            s2 = "41f"
        Case "uk","uk-ua"
            s2 = "422"
        Case "vi","vi-vn"
            s2 = "42a"
        Case "zh","zh-cn"
            s2 = "804"
        Case "zh-tw"
            s2 = "404"
        Case "zh-hk"
            s2 = "c04"
        Case "zh-sg"
            s2 = "1004"
        Case "zh-mo"
            s2 = "1404"
        Case Else
            s2 = "9" 'en if XP (5.1) can`t tell language.
        End Select
        s3 = "<speak><lang langid = """
        s3 = s3 & s2
        s3 = s3 & """> "
        s3 =  s3 & s4
        s3 = s3 & " <break strength=""strong"" /></lang></speak>" 
    End If
    AddLanguageCodes = s3
End Function


Sub PopMsgBox(sMsg, sHead, sTitle)
    '''
    ' Pops up a message box that closes after a few seconds
    ' It uses the Read Text logo and shows the information
    ' using standard Internet Explorer advisory style.
    '''
    Dim objFile
    Dim objFSO
    Dim oExec
    Dim outFile
    Dim s1
    Dim tempFolder
    Dim WshEnv
    Dim WshShell

    Set objFSO=CreateObject("Scripting.FileSystemObject")

    Set WshShell = CreateObject("WScript.Shell")
    Set WshEnv = WshShell.Environment("Process")
    tempFolder = WshEnv("TEMP")
    ' write temporary file
    outFile = tempFolder & "\read-text-advisory.hta"
    Set objFile = objFSO.CreateTextFile(outFile,True)
    s1 = "<html><head><script> window.resizeTo(600,180);setTimeout(function(){window.close();}, 5000);</script><HTA:APPLICATION ID=""objReadTextDialog"" APPLICATIONNAME=""" & APP_NAME & " Dialog"" SCROLL=""no"" SINGLEINSTANCE=""yes"" CAPTION=""yes"" SHOWINTASKBAR=""no"" maximizeButton=""no"" minimizeButton=""no""><link rel=""stylesheet"" type=""text/css"" href=""res://ieframe.dll/ErrorPageTemplate.css"" /><meta http-equiv=""Content-Type"" content=""text/html; charset=UTF-8"" /><title>"& sTitle & "</title></head><body onkeydown=""window.close();"" onclick=""window.close();"" ><table width=""500"" cellpadding=""0"" cellspacing=""0"" border=""0""><tr><td id=""infoIconAlign"" width=""60"" align=""left"" valign=""top"" rowspan=""2""><img src=""" & fLogoSrc & """ id=""infoIcon"" alt=""Info icon""></td><td id=""mainTitleAlign"" valign=""middle"" align=""left"" width=""*""><h1 id=""mainTitle"">"& sHead & "</h1>"& sMsg & "</td></tr><tr height = ""60""><td id=""infoIconAlign2"" rowspan=""2""></td><td id=""mainTitleAlign2"" valign=""bottom"" align=""left"" width=""*""></td></tr></table></body></html>"
    objFile.Write s1
    objFile.Close
    ' show message
    Set oExec = WshShell.Exec("mshta.exe " & outFile)
    Do While oExec.Status = 0
        WScript.Sleep 100
    Loop
    fbRemoveFile outFile
End Sub


Function SayIt(s1, sRate, sVoice)
    '''
    ' Says the text aloud as long as the text lasts or
    ' the lock file exists.
    '''
    Dim n
    Dim objFile
    Dim objFSO
    Dim Sapi
    Dim TaskLock

    SayIt = False
    Set objFSO=CreateObject("Scripting.FileSystemObject")
    ' write temporary file
    TaskLock = sLockPath("lock")
    If fbFileExists(TaskLock & ".id") Then
        fbRemoveFile TaskLock & ".id"
    End If
    If fbFileExists(TaskLock) Then
        fbRemoveFile TaskLock
    Else
        Set objFile = objFSO.CreateTextFile(TaskLock, True)
        objFile.Write APP_SIGNATURE
        objFile.Close
        Set Sapi=Wscript.CreateObject("SAPI.SpVoice")
        If Sapi Is Nothing Then
            Usage "FAILED Sapi.SpVoice creation. SAPI ne pouvait pas cr&#233;er une voix."
            Exit Function
        Else
            n=0
            While n<Sapi.GetVoices.Count
                If Instr(Lcase(Sapi.GetVoices.Item(n).GetDescription), _
                        Lcase(sVoice)) > 0 Then
                    Set Sapi.Voice=Sapi.GetVoices.Item(n)
                    n=Sapi.GetVoices.Count
                Else
                    n=n+1
                End If
            WEnd
            Sapi.Rate=int(sRate)
            Sapi.Speak "", 1
            Sapi.Speak s1, 3
            Do
                WScript.Sleep 100
            Loop Until Sapi.WaitUntilDone(1) or _
                    (objFSO.FileExists(TaskLock) = False)
            Set Sapi=Nothing 
        End If
    End If
    fbRemoveFile TaskLock
 SayIt = True
End Function


Function WriteIt(s1, _
        sRate, _
        sVoice, _
        sFileName, _
        sMyWords, _
        sLibre, _
        sImage, _
        sDimensions)
    '''
    ' Writes the spoken text as a wave sound file, or if a
    ' converter like iTunes, ffmpeg or Nero AAC encoder
    ' is available, in a compressed sound format that
    ' includes metadata.
    '''
    Dim bOK
    Dim bTattle
    Dim fs
    Dim n
    Dim Sapi
    Dim sFileNameExt
    Dim sLang
    Dim sLastProcess
    Dim sWavename
    Set fs=CreateObject("Scripting.FileSystemObject")
    Set Sapi=Nothing
    Set Sapi=Wscript.CreateObject("SAPI.SpVoice")
    Do
        WScript.Sleep 100
    Loop Until Sapi.WaitUntilDone(1)
    bOK = false
    sLastProcess = APP_NAME
    If Sapi Is Nothing Then
        Usage "FAILED Sapi.SpVoice creation. SAPI ne pouvait pas faire une voix."
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
            fbRemoveFile sFileName
        End If
        sFileNameExt=strExt(sFileName)
        select case sFileNameExt
        case ".wav"
    sWavename = sFileName
        case else
    sWavename = sFileName & ".wav"
        end select
        Set ss=CreateObject("Sapi.SpFileStream") 
        ss.Format.Type = AUDIO_FORMAT
        ss.Open sWaveName,ForWriting,False 
        Set Sapi.AudioOutputStream=ss 
        Sapi.Speak s1
        Set Sapi=Nothing 
        ss.Close 
        Set ss = Nothing
        sLastProcess = "ffmpeg"
        if sFileNameExt = ".wav" then
            sLastProcess = "Speech API"
        elseif Lcase(sLibre) = "true" then
            select case sFileNameExt
            case ".aif", ".aiff"
                bOK = wav2FFmpeg(sWaveName, sFileName, sImage, sDimensions)
            case ".flac"
                if wav2FFmpeg(sWaveName, sFileName, sImage, sDimensions) = false then
                     sLastProcess = "flac"
                     bOK = wav2Flac(sWaveName, sFileName, sMyWords, sImage)
                end if
            case ".m4a"
                sLastProcess = "M4A encoder"
                if wav2m4a(sWaveName, sFileName, sMyWords, sImage) = false then
                     sLastProcess = "ffmpeg"
                     bOK = wav2FFmpeg(sWaveName, sFileName, sImage, sDimensions)
                end if  
            case ".mp3"
                if wav2FFmpeg(sWaveName, sFileName, sImage, sDimensions) = false then
                     sLastProcess = "lame"
                     bOK = wav2mp3(sWaveName, sFileName, sImage)
                end if
            case ".ogg"
                sLastProcess = "OGG Encoder"
                if wav2Ogg(sWaveName,sFileName, sMyWords) = false then
                     sLastProcess = "ffmpeg"
                     bOK = wav2FFmpeg(sWaveName, sFileName, sImage, sDimensions) 
                end if
            case else
                ' Format was not tested, is experimental or is not normally used
                ' with speech clips.
                 bOK = false
            end select
        else
            ' use iTunes
            sLastProcess = "iTunes"
            bPlay = false
            select case sFileNameExt
            case ".aac", ".aif", ".aiff", ".m4a", ".mp3"
                bOK = wav2iTunes(sWaveName, sFileName, sMyWords, sImage, bPlay)
            case else
                bOK = false
            end select
        end if
    end if
    sLang = GetLocale()
    If fbFileExists(sFileName) then
        bOK = true
        PlaySound "C:\Windows\Media\notify.wav"
        PopMsgBox sFileName, _
                "<b>" & sLastProcess & "</b> : " & fsDone(sLang), _
                APP_NAME
    ElseIf fbFileExists(sWaveName) then
        bOK = true
        PlaySound "C:\Windows\Media\chord.wav"
        PopMsgBox "<i>" & sWaveName & "</i>", _
                "<b>" & sLastProcess & "</b> : " & fsDone(sLang), _
                APP_NAME
    End If
    s3 = sLockPath ("lock")
    fbRemoveFile s3
    fbRemoveFile s3 & ".album"
    fbRemoveFile s3 & ".id"
    fbRemoveFile s3 & ".title"
    bTattle = false
    if len(sImage) > 0 and not(fbIsAppDataFile(sImage, bTattle)) then
        ' Remove the temporary song front cover art image created by Impress.
        For n = 1 to 40
            fbRemoveFile sImage
            If fbFileExists(sImage) Then
                ' File is in use and can't be deleted yet.
                WScript.Sleep 250
            Else
                Exit For
            End If
        Next
    end if
    WriteIt = bOK
End Function


Function fsDone(b)
    '''
    ' b - the language name or decimal LCID of a culture group. Returns the 
    ' word "Done"
    ' http://0xcc.net/jsescape/
    ' http://www.microsoft.com/resources/msdn/goglobal/default.mspx
    ' MSDN lists the LCID Culture identifiers in hexidecimal, but VBA needs 
    ' decimal codes.
    '''
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
        a1 = "&#927;&#955;&#959;&#954;&#955;&#951;&#961;&#974;&#952;&#951;"
        a1 = a1 & "&#954;&#949;"
    Case "en", "3081", "10249", "4105", "9225", "2057", "16393", "6153"
        a1 = "Done"
    Case "8201", "5129", "13321", "7177", "11273", "1033", "12297"
        a1 = "Done"
    Case "es","11274", "16394", "13322", "9226", "5130", "7178", "12298"
        a1 = "Finalizado"
    Case "17418", "4106", "18442", "2058", "19466", "6154", "15370", "10250"
        a1 = "Finalizado"
    Case "20490", "1034", "14346", "8202"
        a1 = "Finalizado"
    Case "fr", "3084", "1036", "2060", "11276","9228","12300","5132","13324"
        a1 = "Termin&#233;"
    Case "6156", "14348", "10252", "4108", "7180"
        a1 = "Termin&#233;"
    Case "et", "1061"
        a1 = "&#76;&#245;&#112;&#101;&#116;&#97;&#115;"
    Case "fi", "1035"
        a1 = "Valmiit"
    Case "ga", "2108"
        a1 = "Cr&#237;ochnaithe"
    Case "hi", "1081"
        a1 = "&#2360;&#2350;&#2366;&#2346;&#2381;&#2340;"
    Case "hu", "1038"
        a1 = "K&#233;sz"
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
        a1 = "Conclu&#237;do"
    Case "ro", "1048"
        a1 = "&#238;&#110;&#99;&#101;&#116;&#97;&#116;"
    Case "ru", "1049", "2073"
        a1 = "&#1047;&#1072;&#1074;&#1077;&#1088;&#1096;&#1077;&#1085;&#1086;"
    Case "sk", "1051"
        a1 = "&#68;&#111;&#107;&#111;&#110;&#269;&#101;&#110;&#233;"
    Case "sl", "1060"
        a1 = "&#75;&#111;&#110;&#269;&#97;&#110;&#111;"
    Case "sv", "2077", "1053"
        a1 = "Slutf&#246;rt"
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
End Function


Function PlaySound(sURL)
    '''
    ' Plays a sound in the background
    ' http://stackoverflow.com/questions/22367004/vbs-play-sound-with-no-dialogue '
    '''
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


Function sLockPath(s1)
    '''
    ' Path to temporary file with extension s1
    '''
    Dim tempFolder
    Dim userid
    Dim WshEnv
    Dim wshShell

    Set WshShell = CreateObject("WScript.Shell")
    Set WshEnv = WshShell.Environment("Process")
    tempFolder = WshEnv("TEMP")
    userid = WshEnv("USERNAME")
    sLockPath = tempFolder & "\" & APP_SIGNATURE & "." & userid & "." & s1
End Function


Function fLogoSrc
    '''
    ' Read Text logo base 64 encoded data
    '''
    fLogoSrc = "data:image/png;base64,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"
End function


Function getTextFileContent (strFileName, strCharSet)
    '''
    ' Open a text file using a particular character set.
    ' Stefan Thelenius "VBScript: Reading text files" Friday, 11 April 2008
    ' Accessed September 11, 2013.
    ' http://abouttesting.blogspot.ca/2008/04/vbscript-reading-text-files.html
    '''
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
    '''
    ' Open text file using defaults
    '''
    readFile=getTextFileContent (s0,"UTF-8")
End Function


Sub main()
    '''
    ' Interpret command line, Then speak or convert a text file to a sound file.
    ' If there are no parameters, tests that Windows Speech API works by reading
    ' a short phrase like the current date and time.
    '''
    Dim bOK
    Dim s0
    Dim s1
    Dim s2
    Dim sVoice
    Dim srate
    Dim sLanguage
    Dim sLibre
    Dim sImage
    Dim sDimensions
    Dim sOutFile

    bOK = false
    On Error Resume Next
    'Decode the named arguments...
    sVoice = WScript.Arguments.Named.Item("voice")
    srate = WScript.Arguments.Named.Item("rate")
    sLanguage = WScript.Arguments.Named.Item("language")
    sLibre = WScript.Arguments.Named.Item("use-optional-app")
    sImage = WScript.Arguments.Named.Item("imagefile")
    sDimensions = WScript.Arguments.Named.Item("dimensions")
    If sDimensions  =  "" Then
        sDimensions  =  "400x400"
    End If
    sOutFile = WScript.Arguments.Named.Item("soundfile")
    If sOutFile = "" Then
        sOutFile = WScript.Arguments.Named.Item("wavefile") 'depreciated
    End If
    s0 = WScript.Arguments.Unnamed.Item(0)
    Select Case s0
        Case "-h","--help","/h","-?"
            Usage "Help"
            WScript.Exit(0)
        Case "" 
            s0 = Year(Date) & "-" & Month(Date) & "-" & Day(Date)
            s0 = s0 & ", " & FormatDateTime(now,4)
            Select Case GetLocale()
                Case "de", "1031", "3079", "5127", "4103", "2055"
                    s1 = "Las ein paar Worte..."
                Case "en-CA", "4105"
                    s1 = "Excuse me... Could you please type some text?"
                Case "es","11274", "16394", "13322", "9226", "5130", "7178", "12298"
                    s1 = "Introduzca algunas palabras ..."
                Case "17418", "4106", "18442", "2058", "19466", "6154", "15370"
                    s1 = "Introduzca algunas palabras ..."
                Case "10250", "20490", "1034", "14346", "8202"
                    s1 = "Introduzca algunas palabras ..."
                Case "fr", "3084", "1036", "2060", "11276","9228","12300","5132"
                    s1 = "Tapez quelques mots..."
                Case "13324", "6156", "14348", "10252", "4108", "7180"
                    s1 = "Tapez quelques mots..."
                Case "pt", "1046", "2072"
                    s1 = "Tipo de poucas palavras..."
                Case Else
                    s1 = "Enter a few words..."
            End Select
            s2=InputBox(s1,"Locale: " & GetLocale(),s0)
        Case Else
            s2=getTextFileContent(s0,"UTF-8")
            If Err <> 0 Then
                Usage Err.Number & " -- " &  Err.Description & " -- " & s0
                Wscript.Exit(0)
            End If
    End Select
    If sLanguage = "" Then
        s1 = s2
    Else 
        s1 = AddLanguageCodes(sLanguage,s2)  
    End If
    If sOutFile = "" Then
        bOK = sayIt(s1, sRate, sVoice)
    Else
        bOK = writeIt(s1, _
                sRate, _
                sVoice, _
                sOutFile, _
                s2, _
                sLibre, _
                sImage, _
                sDimensions)
        If not(bOK) Then
    bOK = sayIt (s1, sRate, sVoice)
        End If
    End If
    If Not(bOK) Then

    End If
End Sub

main
