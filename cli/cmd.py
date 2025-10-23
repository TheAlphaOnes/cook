import typer
from typing import Optional
from typing_extensions import Annotated
from handlers.cmd import cmd as cmd_handler
from handlers.pyprompt import Terminal
from handlers.config import getConfigData

app = typer.Typer()
pyp = Terminal()


def get_available_command_groups():
    """Get list of available command groups from config."""
    try:
        config = getConfigData(".")
        cmd_groups = config.get("cmd", {})
        if not cmd_groups:
            return []
        return list(cmd_groups.keys())
    except Exception:
        return []


@app.command("list")
def cmd_list():
    """List all available command groups."""
    cmd_handler.list()


@app.command("run")
def cmd_run(
    group: Annotated[Optional[str], typer.Argument()] = None,
    hot: bool = typer.Option(False, "--hot", help="Enable hot/stir mode")
):
    """Run commands in a specified group."""
    if group:
        cmd_handler.run(group, hot)
    else:
        # Get available command groups
        available_groups = get_available_command_groups()

        if not available_groups:
            pyp.error("No command groups found in cook.conf.json.")
            return

        # Use MCQ to select command group
        group = pyp.mcq(available_groups, "Select command group to run:")
        cmd_handler.run(group, hot)

