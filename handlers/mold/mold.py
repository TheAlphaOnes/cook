from handlers.utils import *
from handlers import config
from handlers.pyprompt import Terminal
from handlers import packer
from handlers import user
from handlers import backend

pyp = Terminal()








def UploadTemplate(dir):

  config_data = dict( config.getConfigData(dir))

  user_data = user.readUserData()

  uuid = f"{user_data['username']}/@{config_data['template']['category']}/{config_data['template']['name']}"

  # print(f"UUID: {uuid}")

  comp_file = os.path.join(dir, f"cook_template_{config_data['template']['name']}")

  spiner_comp = pyp.spinner("Compressing template folder...")
  packer.compress_folder(dir , comp_file)
  spiner_comp.ok("[success]")

  spiner_upload = pyp.spinner("Uploading template to backend...")
  uploaded_file_data = backend.upload_template(comp_file+".tar.zst")

  print(uploaded_file_data)

  templteMetaData =  config_data.copy()
  templteMetaData.update({
    "fileID":uploaded_file_data['file'],
    "id":uuid
  })

  backend.setMetaUploadTemplate(templteMetaData)
  spiner_upload.ok("[success]")


def add(dir, name, category, version, stack, github):

  isConfFile = config.checkConfigFile(dirPath=dir)

  if isConfFile:
    config.updateConfigData(dirPath=dir,data={
       "template": {
         "name": name,
         "category": category,
         "version": version,
         "stack": stack,
         "github": github
       }
     })
  else:

    template_data = {
      "name": name,
      "category": category,
      "version": version,
      "stack": stack,
      "github": github
    }

    pyp.high("Creating Cook config file...")

    config_data = config.inputConfigData(ask_template=False, template_data=template_data)

    config.createCookConfigFile(dirPath=dir,config_data=config_data)

    pyp.good("Cook config file created successfully!")


  UploadTemplate(dir)
  pyp.good("Template added successfully!")





def show(dir):
  isConfFile = config.checkConfigFile(dirPath=dir)

  if not isConfFile:
    pyp.error("Cook config file not found!")
    return

  config_data = config.getConfigData(dirPath=dir)

  if 'template' in config_data:
    template = config_data['template']

    tempForm = []

    for k, v in template.items():
        tempForm.append({k:v})

    pyp.display_form(title="template info",fields=tempForm)


  else:
    pyp.error("No template data found in the configuration.")
