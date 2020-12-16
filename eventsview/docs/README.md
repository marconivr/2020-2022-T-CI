# eventsview
[![GitHub license](https://img.shields.io/badge/licence-GNU-green?style=flat)](https://github.com/CastellaniDavide/cpp-eventsview/blob/master/LICENSE) ![Author](https://img.shields.io/badge/author-Castellani%20Davide-green?style=flat) ![Version](https://img.shields.io/badge/version-v01.01-blue?style=flat) ![Language Python](https://img.shields.io/badge/language-Python-yellowgreen?style=flat) ![sys.platform supported](https://img.shields.io/badge/OS%20platform%20supported-Windows-blue?style=flat) [![On GitHub](https://img.shields.io/badge/on%20GitHub-True-green?style=flat&logo=github)](https://github.com/CastellaniDavide/eventsview)

## Description
View some event viewer infos (where it is an error).

### Tags
 #wmi, #automation, #python3, #eventviewer, #ping, #csv, #database, #datetime

## Goals
 - [x] Save in csv file the event viewer infos
 - [x] Save the infos in a database
 - [x] Print only if in debug mode
 - [x] Make standard csv
 - [x] Make database optional
 - [x] Check if PC is avariable (using ping)
 - [x] Use append method
 - [x] Add date info
 - [x] Add unchecked_PC.csv file and unchecked_PC table for the PCs that i can't reach
 - [x] Add folder variable
 - [x] Add a tester

## Required
 - python3
 - pip3 librerias (in project core: pip3 install -r requirements/requirements.txt)
 
## Directories structure
 - .github
   - ISSUE_TEMPLATE
     - bug_report.md
     - feature-request.md
   - workflows
     - python-test.yml
 - bin
   - **eventsview.py**
   - test_eventsview.py
 - docs
   - LICENSE
   - README.md
 - flussi
   - computers.csv
   - eventsview.csv <- On first run
   - eventsview.db (optional) <- On first run
   - eventsview_history.csv <- On first run
   - unchecked_PC.csv
 - log
   - trace.log
 - requirements
   - requirements.txt
   
## Execution examples
 - python3 eventsview.py
 - python3 test_eventsview.py/ pytest in core repo or in bin folder (you need one more packet: pytest)

## Attention
This programm will use lots of resources.
You need:
 - 8 GiB of RAM (better if 16)
 - Lots of time (for me this program was very slow)

## Changelog
 - [Version_01.01_2020-11-13](#Version_0101_2020-11-13)

### Version_01.01_2020-11-13
 - Save in csv file the event viewer infos
 - Save the infos in a database
 - Print only if in debug mode
 - Make standard csv
 - Make database optional
 - Check if PC is avariable (using ping)
 - Use append method
 - Add date info
 - Add unchecked_PC.csv file and unchecked_PC table for the PCs that i can't reach
 - Add folder variable
 - Add a tester

---
Made by Castellani Davide 
If you have any problem please contact me:
- help@castellanidavide.it
- [Issue](https://github.com/CastellaniDavide/eventsview/issues)
