import picamera
import os
from datetime import datetime

from rpi_backlight import Backlight

def shutdown():
    os.system('sudo shutdown now')

def restart():
    os.system('sudo reboot now')

def setBrightness(brightVal):
    backlight = Backlight()
    if brightVal > 100:
        brightVal = 100
    elif brightVal < 0: 
        brightVal = 0
    backlight.brightness = brightVal

def getImage():
    with picamera.PiCamera() as camera:
        fileName = "{}.jpg".format(datetime.now().strftime("%b%d%Y%H%M%S"))
        camera.vflip = True
        camera.capture(fileName)
        return fileName
    
