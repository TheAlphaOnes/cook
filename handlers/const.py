
# MAKE SURE THE URL NOT END WITH '/'
TAO_SERVER_URL = "https://cook-platform.vercel.app"
# TAO_SERVER_URL = "http://localhost:3000"


DEFAULT_USER_DATA = {
    "username": "",
    "name": "",
    "email": "",
    "key": ""
}


DEFAULT_COOK_CONFIG = {
      "name": "",
      "author": "",
      # "stir": True,
      "cmd": {
          "serve": [],
          "build": [],
          "clean": []
      },
      "template": {
          "name": "",
          "category": "",
          "date": "",
          "author": "",
          "stack": [],
          "github": "",
          "readme":""
      }
  }

DEFAULT_STIR_CONFIG = {
  "command": [],
  "ignore_patterns": [],
  "watch_dir": ""
}

COOK_BANNER = r'''
  _________  ____  __ __
 / ___/ __ \/ __ \/ //_/
/ /__/ /_/ / /_/ / ,<
\___/\____/\____/_/|_|

  '''


COOK_VERSION = "COOK_VERSION 1.0.0 (alpha)"


COOK_INVISIBLE_FF = [
  ".git",
  "node_modules",
  "__pycache__",
  ".DS_Store",
  ".venv",
  "venv",
  ".vscode",
  ".pytest_cache",
  ".cache",
]
