import typer
from typing import Optional
from typing_extensions import Annotated

from handlers.auth import auth
from handlers.pyprompt import Terminal

app = typer.Typer()
pyp = Terminal()


@app.command("login")
def login(key: Annotated[Optional[str], typer.Argument()] = None):
    """Login to your Cook account using connection key."""
    if key:
        # Direct login with provided key
        auth.login_with_key(key)
    else:
        # Interactive login
        auth.login()


@app.command("logout")
def logout():
    """Logout from your Cook account and clear stored credentials."""
    auth.logout()


@app.command("now")
def now():
    """Show current authentication status and user information."""
    auth.now()
