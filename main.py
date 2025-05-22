import typer
import os
# from pathlib import Path
# from cli import template

app = typer.Typer()
slice_app = typer.Typer(help="Slice-related commands")
app.add_typer(slice_app, name="slice")
# app.add_typer(template.app,name="template")

@app.command()
def ping():
    print("COOK CLI TOOL - PING")

@slice_app.command("add")
def add(add: str):
    print("new " + add + " code snipped added!")

@slice_app.command("share")
def add(share: str):
    print("shared!")

@slice_app.command("list")
def add():
    print("listed")

@slice_app.command("remove")
def add(remove: str):
    print("Removed")

@slice_app.command("")
def add(add: str):
    print("new " + add + " code snipped added!")

@slice_app.command("add")
def add(add: str):
    print("new " + add + " code snipped added!")          

if __name__=="__main__":
    app()
