import picamera
import os
from datetime import datetime

from rpi_backlight import Backlight

def shutdown():
    try:
        os.system('sudo shutdown now')
    except Exception as e:
        raise Exception('Error shutting down')

def restart():
    try:
        os.system('sudo reboot now')
    except Exception as e:
        raise Exception('Error restarting down')


def setBrightness(brightVal):
    try:
    backlight = Backlight()
    if brightVal > 100:
        brightVal = 100
    elif brightVal < 0: 
        brightVal = 0
    backlight.brightness = brightVal
    except Exception as e:
        raise Exception('error setting brightness')


def getImage():
    with picamera.PiCamera() as camera:
        fileName = "{}.jpg".format(datetime.now().strftime("%b%d%Y%H%M%S"))
        camera.vflip = True
        camera.capture(fileName)
        return fileName
    
