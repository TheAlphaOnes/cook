import typer
from typing import Optional,List
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
from cli import license as cook_licence

from handlers.loc import line_of_code
from handlers import tree
from handlers.pyprompt import Terminal
from handlers import const
from handlers import user
import os
import warnings
from handlers.config import createCookConfigFile,checkConfigFile,getConfigData,inputConfigData
from handlers.const import DEFAULT_COOK_CONFIG

# Suppress all warnings
warnings.filterwarnings("ignore")

pyp = Terminal()

app = typer.Typer()


app.add_typer(cook_auth.app,name="auth")
app.add_typer(mold.app,name="mold")
app.add_typer(cook_licence.app,name="licence")

# app.add_typer(cook_cleanup.app, name="cleanup")
# app.add_typer(cook_stir.app, name= "stir")

# app.add_typer(cook_ignite.app, name="ignite")
# app.add_typer(cook_tunnel.app, name="tunnel")

# app.add_typer(cook_plate.app, name="plate")
app.add_typer(cook_cmd.app, name="cmd")

# app.add_typer(cook_layer.app, name="layer")
# app.add_typer(cook_slice.app,name="slice")



ROOT_DIR = os.path.dirname(os.path.abspath(__file__))



@app.command(".")
def ping():
    pyp.high(const.COOK_BANNER)


@app.command("loc")
def loc(exclude: Annotated[List[str], typer.Argument()] = None):
    line_of_code(".",exclude)


@app.command("tree")
def tree_func(exclude: Annotated[List[str], typer.Argument()] = None):
    tree.show_tree_for_directory(".",exclude if exclude else [])


@app.command("version")
def version():
    pyp.high(const.COOK_BANNER)

    pyp.high(const.COOK_VERSION)

@app.command("init")
def init():
    if checkConfigFile(".")==False:
        pyp.error("cook.conf.json file not found, creating a new one...")
        config_data=inputConfigData(ask_template=False)
        createCookConfigFile(".",config_data)
        pyp.good("cook.conf.json has been created successfully.")



# Follow this for version

# MAJOR.MINOR.PATCH


# MAJOR: Breaking changes (e.g. incompatible APIs)
# MINOR: New features, backward compatible
# PATCH: Bug fixes or small tweaks




if __name__=="__main__":
    app()
