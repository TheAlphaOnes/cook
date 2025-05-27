import typer
from typing import Optional
from typing_extensions import Annotated

from pathlib import Path

from handlers import packer
from handlers.pyprompt import Terminal
from handlers.utils import *
from handlers.mold import mold


pyp = Terminal()
app = typer.Typer()


# name, catagory, author, version, stack, dir, github
@app.command("add")
def template_create(
    dir: Annotated[Optional[Path], typer.Argument()] = None,
    name: Annotated[Optional[str], typer.Argument()] = None,
    catagory: Annotated[Optional[str], typer.Argument()] = None,
    version: Annotated[Optional[str], typer.Argument()] = None,
    stack: Annotated[Optional[str], typer.Argument()] = None,
    github: Annotated[Optional[str], typer.Argument()] = None,
):

    print(dir, name)
    RespValidate = validateArgs(
        dir, name, catagory, version, stack, github)

    if RespValidate:

        stack = stack.split(",")

        # print("WELL DONE",dir, name,catagory, author, version, stack, github)
        # print(stack)
        mold.add(dir, name, catagory, version, stack, github)

    elif RespValidate == False:
        print("FILL THE FORM")

        pyp.ask("template name", "name")
        pyp.ask("template catagory", "catagory")
        pyp.ask()


@app.command("list")
def template_list():

    return


@app.command("use")
def template_use():

    return
