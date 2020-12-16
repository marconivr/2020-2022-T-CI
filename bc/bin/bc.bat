@ECHO OFF
CLS

REM bc
REM Made by Castellani Davide

ECHO Start time: %DATE% %TIME% >> ..\log\trace.log

ECHO Opened all files >> ..\log\trace.log
ECHO Running: bc.bat >> ..\log\trace.log

python ./uptime.py -b
cscript ./updatepending.vbs

ECHO End time: %DATE% %TIME% >> ..\log\trace.log
ECHO. >> ..\log\trace.log
