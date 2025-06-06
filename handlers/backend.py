import httpx

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





# import requests

# url = "https://cook-platform.vercel.app/api/app/user/getByKey"
# headers = {
#     "X-COOK-APP": "cli",
#     "X-COOK-KEY": "cook_connection_key_60e1771c-1b66-4596-8c57-30f99383a8b9"
# }
# querystring = {"key":"cook_connection_key_60e1771c-1b66-4596-8c57-30f99383a8b9"}

# response = requests.get(url, params=querystring, headers=headers)

# print(response.json())
