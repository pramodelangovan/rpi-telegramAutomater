import requests
import socket
import subprocess
from constants import chatId, botApi

hostName = socket.gethostname()
url = "https://api.telegram.org/bot{}/sendMessage".format(botApi)
safeTemp = 75.0

def sendMessage(text):
    data = {"chat_id" : chatId, "text" : text}
    requests.get(url, params = data)

def checkTemperature():
    try:
        temp = str(subprocess.Popen("vcgencmd measure_temp", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True).communicate()[0])
        temp = float(temp.replace("b\"temp=", "").replace("'C\\n\"", ""))

        if temp >= safeTemp:
            text = "Temperature has crossed set thresold, current temperature on {} is {}".format(hostName,  temp)
            sendMessage(text)
    except Exception as e:
        text = "error occured on {}, error: {}".format(hostName,  str(e))
        sendMessage(text)

if __name__ == '__main__':
    checkTemperature()


