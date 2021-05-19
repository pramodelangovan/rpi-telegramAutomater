import setup

from constants import ownerChatId, ownerName
from teleModel.models import users

def getAdmins():
    ret = []
    for user in users.objects.filter(isAdmin=True).values_list('userId'):
        ret.append(int(user[0]))
    return ret

def getUsers():
    ret = []
    for user in users.objects.all().values_list('userId'):
        ret.append(int(user[0]))
    return ret

def isAdmin(userId):
    return users.objects.filter(userId=userId, isAdmin=True).exists()

def AddUsers(requester, data):
    try:
        requestee, name = data.strip().split("/")
        if isAdmin(requester):
            if not users.objects.filter(userId=requestee).exists():
                usersObj = users()
                usersObj.userId = requestee.strip()
                usersObj.addedBy = requester
                usersObj.name = name.strip()
                usersObj.save()
                return "User added successfully!", True
            else:
                return "User already exists!", False
        else:
            return "You are not authorized to add user!, send \"add admin\" to request admin access", False
    except Exception as e:
        return "Error occured in adding user, error:{}".format(str(e)), False


def addAdmin(requester, data):
    try:
        requestee = data.strip()
        if isAdmin(requester):
            if users.objects.filter(userId=requestee).exists():
                users.objects.filter(userId=requestee).update(isAdmin=True)
                return "User {} upgraded as admin successfully!".format(requestee), True
            else:
                return "User does not exists, send \"add user <telegram id>/<name> to add a user\"", False
        else:
            return "You are not authorized to add user!, send \"add admin\" to request admin access", False
    except Exception as e:
        return "Error occured in adding user, error:{}".format(str(e)), False


if __name__ == "__main__":
    print(getAdmins())