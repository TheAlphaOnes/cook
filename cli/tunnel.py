import typer
from handlers import tunnel as cook_tunnel


app = typer.Typer()


@app.command("prep")
def cook_prep():
    cook_tunnel.prep()

@app.command("server")
def cook_serve():
    cook_tunnel.serve()
