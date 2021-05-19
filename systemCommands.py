import picamera
import os
import time

from datetime import datetime
from rpi_backlight import Backlight

from userUtils import isAdmin
from utils import executeCommand, sendMessage

def setBrightness(brightVal):
    try:
        backlight = Backlight()
        if brightVal > 100:
            brightVal = 100
        elif brightVal < 0:
            brightVal = 0
        backlight.brightness = brightVal
    except Exception as e:
        raise Exception('Error setting brightness: {}'.format(str(e)))


def getImage():
    try:
        with picamera.PiCamera() as camera:
            camera.rotation = 270
            camera.resolution = (1920, 1080)
            camera.brightness = 60
            camera.ISO = 1500
            fileName = "{}.jpg".format(datetime.now().strftime("%b%d%Y%H%M%S"))
            camera.vflip = True
            camera.capture(fileName)
            return fileName
    except Exception as e:
        raise Exception('Error taking picture: {}'.format(str(e)))

def commandExecutor(senderChatId, cmd):
    if isAdmin(senderChatId):
        if cmd == "restart transmission":
            command = "sudo service transmission-daemon restart"
            res = "Tramsmission restarted successfully"
        elif cmd == "restart goldstats":
            command = "sudo service goldstats restart"
            res = "Gold rate service restarted successfully"
        elif cmd == "shutdown":
            command = "sudo shutdown now"
            sendMessage(senderChatId, 'Initiating shutdown')
            time.sleep(10)
            os.system(command)
        elif cmd == "reboot":
            command = "sudo reboot now"
            sendMessage(senderChatId, 'Initiating shutdown')
            time.sleep(10)
            os.system(command)

        if command:
            return "{}, {}".format(executeCommand(command), res)
        else:
            return "Invalid Command!"
    else:
        sendMessage(senderChatId, "You are not authorized to use this Command!, send \"add admin\" to request admin access")