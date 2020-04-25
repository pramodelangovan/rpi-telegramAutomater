'''
Require this command to executed as root before setting up this for brightness.
echo 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"' | sudo tee -a /etc/udev/rules.d/backlight-permissions.rules
'''
import time
import random
import datetime
import telepot
from telepot.loop import MessageLoop
from constants import chatId, botApi, systemName
from tempNotify import getTemperature
from systemCommands import shutdown, restart, setBrightness, getImage


def handle(msg):
    chat_id = msg['chat']['id']
    fullCommand = msg['text'].lower().split('@')

    system = fullCommand[0]
    command = fullCommand[1]

    if system == systemName:
        if chat_id == int(chatId):
            try:
                if command == 'temp':
                    bot.sendMessage(chat_id, getTemperature())
                elif command == 'shutdown':
                    bot.sendMessage(chat_id, 'Initiating shutdown')
                    time.sleep(10)
                    shutdown()
                elif command == 'restart':
                    bot.sendMessage(chat_id, 'Initiating reboot')
                    time.sleep(10)
                    restart()
                elif command.startswith('brightness'):
                    brightVal = int(command.replace('brightness', '').strip())
                    setBrightness(brightVal)
                    bot.sendMessage(chat_id, 'Brightness set to {}%'.format(brightVal))
                elif command == 'picture':
                    fileName = getImage()
                    bot.sendPhoto(chat_id=chat_id, photo=open(fileName, "rb"))
                    os.remove(fileName)
                else:
                    bot.sendMessage(chat_id, 'Invalid command, try systemName@command')
            except Exception as e:
                bot.sendMessage(chatId, 'Error occured: {}'.format(str(e)))

        else:
            bot.sendMessage(chat_id, 'You are not authorized to use this bot!')
            bot.sendMessage(int(chatId), 'Unauthorized message from {}'.format(str(msg)))

bot = telepot.Bot(botApi)

MessageLoop(bot, handle).run_as_thread()

while 1:
    time.sleep(10)