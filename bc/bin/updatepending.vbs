'Update pending
'By Castellani Davide

'init
Dim init_time
init_time = Timer
Set updateSession = CreateObject("Microsoft.Update.Session")
updateSession.ClientApplicationID = "updatepending.vbs"

'functions
Sub myPrint(logFile, message)
	logFile.WriteLine("	" & message)
	'WScript.Echo message 'debug
End Sub

Function getUpdates(logFile)
    call myPrint(logFile, "Search updates")
    
    'return
	Set getUpdates = updateSession.CreateUpdateSearcher().Search("IsInstalled=0")
End Function

Sub printUpdates(logFile, csvFile, csvFileNormal, updates)
    If updates.Updates.Count = 0 Then
        call myPrint(logFile, "There are no applicable updates.")
    Else
        call myPrint(logFile, "Updates:")
        For I = 0 To updates.Updates.Count-1
            call myPrint(logFile, "	" & I + 1 & ". " & updates.Updates.Item(I).Title)
            csvFileNormal.WriteLine(CreateObject("WScript.Network").ComputerName & "," & updates.Updates.Item(I).Title)
            csvFile.WriteLine(CreateObject("WScript.Network").ComputerName & "," & updates.Updates.Item(I).Title)
        Next
    End If
End Sub

Sub reboot(logFile, csvFile, csvFileNormal)
    call myPrint(logFile, "Check if rebootis necessary")

    If CreateObject("Microsoft.Update.SystemInfo").RebootRequired Then
        call myPrint(logFile, "Update necessary")

        'create a box to choose your option
        If vbOk = Msgbox("A Reboot is pending, Press ""OK"" to reboot now or ""Cancel"" to reboot later", vbOkCancel, "CRISTA IT") Then
            call myPrint(logFile, "Rebooting")
            call myEnd(logFile, csvFile, csvFileNormal)
            
            for each OpSys in GetObject("winmgmts:{(Shutdown)}//./root/cimv2").ExecQuery("select * from Win32_OperatingSystem where Primary=true") 'https://docs.microsoft.com/en-us/windows/win32/cimwin32prov/reboot-method-in-class-win32-operatingsystem
                OpSys.Reboot()
            next
        Else
            call myPrint(logFile, "You didn't want reboot your PC")
        End If
    End If
End Sub

Sub myEnd(logFile, csvFile, csvFileNormal)
    call myPrint(logFile, "End time: " +  FormatDateTime(Now()))
    call myPrint(logFile, "Total time: " + CStr(Timer - init_time))
	logFile.WriteLine("	" & message)
    logFile.Close
    csvFile.Close
    Set logFile = Nothing
    Set csvFile = Nothing
End Sub

'Open files
Set logFile = CreateObject("Scripting.FileSystemObject").OpenTextFile("..\log\trace.log", 8, true)
Set csvFileNormal = CreateObject("Scripting.FileSystemObject").OpenTextFile("..\flussi\updatepending.csv", 2, true)
Set csvFile = CreateObject("Scripting.FileSystemObject").OpenTextFile("..\flussi\updatepending_history.csv", 8, true)
csvFileNormal.WriteLine("PC_name,Update")

call myPrint(logFile, "Start time: " +  FormatDateTime(Now()))
call myPrint(logFile, "Opened all files")
call myPrint(logFile, "Running: updatepending.vbs")

'core
call printUpdates(logFile, csvFile, csvFileNormal, getUpdates(logFile))
call reboot(logFile, csvFile, csvFileNormal)

'end
call myEnd(logFile, csvFile, csvFileNormal)
