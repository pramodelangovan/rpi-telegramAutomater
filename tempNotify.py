import requests
import socket
import subprocess

hostName = socket.gethostname()
hostIp = socket.gethostbyname(hostName)
chatId = "1155196460"
botApi = "1018001497:AAG8ton3K3hZ9xaJkHHMRVpN6aRZVD_qp0A"
url = "https://api.telegram.org/bot{}/sendMessage".format(botApi)
safeTemp = 75.0
flag = False

def send_message(text):
    data = {"chat_id" : chatId, "text" : text}
    requests.get(url, params = data)

def check_message():
    try:

        temp = str(subprocess.Popen("vcgencmd measure_temp", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True).communicate()[0])
        temp = float(temp.replace("b\"temp=", "").replace("'C\\n\"", ""))

        if temp >= safeTemp:
            text = "Temperature has crossed set thresold, current temperature on {} is {}".format(hostName,  temp)
            send_message(text)

    except Exception as e:
        text = "error occured on {}, error: {}".format(hostName,  str(e))
        send_message(text)

if __name__ == '__main__':
    check_message()


