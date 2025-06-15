import typer
from handlers.license.license import license_list
from handlers.license.license import listlicense
from handlers.license import license
from typing_extensions import Annotated
from typing import Optional
from pathlib import Path
from handlers.pyprompt import Terminal
from handlers.utils import *


app = typer.Typer()
pyp = Terminal()



@app.command ("list")
def list ():
    listlicense()
    




@app.command("licensegen")
def licensegen(

    licensename: Annotated[Optional[str], typer.Argument()] = None,
    author: Annotated[Optional[str], typer.Argument()] = None,
):
    
    
    
    if licensename is None:
        licensename = pyp.mcq(license_list, "Select a license")

    if licensename == "none":
        return

# Only reaches here if license is valid
    pyp.show("Enter the name of the author.")
    author = input()
   
