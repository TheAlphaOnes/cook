import typer
from handlers.license import license as license_handler
from handlers import utils

from typing import Optional
from typing_extensions import Annotated


app = typer.Typer()


@app.command("gen")
def license_gen(licence_name: Annotated[Optional[str], typer.Argument()] = None,project_name: Annotated[Optional[str], typer.Argument()] = None):
    isValid = utils.validateArgs(licence_name,project_name)

    license_handler.gen(licence_name=licence_name,project_name=project_name,ask=not isValid)


@app.command("list")
def license_list():
    license_handler.list_licence()


@app.command("show")
def license_show(licence_name: Annotated[Optional[str], typer.Argument()] = None):
    isValid = utils.validateArgs(licence_name)
    license_handler.show(licence_name=licence_name,ask=not isValid)


