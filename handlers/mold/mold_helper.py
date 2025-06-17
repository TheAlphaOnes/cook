from handlers.pyprompt import Terminal
from handlers import config
from handlers import user
from handlers import backend
from handlers import packer

import sys
import os

pyp = Terminal()


def display_template_info(templateData={},dir=None,fromDir=False,fromConfig=False):

    if fromConfig:
        pyp.display_form(
          title="Template Data",
          fields=[{k: v} for k, v in templateData.items() if k != 'fileID' and k != 'info']
        )

        isMore = pyp.confirm("Display more info? ")
        if isMore: pyp.markdown(templateData['info'])
        return templateData

    if fromDir:
        isConfFile = config.checkConfigFile(dirPath=dir)

        if not isConfFile:
            pyp.error("Cook config file not found")
            sys.exit()


        userConfig = config.getConfigData(dir)
        pyp.display_form(
            title="Template Data",
            fields=[{k: v} for k, v in userConfig['template'].items() if k != 'fileID' and k != 'info']
          )

        if "info" in userConfig.get("template", {}):
          isMore = pyp.confirm("Display more info? ")
          if isMore:
            pyp.markdown(userConfig["template"]["info"])


        return userConfig['template']


def ask_template_by_config(templateData={},dir=None,fromDir=False,fromConfig=False):

    nowTemplateData = {}

    if fromConfig:
        nowTemplateData.update(templateData)

    if fromDir:
        isConfFile = config.checkConfigFile(dirPath=dir)

        if not isConfFile:
            pyp.error("Cook config file not found")
            sys.exit()


        userConfig = config.getConfigData(dir)
        nowTemplateData.update(userConfig.get('template',{}))


    prompt_name  = pyp.ask("template name", default=nowTemplateData.get('name', None))

    prompt_catagory = pyp.ask("template catagory", default=nowTemplateData.get('category', None))

    prompt_version = pyp.ask("template version", default=nowTemplateData.get('version', None))

    pyp.show_list("old template stack", nowTemplateData.get('stack', []))

    prompt_stack = pyp.ask_list("template stack", default_list=nowTemplateData.get('stack', None))

    prompt_github = pyp.ask("template github link", default=nowTemplateData.get('github', None))

    prompt_readme = pyp.choose_file("choose README.md file", start_dir=dir if dir else ".")

    # Get the relative path of the selected README file with respect to dir
    if prompt_readme and os.path.isabs(prompt_readme) and dir:
      prompt_readme = os.path.relpath(prompt_readme, dir)


    return {
      "name": prompt_name,
      "category": prompt_catagory,
      "version": prompt_version,
      "stack": prompt_stack,
      "github": prompt_github,
      "readme": prompt_readme
    }


def ask_template_new(dir:str):
    prompt_name  = pyp.ask("template name",required=True)

    prompt_catagory = pyp.ask("template catagory",required=True)

    prompt_version = pyp.ask("template version",required=True)

    prompt_stack = pyp.ask_list("template stack")

    prompt_github = pyp.ask("template github link",required=True)

    prompt_readme = pyp.choose_file("choose README.md file", start_dir=dir if dir else ".")
    # Get the relative path of the selected README file with respect to dir
    if prompt_readme and os.path.isabs(prompt_readme) and dir:
      prompt_readme = os.path.relpath(prompt_readme, dir)


    return {
      "name": prompt_name,
      "category": prompt_catagory,
      "version": prompt_version,
      "stack": prompt_stack,
      "github": prompt_github,
      "readme": prompt_readme
    }



def getUserTemplatesList():

    userData = user.readUserData()
    response = backend.listUserTemplates(userData['username'])

    try:
        userTemplateList = dict(response)
        templates_list = userTemplateList.get("data", [])


        return templates_list

    except Exception as e:
        pyp.error(f"Error fetching templates: {e}")
        sys.exit()
        return []


def getUserTemplateNames(userTemplateList={}):

    template_names = [template.get("id") for template in userTemplateList]
    return template_names



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



    templteMetaData.update({
        "fileID": uploaded_file_data['file'],
        "id": uuid,
        "info":md
    })




    backend.setMetaUploadTemplate(templteMetaData)
    os.remove(comp_file+".tar.zst")
    spiner_upload.ok("[success]")





