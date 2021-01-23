@ECHO OFF
REM Agent che esegue i programmi python sul logging del pc
CLS
where python.exe
if not errorlevel 1 (
	if "%1" == "all" (
	REM Esegue tutto
	python netinfo.py
	python product.py
	python eventsview.py
	python osversion.py
	)
	if "%1" == "n" (
	REM Esegue netinfo.py
	python netinfo.py
	GOTO 2
	)
	if "%1" == "p" (
	REM Esegue product.py
	python product.py
	GOTO 2
	)
	if "%1" == "e" (
	REM Esegue eventsview.py
	python eventsview.py
	GOTO 2
	)
	if "%1" == "o" (
	REM Esegue osversion.py
	python osversion.py
	GOTO 2
	)
	:2
	if "%2" == "n" (
	REM Esegue netinfo.py
	python netinfo.py
	GOTO 3
	)
	if "%2" == "p" (
	REM Esegue product.py
	python product.py
	GOTO 3
	)
	if "%2" == "e" (
	REM Esegue eventsview.py
	python eventsview.py
	GOTO 3
	)
	if "%2" == "o" (
	REM Esegue osversion.py
	python osversion.py
	GOTO 3
	)
	:3
	if "%3" == "n" (
	REM Esegue netinfo.py
	python netinfo.py
	GOTO 4
	)
	if "%3" == "p" (
	REM Esegue product.py
	python product.py
	GOTO 4
	)
	if "%3" == "e" (
	REM Esegue eventsview.py
	python eventsview.py
	GOTO 4
	)
	if "%3" == "o" (
	REM Esegue osversion.py
	python osversion.py
	GOTO 4
	)
	:4
	if "%4" == "n" (
	REM Esegue netinfo.py
	python netinfo.py
	)
	if "%4" == "p" (
	REM Esegue product.py
	python product.py
	)
	if "%4" == "e" (
	REM Esegue eventsview.py
	python eventsview.py
	)
	if "%4" == "o" (
	REM Esegue osversion.py
	python osversion.py
	)
	sync.bat
) else (echo python non installato)
pause
exit


