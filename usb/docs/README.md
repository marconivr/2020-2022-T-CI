# usb
[![GitHub license](https://img.shields.io/badge/licence-GNU-green?style=flat)](https://github.com/CastellaniDavide/cpp-usb/blob/master/LICENSE) ![Author](https://img.shields.io/badge/author-Castellani%20Davide-green?style=flat) ![Version](https://img.shields.io/badge/version-v01.03-blue?style=flat) ![Language Batch, Python](https://img.shields.io/badge/language-Batch,%20Python-yellowgreen?style=flat) ![sys.platform supported](https://img.shields.io/badge/OS%20platform%20supported-Linux,%20Windows%20&%20Mac%20OS-blue?style=flat) [![On GitHub](https://img.shields.io/badge/on%20GitHub-True-green?style=flat&logo=github)](https://github.com/CastellaniDavide/usb)

## Tags
 #python3, #bat, #batch, #chocolatey, #usb, #windows-10, #task-scheduler, #setup, #csv, #database, #log

## Description
Get and filter USB infos.

You can see the project website here [https://castellanidavide.github.io/usb/](https://castellanidavide.github.io/usb/)
![Funcionality image](https://raw.githubusercontent.com/CastellaniDavide/usb/main/docs/funcionality.png)

## Goals
 - [x] Get csv USBDview.exe output and save in temp.csv (bat)
 - [x] Get csv USBDview.exe output and save in temp.csv (bat)
 - [x] Call usb.py by bat
 - [x] Filter the temp.csv file
 - [x] Save filtred info into usb.csv
 - [x] Debug setup by .bat file
 - [x] After executing delate temporaly files
 - [x] Get & manage user-name
 - [x] Run every log in
 - [x] Create a guide setup
 - [x] Create a setup file
 - [x] Add website
 - [x] Paramized (output) folder variable

## Required/ Setup
 - python3 & pip3 packages & task scheduler & ...
   - launch setup(.lnk) and accept Administrator mode (or launch setup.bat as Administrator)

### ATTENTION: don't move or delate folder after setup

## Directories structure
 - .github
   - ISSUE_TEMPLATE
     - bug_report.md
     - feature-request.md
 - bin
   - setup.bat
   - **setup(.lnk)**
   - usb.bat <- for debugging
   - usb.py
   - USBDview.exe
 - docs or doc
   - _config.yml
   - funcionality.png
   - LICENSE
   - README.md
 - flussi
   - lastUser.txt
   - temp.csv <- only during the code executing
   - usb.csv
   - usb.db <- if you eank to use database (default true)
 - log
   - trace.log
 - requirements
   - requirements.txt
   - USB_CASTELLANIDAVIDE.xml
   
### Execution examples debug (in bin folder)
 - ./usb.bat

# Changelog
 - [Version_01.03_2020-10-15](#Version_0103_2020-10-15)
 - [Version_01.02_2020-10-09](#Version_0102_2020-10-09)
 - [Version_01.01_2020-10-04](#Version_0101_2020-10-04)

## Version 01.03 2020-10-15
 - Fixed a bug

## Version 01.02 2020-10-09
 - Paramized (output) folder variable

## Version_01.01_2020-10-04
 - Get csv USBDview.exe output and save in temp.csv (bat)
 - Call usb.py by bat
 - Filter the temp.csv file
 - Save filtred info into usb.csv
 - Debug setup by .bat file
 - After executing delate temporaly files
 - Get & manage user-name
 - Run every log in
 - Create a guide setup
 - Create a setup file
 - Add website

---
Made by Castellani Davide 
If you have any problem please contact me:
- [help@castellanidavide.it](mailto:help@castellanidavide.it)
- [Issue](https://github.com/CastellaniDavide/usb/issues)
