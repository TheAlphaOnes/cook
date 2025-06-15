from handlers.utils import *
from handlers import config
from handlers.pyprompt import Terminal
from handlers import packer
from handlers import user
from handlers import backend

import sys

pyp = Terminal()



# TODO  in mold/use make it with public + user private
# TODO  in mold/show make it with public + user private and with id
# TODO  in mold/update make it update  user private




def getUserTemplateNames():

    userData = user.readUserData()
    spinner = pyp.spinner("Getting user templates")
    response = backend.listUserTemplates(userData['username'])

    try:
        userTemplateList = dict(response)
        templates = userTemplateList.get("data", [])

        template_names = [template.get("id") for template in templates]

        spinner.ok("[success]")
        return template_names

    except Exception as e:
        spinner.fail("[error]")
        pyp.error(f"Error fetching templates: {e}")
        sys.exit()
        return []


def UploadTemplate(dir):

    config_data = dict(config.getConfigData(dir))

    user_data = user.readUserData()

    uuid = f"{user_data['username']}/@{config_data['template']['category']}/{config_data['template']['name']}"

    check_template = pyp.spinner("validating template data")

    try:
        (isValid, _) = backend.doesTemplatExist(uuid)
        check_template.ok("[success]")

    except:
        check_template.fail("[error]")

    if isValid:

        pyp.error(
            f'template with the name "{config_data['template']['name']}" and category "{config_data['template']['category']}" already exist')

        sys.exit()

    comp_file = os.path.join(
        dir, f"cook_template_{config_data['template']['name']}")

    spiner_comp = pyp.spinner("Compressing template folder...")
    packer.compress_folder(dir, comp_file)
    spiner_comp.ok("[success]")

    spiner_upload = pyp.spinner("Uploading template...")
    uploaded_file_data = backend.upload_template(comp_file+".tar.zst")

    templteMetaData = config_data.copy()



    f = open(templteMetaData['template']['readme'],'r')
    md = f.read()
    f.close()



    # templteMetaData['template'].pop("readme")



    templteMetaData.update({
        "fileID": uploaded_file_data['file'],
        "id": uuid,
        "info":md
    })




    backend.setMetaUploadTemplate(templteMetaData)
    os.remove(comp_file+".tar.zst")
    spiner_upload.ok("[success]")













def add(dir, name, category, version, stack, github,readme):

    isConfFile = config.checkConfigFile(dirPath=dir)

    if isConfFile:
        config.updateConfigData(dirPath=dir, data={
            "template": {
                "name": name,
                "category": category,
                "version": version,
                "stack": stack,
                "github": github,
                "readme":readme
            }
        })
    else:

        template_data = {
            "name": name,
            "category": category,
            "version": version,
            "stack": stack,
            "github": github,
            "readme":readme
        }

        pyp.high("Creating Cook config file...")

        config_data = config.inputConfigData(
            ask_template=False, template_data=template_data)

        config.createCookConfigFile(dirPath=dir, config_data=config_data)

        pyp.good("Cook config file created successfully!")

    UploadTemplate(dir)
    pyp.good("Template added successfully!")


def show(uuid:str, ask=False):

  templateData = {}
  userData = user.readUserData()

  if ask:

    spinner = pyp.spinner("Fetching user templates...")
    try:
      userTemplateList = backend.listUserTemplates(userData['username'])
      templates = userTemplateList.get("data", [])
      spinner.ok("[success]")
    except Exception as e:
      spinner.fail("[error]")
      pyp.error(f"Error fetching templates: {e}")
      return

    template_names = [template.get("id") for template in templates]

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

  pyp.display_form(
    title="Template Data",
    fields=[{k: v} for k, v in templateData.items() if k != 'fileID' and k != 'info']
  )

  isMore = pyp.confirm("Display more info? ")
  if isMore: pyp.markdown(templateData['info'])


def list_template():

    userData = user.readUserData()
    spinner = pyp.spinner("Getting user templates")

    try:
        response = backend.listUserTemplates(userData['username'])
        userTemplateList = dict(response)
        templates = userTemplateList.get("data", [])

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


def use(uuid:str, ask=False):

  templateData = {}
  userData = user.readUserData()

  if ask:

    spinner = pyp.spinner("Fetching user templates...")
    try:
      userTemplateList = backend.listUserTemplates(userData['username'])
      templates = userTemplateList.get("data", [])
      spinner.ok("[success]")
    except Exception as e:
      spinner.fail("[error]")
      pyp.error(f"Error fetching templates: {e}")
      return

    template_names = [template.get("id") for template in templates]

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

  pyp.display_form(
    title="Template Data",
    fields=[{k: v} for k, v in templateData.items() if k != 'fileID' and k != 'info']
  )

  isMore = pyp.confirm("Display more info? ")
  if isMore: pyp.markdown(templateData['info'])


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
      packer.decompress_folder(filePath, newFolderName)
      os.remove(filePath)
      spinner.ok("[success]")
    except Exception as e:
      spinner.fail("[error]")
      pyp.error(f"Error extracting template: {e}")
  else:
    pyp.error("Process cancelled.")


def update(dir,ask=False):

    nowDir = ''

    if ask:
        prompt_dir = pyp.choose_dir("choose template directory")
        nowDir = prompt_dir

    else:
      nowDir = dir

    print(nowDir)
