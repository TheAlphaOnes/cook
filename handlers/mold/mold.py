from handlers.utils import *

def add(dir, name, catagory, version, stack, github):

  isConfFile = checkConfigFile(dirPath=dir)

  if isConfFile:
    return
  else:
    createCookConfigFile(dirPath=dir)

  return
