import os
import requests
import setup
import time
import subprocess
import telepot
from constants import ownerChatId, ownerName
from constants import botApi, doumentDownloadUrl
from userUtils import getAdmins

from teleModel.models import users


bot = telepot.Bot(botApi)
downloadDir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tmp")

def alertOwner(message):
    for admin in getAdmins():
        bot.sendMessage(admin, message)

def sendMessage(chatId, message):
    bot.sendMessage(chatId, message)

def timedeltaToReadable(td):
    return "{} days, {} hours, {} minutes".format(td.days, td.seconds//3600, (td.seconds//60)%60)

def executeCommand(command, sendOut=False):
    errors = ""
    try:
        excutedCmd = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = excutedCmd.communicate()
        if errors:
            return "Error Occured with command execution, error: {}".format(str(errors))
        else:
            retStr = "Command executed successfully!"
            if sendOut:
                retStr += "\n{}".format(output)
    except Exception as e:
        return "Error Occured while execution, error: {}".format(str(errors))

def downloadFile(filepath, fileName):
    try:
        url = doumentDownloadUrl + filepath
        res = requests.get(url, allow_redirects=True)
        downloadPath = os.path.join(downloadDir, fileName)
        with open(downloadPath, 'wb') as download:
            download.write(res.content)
        return downloadPath
    except Exception as e:
        return "Error Occured: {}".format(str(e))

def CreatesuperAdmin():
    try:
        if not users.objects.filter(userId=ownerChatId).exists():
            usersObj = users()
            usersObj.userId = ownerChatId
            usersObj.addedBy = ownerChatId
            usersObj.name = ownerName
            usersObj.isAdmin = True
            usersObj.save()
            sendMessage(ownerChatId, "Super user added successfully!")
    except Exception as e:
        sendMessage(ownerChatId, "Error occured in adding user, error:{}".format(str(e)))

def addRequest(senderChatId, senderName):
    if users.objects.filter(userId=senderChatId).exists():
        sendMessage(senderChatId, "Hi {}, You are already an user of this bot!".format(senderName))
    else:
        for admin in getAdmins():
            sendMessage(admin, "{}/{} is requesting to be added to the bot, use \"add user <chatId>/<userName>\" to add a user".format(senderChatId, senderName))
        sendMessage(senderChatId, "Your add request has been placed successfully")

def upgradeRequest(senderChatId, senderName):
    if users.objects.filter(userId=senderChatId, isAdmin=True).exists():
        sendMessage(senderChatId, "Hi {}, You are already an admin of this bot!".format(senderName))
    else:
        for admin in getAdmins():
            sendMessage(admin, "{}/{} is requesting to be added as a admin to the bot, use \"make admin <chatId>\" to add a user".format(senderChatId, senderName))
        sendMessage(senderChatId, "Your admin request has been placed successfully")

def addedMessage(data):
    newUserChatId, name = data.strip().split("/")
    sendMessage(newUserChatId, "Hi {}, you have been added to the bot, Welcome!!".format(name))

def upgradedMessage(data):
    newAdminChatId = data.strip()
    sendMessage(newAdminChatId, "Hi, you have been added as an admin.")