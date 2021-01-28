import wmi
import sys
import os
from datetime import datetime
from time import time

__authors__ = "De Battisti Tommaso, Falsarolo Leonardo, Scamperle Mattia"
__version__ = "1.2 2021-01-12"


def main():
    """main function
    """
    file_in = "../flussi/computers.csv"

    # Optional CLI args
    output_folder = "../flussi/"
    out = "ldisk.csv"
    vonly = None

    log(f"{round(time())}")
    log(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    for arg in sys.argv:
        if "--outputfile=" in arg:
            out = arg.split("=")[1].replace(".csv", "")
        if "--outputfolder=" in arg:
            output_folder = arg.split("=")[1]
            if not os.path.isdir(output_folder):
                os.mkdir(output_folder)
        if "--help" in arg:
            print("Optional parameters:")
            print("--outputfile=[output file] | Selects the output file. Default to 'ldisk.csv'")
            print("--outputfolder=[output folder] | Selects the output folder. Default to 'ldisk.csv'")
            print("\nAdditional flags:")
            print("--help | Shows this message")
            print("--version | Shows program's version")
            print("-v | Activate Verbose (on-screen execution)")
            print(
                "--vonly=[class attribute,class attribute] | Activate verbose only for given attributes. Separator "
                "must be ','")
            exit(0)
        if "--version" in arg:
            print(__version__)
            exit(0)
        if "--vonly=" in arg:
            vonly = arg.split("=")[1]

    global verbose
    verbose = True if ("-v" in sys.argv and vonly is None) else False
    out = out.replace(".csv", "")
    file_out = f"{output_folder}/{out}.csv"
    log(f"ldisk.py inizialized, verbose {verbose}")
    start_time = time()

    # create a list containing machine names from the input file
    machines = []
    with open(file_in, "r") as fn:
        for line in fn.readlines():
            if not '#' in line and line != "\n":
                machines.append(line.replace("\n", "").replace(" ", ""))
        log("list of machines created")
        fn.close()

    # creates the output file and put the data in it
    with open(file_out, "a+") as fm:
        log(f"{file_out.split('/')[2]} inizialized")

        for i in range(len(machines)):
            # checks if hostname is reachable
            if is_reachable(machines[i]):
                try:
                    # wmi connection to hostname
                    con = wmi.WMI(machines[i])
                    for ldisk in con.Win32_LogicalDisk():
                        csv_row = ""

                        # filter (and prints) only user's parameters
                        if vonly is not None:
                            string = f"{machines[i]:<15} {str(ldisk.Name):<65}"
                            for attribute in vonly.split(","):
                                for instance in (str(ldisk).split(";")):
                                    for row in (str(instance).split("\n")):
                                        if attribute in row:
                                            string += row.rstrip().lstrip().replace(attribute + " = ", "") + "; "
                            print(string)

                        # sending - showing Data to the output file
                        printv(ldisk)
                        csv_row += f'"{round(time())}";'
                        csv_row += f'"{machines[i]}";'
                        csv_row += f'"{ldisk.Name}";'
                        csv_row += f'"{ldisk.FileSystem}";'
                        csv_row += f'"{ldisk.DriveType}";'
                        csv_row += f'"{ldisk.VolumeName}";'
                        csv_row += f'"{ldisk.Size}";'
                        csv_row += f'"{ldisk.FreeSpace}";'
                        csv_row += f'"{ldisk.VolumeSerialNumber}"\n'

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
        print_log(f"ldisk.py done in {round(end_time - start_time, 4)} s")
    log()
    exit(0)


def collection2csv(tuple_, sep=";"):
    """
    given a collection, it normalize it to be a csv item

    Args:
        tuple_ (tuple): collection
        sep (str): MAC address separator

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


def log(item="\n", log_file=f"../log/{datetime.now().strftime('%Y%m%d')}.log"):
    """Log an item to the log file\n

    Args:
        item (any)
        log_file (str, Optional): log file
    """
    if item == "\n":
        open(log_file, "a+").write("\n")
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

