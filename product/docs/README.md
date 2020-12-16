# product
[![GitHub license](https://img.shields.io/badge/licence-GNU-green?style=flat)](https://github.com/CastellaniDavide/cpp-product/blob/master/LICENSE) ![Author](https://img.shields.io/badge/author-Castellani%20Davide-green?style=flat) ![Version](https://img.shields.io/badge/version-v01.01-blue?style=flat) ![Language Python](https://img.shields.io/badge/language-Python-yellowgreen?style=flat) ![sys.platform supported](https://img.shields.io/badge/OS%20platform%20supported-Linux,%20Windows%20&%20Mac%20OS-blue?style=flat) [![On GitHub](https://img.shields.io/badge/on%20GitHub-True-green?style=flat&logo=github)](https://github.com/CastellaniDavide/product)

## Description
Get win32_Product infos.

## Required
 - python3
 - pip3 librerias (in project core: pip3 install -r requirements/requirements.txt)
 
## Goals
 - [x] Save in csv file the PC's infos
 - [x] Save the infos in a database
 - [x] Print only if in debug mode
 - [x] Make standard csv
 - [x] Make database optional
 - [x] Check if PC is avariable (using ping)
 - [x] Use append method
 - [x] Add date info
 - [x] Add unchecked_PC.csv file and unchecked_PC table for the PCs that i can't reach
 - [x] Add folder variable
 - [x] Add tester

## Directories structure (most important files and folders)
 - .github
   - ISSUE_TEMPLATE
     - bug_report.md
     - feature-request.md
   - workflows
     - python-test.yml
 - bin
   - ***product.py***
   - test_product.py
 - docs or doc
   - LICENSE
   - README.md
   - _config.yml
 - flussi
   - **computers.csv** <- insert here a list of computer to test
   - product.csv <- on first run
   - product.db <- on first run
   - product_history <- on first run
   - unchecked_PC.csv
 - log
   - trace.log
 - requirements
   - requirements.txt
   
### Execution examples
 - python3 product.py
 - python3 test_product.py

# Changelog
 - [Version_01.01_2020-11-20](#Version_0101_2020-11-20)

## Version_01.01_2020-11-20
 - Save in csv file the PC's infos
 - Save the infos in a database
 - Print only if in debug mode
 - Make standard csv
 - Make database optional
 - Check if PC is avariable (using ping)
 - Use append method
 - Add date info
 - Add unchecked_PC.csv file and unchecked_PC table for the PCs that i can't reach
 - Add folder variable
 - Add tester

---
Made by Castellani Davide 
If you have any problem please contact me:
- help@castellanidavide.it
- [Issue](https://github.com/CastellaniDavide/product/issues)
