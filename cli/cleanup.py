import typer
from handlers import cleanup as cook_cleanup

app = typer.Typer()

@app.command()
def cleanup():
    cook_cleanup.cleanup()