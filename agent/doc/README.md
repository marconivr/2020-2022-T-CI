# Agent

**Python, Win32_NetworkAdapterConfiguration, wmi, cmd, os, Win32_Product, batch, Win32_OperatingSystem, Win32_NTLogEvent, logging, csv**

## Descrizione

Abbiamo creato un programma agent.bat che chiama tutti i programmi che abbiamo sviluppato in questo trimestre.
Il programma agent.bat chiama inoltre il programma sync.bat. quest'ultimo carica i file di output e il file di log
in una cartella di prova, che dopo sarà una cartella condivisa tra delle macchine virtuali. Con questa consegna si
vuole dimostrare l'importanza del tenere traccia (log) delle informazioni di specifica del nostro computer.

## Requisiti

Avere python installato e il path di python e tanto tempo nel caso si voglia un'esecuzione completa

## Esempio di esecuzione

Dal cmd scrivere: C:\...\bin>agent.bat [1] [2] [3] [4]
Si possono utilizzare i seguenti parametri con le seguenti combinazioni:
- "all"	solo questo come primo parametro
- "n" "p" "e" "o"	si può decidere di non usarli tutti e di cambiare l'ordine
Questo programma non implementa la risoluzione di problemi relativi all'autenticazione nel momento in cui usiamo
cartelle condivise in rete. Questo perché, nel nostro caso, avremo tutti quanti la macchina virtuale con stesso
nome utente e password data dal professore quindi non ci saranno problemi.
##### Importante: non usare lo stesso parametro 2 volte, non usare più di 4 parametri.

## Autore

Bellamoli Riccardo in collaborazione con Foroncelli Claudio
Programma sync.bat in collaborazione con Foroncelli Claudio, Perlini Tommaso e Morellato Pietro

# Changelog

/

## [01.01] - 2021-01-19

### Added
- /

### Changed
- /

### Removed
- /

## Prima versione
