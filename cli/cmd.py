import typer 
from handlers.cmd import cmd as cook_cmd


app = typer.Typer()


@app.command("add_global")
def cmd_global():
    cook_cmd.add_global()
    
@app.command("add_local")
def cmd_local():
    cook_cmd.add_local()

@app.command("list")
def cmd_list():
    cook_cmd.list()

@app.command("remove")
def cmd_remove():
    cook_cmd.remove()


