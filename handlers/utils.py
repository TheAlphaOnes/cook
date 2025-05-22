import os


def validateArgs (*args) :

  if set(args) == {None}:
    return False

  if None in args:
    print("FILL ALL THE ARGS")
    return None
  else:
    return True


def getConfigPath(dirPath):
  return os.path.join(dirPath,"cook.conf.json")

def checkConfigFile(dirPath):
  return os.path.isfile(getConfigPath(dirPath))


def createCookConfigFile(dirPath):
  file = open(getConfigPath(dirPath),"w")
  file.close()
  return
