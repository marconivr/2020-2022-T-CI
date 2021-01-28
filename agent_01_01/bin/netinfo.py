import wmi
import sys
import os
import urllib.request as urllib2
import json
import codecs
from datetime import datetime
from time import time

__author__ = "De Battisti Tommaso, Falsarolo Leonardo"
__contacts__ = "18605@studenti.marconiverona.edu.it, 18617@studenti.marconiverona.edu.it"
__version__ = "5.2 2020-12-12"


def main():
    """main function
    """
    file_in = "../flussi/computers.csv"

    # Optional CLI args
    output_folder = "../flussi/"
    out = "netinfo.csv"
    format_ = ":"
    vonly = None

    log(f"{round(time())}")
    log(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    for arg in sys.argv:
        if "--format=" in arg:
            format_ = arg.split("=")[1]
        if "--outputfile=" in arg:
            out = arg.split("=")[1].replace(".csv", "")
        if "--outputfolder=" in arg:
            output_folder = arg.split("=")[1]
            if not os.path.isdir(output_folder):
                os.mkdir(output_folder)
        if "--help" in arg:
            print("Optional parameters:")
            print("--format=[format] | Selects the format of the MAC Addresses. Default to ':'")
            print("--outputfile=[output file] | Selects the output file. Default to 'netinfo.csv'")
            print("--outputfolder=[output folder] | Selects the output folder. Default to 'netinfo.csv'")
            print("\nAdditional flags:")
            print("--help | Shows this message")
            print("--version | Shows program's version")
            print("-v | Activate Verbose (on-screen execution)")
            print("--vonly=[class attribute,class attribute] | Activate verbose only for given attributes. Separator "
                  "must be ','")
            exit()
        if "--version" in arg:
            print(__version__)
            exit()
        if "--vonly=" in arg:
            vonly = arg.split("=")[1]

    global verbose
    verbose = True if ("-v" in sys.argv and vonly is None) else False
    out = out.replace(".csv", "")
    file_out = f"{output_folder}/{out}.csv"
    log(f"netinfo.py inizialized, verbose {verbose}")
    start_time = time()

    # create a list containing machine names from the input file
    machines = []
    with open(file_in, "r") as fn:
        for line in fn.readlines():
            if not '#' in line and line != "\n":
                machines.append(line.replace("\n", "").replace(" ", ""))
        log("list of machines created")
        fn.close()

    is_intestated = True
    intestation = '"Timestamp";"Hostname";"Adapter";"MACAddress";"IPv4";"IPv6";"DHCPEnabled";"DefaultGateway";"Vendor' \
                  '"\n '
    try:
        with open(file_out, "r") as temp:
            if temp.read() == "":
                is_intestated = False
            temp.close()
    except FileNotFoundError:
        is_intestated = False

    # creates the output file and put the data in it
    with open(file_out, "a+") as fm:
        log(f"{file_out.split('/')[2]} inizialized")
        if not is_intestated:
            fm.write(intestation)

        for i in range(len(machines)):
            # checks if hostname is reachable
            if is_reachable(machines[i]):
                try:
                    # wmi connection to hostname
                    con = wmi.WMI(machines[i])
                    for netadapter in con.Win32_NetworkAdapterConfiguration(IPEnabled=1):
                        csv_row = ""
                        if check_vm(netadapter.Description):
                            vendor = get_vendor(netadapter.MACAddress)

                        # filter (and prints) only user's parameters
                        if vonly is not None:
                            string = f"{machines[i]:<15} {netadapter.Description:<50}"
                            for attribute in vonly.split(","):
                                for instance in (str(netadapter).split(";")):
                                    for row in (str(instance).split("\n")):
                                        if attribute in row:
                                            string += row.rstrip().lstrip() + "; "
                            print(string)

                        # sending - showing Data to the output file
                        printv(netadapter)
                        csv_row += f'"{round(time())}";'
                        csv_row += f'"{machines[i]}";'
                        csv_row += f'"{netadapter.Description}";'
                        csv_row += f'"{normalize_mac(netadapter.MACAddress, format_)}";'

                        # checks if IPAddress has more than 2 IPv4 or IPv6
                        if len(netadapter.IPAddress) <= 2:
                            csv_row += collection2csv(netadapter.IPAddress) + ";"
                        else:
                            ips = collection2csv(netadapter.IPAddress).split(";")
                            csv_row += ips[0] + ";" + ips[1] + ";"
                        csv_row += f'"{netadapter.DHCPEnabled}";'
                        csv_row += f'"{str(netadapter.DefaultIPGateway)}";'
                        csv_row += f'"{vendor}"\n'
                        csv_row = csv_row.replace("(", "").replace(")", "").replace("'", "").replace(",", "")
                        fm.write(csv_row)

                except wmi.x_wmi:
                    # wmi.x_wmi handling
                    print_log(f"error: couldn't connect to {machines[i]}")
            else:
                print_log(f"error: {machines[i]} is not reachable")
            printv()

        print_log(f"machine data sent to {file_out.split('/')[2]}")
        fm.close()
        end_time = time()
        print_log(f"netinfo.py done in {round(end_time - start_time, 4)} s")
    log()
    exit(0)


def collection2csv(tuple_, sep=";"):
    """given a collection, it normalize it to be a csv item

    Args:
        sep: separator
        tuple_ : collection

    Returns:
        normalized collection
    """
    log("Called collection2csv function")
    tuple_ = str(tuple_).replace("'", '"').replace(" ", "").replace(",", sep).replace("(", "").replace(")", "")
    tuple_ = tuple_.replace("[", "").replace("]", "").replace("{", "").replace("}", "")
    return tuple_


def is_reachable(pc):
    """
    check if a hostname is reachable

    Args:
        pc (str): hostname

    Returns:
        (bool): True if host is reachable else False
    """
    log(f"called is_reachable function with '{pc}' as argument")
    if os.name == "nt":
        # execute a ping on the given hostname and stores the result on a variable
        request = os.popen(f"ping -n 1 {pc}")
        return not "Impossibile trovare" in request.read()


def get_vendor(mac):
    """
    Get vendor from a MAC Address using an API

    Args:
        mac (str): mac to check

    Returns:
        (tuple) vendor and address
    """
    log(f"called get_vendor function with '{mac}' as argument")
    url = "http://macvendors.co/api/"

    try:
        request = urllib2.Request(url + mac, headers={'User-Agent': "API Browser"})
        response = urllib2.urlopen(request)
    except:
        return "Error", "Error"

    reader = codecs.getreader("utf-8")
    obj = json.load(reader(response))

    try:
        vendor = (obj['result']['company'], obj['result']['address'])
    except:
        vendor = ("None", "None")
    return vendor


def normalize_mac(mac, format_=":"):
    """
    normalize the given mac address using the given format

    Args:
        mac (str): Mac address to normalize
        format_ (str, optional): format. Defaults to ":".

    Returns:
        str: normalized mac address
    """
    log(f"Called normalize_mac function with '{mac}' and '{format_}' as arguments")
    return mac.replace(get_format(mac), format_)


def check_vm(driver):
    """
    check if a pc is network driver is virtual

    Args:
        driver (str): driver

    Returns:
        (boolean): True or False based on the result
    """
    log(f"called check_vm function with '{driver}' as argument")
    return not "virtualbox" in driver.lower()


def get_format(mac):
    """Gets the format (or the separator) of a MAC address

    Args:
        mac (str): mac to check

    Returns:
        (str): separator
    """
    if "-" in mac:
        return "-"
    if ":" in mac:
        return ":"


def log(item="\n", log_file=f"../log/{datetime.now().strftime('%Y%m%d')}.log"):
    """
    log an item to the log file\n

    Args:
        item (any)
        log_file (str, Optional): log file
    """
    if item == "\n":
        open(log_file, "a+").write(f"\n")
    else:
        open(log_file, "a+").write(f"\"{str(item)}\";")
    return 0


def printv(item=""):
    """Print an element if verbose is on

    Args:
        item (any): item
    """
    if verbose:
        print(str(item))
    return 0


def print_log(item=""):
    """Print an item and logs it in the log file

    Args:
        item (any): item
    """
    log(item)
    printv(item)
    return 0


if __name__ == "__main__":
    main()
