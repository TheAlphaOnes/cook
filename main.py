import typer
# from pathlib import Path
# from cli import template

app = typer.Typer()

# app.add_typer(template.app,name="template")

@app.command("ping")
def ping():
    print("COOK CLI TOOL - PING")



if __name__=="__main__":
    app()
