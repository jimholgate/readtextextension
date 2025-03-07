'''
'' Read text
'' =========
'' 
'' **Read Text** reads text aloud, saves audio files and
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
'' To save space, convert `.wav` files to small `.m4a` or `mp3` files
'' that you can share on most mobile phones, music players and tablets.
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
''	 C:\Windows\SysWOW64\wscript.exe
'' 
'' Command line options (default):
'' 
''	 "(TTS_WSCRIPT_VBS)" "(TMP)"
'' 
'' or (save as a .wav file in the home directory):
'' 
''	 "(TTS_WSCRIPT_VBS)" /soundfile:"(HOME)(NOW).wav" "(TMP)"
'' 
'' or (use a named voice)
'' 
''	 "(TTS_WSCRIPT_VBS)" /voice:"Microsoft Hortense Desktop - French" "(TMP)"
'' 
'' or (read a little slower)
'' 
''	 "(TTS_WSCRIPT_VBS)" /rate:-3 "(TMP)"
'' 
'' or (change voice by language)
'' 
''	 "(TTS_WSCRIPT_VBS)" /language:"(SELECTION_LANGUAGE_COUNTRY_CODE)" "(TMP)"
'' 
'' **Note**: Selecting this option doesn't work with the SAPI
'' speech synthesizer if you haven't installed a voice in the
'' language.
'' 
'' Visual helper programs
'' ======================
''
'' Read Text can use helper programs to save audio files using MP3 and other formats.
'' 
'' ## iTunes
'' 
'' **iTunes** is a visual music manager from Apple available at no cost. This
'' application allows you to convert sound to different formats. Read text
'' can use [iTunes](https://www.apple.com/itunes/) to convert sound files with metadata
'' and album cover art. The first time you use iTunes it can take a moment to start.
'' iTunes creates an audio file in it's own directory and signals you with a sound.
'' Read Text Extension puts a copy in a sound directory in your home directory.
'' 
''	 "(TTS_WSCRIPT_VBS)" /language:"en-US" /soundfile:"(HOME)en\(NOW).aif" "(TMP)"
''	 "(TTS_WSCRIPT_VBS)" /language:"en-US" /soundfile:"(HOME)en\(NOW).m4a" "(TMP)"
''	 "(TTS_WSCRIPT_VBS)" /language:"en-US" /soundfile:"(HOME)en\(NOW).mp3" "(TMP)"
''
'' ## VideoLAN VLC
'' 
'' [VideoLAN VLC](https://videolan.org/vlc) is a free viewer, streamer and converter. 
'' To use VLC, install the desktop application using the installer program default
'' location. The script for VLC compresses audio files quickly, and the resulting
'' file does not include personalized metadata. In some cases, your system security
'' policies will prevent this script from running VLC directly, although you will
'' still be able to compress audio files using the desktop application or a `vlc.exe`
'' command  from the system Command Prompt program.
'' 
''	 "(TTS_WSCRIPT_VBS)" /use-optional-app:"True" /soundfile:"(HOME)en\(NOW).mp3" "(TMP)"
''	 "(TTS_WSCRIPT_VBS)" /use-optional-app:"True" /soundfile:"(HOME)en\(NOW).ogg" "(TMP)"
''
'' Command line programs
'' =====================
''
'' These programs are more challenging to install and use on Windows than visual helper
'' programs. You can install them locally in the Windows user `LOCALAPPDATA` directory,
'' or choose a custom directory by setting the `READTEXTHELPER` environment variable
'' to a directory that you specify.
''
'' ## FFmpeg
'' 
'' [ffmpeg](https://ffmpeg.org/download.html#build-windows) is a free media converter. 
'' If it is correctly installed, you will see these options in the Read Text extension
'' main dialogue.
'' 
''	 "(TTS_WSCRIPT_VBS)" /use-optional-app:"True" /soundfile:"(HOME)en\(NOW).mp3" "(TMP)"
''	 "(TTS_WSCRIPT_VBS)" /use-optional-app:"True" /soundfile:"(HOME)en\(NOW).ogg" "(TMP)"
'' 
'' ## Flac
'' 
'' **[FLAC](https://xiph.org/flac/)** is a free lossless audio codec.
'' 
''  * [Get flac encoder](https://xiph.org/flac/links.html#software)
''  * [Players and plugins](https://xiph.org/flac/)
'' 
''	 "(TTS_WSCRIPT_VBS)" /use-optional-app:"True" /soundfile:"(HOME)en\(NOW).flac" "(TMP)"
'' 
'' ## Lame
''
'' **[LAME](https://lame.sourceforge.io/)** (Lame Ain't an MP3 Encoder)
'' is an open source project that creates MP3 compatible audio files
'' with options to specify compression and psychoacoustic properties.
''
'' > LAME is an educational tool to be used for learning about MP3 encoding.
'' >
'' > -- *[About LAME](https://lame.sourceforge.io/about.php)*. LAME Project. (2020).
'' 
''  * [Get Lame encoder](https://lame.sourceforge.io/links.php#Binaries)
'' 
''	 "(TTS_WSCRIPT_VBS)" /use-optional-app:"True" /soundfile:"(HOME)en\(NOW).mp3" "(TMP)"
'' 
'' ## OggEnc
''
'' **[OGG](https://xiph.org/vorbis/)** is a file format that uses free 
'' audio codecs.
'' 
'' Play ogg encoded sound files with Firefox and browsers based on the Chromium
'' platform, like Chrome and Edge.
'' 
'' Use `oggenc.exe` or `oggenc2.exe` to make an ogg file
'' 
''  * [About oggenc2 encoder](https://www.rarewares.org/ogg.php)
''  * [Players and plugins](https://xiph.org/vorbis/)
'' 
''	 "(TTS_WSCRIPT_VBS)" /use-optional-app:"True" /soundfile:"(HOME)en\(NOW).ogg" "(TMP)"
'' 
'' ----------------------------------------------------------------------------
'' 
'' [Read Text Extension](https://sites.google.com/site/readtextextension/)
'' 
'' Copyright (c) 2011 - 2025 James Holgate
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
	s1 = sA & Chr(10) & _
			Chr(10)& _
			"tts_wscript.vbs [/language:""xxx"" | /voice:""xxx""] [/rate:" & _
			"nn] [/soundfile:""c:\xxx.wav""] [/visible""false""] ""filename.txt""" & Chr(10) & _
			Chr(10) & _
			"/language:""fr"" - Language option" & Chr(10)& _
			"/voice:""Microsoft Hortense Desktop - French""" & _
			Chr(10) & _
			"/rate:-3 - Minimum -10 & Maximum 10" & Chr(10) & _
			"/soundfile:""C:\xxx.wav"" - sound file path" & Chr(10) & _
			"/imagefile:""C:\xxx.[png|jpg]"" - input png or jpg for album" & _
			" cover" & Chr(10) & _
			"/sDimensions = ""400x400"" - suggested album" & _
			" cover size in pixels" & Chr(10) & _
			"/visible = ""false"" - if ""true"" then" & _
			" play media with Windows Media Player" & Chr(10) & _
			"""filename.txt"" Text Document to read (required)"
	MsgBox s1, 0, APP_NAME
End Sub
Function bWriteText(outFile, theString)
	'''
	' Write text to a new file using UTF-8 character coding
	'''
	Dim strm
	Dim objFile
	Set strm = CreateObject("ADODB.Stream")
	With strm
		.Open
		.CharSet = "UTF-8"
		.WriteText theString
		.SaveToFile outFile, 1
		.Close
	End With
	bwriteText = fbFileExists(outFile)
End Function
Function FileSize(sfilespec)
	'''
	' If file size exists, return file size, otherwise `0`
	'''
	Dim fso
	Dim file_size
	file_size = 0
	If fbFileExists(sfilespec) Then
		Set fso = CreateObject("Scripting.FileSystemObject")
		file_size = fso.GetFile(sfilespec).Size
	End If
	FileSize = file_size
End Function
Function EscapeReturnsAndReplaceQuotes(sA)
	'''
	' Use a normal plain text string to generate a 'lyrics' string
	' with smart quotes and no carriage returns.
	'''
	Dim s1
	Dim LQ
	Dim RQ
	LQ = Chr(147)
	RQ = Chr(148)
	EscapeReturnsAndReplaceQuotes = ""
	' Not all audio players can show lyrics longer than 1000 characters.
	If Len(sA) > 1000 Then
		sA = Left(sA, 996) & " ..."
	ElseIf sA = "" Then
		Exit Function
	End If
	s1 = Replace(sA, Chr(13), "\n")  ' escaped CR
	s1 = Replace(s1, " """, " " & LQ)  ' SPACE, left double quote
	s1 = Replace(s1, Chr(10) & """", Chr(10) & "" & LQ)  ' LF, left double quote
	s1 = Replace(s1, Chr(9) & """", Chr(9) & "" & LQ)  ' TAB, left double quote
	s1 = Replace(s1, "(" & """", "(" & LQ)  ' left (, left double quote
	s1 = Replace(s1, "[" & """", "[" & LQ)  ' left [, left double quote
	s1 = Replace(s1, "*" & """", "*" & LQ)  ' *, list symbol from markdown
	s1 = Replace(s1, "_" & """", "_" & LQ)  ' _, emphasis symbol from markdown
	s1 = Replace(s1, """", RQ)  ' all others, right double quote
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
	On Error Resume Next
	If Len(sA) > 0  Then
		Set WshShell = CreateObject("WScript.Shell")
		Set oExec = WshShell.Exec(sA)
		If bWaitTilDone Then
			Do While oExec.Status = 0
				 WScript.Sleep 100
			Loop
		End If
	End If
	If Err.Number <> 0 Then
		MsgBox Err.Description
		doExecute = False
	Else
		doExecute = True
	End If
End Function
Function OpenWithWindowsMedia(sfilespec)
	'''
	' Play a sound file with Windows Media Player. Returns true if successful.
	'''
	OpenWithWindowsMedia = False
	Dim exts
	Dim ok
	Dim x
	Dim oWMP
	If Not fbFileExists(sfilespec) Then
		Exit Function
	End If
	exts = Array("aif", "aifc", "aiff", "au", "avi", "m4a", "mp3", "mpeg", _
	"mpg", "wav", "wma", "wmv")
	For x = Lbound(exts) To Ubound(exts)
		If strExt(sfilespec) = "." & exts(x) Then
			Set oWMP = CreateObject("WMPlayer.OCX")
			With oWMP
				.settings.autoStart = True
				.settings.volume = 70 ' 0 - 100
				.settings.balance = 0 ' -100 to 100
				.enableContextMenu = True
				.openPlayer(sfilespec)
				OpenWithWindowsMedia = True
			End With
			Exit Function
		End If
	Next
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
	fbRemoveFile = Not(fso.FileExists(sfilespec))
End Function
Function fsGetPath(app)
	' Use the system path to select a complete application URI
	' or return `''` if the application is not in the path.
	fsGetPath = ""
	Dim a1
	If Len(app) = 0 Then
		Exit Function
	End If
	a1 = Split(fsGetEnvironResult("PATH"), ";")
	Dim n
	Dim prueba
	For n = Lbound(a1) To Ubound(a1)
		prueba = a1(n) & "\" & app
		If fbFileExists(prueba) Then
			fsGetPath = prueba
			Exit Function
		End If
	Next
	Exit Function
End Function
Function fsXmlInputBox(s1)
	'''
	' Debug or pause execution. Returns string or blank if you click 'Cancel'
	'''
	fsXmlInputBox = ""
	Dim cr
	Dim s0
	Dim source
	Dim sformat
	Dim album
	Dim artist
	Dim genre
	Dim title
	Dim track
	Dim xDoc
	source = sLockPath("lock") & ".xml"
	If fbFileExists(source) Then
		Set xDoc = Nothing
		Set xDoc = CreateObject("Microsoft.XMLDOM")
		xDoc.Load(source)
		For Each MusicInfoElement in xDoc.selectNodes("/audiotrack")
			album = MusicInfoElement.selectSingleNode("album").text
			artist = MusicInfoElement.selectSingleNode("artist").text
			genre = MusicInfoElement.selectSingleNode("genre").text
			title = MusicInfoElement.selectSingleNode("title").text
			track = MusicInfoElement.selectSingleNode("track").text
		Next
		Set xDoc = Nothing
	Else
		album = "_album"
		artist = "_artist"
		genre = "_genre"
		title = "_title"
		track = "1"
		syear = cstr(Year(Now))
	End If
	cr = Chr(10)
	fsXmlInputBox = InputBox(album & cr & artist & cr & cr & track & ". " & title, genre, s1)
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
	cr = Chr(10)
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
		fbFileExists = fso.FileExists(sfilespec)
	End If
End Function
Function fsfixfFfmpegMetaVal(s1)
	fsfixfFfmpegMetaVal = ""
	Dim a1 : a1 = array(_
			"\", _
			"=", _
			";",_
			"#", _
			chr(10), _
			chr(13))
	Dim n
	n = 0
	If len(s1) <> 0 Then
		For n = lbound(a1) to ubound(a1)
			s1 = Replace(s1, a1(n), "\" & a1(n))
		Next
	End If
	fsfixfFfmpegMetaVal = s1
End Function
Function getXmlMeta(sformat, bShowInput)
	' Format a c9hverter's metadata string using an XML data
	' source.
	'
	' + `sformat` - code for the return format i.e.: `ffmpeg`
	' + `bShowInput` - `True` to show an input box, `False` to skip.
	getXmlMeta = ""
	Dim b1
	Dim s1
	Dim s2
	Dim source
	Dim album
	Dim artist
	Dim genre
	Dim title
	Dim track
	Dim syear
	Dim xDoc
	Set xDoc = Nothing
	source = sLockPath("lock") & ".xml"
	If fbFileExists(source) Then
		Set xDoc = CreateObject("Microsoft.XMLDOM")
		xDoc.Load(source)
		For Each MusicInfoElement in xDoc.selectNodes("/audiotrack")
			album = MusicInfoElement.selectSingleNode("album").text
			artist = MusicInfoElement.selectSingleNode("artist").text
			genre = MusicInfoElement.selectSingleNode("genre").text
			title = MusicInfoElement.selectSingleNode("title").text
			track = MusicInfoElement.selectSingleNode("track").text
			syear = MusicInfoElement.selectSingleNode("year").text
		Next
	Set xDoc = Nothing
	Else
		Exit Function
	End If
	'verify title
	Select Case bShowInput
	Case True
		s1 = fsMyInputBox(title)
	Case Else
		s1 = title
	End Select
	if len(s1) <> 0 then 
		Select Case sformat
		Case "ffmpeg.ini", "ToFfmpeg.ini", "ToAvconv.ini"
			album = fsfixfFfmpegMetaVal(album)
			artist = fsfixfFfmpegMetaVal(artist)
			genre = fsfixfFfmpegMetaVal(genre)
			s1 = fsfixfFfmpegMetaVal(s1)
			track = fsfixfFfmpegMetaVal(track)
			syear = fsfixfFfmpegMetaVal(syear)
		Case Else
			album = EscapeReturnsAndReplaceQuotes(album)
			artist = EscapeReturnsAndReplaceQuotes(artist)
			genre = EscapeReturnsAndReplaceQuotes(genre)
			s1 = EscapeReturnsAndReplaceQuotes(s1)
			track = EscapeReturnsAndReplaceQuotes(track)
			syear = EscapeReturnsAndReplaceQuotes(syear)
		End Select
		Select Case sformat
		' Simple strings - iTunes
		Case "album"
			getXmlMeta = album
		Case "artist"
			getXmlMeta = artist
		Case "genre"
			getXmlMeta = genre
		Case "title"
			getXmlMeta = s1
		Case "checkedtitle"
			getXmlMeta = fsMyInputBox(title)
		Case "track"
			getXmlMeta = track
		Case "year"
			getXmlMeta = syear
		' Long strings - ffmpeg etc.
		Case "ffmpeg", "avconv"
			getXmlMeta = Join(Array(" -metadata album=""", album, _
					""" -metadata artist=""", artist, _
					""" -metadata comment=""" & "[FFmpeg](https://www.ffmpeg.org)", _
					""" -metadata genre=""" & genre, _
					""" -metadata title=""", s1, _
					""" -metadata track=""", track, _
					""" -metadata year=""", syear, """ "), _
					"")
		Case "ffmpeg.ini", "ToFfmpeg.ini", "ToAvconv.ini"
			' For writing to a utf-8 encoded text file.
			'
			' Documented at <https://ffmpeg.org>
			'
			' Reinserting edited metadata information from the FFMETADATAFILE file
			' can be done as:
			'
			'	ffmpeg -i INPUT -i FFMETADATAFILE -map_metadata 1 -codec copy OUTPUT
			'
			getXmlMeta = Join(Array(_
					";FFMETADATA1", _
					"album=" & album, _
					"artist=" & artist, _
					"genre=" & genre, _
					"title=" & s1, _
					"track=" & track, _
					"year=" & syear), _
					chr(10))
			s2 = source & sformat
			If fbFileExists(s2) Then
				fbRemoveFile(s2)
			End If
			If Len(album) <> 0 Then
				b1 = bWriteText(s2, getXmlMeta)
			End If
		Case "vorbis", "flac"
			getXmlMeta = Join(Array(_
					" -T ALBUM=""", album, _
					""" -T ARTIST=""", artist, _
					""" -T GENRE=""", genre, _
					""" -T TITLE=""", s1, _
					""" -T TRACKNUMBER=""", track, _
					""" "), "")
		Case "ogg2"
			getXmlMeta = Join(Array(" --album """, album, _
					""" --artist """, artist, _
					""" --genre """, genre, _
					""" --title """, s1, _
					""" --tracknum """, track, _
					""" "), "")
		Case "nero"
			getXmlMeta = Join(Array(" -meta:album=""", album, _
					""" -meta:artist=""", artist, _
					""" -meta:composer=""", artist, _
					""" -meta:comment=""", "[Nero AAC Encoder](https://www.nero.com)", _
					""" -meta:genre=""", genre, _
					""" -meta:title=""", s1, _
					""" -meta:track=""", track, _
					""" -meta:year=""", syear, _
					""" "), "")
		Case "lame"
			getXmlMeta = Join(Array(" --tt """, s1, _
					""" --ta """, artist, _
					""" --tc """, "[Lame.exe](http://www.rarewares.org)", _
					""" --tl """, album, _
					""" --ty """, syear, _
					""" --tn """, track, _
					""" --tg """, genre, _
					""" "), "")
		Case Else
			getXmlMeta = ""
		End Select
	End If
Exit Function
getXmlMetaErr:
getXmlMeta = ""
End Function
Function fsGetEnvironResult(sA)
	'''
	' `fsGetEnvironResult("ProgramFiles(x86)")`
	' `> C:\Program Files(x86)\`
	' Converts an environment variable to a file path followed by
	' a backslash, or `""` if the environment variable was not set. '''
	fsGetEnvironResult = ""
	Dim return_value
	Dim objFSO
	Dim WshEnv
	Dim WshShell
	return_value = ""
	Set objFSO=CreateObject("Scripting.FileSystemObject")
	Set WshShell = CreateObject("WScript.Shell")
	Set WshEnv = WshShell.Environment("Process")
	On Error Resume Next
	If Len(sA) = 0 Then
		Exit Function
	Else
		return_value = WshEnv(sA)
		If Len(return_value) < 2 Then
			return_value = ""
		ElseIf not Right(return_value, 1) = "\" Then
			return_value = return_value & "\"
		End If
	End If
	fsGetEnvironResult = return_value
End Function
Function fsFindAppPath(sA)
	 '''
	' Given an Application subpath in the form
	' `fsFindAppPath("Adobe\Adobe Digital Editions 4.5\DigitalEditions.exe")`
	' `fsFindAppPath("Audacity\Audacity.exe")`
	' `fsFindAppPath("Common Files\microsoft shared\MSInfo\msinfo32.exe")`
	' `fsFindAppPath("ffmpeg\bin\ffmpeg.exe")`
	' `fsFindAppPath("ffmpeg\bin\ffplay.exe")`
	' `fsFindAppPath("Internet Explorer\iexplore.exe")`
	' `fsFindAppPath("lame3\lame.exe")`
	' `fsFindAppPath("LibreOffice\program\soffice.exe")`
	' `fsFindAppPath("Microsoft VS Code\Code.exe")`
	' `fsFindAppPath("Mozilla Firefox\firefox.exe")`
	' `fsFindAppPath("OpenOffice 4\program\soffice.exe")`
	' `fsFindAppPath("Pandoc\pandoc.exe")`
	' `fsFindAppPath("Python\Python310\python.exe")`
	' `fsFindAppPath("xiph\flac.exe")`
	' `fsFindAppPath("rarewares\oggenc.exe")`
	' `fsFindAppPath("rarewares\oggenc2.exe")`
	' `fsFindAppPath("VideoLAN\VLC\vlc.exe")`
	' `fsFindAppPath("Windows Media Player\wmplayer.exe")`
	' `fsFindAppPath("Windows NT\Accessories\wordpad.exe")
	' `fsFindAppPath("Zulu\zulu-17\bin\java.exe")`
	' returns a full path if it is in a normal
	' location, like `C:\Program Files\` or it
	' returns `""` if it is not.
	'''
	Dim a1
	Dim n
	fsFindAppPath = ""
	a1 = Array(_
			fsGetEnvironResult("READTEXTHELPER"), _
			fsGetEnvironResult("LOCALAPPDATA"), _
			fsGetEnvironResult("ProgramFiles"), _
			fsGetEnvironResult("ProgramFiles(x86)"), _
			fsGetEnvironResult("ProgramW6432"), _
			fsGetEnvironResult("HOMEDRIVE") & "opt\", _
			fsGetEnvironResult("SystemRoot"), _
			fsGetEnvironResult("USERPROFILE") & "opt\", _
			fsGetEnvironResult("HOMEDRIVE") & "opt\", _
			fsGetEnvironResult("LOCALAPPDATA") & "Programs\")
	If Len(sA) > 0 Then
		For n = LBound(a1) To UBound(a1)
			If Len(a1(n)) > 1 Then
				If fbFileExists(a1(n) & sA) Then
					fsFindAppPath = a1(n) & sA
					Exit Function
				End If
			End If
		Next
	End If
	fsFindAppPath = fsGetPath(sA)
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
	Dim WshEnv
	Dim WshShell
	fbIsAppDataFile = False
	Set objFSO=CreateObject("Scripting.FileSystemObject")
	Set WshShell = CreateObject("WScript.Shell")
	Set WshEnv = WshShell.Environment("Process")
	a1 = Array(WshEnv("ALLUSERSPROFILE"), _
			WshEnv("APPDATA"), _
			WshEnv("LOCALAPPDATA"), _
			".oxt", _
			WshEnv("ProgramData"), _
			WshEnv("ProgramFiles(x86)"), _
			WshEnv("ProgramFiles"), _
			WshEnv("ProgramW6432"), _
			WshEnv("SystemDrive") & "\opt", _
			WshEnv("SystemRoot"), _
			"uno_packages", _
			WshEnv("USERPROFILE") & "\opt", _
			WshEnv("windir"))
	If Len(sA) > 0 Then
		For n = LBound(a1) To UBound(a1)
			If Len(a1(n)) > 0 Then
				If InStr(sA, a1(n)) > 0 Then
					fbIsAppDataFile = True
					Exit For
				End If
			End If
		Next
	End If
	If fbIsAppDataFile = True And bTattle = True Then
		b1 = InputBox("Restricted path!", APP_NAME, sA)
	End If
End Function
Function canUseSpeechXML
	'''
	' Can the installed version of SAPI use XML?
	'''
	canUseSpeechXML = False
	Dim x
	Dim y
	x = 0
	y = 0
	Set SystemSet = GetObject("winmgmts:").InstancesOf("Win32_OperatingSystem")
	For each System in SystemSet
		a1 = Split(System.Version, ".")
		x = Int(a1(0))
		If Ubound(a1) > 0 Then
			y = 0.1 * Int(a1(1))
		End If
		If x + y > 5.1 Then
			canUseSpeechXML = True
			Exit For
		End If
	Next
End Function
Function lamePath()
	'''
	' Returns path to the lame mp3 converter program.
	'''
	lamePath = ""
	Dim n
	Dim a1
	a1 = Array(_
		"lame3\lame.exe", _
		"lame2\lame.exe", _
		"lame\lame.exe", _
		"Lame For Audacity\lame.exe")
	For n = Lbound(a1) to Ubound(a1)
		If len(fsFindAppPath(a1(n))) > 0 Then
			lamePath = fsFindAppPath(a1(n))
			Exit For
		End If
	Next
End Function
Function oggPath()
	oggPath = ""
	Dim a1
	a1 = Array(_
			"rarewares\oggenc.exe", _
			"rarewares\oggenc2.exe", _
			"xiph\oggenc.exe", _
			"xiph\oggenc2.exe", _
			"oggenc.exe", _
			"oggenc2.exe")
	Dim n
	For n = Lbound(a1) to Ubound(a1)
		If Len(fsFindAppPath(a1(n))) > 0 Then
			oggPath = fsFindAppPath(a1(n))
			Exit For
		End If
	Next
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
	Dim sPath
	wav2ogg = False
	On Error Resume Next
	s1 = oggPath()
	sLyrics = ""
	If fbFileExists(s1) Then
		sPpath = s1
	Else
		Exit Function
	End If
	If Len(sPpath) > 0 Then
		s3 = fsVerifiedMetatitle()
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
		b1 = doExecute(sA, True)
	End If
	If fbFileExists(outfile) Then
		wav2ogg = True
		fbRemoveFile wavfile
	End If
End Function
Function fsVorbisMeta
	'''
	' [Tag specifications](https://www.xiph.org/vorbis/doc/v-comment.html)
	' [About flac converter](https://linux.die.net/man/1/flac)
	' Depending on version of ffmpeg or other player, these tags may be
	' ignored.
	'''
	Dim s3
	s3 = fsVerifiedMetatitle()
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
Function flacPath()
	flacPath = ""
	Dim a1
	a1 = Array(_
			"rarewares\flac.exe", _
			"xiph\flac.exe", _
			"opt\flac.exe", _
			"flac.exe"_ 
			)
	Dim n
	For n = Lbound(a1) to Ubound(a1)
		If Len(fsFindAppPath(a1(n))) > 0 Then
			flacPath = fsFindAppPath(a1(n))
			Exit For
		End If
	Next
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
	s1 = flacPath()
	If fbFileExists(s1) Then
		sPpath = s1
		sPname = s1
	Else
		Exit Function
	End If
	s2 = outfile
	If Len(sImage) > 0 And fbFileExists(sImage) Then
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
	If FileSize(outfile) > 0 Then
		wav2flac = True
		fbRemoveFile wavfile
	End If
End Function
Function neroEncPath()
	neroEncPath = ""
	Dim a1
	a1 = Array(_
			"nero\neroAacEnc.exe", _
			"opt\neroAacEnc.exe", _
			"neroAacEnc.exe"_
			)
	Dim n
	For n = Lbound(a1) to Ubound(a1)
		If Len(fsFindAppPath(a1(n))) > 0 Then
			neroEncPath = fsFindAppPath(a1(n))
			Exit For
		End If
	Next
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
	Dim a1
	s1 = neroEncPath()
	wav2m4a = False
	If fbFileExists(s1) Then
		sPpath = s1
		sPname = s1
	Else
		Exit Function
	End If
	s3 = outFile
	s4 = ""
	If Len(s3) > 0  Then
		sA = sPpath & " -if """ & wavfile & """ -of """ & s3 & """"
		b1 = doExecute(sA, False)
	End If
	b2 = fbTagM4a(s3, sMyWords, sImage)
	If fbFileExists(s3) Then
		wav2m4a = True
		fbRemoveFile wavfile
	End If
End Function
Function neroTagPath()
	neroTagPath = ""
	Dim a1
	a1 = Array(_
			"nero\neroAacTag.exe", _
			"opt\neroAacTag.exe", _
			"neroAacTag.exe"_
			)
	Dim n
	For n = Lbound(a1) to Ubound(a1)
		If Len(fsFindAppPath(a1(n))) > 0 Then
			neroTagPath = fsFindAppPath(a1(n))
			Exit For
		End If
	Next
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
	s1 = neroTagPath()
	s3 = fsVerifiedMetatitle()
	If s3 = "" or s1 = "" Then
		Exit Function
	End If
	If fbFileExists(s1) And fbFileExists(s2) Then
		sMeta = " -meta:album=""" & fsMetaalbum & _
				""" -meta:artist=""" & fsMetaId & _
				""" -meta:composer=""" & fsMetaId & _
				""" -meta:comment=""" & "[Nero AAC Encoder](https://www.nero.com)" & _
				""" -meta:genre=""" & fsMetagenre & _
				""" -meta:title=""" & s3 & _
				""" -meta:track=""" & fsMetatrack & _
				""" -meta:year=""" & Year(Now) & _
				""" "
		If Len(sImage) > 0 And fbFileExists(sImage) Then
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
Function executeVideoLanVLC(in_sound_path, out_sound_path)
	' Create a simple compressed file with the [VideoLAN
	' VLC](https://videolan.org/vlc) Desktop application
	' for Windows.
    executeVideoLanVLC = False
	Dim vlc_app
	vlc_app = fsFindAppPath("VideoLAN\VLC\vlc.exe")
	If len(vlc_app) > 0 Then
		vlc_app = """" & vlc_app & """"
	Else
		Exit Function
	End If
	Dim CR
	CR = Chr(10)
	Dim command_line
	command_line = ""
	Dim command_line2
	command_line2 = ""
	Dim channel_count
	channel_count = "2"
	Dim audio_codec
	audio_codec = ""
	Dim average_bitrate
	average_bitrate = "0"
	Dim sample_rate
	sample_rate = "0"
	Dim mux
	mux = ""
	Dim verbosity
	verbosity = ""
	Dim extension
	extension = LCase(strExt(out_sound_path))
	Dim error_code
	error_code = ""
	Select Case extension
	' 2022-09 - This extension does not support VLC flac export.
	' Install ffmpeg.
	'Case ".flac"
	'	audio_codec = "flac"
	'	average_bitrate = "0"
    '	channel_count = "0"
	'	sample_rate = "0"
	'	mux = "raw"
	Case ".mp2"
		audio_codec = "mp2"
		average_bitrate = "128"
    	channel_count = "1"
		sample_rate = "16000"
		mux = "dummy"
	Case ".mp3"
		audio_codec = "mp3"
		average_bitrate = "128"
		sample_rate = "44100"
		mux = "dummy"
	Case ".ogg", ".oga"
		audio_codec = "vorb"
		average_bitrate = "128"
		sample_rate = "44100"
		mux = "ogg"
	Case ".opus"
		audio_codec = "opus"
		average_bitrate = "96"
		sample_rate = "16000"
		mux = "ogg"
	Case ".wav"
		audio_codec = "s16l"
		average_bitrate = "0"
        	channel_count = "1"
		sample_rate = "16000"
		mux = "wav"
	Case ".webm"
		audio_codec = "vorb"
		average_bitrate = "96"
        	channel_count = "1"
		sample_rate = "16000"
		mux = "mkv"
	Case Else
		executeVideoLanVLC = False 
		Exit Function
	End Select
    Dim comment
    comment = "Convert with VideoLAN VLC?" & _
		CR & _
		"Average Bitrate: " & _
		average_bitrate & _
		CR & _
		"Channel Count: " & _
		channel_count & _
		CR & _
		"Codec: " & _
		audio_codec & _
		CR & _
		"Sample Rate: " & _
		sample_rate
	Select Case mux
	Case "raw", ""
		compression = ""
	Case Else
		compression = join(_
		array(_
		",ab=", _
		average_bitrate, _
		",channels=", _
		channel_count, _
		",samplerate=", _
		sample_rate))
	End Select
	command_line = join(_
	array(_
	"""", _
	in_sound_path, _
	"""", _
	" --intf dummy ", _
	verbosity, _
	"--sout=", _
	"""", _
	"#transcode{vcodec=none,acodec=", _
	audio_codec, _
	compression, _
	"}:std{access=file,mux=", _
	mux, _
	",dst='", _
	out_sound_path, _
	"'}", _
	"""", _
	" vlc://quit"), _
	"")
	On Error Resume Next
	' On slow computers, the speech synthesizer might take a moment to
	' create the `in_sound_path`. On some systems, security settings
	' might prevent running VLC from a script or VLC might fail to
	' initialize on the first run.
	If FileSize(in_sound_path) = 0 Then
		WScript.Sleep 2000
	End If
	error_code = doExecute(_
	vlc_app & _
	" " & _
	command_line, True)
	executeVideoLanVLC = FileSize(out_sound_path) > 0
    If executeVideoLanVLC Then
        fbRemoveFile in_sound_path
	Else
		' The source file does not exist yet. Pause and get consent.
		command_line2 = InputBox(_
        comment, _
		APP_NAME, _
		vlc_app & " " & command_line)
		If InStr(command_line2 & " ", vlc_app) = 1 Then
			error_code = doExecute(command_line2, False)
            fbRemoveFile in_sound_path
		Else
            fbRemoveFile out_sound_path
            fbRemoveFile in_sound_path
		End If
		executeVideoLanVLC = FileSize(out_sound_path) > 0
	End If
	Exit Function
	executeVideoLanVLCErr:
	executeVideoLanVLC = False 
End Function
Function wav2mp3(wavfile, outFile, sImage)
	'''
	' Use [L. A. M. E.](https://www.rarewares.org) - a free
	' command line program to convert a wave sound file to 
	' an MP3 file.
	'''
	Dim s1
	Dim s2
	Dim s3
	Dim sMeta
	Dim sPath
	wav2mp3 = False
	On Error Resume Next
	s1 = lamePath()
	If len(s1) > 0 Then
		sPpath = s1
	Else
		Exit Function
	End If
	s3 = fsVerifiedMetatitle()
	If s3 = "" Then
		sMeta = ""
	Else
		sMeta = " --tt """ & s3 & _
			""" --ta """ & fsMetaId & _
			""" --tc """ & "[lame.exe](https://www.rarewares.org)" & _
			""" --tl """ & fsMetaalbum & _
			""" --ty """ & Year(Now) & _
			""" --tn """ & fsMetatrack & _
			""" --tg """ & fsMetagenre & _
			""" "
	End If
	If Len(sImage) > 0 And fbFileExists(sImage) Then
		Select Case LCase(strExt(sImage))
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
	a1 = Split(".album,.genre,.id,.title,.track", ",")
	For n = LBound(a1) To UBound(a1)
		fbRemoveFile s1 & a1(n)
	Next
End Sub
Function wav2iTunes(wavfile,sOut2file,sMyWords,sImage, bPlay)
	'''
	' iTunes makes a mp3, aac or m4a in the iTunes Music Library
	' if Length of sOutFile is not zero, Then saves to sOutFile Path
	' [iTunes Interface Reference][1]
	' [1]: (https://www.joshkunz.com/iTunesControl/interfaceIiTunes.html)
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
	Set iTunesApp = WScript.CreateObject("iTunes.Application.1")
	vers = iTunesApp.Version
	Set encoderCollection = iTunesApp.Encoders
	oldEncoder = iTunesApp.CurrentEncoder
	myExt = strExt(sOut2file)
	Select Case myExt
		Case ".mp3"
			Set encoder = encoderCollection.ItemByName("MP3 Encoder")
		Case ".aif",".aiff"
			Set encoder = encoderCollection.ItemByName("AIFF Encoder")
		Case Else ' ".m4a",".aac", ""
			Set encoder = encoderCollection.ItemByName("AAC Encoder")
	End Select
	iTunesApp.CurrentEncoder = encoder
	Set fso = CreateObject("Scripting.FileSystemObject")
	Set opStatus = iTunesApp.ConvertFile(wavfile)
	While opStatus.InProgress
		WScript.Sleep 1000
	Wend
	WScript.Sleep 1000 'Make sure itunes is done
	iTunesApp.CurrentEncoder=oldEncoder
	s3 = fsVerifiedMetatitle
	If Len(s3) > 0 Then
	   ' Add metadata
	   Set track = opStatus.Tracks.Item(1)
	   track.Album = fsMetaalbum()
	   track.Artist = fsMetaId()
	   track.Composer = fsMetaId()
	   track.Genre = fsMetagenre()
	   track.Lyrics = sMyWords
	   track.Name = s3
	   track.TrackNumber = fsMetatrack()
	   track.Year = Year(Now)
	   If Len(sImage) > 0 And fbFileExists(sImage) Then
		   track.AddArtworkFromFile(sImage)
	   End If
	End If
	Set outfile=fso.GetFile(track.Location)
	If Len(sOut2file) > 0 Then
		outfile.copy(sOut2file)
	End If
	If bplay Then
		track.Play()
	End If
	If Err <> 0 And Err <> 13 Then
		Usage "Did not find a supported iTunes version" & Chr(10) & vers & Chr(10) & Err.Description
		Wscript.Exit(0)
	Else
		If fbFileExists(outfile) Then
			wav2iTunes = True
			fbRemoveFile wavfile
		End If
	End If
End Function
Function compressWaveAudioWithFfmpeg(sWaveName, sOutName, sImage, sDimensions)
	'''
	''
	'' compressWaveAudioWithFfmpeg
	'' ===========================
	''
	'' Converts wav format sound to compressed format optionally
	'' including a picture if supported by the ffmpeg muxer.
	'' returns True if it creates a file; otherwise returns False.
	''
	''	 sWaveName - the wave sound to convert `input.wav`
	''	 sOutName - the converted file' `output.mp3`
	''	 sImage - a png file to use as a poster `input.png`
	''	   value is ignored for muxers and codecs that don't support it.
	''	 sDimensions - suggested dimensions for video output `400x400`
	''	   value is ignored for audio
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
	cr= Chr(10)
	compressWaveAudioWithFfmpeg = False 'default when exiting Function before creating a file
	doJob = ""
	doJob1 = ""
	doJob2 = ""
	ffMeta = ""
	If Len(sDimensions) = 0 Then
		sDimensions = "400x400"
	End If
	sFileNameExt = strExt(sOutName)' ### Where's ffmpeg?
	myConverter = fsFindAppPath("ffmpeg\bin\ffmpeg.exe")
	If Len(myConverter) = 0 Then
		Exit Function
	End If
	' ### Which codecs can skip the preflight check?
	Select Case sFileNameExt
		Case ".m4a"
			sPreProcess = ""
			sPostProcess = ""
			If len(neroEncPath()) > 0 Then
			 '[Nero](https://www.nero.com/) m4a encoder produces standards
			 ' compliant m4a output.
				 Exit Function
			End If
		Case ".mp3"
			sPreProcess = ""
			sPostProcess = ""
			If Len(lamePath()) > 0 Then
				' You appear to prefer the lame encoder.
				Exit Function
			End If
		Case ".aif", ".aiff"
			' Lossless audio interchange format
			sPreProcess = ""
			sPostProcess = ""
		Case ".flac"
			' Lossless audio format
			' flac is compressed, but requires a player or plugin
			sPreProcess = ""
			sPostProcess = ""
			If len(flacPath()) > 0 Then
				' You appear to prefer the flac conversion utility.
				Exit Function
			End If
		Case ".ogg"
			sPreProcess = ""
			sPostProcess = ""
			If Len(oggPath()) > 0 Then
				' You appear to prefer the oggenc2 conversion utility.
				Exit Function
			End If
		Case ".webm"
			' Webm - Web video media file for Chromium, Google Chrome and Firefox.
			sPreProcess = ""
			sPostProcess = ""
		Case ".m4v", ".mp4"
			' Video media format file
			sPreProcess = "preFlightCheck"
			sPostProcess = ""
		Case Else ' ".aac"
			Exit Function
	End Select
	' ###Ffmpeg metadata
'
' A muxer may ignore some or all metadata tags. For example if the format
' doesn't support a field, ffmpeg ignores the tag.
ffmeta = Join(Array(" -metadata album=""", fsMetaalbum, _
			""" -metadata artist=""", fsMetaId, _
			""" -metadata comment=""", "[FFmpeg](https://www.ffmpeg.org)", _
			""" -metadata genre=""", fsMetagenre, _
			""" -metadata title=""", fsMetatitle, _
			""" -metadata track=""", fsMetatrack, _
			""" -metadata year=""", Year(Now), """ "), "")' ### Default muxer settings
'
	doJob = Join(Array("""", myConverter, """ -i """, sWaveName, """ ", _
	ffmeta, " -y """, sOutName, """"), "")
	Select Case sFileNameExt
	Case ".mp3"
		' Name temporary file - something like Filename.mp3.mp3
		cout2 = Join(Array(sOutName, ".mp3"), "")
		doJob = Join(Array("""", myConverter, """ -i """, sWaveName, """ ", _
		ffmeta, " -y """, cout2, """"), "")
		doJob2 = Join(Array("""", myConverter, """ -i """, cout2, """ -i """, _
		sImage, """ -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v", _
		" title=""Album cover"" -metadata:s:v comment=""Cover (Front)""", _
		" -y """, sOutName, """"), "")
		If sPreProcess = "preFlightCheck" Then
			retval = fsMyInputBox(doJob)
			If Len(retVal) = 0 Then
				Exit Function
			Else
				doJob = retVal
			End If
		End If
		b1 = doExecute(doJob, True)		' Add the image
		If Len(sImage) > 0 And fbFileExists(sImage) Then
			If sPreProcess = "preFlightCheck" Or sPreProcess = "postFlightCheck" Then
				retval = fsMyInputBox(doJob2)
				If Len(retVal) = 0 Then
					Exit Function
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
	Case ".m4a", ".aac", ".aif", ".aiff", ".ogg", ".flac"
		If sPreProcess = "preFlightCheck" Then
			retval = fsMyInputBox(doJob)
			If Len(retVal) = 0 Then
				Exit Function
			Else
				doJob = retVal
			End If
		End If
		b1 = doExecute(doJob, True)
	Case ".webm"
		doJob1 = Join(Array("""", myConverter, """ -i """, sImage, _
		""" -i """, sWaveName, """ -vcodec libvpx -g 120 -lag-in-frames 16", _
		" -deadline good -cpu-used 0 -vprofile 0 -qmax 63 -qmin 0 ", _
		"-b:v 768k -acodec libvorbis -ab 112k -ar 44100 -f webm -s """, _
		sDimensions, """ -y """,  sOutName, """"), "")
		If sPreProcess = "preFlightCheck" Then
			retval = fsMyInputBox(doJob1)
			If Len(retVal) = 0 Then
				Exit Function
			Else
				doJob1 = retVal
			End If
		End If
		b1 = doExecute(doJob1, True)
	Case ".m4v"
		' 2023-12 : Can view with VideoLAN VLC; WebM recommended
		' because the format is strictly defined.
		doJob1 = Join(Array("""", myConverter, """ -loop 1 -i """, sImage, _
		""" -i """, sWaveName, _
		""" -ac 2 -c:v libx264 -r 25 -c:a aac -shortest -y """, cout2, _
		""""), "")
		b1 = doExecute(doJob1, True)
	Case Else
		doJob = Join(Array("""", myConverter, """ -i """, sWaveName, _
		""" -y """, sOutName, """"), "")
		b1 = doExecute(doJob, True)
	End Select
	If FileSize(sOutName) > 0 Then
		fbRemoveFile sWaveName
		removeMetaFiles()
		compressWaveAudioWithFfmpeg = True
	End If
End Function
Function AddLanguageCodes(s1, s4)
	'''
	' On supported Windows systems, adds standard speech XML.
	' On legacy Windows systems (XP), adds Microsoft markup.
	'''
	Dim s2
	Dim s3
	s4 = Replace(_
		Replace(_
			s4, ">", "&#62;"), "<", "&#60;")
	s1 = LCase(s1)
	If canUseSpeechXML Then
		' With Sapi 5.3 and above we use the ISO language code
		s3 = Join(Array(_
		"<?xml version = ""1.0""?>", _
		" <speak version = ""1.0"" xmlns =", _
		" ""http://www.w3.org/2001/10/synthesis""", _
		" xmlns:xsi = ""http://www.w3.org/2001/XMLSchema-instance""", _
		" xsi:schemaLocation = ""http://www.w3.org/2001/10/synthesis", _
		" http://www.w3.org/TR/speech-synthesis/synthesis.xsd""", _
		" xml:lang = """, _
		fsWindowsCloseMatchLanguage(s1), _
		"""> ", _
		s4, _
		" </speak>"), "")
	Else
		' XP  Sapi 5.1- we look up the Microsoft language code
		s2 = fsIsoToHumanReadable(s1, 3)
		If s2 = "1000" Then s2 = "409"  ' Use en-US if undefined language
		s3 = Join(Array(_
		"<speak><lang langid = """, _
		s2, _
		"""> ", _
		s4, _
		"<break strength=""strong"" /></lang></speak>"), "")
	End If
	AddLanguageCodes = s3
End Function
Function sTempDir()
	sTempDir = ""
	Dim WshShell
	Dim WshEnv
	Set WshShell = CreateObject("WScript.Shell")
	Set WshEnv = WshShell.Environment("Process")
	If bValidEnvironVar("READTEXTTEMP") Then
		sTempDir= WshEnv("READTEXTTEMP")
	Else
		sTempDir = WshEnv("TEMP")
	End If
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
	Dim WshShell
	Set objFSO = CreateObject("Scripting.FileSystemObject")
	' write temporary file
	outFile = sTempDir() & "\read-text-advisory.hta"
	Set objFile = objFSO.CreateTextFile(outFile,True)
	s1 = "<html><head><script> window.resizeTo(600,180);setTimeout(function(){window.close();}, 5000);</script><HTA:APPLICATION ID=""objReadTextDialog"" APPLICATIONNAME=""" & APP_NAME & " Dialog"" SCROLL=""no"" SINGLEINSTANCE=""yes"" CAPTION=""yes"" SHOWINTASKBAR=""no"" maximizeButton=""no"" minimizeButton=""no""><link rel=""stylesheet"" type=""text/css"" href=""res://ieframe.dll/ErrorPageTemplate.css"" /><meta http-equiv=""Content-Type"" content=""text/html; charset=UTF-8"" /><title>" & sTitle & "</title></head><body onkeydown=""window.close();"" onclick=""window.close();"" ><table width=""500"" cellpadding=""0"" cellspacing=""0"" border=""0""><tr><td id=""infoIconAlign"" width=""60"" align=""left"" valign=""top"" rowspan=""2""><img src=""" & fLogoSrc & """ id=""infoIcon"" alt=""Info icon""></td><td id=""mainTitleAlign"" valign=""middle"" align=""left"" width=""*""><h1 id=""mainTitle"">" & sHead & "</h1>" & sMsg & "</td></tr><tr height = ""60""><td id=""infoIconAlign2"" rowspan=""2""></td><td id=""mainTitleAlign2"" valign=""bottom"" align=""left"" width=""*""></td></tr></table></body></html>"
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
	Set objFSO = CreateObject("Scripting.FileSystemObject")
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
		Set Sapi = Wscript.CreateObject("SAPI.SpVoice")
		If Sapi Is Nothing Then
			Usage "FAILED Sapi.SpVoice creation. SAPI ne pouvait pas cr&#233;er une voix."
			Exit Function
		Else
			For n = 0 To Sapi.GetVoices.Count - 1
				If InStr(LCase(Sapi.GetVoices.Item(n).GetDescription), LCase(sVoice)) <> 0 Then
					Set Sapi.Voice = Sapi.GetVoices.Item(n)
					Exit For
				End If
			Next
			Sapi.Rate=Int(sRate)
			REM " The Windows `WinSVSFlagsAsync` Flag tells the Speech"
			REM " Application Program Interface (SAPI) to return control"
			REM " immediately. This allows the program to toggle the"
			REM " Windows SAPI voices off immediately."
			REM ""
			REM "`1` is `WinSVSFlagsAsync`"
			Sapi.Speak "", 1
			REM "`3` is `WinSVSFlagsAsync + WinSVSFPurgeBeforeSpeak`"
			Sapi.Speak s1, 3
			Do
				WScript.Sleep 100
			Loop Until Sapi.WaitUntilDone(1) Or _
					(objFSO.FileExists(TaskLock) = False)
			Set Sapi = Nothing
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
		sDimensions, _
		sVisible)
	'''
	' Writes the spoken text as a wave sound file, or if a
	' converter like iTunes, ffmpeg or [avconv](https://libav.org/avconv.html)
	' encoder is available, in a compressed sound format that
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
    Dim Cruft
	Dim CruftTest
	Dim CruftLen
	Set fs = CreateObject("Scripting.FileSystemObject")
	Set Sapi = Nothing
	Set Sapi = Wscript.CreateObject("SAPI.SpVoice")
	Do
		WScript.Sleep 100
	Loop Until Sapi.WaitUntilDone(1)
	bOK = False
	sLastProcess = APP_NAME
	If Sapi Is Nothing Then
		Usage "FAILED Sapi.SpVoice creation. SAPI ne pouvait pas faire une voix."
	Else
		n=0
		While n<Sapi.GetVoices.Count
			If InStr(LCase(Sapi.GetVoices.Item(n).GetDescription),LCase(sVoice)) > 0 Then
				Set Sapi.Voice = Sapi.GetVoices.Item(n)
				n=Sapi.GetVoices.Count
			Else
				n=n+1
			End If
		Wend
		Sapi.Rate=Int(sRate)
		If fbFileExists(sFileName) Then
			fbRemoveFile sFileName
		End If
		sFileNameExt=strExt(sFileName)
		Select Case sFileNameExt
		Case ".wav"
			sWavename = sFileName
		Case Else
			sWavename = sFileName & ".wav"
		End Select
		Set ss=CreateObject("Sapi.SpFileStream")
		ss.Format.Type = AUDIO_FORMAT
		ss.Open sWaveName,ForWriting,False
		Set Sapi.AudioOutputStream = ss
		Sapi.Speak s1
		Set Sapi = Nothing
		ss.Close
		Set ss = Nothing
		sLastProcess = "ffmpeg"
		If sFileNameExt = ".wav" Then
			sLastProcess = "Speech API"
		ElseIf LCase(sLibre) = "true" Then
			Select Case sFileNameExt
			Case ".aif", ".aiff"
				bOK = compressWaveAudioWithFfmpeg(sWaveName, sFileName, sImage, sDimensions)
			Case ".flac"
				If compressWaveAudioWithFfmpeg(sWaveName, sFileName, sImage, sDimensions) = False Then
					 sLastProcess = "flac"
					 bOK = wav2Flac(sWaveName, sFileName, sMyWords, sImage)
				End If
			Case ".m4a"
				sLastProcess = "M4A encoder"
				If wav2m4a(sWaveName, sFileName, sMyWords, sImage) = False Then
					 sLastProcess = "ffmpeg"
					 bOK = compressWaveAudioWithFfmpeg(sWaveName, sFileName, sImage, sDimensions)
				End If
			Case ".mp3"
				If compressWaveAudioWithFfmpeg(sWaveName, sFileName, sImage, sDimensions) = False Then
					If Len(lamePath()) > 0 Then
					 	sLastProcess = "lame"
					End If
					 bOK = wav2mp3(sWaveName, sFileName, sImage)
				End If
			Case ".ogg"
				sLastProcess = "OGG Encoder"
				If wav2Ogg(sWaveName,sFileName, sMyWords) = False Then
					 sLastProcess = "ffmpeg"
					 bOK = compressWaveAudioWithFfmpeg(sWaveName, sFileName, sImage, sDimensions)
				End If
			Case Else
				' Format was not tested, is experimental or is not normally used
				' with speech clips.
				 bOK = False
			End Select
			If Not bOK Then
				' Use [VideoLAN VLC](https://videolan.org/vlc) video player
				' in "dummy" (non-interactive) mode to create a compressed
				' audio file with no metadata.
				If Len(fsFindAppPath("VideoLAN\VLC\vlc.exe")) > 0 Then
					sLastProcess = "VideoLAN VLC"
					bOK = executeVideoLanVLC(sWaveName, sFileName)
				End If
			End If
		Else
			' use iTunes
			sLastProcess = "iTunes"
			bPlay = False
			Select Case sFileNameExt
			Case ".aac", ".aif", ".aiff", ".m4a", ".mp3"
				bOK = wav2iTunes(sWaveName, sFileName, sMyWords, sImage, bPlay)
			Case Else
				bOK = False
			End Select
		End If
	End If
	sLang = fsIsoToHumanReadable(fsDec2Hex(Int(GetLocale())), 0)
	If fbFileExists(sFileName) Then
		If sVisible = "" or LCase(sVisible) = "false" Then
			bOK = True
			PlaySound "C:\Windows\Media\notify.wav"
			PopMsgBox sFileName, _
			"<b>" & sLastProcess & "</b> : " & fsDone(sLang), _
			APP_NAME
		ElseIf Not sLastProcess = "iTunes" Then
			If Not OpenWithWindowsMedia(sFileName) Then
				OpenWithWindowsMedia(sWaveName)
			End If
		End If
	ElseIf fbFileExists(sWaveName) Then
		bOK = True
		if sVisible = "" or LCase(sVisible) = "false" Then
			PlaySound "C:\Windows\Media\chord.wav"
			PopMsgBox "<i>" & sWaveName & "</i>", _
			"<b>" & sLastProcess & "</b> : " & fsDone(sLang), _
			APP_NAME
		Else
			OpenWithWindowsMedia(sWaveName)
		End If
	End If
	s3 = sLockPath("lock")
	fbRemoveFile s3
	fbRemoveFile s3 & ".album"
	fbRemoveFile s3 & ".id"
	fbRemoveFile s3 & ".title"
    Cruft = Split(sFileName, ".")(0)
	CruftLen = 20
	' Remove unwanted system generated files (a. k. a. "Cruft")
    For n = 1 to CruftLen
		CruftTest = Left(Cruft, Len(Cruft) - n)
		If Right(CruftTest, 1) = "\" Then
			Exit For
		End If
        fbRemoveFile CruftTest
    Next
	bTattle = False
	If Len(sImage) > 0 And Not(fbIsAppDataFile(sImage, bTattle)) Then
		' Remove the temporary song front cover art image created by Impress.
		For n = 1 To 40
			fbRemoveFile sImage
			If fbFileExists(sImage) Then
				' File is in use and can't be deleted yet.
				WScript.Sleep 250
			Else
				Exit For
			End If
		Next
	End If
	WriteIt = bOK
End Function
Function fsDone(b)
	'''
	' b - the language name of a culture group. Returns the
	' word "Done"
	'''
	Select Case Left(b, 2)
	Case "af"
		a1 = "Klaar"
	Case "bg"
		a1 = "&#1043;&#1086;&#1090;&#1086;&#1074;&#1086;"
	Case "ca"
		a1 = "Finalitzada"
	Case "cs"
		a1 = "&#68;&#111;&#107;&#111;&#110;&#269;&#101;&#110;&#111;"
	Case "da"
		a1 = "&#102;&#230;&#114;&#100;&#105;&#103;"
	Case "de"
		a1 = "Beendet"
	Case "el"
		a1 = "&#927;&#955;&#959;&#954;&#955;&#951;&#961;&#974;&#952;&#951;"
		a1 = a1 & "&#954;&#949;"
	Case "en"
		a1 = "Done"
	Case "es"
		a1 = "Finalizado"
	Case "fr"
		a1 = "Termin&#233;"
	Case "et"
		a1 = "&#76;&#245;&#112;&#101;&#116;&#97;&#115;"
	Case "fi"
		a1 = "Valmiit"
	Case "ga"
		a1 = "Cr&#237;ochnaithe"
	Case "hi"
		a1 = "&#2360;&#2350;&#2366;&#2346;&#2381;&#2340;"
	Case "hu"
		a1 = "K&#233;sz"
	Case "id"
		a1 = "Selesai"
	Case "is"
		a1 = "&#108;&#111;&#107;&#105;&#240;"
	Case "it"
		a1 = "Terminato"
	Case "ja"
		a1 = "&#23436;&#25104;"
	Case "ko"
		a1 = "&#50756;&#47308;"
	Case "lv"
		a1 = "Pabeigts"
	Case "lt"
		a1 = "Baigta"
	Case "mt"
		a1 = "Lest"
	Case "nl"
		a1 = "Voltooid"
	Case "pl"
		a1 = "Zakonczono"
	Case "pt"
		a1 = "Conclu&#237;do"
	Case "ro"
		a1 = "&#238;&#110;&#99;&#101;&#116;&#97;&#116;"
	Case "ru"
		a1 = "&#1047;&#1072;&#1074;&#1077;&#1088;&#1096;&#1077;&#1085;&#1086;"
	Case "sk"
		a1 = "&#68;&#111;&#107;&#111;&#110;&#269;&#101;&#110;&#233;"
	Case "sl"
		a1 = "&#75;&#111;&#110;&#269;&#97;&#110;&#111;"
	Case "sv"
		a1 = "Slutf&#246;rt"
	Case "sr"
		a1 = "&#1047;&#1072;&#1074;&#1088;&#1096;&#1077;&#1085;&#1086;"
	Case "tl"
		a1 = "Tapos"
	Case "tr"
		a1 = "Bitirdi"
	Case "uk"
		a1 = "&#x0413;&#x043E;&#x0442;&#x043E;&#x0432;&#x43e;"
	Case "zh"
		If InStr(b1, "TW") > 0 Then
			a1 = "&#2360;&#2350;&#2366;&#2346;&#2381;&#2340;"
		Else
			a1 = "&#2360;&#2350;&#2366;&#2346;&#2381;&#2340;"
		End If
	Case Else '"en" English (default)
		a1 = "Done"
	End Select
	fsDone = a1
End Function
Function PlaySound(sURL)
	'''
	' Plays a sound in the background
	' https://stackoverflow.com/questions/22367004/vbs-play-sound-with-no-dialogue '
	'''
	Dim b1
	Dim o1
	If fbFileExists(sURL) Then
		b1 = True
		Set o1 = CreateObject("WMPlayer.OCX")
		o1.URL = sURL
		o1.controls.play
		While o1.playState <> 1
			WScript.Sleep 100
		Wend
		o1.close
	Else
		b1 = False
	End If
	PlaySound = b1
End Function
Function sLockPath(s1)
	'''
	' Path to temporary file with extension s1
	'''
	Dim WshEnv
	Dim WshShell
	Set WshShell = CreateObject("WScript.Shell")
	Set WshEnv = WshShell.Environment("Process")
	Dim userid
	userid = WshEnv("USERNAME")
	sLockPath = sTempDir() & "\" & APP_SIGNATURE & "." & userid & "." & s1
End Function
Function bValidEnvironVar(sA)
	'''
	' Is an optional system environment variable like `READTEXTTEMP` valid?
	'''
	Dim s1
	Dim userid
	Dim WshEnv
	Dim wshShell
	Set WshShell = CreateObject("WScript.Shell")
	Set WshEnv = WshShell.Environment("Process")
	s1= WshEnv(sA)
	If len(s1) = 0 Then
		bValidEnvironVar = False
	Else
		bValidEnvironVar = True
	End If
End Function
Function fLogoSrc
	'''
	' Read Text logo base 64 encoded data
	'''
	fLogoSrc = "data:image/png;base64,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"
End Function
Function getTextFileContent(strFileName, strCharSet)
	'''
	' Open a text file using a particular character set.
	' Stefan Thelenius "VBScript: Reading text files" Friday, 11 April 2008
	' Accessed September 11, 2013.
	' https://abouttesting.blogspot.com/2008/04/vbscript-reading-text-files.html
	'''
	Const adTypeBinary = 1 'not used
	Const adTypeText = 2
	'Set default CharSet
	If strCharSet = "" Then strCharSet = "ASCII"
	' *** CharSets ***
	'	Windows-1252
	'	Windows-1257
	'	UTF-16
	'	UTF-8
	'	UTF-7
	'	ASCII
	'	X-ANSI
	'   iso-8859-2
	Set objStreamFile = CreateObject("Adodb.Stream")
	With objStreamFile
		.CharSet = strCharSet
		.Type = adTypeText
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
	readFile=getTextFileContent(s0, "UTF-8")
End Function
Function fsIsoToHumanReadable(sA, iForceEnglish)
	'''
	' Returns name of language, if known
	'''
	Dim a1
	a1 = Array("409", "English (United States)", "en-US")
	Select Case LCase(sA)
	Case "en-us", "english (united states)", "409"
		a1 = Array("409", "English (United States)", "en-US")
	Case "en-gb", "english (great britain)", "809"
		a1 = Array("809", "English (Great Britain)", "en-GB")
	Case "en-vg", "english (british virgin islands)"
		a1 = Array("809", "English (British Virgin Islands)", "en-VG")
	Case "en-io"
		a1 = Array("809", "English (Great Britain)", "en-IO")
	Case "en-gg", "english (guernsey)"
		a1 = Array("809", "English (Guernsey)", "en-GG")
	Case "en-au", "english (australia)", "c09"
		a1 = Array("c09", "English (Australia)", "en-AU")
	Case "en-bz", "english (belize)", "2809"
		a1 = Array("2809", "English (Belize)", "en-BZ")
	Case "en-ca", "english (canada)", "1009"
		a1 = Array("1009", "English (Canada)", "en-CA")
	Case "en-bs", "english (bahamas)", "2409"
		a1 = Array("2409", "English (Bahamas)", "en-BS")
	Case "en-hk", "english (hong kong)", "3c09"
	   	a1 = Array("3c09", "English (Hong Kong)", "en-HK")
	Case "en-in", "english (india)", "4009"
		a1 = Array("4009", "English (India)", "en-IN")
	Case "en-id", "english (indonesia)", "3809"
		a1 = Array("3809", "English (Indonesia)", "en-ID")
	Case "en-ie", "english (ireland)", "1809"
		a1 = Array("1809", "English (Ireland)", "en-IE")
	Case "en-jm", "english (jamaica)", "2009"
		a1 = Array("2009", "English (Jamaica)", "en-JM")
	Case "en-my", "english (malaysia)", "4409"
		a1 = Array("4409", "English (Malaysia)", "en-MY")
	Case "en-nz", "english (new zealand)", "1409"
		a1 = Array("1409", "English (New Zealand)", "en-NZ")
	Case "en-ph", "english (philippines)", "3409"
		a1 = Array("3409", "English (Philippines)", "en-PH")
	Case "en-sg", "english (singapore)", "4809"
		a1 = Array("4809", "English (Singapore)", "en-SG")
	Case "en-za", "english (south africa)", "1c09"
		a1 = Array("1c09", "English (South Africa)", "en-ZA")
	Case "en-tt", "english (trinidad ", "english (trinidad)", "2c09"
		a1 = Array("2c09", "English (Trinidad ", "en-TT") ' sic
	Case "en-zw", "english (zimbabwe)", "3009"
		a1 = Array("3009", "English (Zimbabwe)", "en-ZW")
	Case "en", "english", "409"
		a1 = Array("409", "English", "en")
	Case "fr-be", "french (belgium)", "80c"
		a1 = Array("80c", "French (Belgium)", "fr-BE")
	Case "fr-ca", "french (canada)", "c0c"
		a1 = Array("c0c", "French (Canada)", "fr-CA")
	Case "fr-cg", "french (congo)", "240c"
		a1 = Array("240c", "French (Congo)", "fr-CG")
	Case "fr-ch", "french (switzerland)", "100c"
		a1 = Array("100c", "French (Switzerland)", "fr-CH")
	Case "fr-ci", "french (ivory coast)", "300c"
		a1 = Array("300c", "French (Ivory Coast)", "fr-CI")
	Case "fr-cm", "french (cameroon)", "2c0c"
		a1 = Array("2c0c", "French (Cameroon)", "fr-CM")
	Case "fr-fr", "french (france)", "40c"
		a1 = Array("40c", "French (France)", "fr-FR")
	Case "fr-ht", "french (haiti)", "3c0c"
		a1 = Array("3c0c", "French (Haiti)", "fr-HT")
	Case "fr-lu", "french (luxembourg)", "140c"
		a1 = Array("140c", "French (Luxembourg)", "fr-LU")
	Case "fr-ma", "french (morocco)", "380c"
		a1 = Array("380c", "French (Morocco)", "fr-MA")
	Case "fr-mc", "french (monaco)", "180c"
		a1 = Array("180c", "French (Monaco)", "fr-MC")
	Case "fr-ml", "french (mali)", "340c"
		a1 = Array("340c", "French (Mali)", "fr-ML")
	Case "fr-re", "french (reunion)", "200c"
		a1 = Array("200c", "French (Reunion)", "fr-RE")
	Case "fr-sn", "french (senegal)", "280c"
		a1 = Array("280c", "French (Senegal)", "fr-SN")
	Case "fr", "french", "40c"
		a1 = Array("40c", "French", "fr")
	Case "it", "it-it", "italian", "410"
		a1 = Array("410", "Italian", "it-IT")
	Case "de-at", "german (austria)", "c07"
		a1 = Array("c07", "German (Austria)", "de-AT")
	Case "de-ch", "german (switzerland)", "807"
		a1 = Array("807", "German (Switzerland)", "de-CH")
	Case "de-de", "german (germany)", "407"
		a1 = Array("407", "German (Germany)", "de-DE")
	Case "de-li", "german (lithuania)", "1407"
		a1 = Array("1407", "German (Lithuania)", "de-LI")
	Case "de-lu", "german (luxembourg)", "1007"
		a1 = Array("1007", "German (Luxembourg)", "de-LU")
	Case "de", "german", "407"
		a1 = Array("407", "German", "de")
	Case "es-es", "spanish (spain)", "c0a"
		a1 = Array("c0a", "Spanish (Spain)", "es-ES")
	Case "es-ar", "spanish (argentina)", "2c0a"
		a1 = Array("2c0a", "Spanish (Argentina)", "es-AR")
	Case "es-bo", "spanish (bolivia)", "400a"
		a1 = Array("400a", "Spanish (Bolivia)", "es-BO")
	Case "es-cl", "spanish (chile)", "340a"
		a1 = Array("340a", "Spanish (Chile)", "es-CL")
	Case "es-co", "spanish (colombia)", "240a"
		a1 = Array("240a", "Spanish (Colombia)", "es-CO")
	Case "es-cr", "spanish (costa rica)", "140a"
		a1 = Array("140a", "Spanish (Costa Rica)", "es-CR")
	Case "es-do", "spanish (dominican republic)", "1c0a"
		a1 = Array("1c0a", "Spanish (Dominican Republic)", "es-DO")
	Case "es-ec", "spanish (ecuador)", "300a"
		a1 = Array("300a", "Spanish (Ecuador)", "es-EC")
	Case "es-sv", "spanish (svalbard)", "440a"
		a1 = Array("440a", "Spanish (Svalbard)", "es-SV")
	Case "es-gt", "spanish (guatemala)", "100a"
		a1 = Array("100a", "Spanish (Guatemala)", "es-GT")
	Case "es-hn", "spanish (honduras)", "480a"
		a1 = Array("480a", "Spanish (Honduras)", "es-HN")
	Case "es-mx", "spanish (mexico)", "80a"
		a1 = Array("80a", "Spanish (Mexico)", "es-MX")
	Case "es-ni", "spanish (nicaragua)", "4c0a"
		a1 = Array("4c0a", "Spanish (Nicaragua)", "es-NI")
	Case "es-pa", "spanish (panama)", "180a"
		a1 = Array("180a", "Spanish (Panama)", "es-PA")
	Case "es-py", "spanish (paraguay)", "3c0a"
		a1 = Array("3c0a", "Spanish (Paraguay)", "es-PY")
	Case "es-pe", "spanish (peru)", "280a"
		a1 = Array("280a", "Spanish (Peru)", "es-PE")
	Case "es-pr", "spanish (puerto rico)", "500a"
		a1 = Array("500a", "Spanish (Puerto Rico)", "es-PR")
	Case "es-us", "spanish (united states)", "540a"
		a1 = Array("540a", "Spanish (United States)", "es-US")
	Case "es-uy", "spanish (uraguay)", "540a"
		a1 = Array("540a", "Spanish (Uraguay)", "es-UR")
	Case "es-ve", "spanish (venezuela)", "200a"
		a1 = Array("200a", "Spanish (Venezuela)", "es-VE")
	Case "es", "spanish", "c0a"
		a1 = Array("c0a", "Spanish", "es")
	Case "ru", "ru-ru", "russian", "419"
		a1 = Array("419", "Russian", "ru-RU")
	Case "hi", "hi-in", "hindi", "439"
		a1 = Array("439", "Hindi", "hi-IN")
	Case "af", "af-za", "afrikaans", "436"
		a1 = Array("436", "Afrikaans", "af-ZA")
	Case "ak", "ak-gh", "akan"
		a1 = Array("1000", "Akan", "ak-GH")
	Case "an", "an-es", "argonese"
		a1 = Array("1000", "Argonese", "an-ES")
	Case "az", "az-az", "azerbaijani"
		a1 = Array("1000", "Azerbaijani", "az=AZ")
	Case "ar-sa", "arabic (saudi arabia)", "401"
		a1 = Array("401", "Arabic (Saudi Arabia)", "ar-SA")
	Case "ar-dz", "arabic (algeria)", "1401"
		a1 = Array("1401", "Arabic (Algeria)", "ar-DZ")
	Case "ar-bh", "arabic (bhutan)", "3c01"
		a1 = Array("3c01", "Arabic (Bhutan)", "ar-BH")
	Case "ar-eg", "arabic (egypt)", "c01"
		a1 = Array("c01", "Arabic (Egypt)", "ar-EG")
	Case "ar-iq", "arabic (iraq)", "801"
		a1 = Array("801", "Arabic (Iraq)", "ar-IQ")
	Case "ar-jo", "arabic (jordan)", "2c01"
		a1 = Array("2c01", "Arabic (Jordan)", "ar-JO")
	Case "ar-kw", "arabic (kuwait)", "3401"
		a1 = Array("3401", "Arabic (Kuwait)", "ar-KW")
	Case "ar-lb", "arabic (lebanon)", "3001"
		a1 = Array("3001", "Arabic (Lebanon)", "ar-LB")
	Case "ar-ly", "arabic (libya)", "1001"
		a1 = Array("1001", "Arabic (Libya)", "ar-LY")
	Case "ar-ma", "arabic (moroco)", "1801"
		a1 = Array("1801", "Arabic (Morocco)", "ar-MA")
	Case "ar-om", "arabic (oman)", "2001"
		a1 = Array("2001", "Arabic (Oman)", "ar-OM")
	Case "ar-qa", "arabic (qatar)", "4001"
		a1 = Array("4001", "Arabic (Qatar)", "ar-QA")
	Case "ar-sy", "arabic (syria)", "2801"
		a1 = Array("2801", "Arabic (Syria)", "ar-SY")
	Case "ar-tn", "arabic (tunisia)", "1c01"
		a1 = Array("1c01", "Arabic (Tunisia)", "ar-TU")
	Case "ar-ae", "arabic (united arab emirates)", "3801"
		a1 = Array("3801", "Arabic (United Arab Emirates)", "ar-AE")
	Case "ar-ye", "arabic (yemen)", "2401"
		a1 = Array("2401", "Arabic (Yemen)", "ar-YE")
	Case "ar", "arabic", "401"
		a1 = Array("401", "Arabic", "ar")
	Case "be", "be-by", "belarusian", "0423"
		a1 = Array("0423", "Belarusian", "be-BY")
	Case "bm", "bm-ml", "bambara"
		a1 = Array("1000", "Bambara", "bm-ML")
	Case "beq", "beq-cg", "beembe"
		a1 = Array("1000", "Beembe", "beq-CG")
	Case "bk", "bkw-cg", "bekwel"
		a1 = Array("1000", "Bekwel", "bk-CG")
	Case "bn", "bn-bd", "bengali"
		a1 = Array("1000", "Bengali", "bn-BD")
	Case "bs", "bs-bn", "bosnian"
		a1 = Array("1000", "Bosnian", "bs-BN")
	Case "buc", "buc-yt", "bushi"
		a1 = Array("1000", "Bushi", "buc-YT")
	Case "eu", "eu-fr", "eu-es", "basque"
		a1 = Array("1000", "Basque", "eu")
	Case "bg", "bg-bg", "bulgarian", "402"
		a1 = Array("402", "Bulgarian", "bg-BG")
	Case "ca", "ca-es", "catalan", "403"
		a1 = Array("403", "Catalan", "ca-ES")
	Case "ceb", "ceb-ph", "cebuano"
		a1 = Array("1000", "Cebuano", "ceb-PH")
	Case "cop", "cop-eg", "coptic"
		a1 = Array("1000", "Coptic", "cop-EG")
	Case "csb", "csb-pl", "kashubian"
		a1 = Array("1000", "Kashubian", "csb-PL")
	Case "cv", "cv-ru", "chuvash"
		a1 = Array("1000", "Chuvash", "cv-RU")
	Case "cs", "cs-cz", "czech", "405"
		a1 = Array("405", "Czech", "cs-CZ")
	Case "cy", "cy-gb", "welsh", "452"
		a1 = Array("452", "Welsh", "cy-GB")
	Case "da", "da-dk", "danish", "406"
		a1 = Array("406", "Danish", "da-DK")
	Case "dsb", "dsb-de", "sorbian, lower", "425"
		a1 = Array("425", "Sorbian, Lower", "dsb-DE")
	Case "ebo", "ebo-cg", "teke-eboo"
		a1 = Array("1000", "Teke-Eboo", "ebo-CG")
	Case "ee", "ee-gh", "ewe", Chr(233) & "w" & Chr(233)
		a1 = Array("1000", Chr(201) & "w" & Chr(233), "ee-GH")
	Case "el", "el-gr", "greek", "408"
		a1 = Array("408", "Greek", "el-GR")
	Case "eo", "eo-", "esperanto"
		a1 = Array("1000", "Esperanto", "eo")
	Case "et", "et-ee", "estonian", "425"
		a1 = Array("425", "Estonian", "et-EE")
	Case "fa", "fa-ir", "farsi"
		a1 = Array("1000", "Farsi", "fa-IR")
	Case "fi", "finnish", "40b"
		a1 = Array("40b", "Finnish", "fi")
	Case "fi-fi", "finnish (finland)", "40b"
		a1 = Array("40b", "Finnish (Finland)", "fi-FI")
	Case "fj", "fj-fj", "fijian"
		a1 = Array("1000", "Fijian", "fj-FJ")
	Case "fu", "fu-it", "friulian"
		a1 = Array("1000", "Friulian", "fu-IT")
	Case "fy", "fy-nl", "frisian"
		a1 = Array("1000", "Frisian", "fy-NL")
	Case "ga", "ga-ie", "irish", "83c"
		a1 = Array("83c", "Irish", "ga-IE")
	Case "gd", "gd-gb", "gaelic", "43c"
		a1 = Array("43c", "Gaelic", "gd-GB")
	Case "gl", "gl-es", "galician"
		a1 = Array("1000", "Galician", "gl-ES")
	Case "gu", "gu-in", "gujarati"
		a1 = Array("1000", "Gujarati", "gu-IN")
	Case "gd", "gd-gb", "gaelic"
		a1 = Array("1000", "Gaelic", "gd-GB")
	Case "gsc", "gsc-fr", "gascon"
		a1 = Array("1000", "Gascon", "gsc-FR")
	Case "gug", "gug-py", "guarani"
		a1 = Array("1000", "Guarani", "fug-PY")
	Case "haw", "haw-us", "hawaiian"
		a1 = Array("1000", "Hawaiian", "haw-US")
	Case "he", "he-il", "hebrew", "40d"
		a1 = Array("40d", "Hebrew", "he-IL")
	Case "hr", "hr-hr", "croatian", "41a"
		a1 = Array("41a", "Croatian", "hr-HR")
	Case "hsb", "hsb-de", "sorbian, upper"
		a1 = Array("1000", "Sorbian, Upper", "hsb-DE")
	Case "ht", "ht-ht", "haitian"
		a1 = Array("1000", "Haitian", "ht-HT")
	Case "hu", "hu-hu", "hungarian", "40e"
		a1 = Array("40e", "Hungarian", "hu-HU")
	Case "ha", "ha-gh", "ha-ng", "hausa"
		a1 = Array("1000", "Hausa", "ha")
	Case "hil", "hil-ph", "hiligaynon"
		a1 = Array("1000", "Hiligaynon", "hil-PH")
	Case "ia", "ia-", "interlingua"
		a1 = Array("1000", "Interlingua", "ia")
	Case "id", "id-id", "indonesian", "421"
		a1 = Array("421", "Indonesian", "id-ID")
	Case "is", "is-is", "icelandic", "40f"
		a1 = Array("40f", "Icelandic", "is-IS")
	Case "jbo", "jbo-", "lojban"
		a1 = Array("1000", "Lojban", "jbo")
	Case "ja", "ja-jp", "japanese", "411"
		a1 = Array("411", "Japanese", "ja-JP")
	Case "kab", "kab-dz", "kabyle"
		a1 = Array("1000", "Kabyle", "kab-DZ")
	Case "ki", "ki-ke", "gikuyu"
		a1 = Array("1000", "Gikuyu", "ki-KE")
	Case "kk", "kk-kz", "kazak"
		a1 = Array("1000", "Kazak", "kk-KZ")
	Case "kl", "kl-gl", "kalaallisut"
		a1 = Array("1000", "Kalaallisut", "kl-GL")
	Case "ksf", "ksf-cm", "bafia"
		a1 = Array("1000", "Bafia", "ksf-CM")
	Case "ko", "ko-kp", "ko-kr", "korean", "412"
		a1 = Array("412", "Korean", "ko")
	Case "ka", "ka-ge", "georgian"
		a1 = Array("1000", "Georgian", "ka-GE")
	Case "km", "km-kh", "khmer"
		a1 = Array("1000", "Khmer", "km-KH")
	Case "kn", "kn-in", "kannada"
		a1 = Array("1000", "Kannada", "kn-IN")
	Case "kok", "kok-in", "konkani"
		a1 = Array("1000", "Konkani", "kok-IN")
	Case "ku", "ku-sy", "ku-tr", "kurdish"
		a1 = Array("1000", "Kurdish", "ku")
	Case "ky", "ky-kg", "kirghiz"
		a1 = Array("1000", "Kirghiz", "ky-KG")
	Case "la", "la-va", "latin"
		a1 = Array("1000", "Latin", "la-VA")
	Case "lb", "lb-lu", "luxembourgish"
		a1 = Array("1000", "Luxembourgish", "lb-LU")
	Case "ldi", "ldi-cg", "lari"
		a1 = Array("1000", "Lari", "ldi-CG")
	Case "lg", "lg-ug", "ganda"
		a1 = Array("1000", "Ganda", "lg-UG")
	Case "ln", "ln-cd", "lingala"
		a1 = Array("1000", "Lingala", "ln-CD")
	Case "lo", "lo-la", "lao"
		a1 = Array("1000", "Lao", "lo-LA")
	Case "lt", "lt-lt", "lithuanian"
		a1 = Array("1000", "Lithuanian", "lt-LT")
	Case "ltg", "ltg-lv", "latgalian"
		a1 = Array("1000", "Latgalian", "ltg-LV")
	Case "lv", "lv-lv", "latvian"
		a1 = Array("1000", "Latvian", "lv-LV")
	Case "mdw", "mdw-cg", "mbochi"
		a1 = Array("1000", "Mbochi", "mdw-CG")
	Case "mi", "mi-nz", "maori (new zealand)"
		a1 = Array("1000", "Maori (New Zealand)", "mi-NZ")
	Case "ms", "ms-sg", "ms-my", "ms-id", "ms-bn", "malay", "43E"
		a1 = Array("43E", "Malay", "ms")
	Case "mk", "mk-mk", "macedonian"
		a1 = Array("1000", "Macedonian", "mk-MK")
	Case "mkw", "mkw-cg", "kituba", "mk-MK"
		a1 = Array("1000", "Kituba", "mkw-CG")
	Case "mn", "mn-mn", "mongolian"
		a1 = Array("1000", "Mongolian", "mn-MN")
	Case "mo-mn", "mo", "moldavian", "850"
		a1 = Array("850", "Moldavian", "mo-MN")
	Case "mos", "mos-bf", "moore"
		a1 = Array("1000", "Moore", "mos-BF")
	Case "mr", "mr-in", "marathi"
		a1 = Array("1000", "Marathi", "mr-IN")
	Case "nds", "nds-de", "low german"
		a1 = Array("1000", "Low German", "nds-DE")
	Case "nl", "nl-nl", "dutch", "413"
		a1 = Array("413", "Dutch", "nl-NL")
	Case "nl-be", "dutch (belgium)", "813"
		a1 = Array("813", "Dutch (Belgium)", "nl-BE")
	Case "nn", "nn-no", "norwegian norsk", "0814"
		a1 = Array("0814", "Norwegian Norsk", "nn-NO")
	Case "nb", "nb-no", "norwegian bokmal", "0414"
		a1 = Array("0414", "Norwegian Bokmal", "nb-NO")
	Case "no", "no-no", "norwegian", "0014"
		a1 = Array("0014", "Norwegian", "no-NO")
	Case "nr", "nr-za", "ndebele, south"
		a1 = Array("1000", "Ndebele, South", "nr-ZA")
	Case "nso", "nso-za", "northern sotho"
		a1 = Array("1000", "Northern Sotho", "nso-ZA")
	Case "ny", "ny-mw", "nyanja"
		a1 = Array("1000", "Nyanja", "ny-MW")
	Case "oc", "oc-fr", "occitan"
		a1 = Array("1000", "Occitan", "oc-FR")
	Case "om", "om-et", "oromo"
		a1 = Array("1000", "Oromo", "om-ET")
	Case "pap", "pap-aw", "pap-an", "papiamento"
		a1 = Array("1000", "Papiamento", "pap")
	Case "pl", "pl-pl", "polish", "415"
		a1 = Array("415", "Polish", "pl-PL")
	Case "pli", "pli-", "pali"
		a1 = Array("1000", "Pali", "pli")
	Case "plt", "plt-mg", "malagasy"
		a1 = Array("1000", "Malagasy", "plt-MG")
	Case "pt-br", "portuguese (brazil)", "416"
		a1 = Array("416", "Portuguese (Brazil)", "pt-BR")
	Case "pt-pt", "816"
		a1 = Array("816", "portuguese (portugal)", "pt-PT")
	Case "pt", "Portuguese"
		a1 = Array("816", "portuguese", "pt")
	Case "qtz", "qtz-", "keyid"
		a1 = Array("1000", "KeyID", "qtz")
	Case "qul", _
			"quh",_
			"qu", _
			"qul-bo", _
			"qu-ec", _
			"quh-bo", _
			"quechua"
		a1 = Array("1000", "Quechua", "qul")
	Case "rm", "rm-ch", "rhaeto-romance"
		a1 = Array("1000", "Rhaeto-Romance", "rm-CH")
	Case "ro", "ro-ro", "romanian", "418"
		a1 = Array("418", "Romanian", "ro-RO")
	Case "ru", "ru-ru", "ru-ua", "russian", "0419"
		a1 = Array("0419", "Russian", "ru-RU")
	Case "rue", "rue-sk", "rue-ua", "rusyan"
		a1 = Array("1000", "Rusyan", "rue")
	Case "rw", "rw-rw", "kinyarwanda"
		a1 = Array("1000", "Kinyarwanda", "rw-RW")
	Case "se-fi", _
			"se-no", _
			"se-se", _
			"se", _
			"sma-no", _
			"sma-se", _
			"sma", _
			"smj-no", _
			"smj-se", _
			"smj", _
			"smn-fi", _
			"smn-ru", _
			"smn", _
			"sms-fi", _
			"sami"
		a1 = Array("1000", "Sami", "se-FI")
	Case "sh-me", _
			"sh-rs", _
			"sh-su", _
			"sh-yu", _
			"sh", _
			"sr-me", _
			"sr-rs", _
			"sr-su", _
			"sr", _
			"serbian"
		a1 = Array("1000", "Serbian", "sh-RS")
	Case "shs", _
			"shs-ca", _
			"shuswap"
		a1 = Array("1000", "Shuswap", "shs-CA")
	Case "sk", _
			"sk-sk", _
			"slovakian", _
			"41b"
		a1 = Array("41b", "Slovakian", "sk-SK")
	Case "sl", "sl-si", "slovene", "424"
		a1 = Array("424", "Slovene", "si-SI")
	Case "so", "so-so", "somali"
		a1 = Array("1000", "Somali", "so-SO")
	Case "sq", "sq-al", "albanian"
		a1 = Array("1000", "Albanian", "sq-AL")
	Case "src", "src-it", "sardinian (logudorese)"
		a1 = Array("1000", "Sardinian (Logudorese)", "src-IT")
	Case "sdc", "sdc-it", "sardinian (sassarese)"
		a1 = Array("1000", "Sardinian (Sassarese)", "sdc-IT")
	Case "ss", "ss-za", "swazi"
		a1 = Array("1000", "Swazi", "ss-ZA")
	Case "st", "st-za", "southern sotho"
		a1 = Array("1000", "Southern Sotho", "st-ZA")
	Case "sw", "sw-tz", "sw-ke", "swahili"
		a1 = Array("1000", "Swahili", "sw")
	Case "swb", "swb-yt", "maore"
		a1 = Array("1000", "Maore", "swb-YT")
	Case "sv", "sv-se", "swedish", "41D"
		a1 = Array("41D", "Swedish", "sv-SE")
	Case "tek", "tek-cg", "teke-ibali"
		a1 = Array("1000", "Teke-Ibali", "tek-CG")
	Case "tet", "tet-id", "tet-tl", "tetun"
		a1 = Array("1000", "Tetun", "tet")
	Case "tg", "tg-tj", "tajic"
		a1 = Array("1000", "Tajic", "tg-TJ")
	Case "th", "th-th", "thai", "41E"
		a1 = Array("41E", "Thai", "th-TH")
	Case "ti", "ti-er", "ti-et", "tigrigna"
	a1 = Array("1000", "Tigrigna", "ti")
	Case "tk", "tk-tm", "turkmen"
		a1 = Array("1000", "Turkmen", "tk-TM")
	Case "tl", "tl-ph", "tagalog", "464"
		a1 = Array("464", "Tagalog", "tk-PH")
	Case "tn", "tn-bw", "tn-za", "tswana"
		a1 = Array("1000", "Tswana", "tn")
	Case "tpi", "tpi-pg", "tok pisin"
		a1 = Array("1000", "Tok Pisin", "tpi-PG")
	Case "tr", "tr-tr", "turkish", "41f"
		a1 = Array("41f", "Turkish", "tr-TR")
	Case "tt", "tt-ru", "tatar"
		a1 = Array("1000", "Tatar", "")
	Case "ts", "ts-za", "tsonga"
		a1 = Array("1000", "Tsonga", "ts-ZA")
	Case "ty", "ty-pf", "tahitian"
		a1 = Array("1000", "Tahitian", "ty-PF")
	Case "tyx", "tyx-cg", "teke-tyee"
		a1 = Array("1000", "Teke-Tyee", "tyx-CG")
	Case "uk", "uk-ua", "uk-uk", "ukrainian", "422"
		a1 = Array("422", "Ukrainian", "uk-UA")
	Case "ur", "ur-in", "ur-pk", "urdu"
		a1 = Array("1000", "Urdu", "ur")
	Case "uz", "uz-uz", "uzbec"
		a1 = Array("1000", "Uzbec", "uz-UZ")
	Case "ve", "ve-za", "venda"
		a1 = Array("1000", "Venda", "ve-ZA")
	Case "vi", "vi-vn", "vietnamese", "42a"
		a1 = Array("42a", "Vietnamese", "vi-VN")
	Case "vif", "vif-cg", "vili"
		a1 = Array("1000", "Vili", "vif-CG")
	Case "wa", "wa-be", "walloon"
		a1 = Array("1000", "Walloon", "wa-BE")
	Case "xh", "xh-za", "xhosa"
		a1 = Array("1000", "Xhosa", "xh-ZA")
	Case "yi", "yi-us", "yiddish"
		a1 = Array("1000", "Yiddish", "yi-US")
	Case "yo", "yo-ng", "yoruba"
		a1 = Array("1000", "Yoruba", "yo-NG")
	Case "zh-cn", "chinese (simplified)", "804"
		a1 = Array("804", "Chinese (Simplified)", "zh-CN")
	Case "zh-tw", "chinese (traditional)", "404"
		a1 = Array("404", "Chinese (Traditional)", "zh-TW")
	Case "zh-hk", "chinese (hong kong)", "c04"
		a1 = Array("c04", "Chinese (Hong Kong)", "zh-HK")
	Case "zh-sg", "chinese (singapore)", "1004"
		a1 = Array("1004", "Chinese (Singapore)", "zh-SG")
	Case "zh-mo", "chinese (macau)", "1404"
		a1 = Array("1404", "Chinese (Macau)", "zh-MO")
	Case "zh-yue", "zh-yu", "chinese (yue)"
		a1 = Array("1000", "Chinese (Yue)", "zh-YUE")
	Case "zh", "chinese", "804"
		a1 = Array("804", "Chinese", "zh")
	Case "zu", "zu-za", "zulu"
		a1 = Array("1000", "Zulu", "zu-ZA")
	Case "zxx", "zxx-", "ambiguous or missing language", "1000"
		a1 = Array("1000", "Ambiguous Or Missing Language", "zxx")
	Case Else
		' Not Found, So We Return ISO Language Code.
		a1 = Array("1000", sA, sA)
	End Select
	If iForceEnglish = 1 Then
	' The system uses an English string for a path or process name.
	' (i. e.: Festival, Windows SAPI)
		fsIsoToHumanReadable = a1(1)
	ElseIf iForceEnglish = 2 Then
	' Use the Microsoft XP compatible language code
		fsIsoToHumanReadable = a1(0)
	Else
	' Use the ISO language
		fsIsoToHumanReadable = a1(2)
	End If
End Function
Function fsWindowsCloseMatchLanguage(s1)
		Dim s2
		s2 = fsWindowsCloseMatchVoice(s1)
		Dim s3
		s3 = " "
		Dim s4
		s4 = "en-US"
		If Len(s2) > 1 Then
			If InStr(s2, "-") > 4  Then
				' Microsoft voice listing format lists the language
				' in English following a dash
				s3 = "-"
			End If
			Dim a1 : a1 = Split(s2, s3)
			s4 = Trim(a1(UBound(a1)))
			fsWindowsCloseMatchLanguage = fsIsoToHumanReadable(s4, 0)
		Else
			fsWindowsCloseMatchLanguage = s4
		End If
End Function
Function fsWindowsCloseMatchVoice(s1)
	' s1 - iso language string in the form `es-ES` or `en-CA`
	' Returns a human readable string of a language that
	' is installed and that closely matches the requested language
	' in the form `Spanish (Mexico)` or `English (USA)`
	fsWindowsCloseMatchVoice = ""
	Dim i
	i = 0
	Dim s2
	s2 = fsIsoToConciseHumanReadable(s1, 1)
	Dim s3
	s3 = ""
	Dim s4
	s4 = fsIsoToHumanReadable(s1, 1)
	Dim Sapi
	Set Sapi = CreateObject("Sapi.SpVoice")
	' Microsoft SAPI voices have a predictable naming pattern that includes
	' the language name in the form - `Microsoft David Desktop - English (United States)
	If Sapi.GetVoices.Count = 0 Then
		fsWindowsCloseMatchVoice = "Ambiguous Or Missing Language"
	Else
		For i = 0 To Sapi.GetVoices.Count - 1
			s3=Sapi.GetVoices.Item(i).GetDescription
			If Len(s3) > 1 And InStr(s3, s4) > 1 Then
				fsWindowsCloseMatchVoice = s3
				Exit For
			End If
		Next
		If fsWindowsCloseMatchVoice = "" Then
			For i = 0 To Sapi.GetVoices.Count - 1
				s3 = Sapi.GetVoices.Item(i).GetDescription
				If Len(s3) > 1 And InStr(s3, s2) > 1 Then
					fsWindowsCloseMatchVoice = s3
					Exit For
				End If
			Next
		End If
	End If
End Function
Function fsIsoToConciseHumanReadable(s1, iForceEnglish)
'  Returns name of language stripped of region
	Dim a1
	Dim s2
	s2 = fsIsoToHumanReadable(s1, iForceEnglish)
	Dim s3
	s3 = s2
	If InStr(s3, " (") > 0 Then
		a1 = Split(s3, "(")
		s2 = Trim(a1(LBound(a1)))
	End If
	fsIsoToConciseHumanReadable = s2
End Function
Function fsDec2Hex(i1)
' Given an integer, returns a hex string
	Dim s1
	If i1 < 16 Then
		s1 = Mid("0123456789abcdef", i1 + 1, 1)
	Else
		s1 = fsDec2Hex(i1 \ 16) & _
				fsDec2Hex(i1 Mod 16)
	End If
	fsDec2Hex = s1
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
	Dim s3
	Dim sVisible
	Dim sVoice
	Dim srate
	Dim sLanguage
	Dim sLibre
	Dim sImage
	Dim sDimensions
	Dim sOutFile
	bOK = False
	sVisible = ""
	On Error Resume Next
	'Decode the named arguments...
	sVoice = WScript.Arguments.Named.Item("voice")
	srate = WScript.Arguments.Named.Item("rate")
	sLanguage = WScript.Arguments.Named.Item("language")
	sLibre = WScript.Arguments.Named.Item("use-optional-app")
	sImage = WScript.Arguments.Named.Item("imagefile")
	sDimensions = WScript.Arguments.Named.Item("dimensions")
	sVisible = WScript.Arguments.Named.Item("visible") ' Windows Media Player
	If sDimensions = "" Then
		sDimensions = "400x400"
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
			s0 = Join(_
			Array(_
			Year(Date), _
			"-", _
			Month(Date), _
			"-", _
			Day(Date), _
			", ", _
			FormatDateTime(Now,4)), "")
			s3 = Left(fsIsoToHumanReadable(fsDec2Hex(Int(GetLocale())), 0), 2)
			Select Case s3
			Case "de"
				s1 = "Las ein paar Worte..."
			Case "es"
				s1 = "Introduzca algunas palabras ..."
			Case "fr"
				s1 = "Tapez quelques mots..."
			Case "pt"
				s1 = "Tipo de poucas palavras..."
			Case Else
				If "CA" = Right(fsIsoToHumanReadable(fsDec2Hex(Int(GetLocale())), 0), 2) Then
					s1 = "Excuse me... Could you please type some text?"
				Else
					s1 = "Enter a few words..."
				End If
			End Select
			s2=InputBox(s1, fsIsoToHumanReadable(fsDec2Hex(Int(GetLocale())), 1), s0)
		Case Else
			s2=readFile(s0)
			If Err <> 0 Then
				If Err.Number <> 13 Then
					Usage Err.Number & " -- " &  Err.Description & " -- " & s0
					Wscript.Exit(0)
				End If
			End If
	End Select
	If sLanguage = "" Then
		s1 = s2
	Else
		s1 = AddLanguageCodes(sLanguage,s2)
	End If
	If sOutFile = "" Then
		If sVisible = "" or LCase(sVisible) = "false" Then
			bOK = sayIt(s1, sRate, sVoice)
		Else
			sOutFile =  sTempDir() & "\" & APP_NAME & ".wav"
			sVisible = "true"
			fbRemoveFile sOutFile
			bOK = writeIt(s1, _
				sRate, _
				sVoice, _
				sOutFile, _
				s2, _
				sLibre, _
				sImage, _
				sDimensions, _
				sVisible)
			bOK = True
		End If
	Else
		bOK = writeIt(s1, _
				sRate, _
				sVoice, _
				sOutFile, _
				s2, _
				sLibre, _
				sImage, _
				sDimensions, _
				sVisible)
		If Not(bOK) Then
			bOK = sayIt(s1, sRate, sVoice)
		End If
	End If
	If Not(bOK) Then
		Usage APP_NAME & ": SAPI speech is not available"
	End If
End Sub
main()
