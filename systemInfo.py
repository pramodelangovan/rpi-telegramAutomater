"""
https://www.thepythoncode.com/article/get-hardware-system-information-python\
"""
import psutil
import platform
from datetime import datetime

sysData = """System: {system}
Host Name: {hostName}

Boot time: {bootTime}
Up time: {upTime}

RAM Usage
Total: {ramTotal}
Available: {ramAvailable}
Used: {ramUsed}
Percentage: {ramPercentage}

SWAP Usage
Total: {swapTotal}
Free: {swapFree}
Used: {swapUsed}
Percentage: {swapPercentage}

Disks
Total read: {totalRead}
Total write: {totalWrite}

{diskDetails}

Network
{networkDetails}
Total Sent: {totalSent}
Total Recieved: {totalRecieved}
"""

mountDev = """Disk {num}: {device}
Mountpoint: {mountpoint}
File system type: {fsType}
Total Size: {total}
Used: {used}
Free: {free}
Percentage: {percentage}

"""

def getSize(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def getSystemInfo():
    uname = platform.uname()
    system =  uname.system
    hostName = uname.node

    bootTimestamp = psutil.boot_time()
    bootTime = datetime.fromtimestamp(bootTimestamp).replace(microsecond=0)
    now = datetime.now().replace(microsecond=0)
    upTime = str(now - bootTime)
    bootTime = (f"{bootTime.year}/{bootTime.month}/{bootTime.day} {bootTime.hour}:{bootTime.minute}:{bootTime.second}")

    ramDetails = psutil.virtual_memory()
    ramTotal = getSize(ramDetails.total)
    ramAvailable = getSize(ramDetails.available)
    ramUsed = getSize(ramDetails.used)
    ramPercentage = f"{ramDetails.percent}%"

    swapDetails = psutil.swap_memory()
    swapTotal = getSize(swapDetails.total)
    swapFree = getSize(swapDetails.free)
    swapUsed = getSize(swapDetails.used)
    swapPercentage = f"{swapDetails.percent}%"

    partitions = psutil.disk_partitions()
    diskDetails = ""
    num=1
    for partition in partitions:
        try:
            partitionUsage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        diskDetails += mountDev.format(num=num,
                        device=partition.device,
                        mountpoint=partition.mountpoint,
                        fsType=partition.fstype,
                        total=getSize(partitionUsage.total),
                        used=getSize(partitionUsage.used),
                        free=getSize(partitionUsage.free),
                        percentage=f"{partitionUsage.percent}%")
        num+=1

    diskIO = psutil.disk_io_counters()
    totalRead = getSize(diskIO.read_bytes)
    totalWrite = getSize(diskIO.write_bytes)

    ifAddrs = psutil.net_if_addrs()
    networkDetails = ""
    for interfaceName, interfaceAddresses in ifAddrs.items():
        for address in interfaceAddresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                networkDetails += "Interface: {}, IP Address: {}\n".format(interfaceName, address.address)

    netIO = psutil.net_io_counters()
    totalSent = getSize(netIO.bytes_sent)
    totalRecieved = getSize(netIO.bytes_recv)

    return sysData.format(system=system, hostName=hostName, bootTime=bootTime, upTime=upTime,
                        ramTotal=ramTotal, ramAvailable=ramAvailable, ramUsed=ramUsed, ramPercentage=ramPercentage,
                        swapTotal=swapTotal, swapFree=swapFree, swapUsed=swapUsed, swapPercentage=swapPercentage,
                        diskDetails=diskDetails.strip(), totalRead=totalRead, totalWrite=totalWrite,
                        networkDetails=networkDetails.strip(), totalSent=totalSent, totalRecieved=totalRecieved
                        )

if __name__ == "__main__":
    print(getSystemInfo())