import httpx
import os

from datetime import datetime
from handlers.user import readUserData

from  handlers.const import TAO_SERVER_URL



reqClient = httpx.Client()



BASE = TAO_SERVER_URL

COOK_KEY = readUserData()['key']
COOK_APP = "cli"


headers = {
    "X-COOK-APP": COOK_APP,
    "X-COOK-KEY": COOK_KEY
}


def get_user_by_key(key:str=COOK_KEY):

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
            "file": (filename, f, 'application/zstd')  # or 'application/octet-stream'
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
      "fileID": metaData['fileID']
  }




  response = reqClient.post(url, json=payload, headers=headers)


  return response.json()


