"""
Programma con wmi
@author Bellamoli Riccardo
@version 05.01 2020-11-24
"""

import wmi
import logging
from datetime import datetime
import urllib.request as urllib2
import json
import codecs


def main():
    """richiama la funzione read, elaboration, write solo se eseguito come script
    """
    logging.basicConfig(filename='..\\log\\log.log', level=logging.DEBUG, format='%(message)s')
    open('..\\log\\log.log', 'a').close()
    file = open("../flussi/computers.csv", "r", encoding="UTF-8").readlines()
    div = (";")
    div_2 = ("-")
    div_3= (":")
    read(file, div, div_2, div_3)


def read(file, div, div_2, div_3):
    """legge il file di input
    """
    for line in file:
        line = line.strip()
        elaboration(div, line, div_2, div_3)


def elaboration(div, line, div_2, div_3):
    """elabora il tutto
    """
    import os.path
    if os.path.getsize("../log/log.log") == 0.0:
        logging.info('"ComputerName"; "Programma"; "Azione"; "tic"; "data"')
    now = datetime.now()
    logging.info(f'"null"; "netinfo"; "Inizio";{datetime.timestamp(now)}; "{now.day}/{now.month}/{now.year}"')
    i = 0
    names = line.split(div)
    while i < len(names):
        data = ""
        name_file = f"../flussi/{names[i]}.csv"
        final_file = open(name_file, "a", encoding="UTF-8")
        import os
        name = f"{names[i]}"
        respons = os.popen(f"ping -n 1 " + name).read()
        if "Risposta da " in respons:
            now = datetime.now()
            logging.info(f'"{name}"; "netinfo"; "Il terminale è accessibile";{datetime.timestamp(now)}; "{now.day}/{now.month}/{now.year}"')
            a = wmi.WMI(names[i])
            # print(a)
            os = a.Win32_NetworkAdapterConfiguration()
            for classes in os:
                ipenable = classes.IPEnabled
                if ipenable is True:
                    ip_address = classes.IPAddress
                    ipv6 = ""
                    i2 = 0
                    j = 0
                    while j < len(ip_address):
                        if j == 0:
                            ipv4 = ip_address[j]
                        else:
                            ipv6 += f'{j}){ip_address[j]}/'
                        j += 1
                    now = datetime.now()
                    if "VirtualBox" in classes.Caption:
                        data += f'"{classes.Caption}"{div}"{classes.MacAddress}"{div}"None"{div}"{ipv4}"{div}"{ipv6}"{div}"{classes.DNSDomain}"{div}"{datetime.timestamp(now)}"\n'
                    else:
                        mac_address = classes.MacAddress
                        if div_2 in mac_address:
                            mac_address = mac_address.replace(div_2, div_3)
                        url = "http://macvendors.co/api/"
                        request = urllib2.Request(url+mac_address, headers={'User-Agent' : "API Browser"}) 
                        response = urllib2.urlopen( request )
                        reader = codecs.getreader("utf-8")
                        obj = json.load(reader(response))
                        vendor = f"{obj['result']['company']} , {obj['result']['address']}"
                        data += f'"{classes.Caption}"{div}"{classes.MacAddress}"{div}"{vendor}"{div}"{ipv4}"{div}"{ipv6}"{div}"{classes.DNSDomain}"{div}"{datetime.timestamp(now)}"\n'
            write(data, div, final_file)
        else:
            now = datetime.now()
            logging.info(f'"{name}"; "netinfo"; "Scheda di rete disabilitata";{datetime.timestamp(now)}; "{now.day}/{now.month}/{now.year}"')
            data += f'"disable"\n'
            write(data, div, final_file)
        i = i + 1
    # print(names)
    now = datetime.now()
    logging.info(f'"null"; "netinfo"; "Fine";{datetime.timestamp(now)}; "{now.day}/{now.month}/{now.year}"')


def write(data, div, final_file):
    """scrive sul nuovo file
    """
    import os.path
    final_file.write(f'"caption"{div}"macaddress"{div}"vendor"{div}"ipv4"{div}"ipv6"{div}"dnsname"{div}"timestamp"\n')
    final_file.write(data)
    final_file.close()


if __name__ == "__main__":
    main()
