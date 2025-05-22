import typer
# from pathlib import Path
from cli import template
import os


app = typer.Typer()

app.add_typer(template.app,name="mold")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))



@app.command(".")
def ping():
    print("COOK CLI TOOL - PING")



if __name__=="__main__":
    app()
