import picamera
import os
from datetime import datetime

from rpi_backlight import Backlight

def shutdown():
    try:
        os.system('sudo shutdown now')
    except Exception as e:
        raise Exception('Error shutting down: {}'.format(str(e)))

def restart():
    try:
        os.system('sudo reboot now')
    except Exception as e:
        raise Exception('Error restarting down: {}'.format(str(e)))


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
