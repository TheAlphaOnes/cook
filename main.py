import typer
import os
# from pathlib import Path
# from cli import template

app = typer.Typer()

# app.add_typer(template.app,name="template")

@app.command()
def ping():
    print("COOK CLI TOOL - PING")


@app.command("file")
def file(file_name: str):
    with open(file_name, "w") as f:
       print(file_name + " was created!")
       f.write(''' 
print ("hello world")
''')
            

if __name__=="__main__":
    app()
