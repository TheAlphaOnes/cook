import typer

from handlers.auth import auth


app = typer.Typer()


@app.command("login")
def login():
  auth.login()

@app.command("logout")
def logout():
  auth.logout()

@app.command("now")
def now():
  auth.now()
