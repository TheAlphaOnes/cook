import typer
from handlers import ignite as cook_ignite

app = typer.Typer()


@app.command("ignite")
def ignite():
    cook_ignite.ignite()