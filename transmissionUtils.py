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
        for torrent in torrents:
            eta = ""
            try:
                eta = timedeltaToReadable(torrent.eta)
            except:
                eta = "Unknown ETA"

            ret.append(message.format(torrent.id, torrent.name, torrent.status,
                    torrent.progress, torrent.ratio, eta))
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
        return "Error occured in starting torrent, error:{}".format(str(e))

def stopTorrent(id):
    client = getClient()
    try:
        torrent = client.get_torrent(int(id.strip()))
        torrent.stop()
        return "Torrent {} stopped successfully!".format(torrent.name)
    except ValueError as v:
        return "Torrent id {} doesn't exists!".format(id)
    except Exception as e:
        return "Error occured in stopping torrent, error:{}".format(str(e))

def removeTorrent(id, deleteData=False):
    client = getClient()
    try:
        id = int(id.strip())
        msgStr = "removed" if deleteData else "purged"
        torrent = client.get_torrent(id)
        client.remove_torrent(id, delete_data=deleteData)

        return "Torrent {} {} successfully!".format(torrent.name, msgStr)
    except ValueError as v:
        return "Torrent id {} doesn't exists!".format(id)
    except Exception as e:
        return "Error occured in {} {} torrent, error:{}".format(msgStr, torrent.name, str(e))

def restartTorrent(id):
    client = getClient()
    try:
        id = int(id.strip())
        torrent = client.get_torrent(id)
        magnet = torrent.magnetLink
        client.remove_torrent(id, delete_data=True)
        client.add_torrent(magnet.strip())

        return "Torrent {} restarted successfully!".format(torrent.name)
    except ValueError as v:
        return "Torrent id {} doesn't exists!".format(id)
    except Exception as e:
        return "Error occured in restarting torrent, error:{}".format(str(e))

def restartAllTorrent():
    client = getClient()
    try:
        torrents = client.get_torrents()
        for torrent in torrents:
            magnet = torrent.magnetLink
            client.remove_torrent(torrent.id, delete_data=True)
            client.add_torrent(magnet.strip())

        return "All torrents has been restarted successfully!"

    except Exception as e:
        return "Error occured while restarting all torrents, error:{}".format(str(e))

def purgeAllTorrent():
    client = getClient()
    try:
        torrents = client.get_torrents()
        for torrent in torrents:
            client.remove_torrent(torrent.id, delete_data=True)

        return "All torrents has been purged successfully!"

    except Exception as e:
        return "Error occured while purging all torrents, error:{}".format(str(e))


def addMagnetUrl(magnet):
    client = getClient()
    try:
        client.add_torrent(magnet.strip())
        return "Torrent magnet link added successfully!"
    except Exception as e:
        return "Error occured in adding magnet link, error:{}".format(str(e))

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