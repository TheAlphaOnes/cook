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

    RespValidate = validateArgs(dir, name, catagory, version, stack, github)

    if RespValidate:

        stack = stack.split(",")

        mold.add(dir, name, catagory, version, stack, github)

    elif RespValidate == False:
        print("FILL THE FORM")

        prompt_name  = pyp.ask("template name")
        prompt_catagory = pyp.ask("template catagory")
        prompt_dir = pyp.choose_dir("choose template directory")
        prompt_version = pyp.ask("template version")
        prompt_stack = pyp.ask_list("template stack (comma separated)")
        prompt_github = pyp.ask("template github link")


        mold.add(prompt_dir, prompt_name, prompt_catagory, prompt_version, prompt_stack, prompt_github)

@app.command("list")
def template_list():

    return


@app.command("use")
def template_use():

    return
