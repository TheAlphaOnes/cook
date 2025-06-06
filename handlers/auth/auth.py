import os
from handlers import user
from handlers import backend
from handlers.pyprompt import Terminal


pyp = Terminal()

def login():

    isUser = user.validateUserData()
    # print("isUser", isUser)
    if isUser:
        print(isUser)
    else:
        key = pyp.ask("Enter your connection key: ",required=True)

        spinerPyp = pyp.spinner("logging in, Please wait while we log you in...")

        try:

          userData = backend.get_user_by_key(key).get("data")
          user.createUserData({
              "username": userData.get("username"),
              "name": userData.get("name"),
              "key": userData.get("connectionKey"),
              "email": userData.get("email"),
              "name": userData.get("name"),
          })
          spinerPyp.ok("[Success]")

        except:
          spinerPyp.fail("[Error]")


def logout():
    isUser = user.validateUserData()
    if not isUser:
      pyp.error("You are not logged in. Please login first.")
    else:
      user.createUserData()


def now():
    isUser = user.validateUserData()

    if not isUser:
      pyp.error("You are not logged in. Please login first.")
    else:
      userData = user.readUserData()

      userDataList = []

      for k, v in userData.items():
        userDataList.append({k:v})

      pyp.display_form("User Data", userDataList)
