@echo off

rem Parametrized execution of all the programs in the ./bin folder 
rem @authors 18605@studenti.marconiverona.edu.it, 18774@studenti.marconiverona.edu.it, 18617@studenti.marconiverona.edu.it
rem @version 2.0 2020-12-03

:: Executes all the programs

if "%1" == "-all" (
    py osversion.py %2 %3 %4
    py netinfo.py %2 %3 %4
    py product.py %2 %3 %4
    py eventsview.py %2 %3 %4
    py ldisk.py %2 %3 %4
    exit /B 0
)

:: Parametrized execution
if "%1" == "-net" (
    py netinfo.py %2 %3 %4
    exit /B 0
)

if "%1" == "-os" (
    py osversion.py %2 %3 %4
    exit /B 0
)

if "%1" == "-event" (
    py eventsview.py %2 %3 %4
    exit /B 0
)

if "%1" == "-prod" (
    py product.py %2 %3 %4
    exit /B 0
)

if "%1" == "" (
    py agent_gui.py
    exit /B 0
)

if "%1" == "-disk" (
    py ldisk.py %2 %3 %4
    exit /B 0
)

if "%1" == "--version" (
    echo agent 1.1 2020-12-03
    exit /B 0
)

if "%1" == "--help" (
    goto help
    exit /B 0
)

:help
    echo Execution parameters:
    echo -all (executes all the programs)
    echo -net (executes only network based programs)
    echo -os (executes only operating-system based programs)
    echo -prod (executes only product based programs)
    echo -event (executes only event-viewer based programs)
    echo -disk (executes only based programs)
    echo.
    echo Optional parameters: (after execution parameters)
    echo -v (verbose mode)
    echo --version (shows the version of each programs)
    echo.
