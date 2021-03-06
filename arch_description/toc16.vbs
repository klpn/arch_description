' Adapted from https://github.com/jgm/pandoc/issues/458#issuecomment-58720613
' Updates TOC, assuming MS Word to be installed.
' Also changes TOC heading, because the English name is hardcoded into Pandoc.

If WScript.Arguments.length = 0 Then 
	WScript.Echo("Filnamn ej angett!")
	WScript.Quit
End If

Const wdReplaceAll = 2

Set objWord = CreateObject("Word.Application")
Set objDoc = objWord.Documents.Open(WScript.Arguments.Item(0))

Set objSelection = objWord.Selection

objSelection.Find.Text = "Table of Contents"
objSelection.Find.Forward = TRUE

objSelection.Find.Replacement.Text = "Innehållsförteckning"

objSelection.Find.Execute ,,,,,,,,,,wdReplaceAll

objDoc.Save()
objDoc.Close()
objWord.Quit()
