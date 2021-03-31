# agent
[![GitHub license](https://img.shields.io/badge/licence-GNU-green?style=flat)](https://github.com/CastellaniDavide/cpp-agent/blob/master/LICENSE) ![Author](https://img.shields.io/badge/author-Castellani%20Davide-green?style=flat) ![Version](https://img.shields.io/badge/version-v03.01-blue?style=flat) ![Language Python](https://img.shields.io/badge/language-Python-yellowgreen?style=flat) ![sys.platform supported](https://img.shields.io/badge/OS%20platform%20supported-Windows-blue?style=flat) [![On GitHub](https://img.shields.io/badge/on%20GitHub-True-green?style=flat&logo=github)](https://github.com/CastellaniDavide/agent)

## Description
Create a container of these programs:
 - [osversion](https://github.com/CastellaniDavide/osversion)
 - [netinfo](https://github.com/CastellaniDavide/netinfo)
 - [eventsview](https://github.com/CastellaniDavide/eventsview)
 - [product](https://github.com/CastellaniDavide/product)

## Required
 - python3
 - pip3 librerias (in project core: pip3 install -r requirements/requirements.txt)
 - Change **settings.yaml** file (in partictuar url, token, table)

## Directories structure
 - .github
   - ISSUE_TEMPLATE
     - bug_report.md
     - feature-request.md
   - workflows
     - python-test.yml
 - bin
   - agent.py
   - test_agent.py
 - docs
   - LICENSE
   - README.md
 - log
   - trace.log
 - settings
   - settings.yaml
 - requirements
   - requirements.txt
   
### Execution examples
 - python3 agent.py
 - python3 test_agent.py
 - pytest

# Changelog
 - [Version_03.01_2021-03-08](#Version_0301_2021-03-08)
 - [Version_01.03_2021-01-14](#Version_0103_2021-01-14)
 - [Version_01.02_2020-12-12](#Version_0102_2020-12-12)
 - [Version_01.01_2020-11-30](#Version_0101_2020-11-30)

## Version_03.01_2021-03-08
 - Added the possibility to add data into a DB
 - Changed tester
 - Changed the method to give settings (now in settings.yaml)
 - Changed the method to create/ manage logs

## Version_01.03_2021-01-14
 - Changed the method to create logs 
 - Changed the method to get settings

## Version_01.03_2021-01-14
 - Optimized log

## Version_01.02_2020-12-12
 - Optimized the log output
 - Updated the ping
 - Fixed some bugs

## Version_01.01_2020-11-30
 - Create a "container" of these programs:
   - [osversion](https://github.com/CastellaniDavide/osversion)
   - [netinfo](https://github.com/CastellaniDavide/netinfo)
   - [eventsview](https://github.com/CastellaniDavide/eventsview)
   - [product](https://github.com/CastellaniDavide/product)

---
Made by Castellani Davide 
If you have any problem please contact me:
- help@castellanidavide.it
- [Issue](https://github.com/CastellaniDavide/agent/issues)
