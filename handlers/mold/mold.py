from handlers.utils import *
from handlers import config
from handlers.pyprompt import Terminal
from handlers import packer
from handlers import user
from handlers import backend
from handlers.mold import mold_helper

import sys,os

pyp = Terminal()


# TODO  in mold/update make it update  user private


# PROD
def add(dir,templateData,ask=False):

    nowDir = None
    nowTemplateData = {}


    if ask:
      prompt_dir = pyp.choose_dir("choose template directory")
      isConfFile = config.checkConfigFile(dirPath=prompt_dir)
      isValid = config.validateConfigTemplateData(prompt_dir)

      if isConfFile and isValid:
          template_data = mold_helper.ask_template_by_config(fromDir=True,dir=prompt_dir)
          nowDir = prompt_dir
          nowTemplateData.update(template_data)
      else:
          template_data = mold_helper.ask_template_new(prompt_dir)
          nowDir = prompt_dir
          nowTemplateData.update(template_data)


    else:
      nowDir = dir
      nowTemplateData.update(templateData)


    isConfFile = config.checkConfigFile(dirPath=nowDir)


    if not isConfFile:
        pyp.error("Creating Cook config file...")

        config_data = config.inputConfigData(
              ask_template=False, template_data=nowTemplateData)

        config.createCookConfigFile(dirPath=nowDir, config_data=config_data)

        pyp.good("Cook config file created successfully!")

    else:
        config.updateConfigData(dirPath=nowDir, data={
            "template": nowTemplateData
        })

    mold_helper.UploadTemplate(nowDir)
    pyp.good("Template added successfully!")


# PROD
def show(uuid:str, ask=False):

  templateData = {}
  userData = user.readUserData()

  if ask:

    spinner = pyp.spinner("Fetching user templates...")
    try:

      templates = mold_helper.getUserTemplatesList()
      spinner.ok("[success]")
    except Exception as e:
      spinner.fail("[error]")
      pyp.error(f"Error fetching templates: {e}")
      return

    template_names = mold_helper.getUserTemplateNames(templates)

    if template_names == []:
      pyp.error("No personal templates found. You can see a public template instead.")
      sys.exit()

    selected_uuid = pyp.mcq(question="Choose a template to see", options=template_names)
    for template in templates:
      if template['id'] == selected_uuid:
        templateData.update(template)
        break

  else:
    spinner = pyp.spinner("Fetching template data...")
    try:

      if userData['username'] == uuid.split("/")[0]:
        userTemplateData = backend.getUserTemplateData(uuid=uuid)

      else:
        userTemplateData = backend.getPublicTemplateData(uuid=uuid)

      spinner.ok("[success]")
    except Exception as e:
      spinner.fail("[error]")
      pyp.error(f"Error fetching template data: {e}")
      return

    if not userTemplateData:
      pyp.error("Template not found.")
      return

    templateData = userTemplateData.copy()

  mold_helper.display_template_info(fromConfig=True,templateData=templateData)


# PROD
def list_template():

    spinner = pyp.spinner("Getting user templates")

    try:
        templates = mold_helper.getUserTemplatesList()

        spinner.ok("[success]")

        for template in templates:
            template.pop("fileID", None)
            template.pop("author", None)
            template.pop("github", None)
            template.pop("date", None)
            template.pop("stars",None)
            template.pop("info",None)
            template.pop("downloads",None)


        # Display table
        pyp.table_from_dicts(title="User Templates", items=templates)
    except Exception as e:
        spinner.fail("[error]")
        pyp.error(f"Error fetching templates: {e}")


# PROD
def use(uuid:str, ask=False):

  templateData = {}
  userData = user.readUserData()

  if ask:

    spinner = pyp.spinner("Fetching user templates...")
    try:

      templates = mold_helper.getUserTemplatesList()
      spinner.ok("[success]")

    except Exception as e:
      spinner.fail("[error]")
      pyp.error(f"Error fetching templates: {e}")
      sys.exit()

    template_names = mold_helper.getUserTemplateNames(templates)

    if template_names == []:
      pyp.error("No personal templates found. You can use a public template instead.")
      sys.exit()

    selected_uuid = pyp.mcq(question="Choose a template to use", options=template_names)

    for template in templates:
      if template['id'] == selected_uuid:
        templateData.update(template)
        break

  else:
    spinner = pyp.spinner("Fetching template data...")
    try:

      if userData['username'] == uuid.split("/")[0]:
        userTemplateData = backend.getUserTemplateData(uuid=uuid)

      else:
        userTemplateData = backend.getPublicTemplateData(uuid=uuid)

      spinner.ok("[success]")
    except Exception as e:
      spinner.fail("[error]")
      pyp.error(f"Error fetching template data: {e}")
      return

    if not userTemplateData:
      pyp.error("Template not found.")
      return

    templateData = userTemplateData.copy()


  mold_helper.display_template_info(fromConfig=True,templateData=templateData)

  isUsing = pyp.confirm("Do you want to continue with this template?")

  if isUsing:
    spinner = pyp.spinner("Downloading template...")
    try:
      filePath = backend.downloadTemplate(templateData.get('fileID', ""), templateData.get("id", ""))
      spinner.ok("[success]")
    except Exception as e:
      spinner.fail("[error]")
      pyp.error(f"Error downloading template: {e}")
      return

    newFolderName = pyp.ask("Enter the project folder name")

    spinner = pyp.spinner("Extracting template files...")
    try:
      folderPath = packer.decompress_folder(filePath, newFolderName)


      config.updateConfigData(folderPath,{"name":newFolderName.lower(),"author":userData.get('username','')})

      os.remove(filePath)
      spinner.ok("[success]")
    except Exception as e:
      spinner.fail("[error]")
      pyp.error(f"Error extracting template: {e}")
  else:
    pyp.error("Process cancelled.")


def update(dir,ask=False):

    nowDir = None

    if ask:
        prompt_dir = pyp.choose_dir("choose template directory")
        nowDir = prompt_dir

    else:


      nowDir = dir

    isConfFile = config.checkConfigFile(dirPath=prompt_dir)
    isValid = config.validateConfigTemplateData(prompt_dir)

    if isConfFile and isValid:

        template_data = mold_helper.display_template_info(fromDir=True,dir=nowDir)

        pyp.high("Updating template information...")

        newTemplateData = mold_helper.ask_template_by_config(fromConfig=True,templateData=template_data)

        print(nowDir)
        print(newTemplateData)

    else:
        pyp.error("Cook config not found or not valid")


        


        # config.updateConfigData(dirPath=nowDir, data={
        #   "template": {
        #     "name": prompt_name,
        #     "category": prompt_catagory,
        #     "version": prompt_version,
        #     "stack": prompt_stack,
        #     "github": prompt_github,
        #     "readme": prompt_readme
        #   }
        # })

        # if isRepack:
        #   UploadTemplate(nowDir)
        #   pyp.good("Template updated and uploaded successfully!")
        # else:
        #   pyp.good("Template metadata updated successfully!")


