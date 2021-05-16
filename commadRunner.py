'''
Require this command to executed as root before setting up this for brightness.
echo 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"' | sudo tee -a /etc/udev/rules.d/backlight-permissions.rules

Follow this to make this run as a service
$ sudo nano /lib/systemd/system/pytel.service

Paste the following:
    [Unit]
    Description=telgram service at port 57777
    After=multi-user.target

    [Service]
    Type=idle
    ExecStart=/usr/bin/python3 /home/pi/piAutomater/commadRunner.py

    [Install]
    WantedBy=multi-user.target

$ sudo chmod 644 /lib/systemd/system/pytel.service
$ sudo systemctl daemon-reload
$ sudo systemctl enable pytel.service
$ sudo reboot now
$ sudo systemctl status pytel.service
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
from systemInfo import getSystemInfo
from goldRate import getCurrentGoldRatesByCity


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
                elif command == 'which bot':
                    bot.sendMessage(senderChatId, systemName)
                    time.sleep(10)
                elif command == "stats":
                    stats = getSystemInfo()
                    bot.sendMessage(senderChatId, stats)
                    time.sleep(10)
                # elif command.startswith('brightness'):
                #        brightVal = int(command.replace('brightness', '').strip())
                #        setBrightness(brightVal)
                #        bot.sendMessage(senderChatId, 'Brightness set to {}%'.format(brightVal))
                # elif command == 'click':
                #        fileName = getImage()
                #        bot.sendPhoto(senderChatId, open(fileName, "rb"))
                #        os.remove(fileName)
                elif  command == 'gold':
                    rates = getCurrentGoldRatesByCity()
                    bot.sendMessage(senderChatId, rates, parse_mode="HTML")
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
