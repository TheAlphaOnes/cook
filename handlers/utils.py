import os
import platformdirs
import json

from handlers.pyprompt import Terminal



pyp = Terminal()

def validateArgs(*args):

    if set(args) == {None}:
        return False

    if None in args:
        # print("FILL ALL THE ARGS")
        pyp.error("All arguments are required. Please provide valid inputs.")
        return None
    else:
        return True


def getConfigPath(dirPath):

    return os.path.join(dirPath, "cook.conf.json")


def checkConfigFile(dirPath):

    return os.path.isfile(getConfigPath(dirPath))


def createCookConfigFile(dirPath):

    file = open(getConfigPath(dirPath), "w")
    file.close()

    config_data = {
        "name": "",
        "author": "",
        "stir": True,
        "cmd": {
            "serve": [],
            "clean": []
        },
        "template": {
            "name": "",
            "category": "",
            "date": "",
            "author": "",
            "stack": [],
            "github": ""
        }
    }




    with open(getConfigPath(dirPath), "w") as file:
        json.dump(config_data, file, indent=4)

    return


def GetUserDataDir():
    appname = "cook-cli"
    appauthor = "TheAlphaOnes"
    dir_user_dir = platformdirs.user_data_dir(appname, appauthor)

    return dir_user_dir
