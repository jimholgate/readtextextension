'VBS Script for Read Text Extension by James Holgate
'Writes a list of voices to a configuration file
Const ForReading=1
Const ForWriting=2
Const ForAppending=8

Sub Usage(s1)
  s1=s1 & chr(10)
  s1=s1 & chr(10)
  s1=s1 & "Returns a list of SAPI voices" & chr(10)
  s1=s1 & chr(10)
  s1=s1 & "Usage" & chr(10)
  s1=s1 & chr(10)
  s1=s1 & "tts_list_voices.vbs [" & chr(34) & "filename.txt" & chr(34)
  s1=s1 & chr(10) & "]"
  s1=s1 & "  " & chr(34) & "filename.txt" & chr(34) 
  s1=s1 & " (optional) is the Document to write to."
  WScript.echo s1
End Sub

function GetmyVoices()
  Set Sapi=Wscript.CreateObject("SAPI.SpVoice")
  If Sapi Is Nothing Then
    s1="FAILED Sapi.SpVoice creation." & chr(10)
    si=s1 & "SAPI ne pouvait pas trouver une voix."
    Usage s1 
  Else
    GetmyVoices=""
    n=0
    While n<Sapi.GetVoices.Count
        GetmyVoices=GetMyVoices & Sapi.GetVoices.Item(n).GetDescription
        GetmyVoices=GetMyVoices & Chr(13) & Chr(10)
      n=n+1
    Wend
  End If
End function

Sub main()
  On Error Resume Next
  'Decode the unnamed argument...
  s1=WScript.Arguments.Unnamed.Item(0)
  select case s1
  case ""
    MsgBox GetMyVoices,0,"tts_list_voices.vbs"
  case "-h","--help","/h","-?"
    Usage "Help"
    WScript.Exit(0)
  case else
    Set objFSO=CreateObject("Scripting.FileSystemObject")
    Set objText=objFSO.CreateTextFile(s1,ForWriting)
    If Err <> 0 Then
      Usage Err.Number & " -- " &  Err.Description & s1
      Wscript.Exit(0)
    Else
      s2=GetMyVoices
      objText.Write(s2)
      objText.Close
    End If
  End Select
End Sub

main
