
from handlers.utils import *

def add(dir,name):

  isConfFile = checkConfigFile(dirPath=dir)

  if isConfFile:
    return
  else:
    createCookConfigFile(dirPath=dir)

  return
