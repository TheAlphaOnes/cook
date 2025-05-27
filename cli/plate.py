import typer
from handlers import plate as cook_plate

app = typer.Typer()


@app.command("share")
def plate_share():
    cook_plate.share()

@app.command("explore")
def plate_explore():
    cook_plate.explore()

@app.command("fetch")
def plate_fetch():
    cook_plate.fetch()
