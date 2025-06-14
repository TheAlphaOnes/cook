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

        prompt_dir = pyp.choose_dir("choose template directory")

        isValid = config.validateConfigTemplateData(prompt_dir)

        pyp.show("Configure the template")

        if isValid:
          userConfig = config.getConfigData(prompt_dir)
          prompt_name  = pyp.ask("template name",default=userConfig['template']["name"])
          prompt_catagory = pyp.ask("template catagory",default=userConfig['template']['category'])
          prompt_version = pyp.ask("template version",default=userConfig['template']['version'])

          pyp.show_list("old template stack", userConfig['template']['stack'])
          prompt_stack = pyp.ask_list("template stack",default_list=userConfig['template']['stack'])

          prompt_github = pyp.ask("template github link",default=userConfig['template']['github'])

          prompt_readme = pyp.choose_file("choose README.md file",start_dir=prompt_dir)


          mold.add(prompt_dir, prompt_name, prompt_catagory, prompt_version, prompt_stack, prompt_github,prompt_readme)

        else:

          prompt_name  = pyp.ask("template name")
          prompt_catagory = pyp.ask("template catagory")
          prompt_version = pyp.ask("template version")
          prompt_stack = pyp.ask_list("template stack")
          prompt_github = pyp.ask("template github link")

          prompt_readme = pyp.choose_file("choose README.md file",start_dir=prompt_dir)



          mold.add(prompt_dir, prompt_name, prompt_catagory, prompt_version, prompt_stack, prompt_github,prompt_readme)

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
def update(template_id: Annotated[Optional[str], typer.Argument()] = None):

    RespValidate = validateArgs(template_id)

    mold.update(template_id, ask=not RespValidate)
