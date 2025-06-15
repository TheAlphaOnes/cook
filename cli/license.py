import typer
from handlers.license.license import license_list, listlicense
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
    




@app.command("gen")
def licensegen(

    licensename: Annotated[Optional[str], typer.Argument()] = None,
    projectname: Annotated[Optional[str], typer.Argument()] = None,
):
    
    RespValidate = validateArgs(licensename,projectname)
    

    if RespValidate == False:

        licensename = pyp.mcq(license_list, "Select a license")

    if licensename == "none":

        return


    pyp.show("Enter your Project Name.")    
    projectname = input()
