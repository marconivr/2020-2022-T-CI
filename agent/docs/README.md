# agent
[![GitHub license](https://img.shields.io/badge/licence-GNU-green?style=flat)](https://github.com/CastellaniDavide/cpp-agent/blob/master/LICENSE) ![Author](https://img.shields.io/badge/author-Castellani%20Davide-green?style=flat) ![Version](https://img.shields.io/badge/version-v01.02-blue?style=flat) ![Language Python](https://img.shields.io/badge/language-Python-yellowgreen?style=flat) ![sys.platform supported](https://img.shields.io/badge/OS%20platform%20supported-Windows-blue?style=flat) [![On GitHub](https://img.shields.io/badge/on%20GitHub-True-green?style=flat&logo=github)](https://github.com/CastellaniDavide/agent)

## Description
 - Create a container of these programs:
   - [osversion](https://github.com/CastellaniDavide/osversion)
   - [netinfo](https://github.com/CastellaniDavide/netinfo)
   - [eventsview](https://github.com/CastellaniDavide/eventsview)
   - [product](https://github.com/CastellaniDavide/product)

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
   - agent.py
   - test_agent.py
 - docs
   - LICENSE
   - README.md
 - log
   - trace.log
 - requirements
   - requirements.txt
   
### Execution examples
 - python3 agent.py
 - python3 agent.py --module=osversion
 - python3 agent.py -m=osversion
 - python3 agent.py --module=netinfo
 - python3 agent.py -m=netinfo
 - python3 agent.py --module=eventsview
 - python3 agent.py -m=eventsview
 - python3 agent.py --module=product
 - python3 agent.py -m=product
 - python3 test_agent.py
 - pytest

# Changelog
 - [Version_01.02_2020-12-12](#Version_10_2020-12-12)
 - [Version_01.01_2020-11-30](#Version_10_2020-11-30)

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
