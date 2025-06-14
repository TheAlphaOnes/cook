import typer
from handlers.license import license

app = typer.Typer()


@app.command("make")
def license_make():
    return



