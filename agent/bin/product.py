"""
Programma con wmi
@author Bellamoli Riccardo
@version 01.01 2020-11-20
"""

import wmi
import logging
from datetime import datetime


def main():
    """richiama la funzione read, elaboration, write solo se eseguito come script
    """
    logging.basicConfig(filename='..\\log\\log.log', level=logging.DEBUG, format='%(message)s')
    open('..\\log\\log.log', 'a').close()
    file = open("../flussi/computers.csv", "r", encoding="UTF-8").readlines()
    div = (";")
    data = ""
    read(file, div)


def read(file, div):
    """legge il file di input
    """
    for line in file:
        line = line.strip()
        elaboration(div, line)


def elaboration(div, line):
    """elabora il tutto
    """
    import os.path
    if os.path.getsize("../log/log.log") == 0.0:
        logging.info('"ComputerName"; "Programma"; "Azione"; "tic"; "data"')
    now = datetime.now()
    logging.info(f'"null"; "product"; "Inizio";{datetime.timestamp(now)}; "{now.day}/{now.month}/{now.year}"')
    i = 0
    data = ""
    names = line.split(div)
    while i < len(names):
        data = ""
        name_file = f"../flussi/{names[i]}.csv"
        final_file = open(name_file, "a", encoding="UTF-8")
        final_file.write(f'"Caption"{div}"Description"{div}"InstallDate"{div}"InstallSource"{div}"Language"{div}"Name"{div}"ProductID"{div}"SKUNumber"{div}"Vendor"{div}"Version"{div}"TimeStamp"\n')
        import os
        name = f"{names[i]}"
        respons = os.popen(f"ping -n 1 " + name).read()
        if "Risposta da " in respons:
            logging.info(f'"{name}"; "product"; "Il terminale è accessibile";{datetime.timestamp(now)}; "{now.day}/{now.month}/{now.year}"')
            a = wmi.WMI(names[i])
            getProduct(a, div, data, final_file, name)
            final_file.write("\n\n")
            final_file.close()
            now = datetime.now()
            logging.info(f'"null"; "osversion"; "Fine";{datetime.timestamp(now)}; "{now.day}/{now.month}/{now.year}"')
            # print(a)
        else:
            now = datetime.now()
            logging.info(f'"{name}"; "product"; "Scheda di rete disabilitata";{datetime.timestamp(now)}; "{now.day}/{now.month}/{now.year}"')
            final_file.write('Terminale Spento')
        i = i + 1


def getProduct(a, div, data, final_file, name):
    """prende le informazioni dall'event viewer
    """
    for classes in a.Win32_Product():
        data = f'"{name}"{div}"{classes.Caption}"{div}"{classes.Description}"{div}"{classes.InstallDate}"{div}"{classes.InstallSource}"{div}"{classes.Language}"{div}"{classes.Name}"{div}"{classes.ProductID}"{div}"{classes.SKUNumber}"{div}"{classes.Vendor}"{div}"{classes.Version}"{div}"{datetime.timestamp(datetime.now())}"\n'
        write(data, final_file)


def write(data, final_file):
    """scrive sul nuovo file
    """
    final_file.write(data)


if __name__ == "__main__":
    main()
