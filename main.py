import typer
from typing import Optional, List
from typing_extensions import Annotated

from cli import cleanup as cook_cleanup
from cli import stir as cook_stir
from cli import ignite as cook_ignite
from cli import tunnel as cook_tunnel
from cli import layer as cook_layer
from cli import plate as cook_plate
from cli import cmd as cook_cmd
from cli import auth as cook_auth
from cli import slice as cook_slice
from cli import mold
from cli import bite as cook_bite
from cli import api as cook_api
from cli import tool as cook_tool

from handlers.loc import line_of_code
from handlers import tree
from handlers.pyprompt import Terminal
from handlers import const
from handlers import user
from handlers.mold import mold as mold_handler
from handlers.cmd import cmd as cmd_handler
import os
import warnings
from handlers.config import createCookConfigFile, checkConfigFile, getConfigData, inputConfigData
from handlers.const import DEFAULT_COOK_CONFIG

# Suppress all warnings
warnings.filterwarnings("ignore")

pyp = Terminal()

app = typer.Typer(name="cook")

# Add sub-applications to main app
app.add_typer(cook_auth.app, name="auth")
app.add_typer(mold.app, name="mold")
app.add_typer(cook_cmd.app, name="cmd")
app.add_typer(cook_tool.app, name="tool")
app.add_typer(cook_api.app, name="api")
app.add_typer(cook_bite.app, name="bite")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


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


# ====================
# ROOT COMMANDS
# ====================

@app.command("init")
def init():
    """Initialize a new cook project."""
    if checkConfigFile(".") == False:
        pyp.error("cook.conf.json file not found, creating a new one...")
        config_data = inputConfigData(ask_template=False)
        createCookConfigFile(".", config_data)
        pyp.good("cook.conf.json has been created successfully.")


@app.command("bake")
def bake(template_id: Annotated[Optional[str], typer.Argument()] = None):
    """Bake the current project (direct command for 'mold use')."""
    if template_id:
        mold_handler.use(template_id, ask=False)
    else:
        mold_handler.use(uuid=None, ask=True)


@app.command("run")
def run(
    group: Annotated[Optional[str], typer.Argument()] = None,
    hot: bool = typer.Option(False, "--hot", help="Enable hot/stir mode")
):
    """Run the current project (direct command for 'cmd run')."""
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


@app.command("version")
def version():
    """Show version information."""
    pyp.high(const.COOK_BANNER)
    pyp.high(const.COOK_VERSION)


if __name__ == "__main__":
    app()
