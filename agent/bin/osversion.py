"""
Programma con wmi
@author Bellamoli Riccardo
@version 01.03 2020-10-11
"""

import wmi
from datetime import datetime
import logging


def main():
    """richiama la funzione read, elaboration, write solo se eseguito come script
    """
    file = open("../flussi/computers.csv", "r", encoding="UTF-8").readlines()
    div = (";")
    logging.basicConfig(filename='..\\log\\log.log', level=logging.DEBUG, format='%(message)s')
    open('..\\log\\log.log', 'a').close()
    read(file, div)


def read(file, div):
    """legge il file di input
    """
    for line in file:
        line = line.strip()
        elaboration(div, line)
    now = datetime.now()
    logging.info(f'"null"; "osversion"; "Fine";{datetime.timestamp(now)}; "{now.day}/{now.month}/{now.year}"')


def elaboration(div, line):
    """elabora il tutto
    """
    import os.path
    if os.path.getsize("../log/log.log") == 0.0:
        logging.info('"ComputerName"; "Programma"; "Azione"; "tic"; "data"')
    now = datetime.now()
    logging.info(f'"null"; "osversion"; "Inizio";{datetime.timestamp(now)}; "{now.day}/{now.month}/{now.year}"')
    i = 0
    data = ""
    names = line.split(div)
    while i < len(names):
        name_file = f"../flussi/{names[i]}.csv"
        data= ""
        final_file = open(name_file, "a", encoding="UTF-8")
        import os
        name = f"{names[i]}"
        respons = os.popen(f"ping -n 1 " + name).read()
        if respons == 0:
            logging.info(f'"{name}"; "osversion"; "Il terminale è accessibile";{datetime.timestamp(now)}; "{now.day}/{now.month}/{now.year}"')
            a = wmi.WMI(names[i])
            #print(a)
            os = a.Win32_OperatingSystem()
            for classes in os:
                caption = classes.Caption
                version = classes.Version
                build = classes.BuildNumber
                now = datetime.now()
                timestamp = datetime.timestamp(now)
                data += f"{caption}{div}{version}{div}{build}{div}{datetime.timestamp(now)}\n"
            write(data, div, final_file)
        else:
            now = datetime.now()
            logging.info(f'"{name}"; "osversion"; "Scheda di rete disabilitata";{datetime.timestamp(now)}; "{now.day}/{now.month}/{now.year}"')
            data += f"disable\n"
            write(data, div, final_file)
        i = i + 1
    #print(names)


def write(data, div, final_file):
    """scrive sul nuovo file
    """
    final_file.write(f"caption{div}version{div}build{div}timestamp\n")
    final_file.write(data)
    final_file.close()


if __name__ == "__main__":
    main()
