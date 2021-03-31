@ECHO OFF
REM usb

REM change directory to the current (for the scheduled task)
CD /D "%~dp0"

REM Init log
ECHO Running setup >> ../log/trace.log

REM Get init time
ECHO Start_time: "%date% %time%" >> ../log/trace.log

REM install choco & python
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command " [System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
ECHO choco installed >> ../log/trace.log
choco install python3 -y --force>> ../log/trace.log
ECHO python3 installed >> ../log/trace.log

REM Update Schedule file, Create Schedule and Reastore Schedule file
ECHO Create Schedule >> ../log/trace.log
python.exe -c "import os; file = open(r'..\requirements\USB_CASTELLANIDAVIDE.xml').read().replace('\x00', '').replace('\n\n', '\n').replace('\\\\', '\\').replace('setup_file_location', os.path.dirname(os.path.abspath('usb.bat'))); open('..\\requirements\\USB_CASTELLANIDAVIDE.xml', 'w', encoding='utf-8').write(file)"
schtasks.exe /Create /XML ..\requirements\USB_CASTELLANIDAVIDE.xml /TN USB_CASTELLANIDAVIDE
python.exe -c "import os; file = open(r'..\requirements\USB_CASTELLANIDAVIDE.xml').read().replace('\x00', '').replace('\n\n', '\n').replace('\\\\', '\\').replace(os.path.dirname(os.path.abspath('usb.bat')), 'setup_file_location'); open('..\\requirements\\USB_CASTELLANIDAVIDE.xml', 'w', encoding='utf-8').write(file)"
ECHO Schedule created >> ../log/trace.log

REM pip packages
ECHO Install pip requirements >> ../log/trace.log
pip3 install -r ..\requirements\requirements.txt
ECHO pip packages installed >> ../log/trace.log

REM Reset last user
ECHO None > ../flussi/lastUser.txt
ECHO Reseted lastUser >> ../log/trace.log

REM Reset usb (output) files
ECHO. >> ../flussi/usb.csv
DEL ../flussi/usb.db
ECHO Reset usb (output) files >> ../log/trace.log

REM Get end time
ECHO End_time: "%date% %time%" >> ../log/trace.log

REM "End setup"
ECHO. >> ../log/trace.log

REM Test funtionality/ First run
./usb.bat
