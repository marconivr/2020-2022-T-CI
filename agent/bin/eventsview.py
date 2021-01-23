"""
Programma con wmi
@author Bellamoli Riccardo
@version 01.01 2020-11-13
"""

import wmi
import logging
from datetime import datetime


def main():
    """richiama la funzione read, elaboration, write solo se eseguito come script
    """
    logtype = 'System'
    logging.basicConfig(filename='..\\log\\log.log', level=logging.DEBUG, format='%(message)s')
    open('..\\log\\log.log', 'a').close()
    file = open("../flussi/computers.csv", "r", encoding="UTF-8").readlines()
    div = (";")
    data = ""
    read(file, div, logtype)


def read(file, div, logtype):
    """legge il file di input
    """
    for line in file:
        line = line.strip()
        elaboration(div, line, logtype)


def elaboration(div, line, logtype):
    """elabora il tutto
    """
    import os.path
    if os.path.getsize("../log/log.log") == 0.0:
        logging.info('"ComputerName"; "Programma"; "Azione"; "tic"; "data"')
    now = datetime.now()
    logging.info(f'"null"; "eventsview"; "Inizio";{datetime.timestamp(now)}; "{now.day}/{now.month}/{now.year}"')
    i = 0
    data = ""
    names = line.split(div)
    while i < len(names):
        data = ""
        name_file = f"../flussi/{names[i]}.csv"
        final_file = open(name_file, "a", encoding="UTF-8")
        final_file.write(f'"ComputerName"{div}"Message"{div}"ErrorLevel"{div}"TimeGenerated"{div}"TimeWritten"\n')
        import os
        name = f"{names[i]}"
        respons = os.popen(f"ping -n 1 " + name).read()
        if "Risposta da " in respons:
            logging.info(f'"{name}"; "eventsview"; "Il terminale è accessibile";{datetime.timestamp(now)}; "{now.day}/{now.month}/{now.year}"')
            a = wmi.WMI(names[i])
            getEvent(logtype, a, div, data, final_file)
            final_file.write("\n\n")
            final_file.close()
            now = datetime.now()
            logging.info(f'"null"; "eventsview"; "Fine";{datetime.timestamp(now)}; "{now.day}/{now.month}/{now.year}"')
            # print(a)
        else:
            now = datetime.now()
            logging.info(f'"{name}"; "eventsview"; "Scheda di rete disabilitata";{datetime.timestamp(now)}; "{now.day}/{now.month}/{now.year}"')
        i = i + 1


def getEvent(logtype, a, div, data, final_file):
    """prende le informazioni dall'event viewer
    """
    for event in a.Win32_NTLogEvent(Logfile=logtype):
        data = f'"{event.ComputerName}"{div}"{event.Message}"{div}"{event.Type}"{div}"{event.TimeGenerated}"{div}"{event.TimeWritten}"'.replace("\r", " ").replace("\n", " ")
        data += "\n"
        write(data, final_file)


def write(data, final_file):
    """scrive sul nuovo file
    """
    final_file.write(data)


if __name__ == "__main__":
    main()
