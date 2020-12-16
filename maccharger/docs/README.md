# maccharger
[![GitHub license](https://img.shields.io/badge/licence-GNU-green?style=flat)](https://github.com/CastellaniDavide/cpp-maccharger/blob/master/LICENSE) ![Author](https://img.shields.io/badge/author-Castellani%20Davide-green?style=flat) ![Version](https://img.shields.io/badge/version-v01.01-blue?style=flat) ![Language Python](https://img.shields.io/badge/language-Python-yellowgreen?style=flat) ![sys.platform supported](https://img.shields.io/badge/OS%20platform%20supported-Linux,%20Windows%20&%20Mac%20OS-blue?style=flat) [![On GitHub](https://img.shields.io/badge/on%20GitHub-True-green?style=flat&logo=github)](https://github.com/CastellaniDavide/maccharger)

## Description
Manage MAC address

## Goals
 - [x] Read MAC Address
 - [x] Change MAC Address with a specific one
 - [x] Change MAC Address with a random one
 - [x] Restore MAC Address
 - [x] Use one-line mode or teminal
 - [x] Make a tester
 - [x] Make an installer
 - [ ] Run into Windows

## Required
 - A browser
   
## Istructions to install all necessary

 - [1. Install VBox]
 - [2. Create VM]
 - [3. Download repo]
 - [4. Run setup]

### 1. Install VBox
#### Video
[![1. Install VBox](https://img.youtube.com/vi/2GwoHz4_Jtg/0.jpg)](https://www.youtube.com/watch?v=2GwoHz4_Jtg)

#### Testual
 - Go to [https://www.virtualbox.org](https://www.virtualbox.org/)
 - Press "Download" bottom
 - Select your OS & distribution (in my case Linux -> Ubuntu 20.04)
 - Install it with double press or using shell (in Ubuntu sudo apt install .\virtualbox...)

### 2. Create VM
#### Video
[![2. Create VM](https://img.youtube.com/vi/8GveEZ9qPDg/0.jpg)](https://www.youtube.com/watch?v=8GveEZ9qPDg)

#### Testual
 - Download a valid iso (eg. [Debian](https://www.debian.org/distrib/))
 - Install VM into VBox following Vbox Manager istructions

### 3. Download repo
#### Video
[![3. Download repo](https://img.youtube.com/vi/qE82wgx6tY0/0.jpg)](https://www.youtube.com/watch?v=qE82wgx6tY0)

#### Testual
 - go to [https://github.com/CastellaniDavide/maccharger](https://github.com/CastellaniDavide/maccharger)
 - press download -> download zip
 - unzip folder

### 4. Run setup
#### Video
[![4. Run setup](https://img.youtube.com/vi/83wxAUZrp3E/0.jpg)](https://www.youtube.com/watch?v=83wxAUZrp3E)

#### Testual
 - do to requirements folder
 - run requirements.sh (lnx) or (requirements.bat) for Windows code as Administrator
 
## Directories structure
 - .github
   - ISSUE_TEMPLATE
     - bug_report.md
     - feature-request.md
   - workflows
     - python-test.yml
 - bin
   - maccharger.py
   - test_maccharger.py
 - docs
   - LICENSE
   - README.md
 - log
   - trace.log
 - requirements
   - requirements.txt
   
### Execution examples
 - sudo python3 maccharger.py
 - sudo python3 maccharger.py -v
 - sudo python3 maccharger.py -v -t 1 3 1 4
 - sudo python3 maccharger.py -t 1 3 1 4
 - python3 test_maccharger.py

# Changelog
 - [Version_01.01_2020-11-5](#Version_10_2020-11-5)

## Version_01.01_2020-11-5
 - Read MAC Address
 - Change MAC Address with a specific one
 - Change MAC Address with a random one
 - Restore MAC Address
 - Use one-line mode or teminal
 - Make a tester
 - Make an installer

---
Made by Castellani Davide 
If you have any problem please contact me:
- help@castellanidavide.it
- [Issue](https://github.com/CastellaniDavide/maccharger/issues)
