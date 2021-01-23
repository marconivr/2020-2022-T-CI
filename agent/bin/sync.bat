@ECHO OFF
REM Programma Sync dei file nelle cartelle flussi e log
CLS
for %%f in (..\flussi\*.csv) do (
	IF not "%%~nf.csv" == "computers.csv" (
		XCOPY "..\flussi\%%~nf.csv" "..\sync\flussi\" /y /q 
	)
)
XCOPY "..\log\log.log" "..\sync\log\" /y /q
exit 


