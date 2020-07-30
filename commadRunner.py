'''
Require this command to executed as root before setting up this for brightness.
echo 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"' | sudo tee -a /etc/udev/rules.d/backlight-permissions.rules

Follow this to make this run as a service
http://devopspy.com/linux/python-script-linux-systemd-service/
'''
import os
import time
import random
import datetime
import telepot
from telepot.loop import MessageLoop
from constants import ownerChatId, botApi, systemName, allowedChatId
from tempNotify import getTemperature
from systemCommands import shutdown, restart, setBrightness, getImage


def handle(msg):
    senderChatId = msg['chat']['id']
    command = msg['text'].lower()

    if len(command) > 1:
        if senderChatId in allowedChatId:
            try:
                if command == 'temp':
                    bot.sendMessage(senderChatId, 'Temperature is {}\'C'.format(getTemperature()))
                elif command == 'shutdown':
                    bot.sendMessage(senderChatId, 'Initiating shutdown')
                    time.sleep(10)
                    shutdown()
                elif command == 'restart':
                    bot.sendMessage(senderChatId, 'Initiating reboot')
                    time.sleep(10)
                    restart()
                elif command.startswith('brightness'):
                       brightVal = int(command.replace('brightness', '').strip())
                       setBrightness(brightVal)
                       bot.sendMessage(senderChatId, 'Brightness set to {}%'.format(brightVal))
                elif command == 'click':
                       fileName = getImage()
                       bot.sendPhoto(senderChatId, open(fileName, "rb"))
                       os.remove(fileName)
                else:
                    bot.sendMessage(senderChatId, 'Invalid command')
            except Exception as e:
                bot.sendMessage(ownerChatId, 'Error occured: {}'.format(str(e)))
        else:
            bot.sendMessage(senderChatId, 'You are not authorized to use this bot!')
            bot.sendMessage(ownerChatId, 'Unauthorized message from {}'.format(str(msg)))
    else:
        bot.sendMessage(senderChatId, 'Invalid command')

bot = telepot.Bot(botApi)

MessageLoop(bot, handle).run_as_thread()

while 1:
    time.sleep(10)
