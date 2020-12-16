@ECHO OFF
REM Install all requirements

REM change directory to the current (for the scheduled task)
CD /D "%~dp0"

REM Init log
ECHO Running installer >> ../log/log.log

REM Get init time
ECHO Start_time: "%date% %time%" >> ../log/log.log

REM install choco & python
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command " [System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" >> ../log/log.log && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin" >> ../log/log.log
ECHO choco installed >> ../log/log.log
choco install python3 -y --force >> ../log/log.log
ECHO python3 installed >> ../log/log.log

REM pip packages
ECHO Install pip requirements >> ../log/log.log
pip3 install -r ..\requirements\requirements.txt >> ../log/log.log
ECHO pip packages installed >> ../log/log.log

REM Get end time
ECHO End_time: "%date% %time%" >> ../log/log.log
ECHO. >> ../log/log.log
