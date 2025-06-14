import httpx
import os

from datetime import datetime
from handlers.user import readUserData

from handlers.const import TAO_SERVER_URL
from handlers import user

reqClient = httpx.Client()


BASE = TAO_SERVER_URL

COOK_KEY = readUserData()['key']
COOK_APP = "cli"


headers = {
    "X-COOK-APP": COOK_APP,
    "X-COOK-KEY": COOK_KEY
}


def get_user_by_key(key: str = COOK_KEY):
    """
    Fetch user details by key.
    """

    url = f"{BASE}/api/app/user/getByKey"

    params = {"key": key}

    headers = {
      "X-COOK-APP": COOK_APP,
      "X-COOK-KEY": key
    }

    response = reqClient.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def upload_template(file_path):
    """
    Upload a .tar.zst template file to the server with the correct filename.
    """
    url = f"{BASE}/api/bucket/upload"
    filename = os.path.basename(file_path)

    with open(file_path, 'rb') as f:
        files = {
            # or 'application/octet-stream'
            "file": (filename, f, 'application/zstd')
        }
        response = reqClient.post(url, files=files, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def setMetaUploadTemplate(metaData):

  url = f"{BASE}/api/app/template/create"

  payload = {
      "id": metaData['id'],
      "name": metaData['template']['name'],
      "category": metaData['template']['category'],

      "date": datetime.today().strftime('%Y-%m-%d'),
      "author": metaData['author'],
      "stack": metaData['template']['stack'],
      "github": metaData['template']['github'],
      "version": metaData['template']['version'],
      "info": metaData['info'],
      "fileID": metaData['fileID']
  }

  response = reqClient.post(url, json=payload, headers=headers)

  return response.json()


def doesTemplatExist(uid):
    url = f"{BASE}/api/app/template/get?uid={uid}"



    response = reqClient.get(url, headers=headers)

    if response.json()['data'] == {}:
        print('none')
        return False,{}
    else:
        return (True,response.json())



def listUserTemplates(username):

    url = f"{BASE}/api/app/template/getByuser"

    querystring = {"username":username}

    response = reqClient.get(url, params=querystring , headers=headers)

    # print(response.json())
    # return response.json()
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def downloadTemplate(file_id,name):

    url = f"{BASE}/api/bucket/download"

    querystring = {"file":file_id}

    response = reqClient.get(url, params=querystring,headers=headers)


    # print(response.json())
    file_url = response.json()['file']

    response = reqClient.get(file_url)
    if response.status_code == 200:

      filename = os.path.basename(f"{name}.tar.zst")
      file_path = os.path.join(os.getcwd(), filename)
      with open(file_path, "wb") as f:
        f.write(response.content)
      return file_path

    else:
      response.raise_for_status()



def getUserTemplateData(uuid):

    user_data = user.readUserData()


    url = f"{BASE}/api/app/template/get"

    querystring = {"uid":uuid,"username":user_data['username']}

    response = reqClient.get(url, params=querystring, headers=headers)

    # print(response.json())

    return response.json()['data']


def getPublicTemplateData(uuid):

    url = f"{BASE}/api/app/template/public-get"


    querystring = {"uid":uuid}

    response = reqClient.get(url, params=querystring, headers=headers)

    # print(response.json())

    return response.json()['data']


