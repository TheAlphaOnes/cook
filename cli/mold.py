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


@app.command("create")
def template_create():
    """Create a new template from current directory."""
    mold.add(dir=None, templateData=None, ask=True)


@app.command("use")
def template_use(template_id: Annotated[Optional[str], typer.Argument()] = None):
    """Use an existing template."""
    if template_id:
        mold.use(template_id, ask=False)
    else:
        mold.use(None, ask=True)


@app.command("list")
def template_list():
    """List all available templates."""
    mold.list_template()


@app.command("show")
def show():
    """Show template details."""
    mold.show(None, ask=True)


@app.command('update')
def update():
    """Update a template."""
    mold.update(None, ask=True)

