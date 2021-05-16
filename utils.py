import telepot
from constants import ownerChatId, botApi

bot = telepot.Bot(botApi)

def alertOwner(message):
    bot.sendMessage(ownerChatId, message)

def sendMessage(chatId, message):
    bot.sendMessage(chatId, message)

if __name__ == "__main__":
    alertOwner("Sample Message")