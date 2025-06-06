import os
import json
from handlers.utils import GetUserDataDir
from handlers.const import DEFAULT_USER_DATA


def getUserInfoFile():
    user_data_dir = GetUserDataDir()
    user_file = os.path.join(user_data_dir, "auth/user.json")

    os.makedirs(os.path.dirname(user_file), exist_ok=True)

    if not os.path.isfile(user_file):
        with open(user_file, "w") as outfile:
            json.dump(DEFAULT_USER_DATA, outfile, indent=2)

    return user_file


# CREATE or RESET user data
def createUserData(data: dict = None):
    user_file = getUserInfoFile()
    data_to_write = data if data else DEFAULT_USER_DATA
    with open(user_file, "w") as outfile:
        json.dump(data_to_write, outfile, indent=2)
    return data_to_write


# READ user data
def readUserData():
    user_file = getUserInfoFile()
    with open(user_file, "r") as infile:
        return json.load(infile)


# UPDATE specific fields in user data
def updateUserData(updates: dict):
    user_file = getUserInfoFile()
    with open(user_file, "r") as infile:
        current_data = json.load(infile)

    current_data.update(updates)

    with open(user_file, "w") as outfile:
        json.dump(current_data, outfile, indent=2)

    return current_data


def validateUserData():
    data = readUserData()

    # Check each required field
    for field in DEFAULT_USER_DATA:
        value = data.get(field)

        # If any field is missing or empty, validation fails
        if not value:
            return False

    # All fields are present and non-empty
    return True

