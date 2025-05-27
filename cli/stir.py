import typer
from handlers import stir as cook_stir

app = typer.Typer()

@app.command("stir")
def stir():
    cook_stir.stir()