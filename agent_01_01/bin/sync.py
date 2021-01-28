import os
import sys
from time import time
from datetime import datetime

__authors__ = "De Battisti Tommaso & Falsarolo Leonardo & Scamperle Mattia"
__version__ = "1.1 2021-01-10"


def main():
    """Entry point
    """
    start = time()
    target_ip = None
    target_path = None
    walk = None
    username = None
    password = None
    for arg in sys.argv:
        if "--ipaddr=" in arg:
            target_ip = arg.split("=")[1]
        if "--pathsearch=" in arg:
            walk = arg.split("=")[1]
        if "--username=" in arg:
            username = arg.split("=")[1]
        if "--password=" in arg:
            password = arg.split("=")[1]
        if "--targetpath=" in arg:
            target_path = arg.split("=")[1]
        if "--help" in arg:
            print("Needed parameters:")
            print("--ipaddr=[ip] | Selects the ip to acc")
            print("--pathsearch=[path] | Selects the path for start to search the file.")
            print("--targetpath=[path] | Selects the output shared folder.")
            print("--username=[username] | Username of the remote machine")
            print("--password=[password] | Password of the remote machine")
            print("\nAdditional flags:")
            print("--help | Shows this message")
            print("--version | Shows program's version")
            print("-v | Activate Verbose (on-screen execution)")
            exit(0)
        if "--version" in arg:
            print(__version__)
            exit(0)

    if target_path is None or target_ip is None or walk is None:
        os.system("py sync_gui.py")
        exit(0)

    log(ticks())
    log(date())
    log("sync.py initialized")
    log(f"shared folder: \\\\{target_ip}\\{target_path}")
    response = is_reachable(target_ip)
    if response:
        log("Ping: OK")
        if username != "" and password != "":
            os.system(f"net use \\\\{target_ip}\\{target_path} /user:{username} {password}")
        if check_authorization(target_ip, target_path):
            log("Authorization: OK")
            log(f"Copying files from {walk} to \\\\{target_ip}\\{target_path}")
            sync = f"sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.mkdir(f"\\\\{target_ip}\\{target_path}\\{sync}")
            path = f"\\\\{target_ip}\\{target_path}\\{sync}"
            os.system(f"xcopy {walk} {path} /E")
        else:
            log("Authorization: FAILED")
            if username != "" and password != "":
                print("Invalid Username or Password")
            else:
                print(f"You must insert the credential to access {target_ip}")
            log()
            exit(1)
    else:
        log("Ping: FAILED")
        print(f"{target_ip} is unreachable")
        log()
        exit(1)
    end = time()
    log(f"done in {round(end - start, 4)} s")
    log()
    exit(0)


def check_authorization(target_ip, target_path):
    """Check if the user has write access to the shared folder

    Args:
        target_ip (str): hostname
        target_path (str): hostname path

    Returns:
        (bool): True if host is accessible else False
    """
    target_path = target_path.split("\\")[0]
    try:
        a = open(f'\\\\{target_ip}\\{target_path}\\test.txt', "w+")
        a.close()
        os.remove(f'\\\\{target_ip}\\{target_path}\\test.txt')
        return True
    except Exception as e:
        print(e)
        return False


def is_reachable(pc):
    """Check if a hostname is reachable

    Args:
        pc (str): hostname

    Returns:
        (bool): True if host is reachable else False
    """
    # log(f"called is_reachable function with '{pc}' as argument")
    if os.name == "nt":
        # execute a ping on the given hostname and stores the result on a variable
        request = os.popen(f"ping -n 1 {pc}").read()
        if "non raggiungibile" in request:
            return False
        elif "Impossibile trovare" in request:
            return False
        else:
            return True


def log(item="\n", log_file=f"../log/{datetime.now().strftime('%Y%m%d')}.log"):
    """Log an item to the log file\n

    Args:
        log_file (str, optional): log file
        item (any): string to log
    """
    if item != "\n":
        open(log_file, "a+").write(f"\"{str(item)}\";")
    else:
        open(log_file, "a+").write("\n")
    return 0


def ticks():
    """Get the current tick

    Returns:
        current tick
    """
    return round(time())


def date():
    """Get the current datetime in user-friendly mode

    Returns:
        current datetime
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    main()
