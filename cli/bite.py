import typer
from handlers.pyprompt import Terminal

app = typer.Typer()
pyp = Terminal()


@app.command("create")
def bite_create():
    """Create a new bite."""
    bite_name = pyp.ask("Enter bite name:")
    # TODO: Implement bite create functionality
    pyp.show(f"Creating bite: {bite_name}")


@app.command("use")
def bite_use():
    """Use an existing bite."""
    bite_name = pyp.ask("Enter bite name to use:")
    # TODO: Implement bite use functionality
    pyp.show(f"Using bite: {bite_name}")


@app.command("list")
def bite_list():
    """List available bites."""
    # TODO: Implement bite list functionality
    pyp.show("Listing available bites...")


@app.command("show")
def bite_show():
    """Show bite details."""
    bite_name = pyp.ask("Enter bite name:")
    # TODO: Implement bite show functionality
    pyp.show(f"Showing bite details: {bite_name}")
