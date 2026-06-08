Set WshShell = CreateObject("WScript.Shell")

WshShell.Run Chr(34) & "C:\SISTEMAS\ti_ticket_system\tasks\process_inbox.bat" & Chr(34), 0, False

Set WshShell = Nothing