import typer
from handlers.cmd import cmd as cmd_handler
from typing_extensions import Annotated

app = typer.Typer()

@app.command("list")
def cmd_list():
    """List all available command groups"""
    cmd_handler.list()

@app.command("run")
def cmd_run(group: Annotated[str, typer.Argument(help="Command group to run")]):
    """Run all commands in the specified group (e.g. serve, build, clean)"""
    cmd_handler.run(group)

