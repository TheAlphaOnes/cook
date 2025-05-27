import typer
from typing import Optional
from typing_extensions import Annotated

from pathlib import Path

from handlers import packer
from handlers.pyprompt import Terminal
from handlers.utils import *
from handlers.mold import mold

app = typer.Typer()




@app.command("add")
def template_create(dir: Annotated[Optional[Path], typer.Argument()] = None,name: Annotated[Optional[str], typer.Argument()] = None):

  print(dir,name)
  RespValidate = validateArgs(dir,name)

  if RespValidate:
    print("WELL DONE")
    mold.add(dir,name)


  elif RespValidate == False:
    print("FILL THE FORM")




@app.command("list")
def template_list():



  return



@app.command("use")
def template_use():



  return
