import typer
# from pathlib import Path
from cli import slice as cook_slice
from cli import template
import os
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")



app = typer.Typer()


app.add_typer(template.app,name="mold")
app.add_typer(cook_slice.app,name="slice")


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))



@app.command(".")
def ping():
    # print("COOK CLI TOOL - PING")
    print(r'''
  _________  ____  __ __
 / ___/ __ \/ __ \/ //_/
/ /__/ /_/ / /_/ / ,<
\___/\____/\____/_/|_|

''')



if __name__=="__main__":
    app()
