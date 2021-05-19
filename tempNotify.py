import requests
import socket
import subprocess
from constants import safeTemp
from utils import alertOwner
import socket

hostName = socket.gethostname()

def getTemperature():
    try:
        temp = str(subprocess.Popen("vcgencmd measure_temp", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True).communicate()[0])
        temp = float(temp.replace("b\"temp=", "").replace("'C\\n\"", ""))

        return temp
    except Exception as e:
        text = "error occured on {}, error: {}".format(hostName,  str(e))
        alertOwner(text)

def checkTemperature():
    temp = getTemperature()
    if temp >= safeTemp:
        text = "Temperature has crossed set thresold, current temperature on {} is {}".format(hostName,  temp)
        alertOwner(text)


if __name__ == '__main__':
    checkTemperature()


