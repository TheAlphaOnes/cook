import typer
from handlers.license import license as license_handler
from handlers import utils
from handlers.pyprompt import Terminal

from typing import Optional
from typing_extensions import Annotated

app = typer.Typer()
pyp = Terminal()


@app.command("gen")
def license_gen():
    """Generate a license file."""
    license_handler.gen(licence_name=None, project_name=None, ask=True)


@app.command("list")
def license_list():
    """List available licenses."""
    license_handler.list_licence()


@app.command("show")
def license_show():
    """Show license details."""
    license_handler.show(licence_name=None, ask=True)


