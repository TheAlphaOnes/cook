import json
import os
from handlers.pyprompt import Terminal
from handlers.const import DEFAULT_COOK_CONFIG
from handlers import user


pyp = Terminal()


def getConfigPath(dirPath):

    return os.path.join(dirPath, "cook.conf.json")


def checkConfigFile(dirPath):

    return os.path.isfile(getConfigPath(dirPath))




def createCookConfigFile(dirPath,config_data=None):

    file = open(getConfigPath(dirPath), "w")
    file.close()

    if config_data is None:
      config_data = DEFAULT_COOK_CONFIG.copy()




    with open(getConfigPath(dirPath), "w") as file:
        json.dump(config_data, file, indent=4)

    return



def getConfigData(dirPath):
    if not checkConfigFile(dirPath):
        createCookConfigFile(dirPath)

    with open(getConfigPath(dirPath), "r") as file:
        config_data = json.load(file)

    return config_data

def updateConfigData(dirPath, data):
    if not checkConfigFile(dirPath):
        createCookConfigFile(dirPath)

    with open(getConfigPath(dirPath), "r") as file:
        config_data = json.load(file)

    config_data.update(data)

    with open(getConfigPath(dirPath), "w") as file:
        json.dump(config_data, file, indent=4)

    return config_data


def validateConfigTemplateData(dirPath):
  if not checkConfigFile(dirPath):
    return False

  try:
    with open(getConfigPath(dirPath), "r") as file:
      config_data = json.load(file)
  except Exception:
    return False

  required_keys = ['template']
  for key in required_keys:
    if key not in config_data:
      return False


  # Check all template values are not empty strings
  for value in config_data['template'].values():
    if value == "":
      return False

  return True


def inputConfigData(ask_template=True, template_data=None):

  userData = user.readUserData()

  config_data = DEFAULT_COOK_CONFIG.copy()

  config_data['name'] = pyp.ask("Enter project name", required=True)
  config_data['stir'] = pyp.confirm("wana stir the project? ")
  config_data['cmd']['serve'] = pyp.ask_list("Enter commands to serve the project")
  config_data['cmd']['build'] = pyp.ask_list("Enter commands to build the project")
  config_data['cmd']['clean'] = pyp.ask_list("Enter commands to clean the project")

  config_data['author'] = userData['username']

# dir, name, category, version, stack, github
  if ask_template:
      isTemplate = pyp.confirm("Do you want to use this as template?")
      if isTemplate:
        config_data['template']['name'] = pyp.ask("Enter template name", required=True)
        config_data['template']['category'] = pyp.ask("Enter template category", required=True)
        config_data['template']['version'] = pyp.ask("Enter template version", required=True)
        config_data['template']['stack'] = pyp.ask_list("Enter template stack")
        config_data['template']['github'] = pyp.ask("Enter template github link", required=True)
        config_data['template']['readme'] = pyp.choose_file("Choose README.md file")

  else:
      if template_data:
          config_data['template'] = template_data


  return config_data



