
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
      "stir": True,
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


NON_CODE_EXTENSIONS = {
    # Image files
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.svg',
    '.webp', '.ico', '.icns',
    # Video files
    '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v',
    '.3gp', '.ogv',
    # Audio files
    '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus',
    # Archive files
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.dmg', '.pkg',
    # Binary/executable files
    '.exe', '.dll', '.so', '.dylib', '.bin', '.app',
    # Font files
    '.ttf', '.otf', '.woff', '.woff2', '.eot',
    # Document files (typically not code)
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    # Database files
    '.db', '.sqlite', '.sqlite3', '.mdb',
    # Other binary/non-text files
    '.pyc', '.pyo', '.class', '.jar', '.war', '.ear'
}
