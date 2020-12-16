import wmi


def get_uptime(computer):
    c = wmi.WMI(computer=computer, find_classes=False)
    secs_up = int([uptime.SystemUpTime for uptime in c.Win32_PerfFormattedData_PerfOS_System()][0])
    hours_up = secs_up / 3600
    return hours_up


if __name__ == "__main__":
    print(get_uptime("."))
