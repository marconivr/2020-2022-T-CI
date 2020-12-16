
'https://superuser.com/questions/1107692/list-pending-windows-updates-from-command-line

Set updateSession = CreateObject("Microsoft.Update.Session")
updateSession.ClientApplicationID = "Gianni Test Scripts"

Set updateSearcher = updateSession.CreateUpdateSearcher()

WScript.Echo "Searching for updates..." & vbCRLF

'Set searchResult = updateSearcher.Search("IsInstalled=0 and Type='Software' and IsHidden=0")
Set searchResult = updateSearcher.Search("IsInstalled=0")

WScript.Echo "List of applicable items on the machine:"

For I = 0 To searchResult.Updates.Count-1
    Set update = searchResult.Updates.Item(I)
    WScript.Echo I + 1 & "> " & update.Title
Next

If searchResult.Updates.Count = 0 Then
    WScript.Echo "There are no applicable updates."
    WScript.Quit
End If


Set objSysInfo = CreateObject("Microsoft.Update.SystemInfo")

WScript.Echo "Test Reboot"

If objSysInfo.RebootRequired Then
     If vbOk=Msgbox("A Reboot is pending, Press ""OK"" to reboot now or ""Cancel"" to reboot later", vbOkCancel, "CRISTA IT") Then
        ' Use WMI to reboot
     End If
End If

