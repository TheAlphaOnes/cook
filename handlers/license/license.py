import os
from pathlib import Path
from handlers.pyprompt import Terminal
from datetime import datetime
# https://github.com/itsmaxymoo/create-license
# refer this repo to create the license command

pyp = Terminal

path = Path("/home/akshat/TheAlphaOnes/Projects/COOK_Python/cook/assets/licenses")
license_list = [file.stem for file in path.glob("*.txt")]

def listlicense():
    pyp.show_list("license", license_list)
  


def licensegen(licensename, author):
     
    license_file = path / f"{licensename.lower()}.txt"
    

    if not license_file.exists():
     raise FileNotFoundError(f"License '{licensename}' not found in {path}.")


    with open(license_file, "r") as f:
        content = f.read()
    content = content.replace("[year]", str(datetime.now().year)).replace("[fullname]", author)

    with open(license_file, "r") as f:
        content = f.read()

    with open("LICENSE", "w") as f:
        f.write(content)

    print(f"{licensename.upper()} license added.")


