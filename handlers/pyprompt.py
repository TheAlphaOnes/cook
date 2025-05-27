import inquirer
from inquirer import themes

from rich.console import Console
from rich.theme import Theme
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.table import Table
from yaspin import yaspin
from tqdm import tqdm


# Define a consistent Rich theme for console outputs
theme = Theme({
    "ok": "green",
    "err": "red",
    "high": "cyan"
})
console = Console(theme=theme)

# Custom Inquirer theme
inquirer_theme = themes.load_theme_from_dict({
    "Question": {
        "mark_color": "yellow",
        "brackets_color": "red",
    },
    "List": {
        "selection_color": "green",
        "selection_cursor": ">"
    }
})


class Terminal:
    """
    A utility class for rich-styled terminal interactions,
    including prompts, tables, markdown rendering, and loaders.
    """

    @staticmethod
    def error(message: str):
        """Prints an error message in red."""
        console.print(message, style="err")

    @staticmethod
    def high(message: str):
        """Prints a highlighted message in cyan."""
        console.print(message, style="high")

    @staticmethod
    def good(message: str):
        """Prints a success message in green."""
        console.print(message, style="ok")

    @staticmethod
    def show(message: str):
        """Prints a plain message to the console."""
        console.print(message)

    @staticmethod
    def ask(prompt_text: str, default: str = None, required: bool = False) -> str:
        """
        Ask the user for input. If required is True, repeat until non-empty.
        """
        while True:
            response = Prompt.ask(f"[green]{prompt_text}[/green]", default=default)
            if required and not response:
                continue
            return response

    @staticmethod
    def confirm(prompt_text: str) -> bool:
        """Ask the user a yes/no confirmation."""
        return Confirm.ask(prompt_text)

    @staticmethod
    def markdown(content: str, style: str = None):
        """Render Markdown content with optional styling."""
        txt = Markdown(content)
        if style == "error":
            console.print(txt,style="err")

        elif style == "good":
            console.print(txt,style="ok")

        elif style == "high":
            console.print(txt,style="high")

        else:
            console.print(txt)

    @staticmethod
    def mcq(options: list, question: str) -> str:
        """Present a multiple-choice question and return the selected answer."""
        questions = [inquirer.List('answer', message=question, choices=options)]
        answers = inquirer.prompt(questions, theme=inquirer_theme)
        return answers.get('answer')

    @staticmethod
    def spinner(message: str):
        """Start a yaspin spinner with a given message."""
        spinner = yaspin(text=message, color="yellow")
        spinner.start()
        # spinner.ok("[Success]") means the operation succeeded.
        # spinner.fail("[Error]") means the operation failed.


        return spinner

    @staticmethod
    def progress(iterable, description: str = "Processing"):
        """
        Wrap an iterable with a tqdm progress bar.

        Usage:
            for item in Terminal.progress(my_list, "Loading items"):
                process(item)
        """
        return tqdm(iterable, desc=description)

    @staticmethod
    def table(title: str, columns: list, rows: list):
        """Render a table with a title, column headers, and row data."""
        table = Table(title=title, expand=True, title_style="ok")
        for col in columns:
            table.add_column(col, justify="center", style="red", overflow="fold")
        for row in rows:
            table.add_row(*[str(cell) for cell in row])
        console.print(table)
