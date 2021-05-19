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
import telepot
from telepot.loop import MessageLoop
from constants import botApi, systemName, torrentMimeTypes
from tempNotify import getTemperature
from systemCommands import setBrightness, getImage, commandExecutor
from systemInfo import getSystemInfo
from goldRate import getCurrentGoldRatesByCity
from utils import  addRequest, addedMessage, alertOwner, sendMessage, downloadFile, CreatesuperAdmin, upgradeRequest, upgradedMessage
from userUtils import AddUsers, addAdmin, getUsers, isAdmin
from transmissionUtils import addMagnetUrl, addTorrentFile, getAllTorrents, startTorrent, stopTorrent

def handle(msg):
    if 'text' in msg:
        commandHandler(msg)
    elif 'document' in msg:
        documentHandler(msg)


def documentHandler(msg):
    senderChatId = msg['chat']['id']
    document = msg['document']
    try:
        filepath = bot.getFile(document['file_id'])['file_path']
        name = document['file_name']
        mineType = document['mime_type']
        if mineType in torrentMimeTypes:
            path = downloadFile(filepath, name)
            res = addTorrentFile(path)
            sendMessage(senderChatId, res)
    except Exception as e:
        sendMessage(senderChatId, 'Error occured: 1{}'.format(str(e)))


def commandHandler(msg):
    chat = msg['chat']
    senderChatId = chat['id']
    senderName = "{} {}".format(chat["first_name"], chat["last_name"])
    command = msg['text'].lower()
    if len(command) > 1:
            try:
                if command == "add me":
                    addRequest(senderChatId, senderName)

                elif senderChatId in getUsers():
                    if command == "add admin":
                        upgradeRequest(senderChatId, senderName)

                    elif command == 'temp':
                        sendMessage(senderChatId, 'Temperature is {}\'C'.format(getTemperature()))

                    elif command in ['shutdown', 'reboot']:
                        commandExecutor(senderChatId, command)

                    elif command == 'which bot':
                        sendMessage(senderChatId, systemName)

                    elif command == "stats":
                        stats = getSystemInfo()
                        sendMessage(senderChatId, stats)

                    elif command.startswith('brightness'):
                        brightVal = int(command.replace('brightness', '').strip())
                        setBrightness(brightVal)
                        sendMessage(senderChatId, 'Brightness set to {}%'.format(brightVal))

                    elif command == 'click':
                        fileName = getImage()
                        bot.sendPhoto(senderChatId, open(fileName, "rb"))
                        os.remove(fileName)

                    elif  command == 'gold':
                        rates = getCurrentGoldRatesByCity()
                        sendMessage(senderChatId, rates, parse_mode="HTML")

                    elif command.startswith("add user"):
                        data = command.replace("add user", "")
                        res, status = AddUsers(senderChatId, data)
                        sendMessage(senderChatId, res)
                        if status:
                            addedMessage(data)

                    elif command.startswith("make admin"):
                        data = command.replace("make admin", "")
                        res, status = addAdmin(senderChatId, data)
                        sendMessage(senderChatId, res)
                        if status:
                            upgradedMessage(data)

                    elif command.startswith("restart"):
                        res = commandExecutor(senderChatId, command)
                        sendMessage(senderChatId, res)

                    elif command.startswith("add torrent"):
                        data = command.replace("add torrent", "")
                        res = addMagnetUrl(data)
                        sendMessage(senderChatId, res)

                    elif command in ['list torrents', 'list torrent']:
                        for res in getAllTorrents():
                            sendMessage(senderChatId, res)

                    elif command.startswith("start torrent"):
                        data = command.replace("start torrent", "")
                        res = startTorrent(data)
                        sendMessage(senderChatId, res)

                    elif command.startswith("stop torrent"):
                        data = command.replace("stop torrent", "")
                        res = stopTorrent(data)
                        sendMessage(senderChatId, res)

                    else:
                        sendMessage(senderChatId, 'Invalid command')
                else:
                    sendMessage(senderChatId, 'You are not authorized to use this bot!, try "add me" to place and request')
                    alertOwner('Unauthorized message from {}'.format(str(msg)))
            except Exception as e:
                alertOwner('Error occured: {}'.format(str(e)))
    else:
        sendMessage(senderChatId, 'Invalid command')

CreatesuperAdmin()
bot = telepot.Bot(botApi)

MessageLoop(bot, handle).run_as_thread()

while 1:
    time.sleep(10)
