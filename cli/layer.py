import typer
from handlers.layer import layer as cook_layer

app = typer.Typer()


@app.command("stack")
def layer_stack():
    cook_layer.stack()

@app.command("list")
def layer_list():
    cook_layer.list()

@app.command("unstack")
def layer_unstack():
    cook_layer.unstack()


