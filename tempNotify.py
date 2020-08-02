import requests
import socket
import subprocess
from constants import ownerChatId, botApi, safeTemp

hostName = socket.gethostname()
url = "https://api.telegram.org/bot{}/sendMessage".format(botApi)

def sendMessage(text):
    data = {"chat_id" : ownerChatId, "text" : text}
    requests.get(url, params = data)

def getTemperature():
    try:
        temp = str(subprocess.Popen("vcgencmd measure_temp", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True).communicate()[0])
        temp = float(temp.replace("b\"temp=", "").replace("'C\\n\"", ""))

        return temp
    except Exception as e:
        text = "error occured on {}, error: {}".format(hostName,  str(e))
        sendMessage(text)

def checkTemperature():
    temp = getTemperature()
    if temp >= safeTemp:
        text = "Temperature has crossed set thresold, current temperature on {} is {}".format(hostName,  temp)
        sendMessage(text)


if __name__ == '__main__':
    checkTemperature()


