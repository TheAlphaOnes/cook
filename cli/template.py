import typer
from typing import Optional
from typing_extensions import Annotated

from pathlib import Path

from handlers import packer
from handlers.pyprompt import Terminal
from handlers.utils import *
from handlers.mold import mold

app = typer.Typer()

# @app.command("scan")
# def scan(dir:Path):
#     if dir.is_dir() :
#         name_temp = Terminal.ask("[green]Enter Your template Name[/green]")
#         resp = Terminal.mcq(['asd',"asdas"],"ter,asd??")
#         # create_devg_file()
#         print(resp,name_temp)
#     else:
#         Terminal.error(f"[yellow]{dir}[/yellow] is Not a Directory, Process Aborted")


@app.command("add")
def template_create(dir: Annotated[Optional[Path], typer.Argument()] = None,name: Annotated[Optional[str], typer.Argument()] = None):

  print(dir,name)
  RespValidate = validateArgs(dir,name)

  if RespValidate:
    print("WELL DONE")
    mold.add(dir,name)


  elif RespValidate == False:
    print("FILL THE FORM")

  else:
    print("FILL ALL THE ARGS")




@app.command("list")
def template_list():



  return



@app.command("use")
def template_use():



  return
