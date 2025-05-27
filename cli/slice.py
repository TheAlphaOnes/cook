import typer
from handlers.slice import slice as cook_slice
from handlers import pyprompt

from time import sleep
app = typer.Typer()

pyp = pyprompt.Terminal()


@app.command("add")
def slice_add():

    cook_slice.add()


@app.command("share")
def slice_share():
    cook_slice.share()
