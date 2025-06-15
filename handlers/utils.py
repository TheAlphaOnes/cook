import platformdirs
import sys
from handlers.pyprompt import Terminal



pyp = Terminal()

def validateArgs(*args):
    if set(args) == {None}:
        return False

    if None in args:
        # print("FILL ALL THE ARGS")
        pyp.error("All arguments are required. Please provide valid inputs.")
        sys.exit()
    else:
        return True


def GetUserDataDir():
    appname = "cook-cli"
    appauthor = "TheAlphaOnes"
    dir_user_dir = platformdirs.user_data_dir(appname, appauthor)

    return dir_user_dir
