import typer
from typing import Optional
from typing_extensions import Annotated

from pathlib import Path

from handlers import packer
from handlers.pyprompt import Terminal
from handlers.utils import *
from handlers.mold import mold
from handlers import config

pyp = Terminal()
app = typer.Typer()



@app.command("add")
def template_create(
    dir: Annotated[Optional[Path], typer.Argument()] = None,
    name: Annotated[Optional[str], typer.Argument()] = None,
    category: Annotated[Optional[str], typer.Argument()] = None,
    version: Annotated[Optional[str], typer.Argument()] = None,
    stack: Annotated[Optional[str], typer.Argument()] = None,
    github: Annotated[Optional[str], typer.Argument()] = None,
    readme: Annotated[Optional[Path], typer.Argument()] = None,):

    RespValidate = validateArgs(dir, name, category, version, stack, github,readme)

    templateData = {
            "name": name,
            "category": category,
            "version": version,
            "stack": stack,
            "github": github,
            "readme":readme
        }


    mold.add(dir=dir,templateData=templateData,ask=not RespValidate)

@app.command("list")
def template_list():
    mold.list_template()
    return


@app.command("use")
def template_use(template_id:Annotated[Optional[str], typer.Argument()] = None):

    RespValidate = validateArgs(template_id)

    mold.use(template_id, ask=not RespValidate)


@app.command("show")
def show(template_id: Annotated[Optional[str], typer.Argument()] = None):

    RespValidate = validateArgs(template_id)

    mold.show(template_id, ask=not RespValidate)


@app.command('update')
def update(dir: Annotated[Optional[Path], typer.Argument()] = None):

    RespValidate = validateArgs(dir)

    mold.update(dir, ask=not RespValidate)

