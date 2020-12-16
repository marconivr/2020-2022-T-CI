@ECHO OFF
REM usb
	
REM change directory to the current (for the scheduled task)
CD /D "%~dp0"

REM Get init time
ECHO Start_time: "%date% %time%" >> ../log/trace.log

REM Run
.\USBDview.exe /scomma ../flussi/temp.csv
ECHO temp.csv created >> ../log/trace.log

REM Call python code
python.exe ./usb.py --batch

REM Delate temp file(s)
DEL "../flussi/temp.csv"

REM Get end time
ECHO End_time: "%date% %time%" >> ../log/trace.log

REM Get end time
ECHO. >> ../log/trace.log
