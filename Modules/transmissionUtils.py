import os

from transmission_rpc import Client

from constants import transmissionHost, transmissionPassword
from constants import transmissionPort, transmissionUser
from utils import  sendMessage, timedeltaToReadable

message = """Torrent ID: {}
Torrent Name: {}
Status: {}
Completed %: {}
Down/Up Ratio: {}
ETA: {}
"""

def getClient():
    client = Client(host=transmissionHost, port=transmissionPort,
            username=transmissionUser, password=transmissionPassword)
    return client

def getAllTorrents():
    ret = []
    client = getClient()
    torrents = client.get_torrents()
    try:
        for client in torrents:
            eta = ""
            try:
                eta = timedeltaToReadable(client.eta)
            except:
                eta = "Unknown ETA"

            ret.append(message.format(client.id, client.name, client.status,
                    client.progress, client.ratio, eta))
        return ret
    except Exception as e:
        return ["Error occured in listing: {}". format(str(e))]

def startTorrent(id):
    client = getClient()
    try:
        torrent = client.get_torrent(int(id.strip()))
        torrent.start()
        return "Torrent {} started successfully!".format(torrent.name)
    except ValueError as v:
        return "Torrent id {} doesn't exists!".format(id)
    except Exception as e:
        return "Error occured in adding user, error:{}".format(str(e))

def stopTorrent(id):
    client = getClient()
    try:
        torrent = client.get_torrent(int(id.strip()))
        torrent.stop()
        return "Torrent {} stopped successfully!".format(torrent.name)
    except ValueError as v:
        return "Torrent id {} doesn't exists!".format(id)
    except Exception as e:
        return "Error occured in adding user, error:{}".format(str(e))

def addMagnetUrl(magnet):
    client = getClient()
    try:
        client.add_torrent(magnet.strip())
        return "Torrent magnet link added successfully!"
    except Exception as e:
        return "Error occured in adding user, error:{}".format(str(e))

def addTorrentFile(filePath):
    client = getClient()
    try:
        with open(filePath, 'rb') as torrentFileContents:
            client.add_torrent(torrentFileContents)
        os.remove(filePath)
        return "Torrent file added successfully"
    except Exception as e:
        return "Error occured in adding Torrent, error:{}".format(str(e))

# if __name__ == "__main__":
#     import json
#     print(json.dumps(getAllTorrents(), indent=4))