import os
from pathlib import Path
from datetime import datetime
from handlers.pyprompt import Terminal

pyp = Terminal()
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
path = ROOT_DIR / "assets" / "licenses"

license_list = [file.stem for file in path.glob("*.txt")]

def listlicense():
    pyp.show_list("license", license_list)

def licensegen(licensename, projectname):
    license_file = path / f"{licensename.lower()}.txt"

    if not license_file.exists():
        raise FileNotFoundError(f"License '{licensename}' not found in {path}.")

    with open(license_file, "r") as f:
        content = f.read()

    content = content.replace("[year]", str(datetime.now().year)).replace("[fullname]",projectname)

    with open("LICENSE", "w") as f:
        f.write(content)

    print(f" {licensename.upper()} license added to project root.")
