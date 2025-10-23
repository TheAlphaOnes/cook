import typer
from typing import Optional, List
from typing_extensions import Annotated

from handlers.loc import line_of_code
from handlers import tree
from handlers.pyprompt import Terminal
from handlers.license import license as license_handler

app = typer.Typer()
pyp = Terminal()


@app.command("loc")
def loc(exclude: Annotated[Optional[List[str]], typer.Argument()] = None):
    """Count lines of code in the current directory."""
    line_of_code(".", exclude)


@app.command("tree")
def tree_func(exclude: Annotated[Optional[List[str]], typer.Argument()] = None):
    """Show directory tree structure."""
    exclude_list = exclude if exclude else []
    tree.show_tree_for_directory(".", exclude_list)


@app.command("licence")
def licence():
    """Manage project licence."""
    # Use pyprompt to ask what the user wants to do
    options = ["Generate licence", "List licences", "Show licence details"]
    action = pyp.mcq(options, "What would you like to do?")

    if action == "Generate licence":
        license_handler.gen(licence_name=None, project_name=None, ask=True)
    elif action == "List licences":
        license_handler.list_licence()
    elif action == "Show licence details":
        license_handler.show(licence_name=None, ask=True)


@app.command("status")
def status():
    """Show project status."""
    # TODO: Implement status functionality
    pyp.show("Status command - not yet implemented")
