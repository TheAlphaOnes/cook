import inquirer
from inquirer import themes

from rich.console import Console
from rich.theme import Theme
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.table import Table
from yaspin import yaspin
from tqdm import tqdm
import os



# TODO:


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
            if response is None or response.strip() == "":
                if default is not None:
                    return default
                if required:
                    console.print("[err]This field is required.[/err]")
                    continue
                return ""
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
            table.add_column(col, justify="left", style="red", overflow="fold")
        for row in rows:
            table.add_row(*[str(cell) for cell in row])
        console.print(table)

    @staticmethod
    def table_from_dicts(title: str, items: list):
      """
      Render a table from a list of dicts.
      Keys become columns, values become rows.
      """
      if not items:
        console.print("[err]No data to display.[/err]")
        return
      columns = list(items[0].keys())
      table = Table(title=title, expand=True, title_style="ok")
      for col in columns:
        table.add_column(str(col), justify="left", style="high", overflow="fold")
      for item in items:
        row = [str(item.get(col, "")) for col in columns]
        table.add_row(*row)
      console.print(table)

    @staticmethod
    def show_list(title: str, items: list):
      """Render a simple list with a title."""
      console.print(f"[ok]{title}[/ok]")
      for idx, item in enumerate(items, 1):
        console.print(f"  [high]{idx}.[/high] {item}")

    @staticmethod
    def ask_list(prompt_text: str, min_items: int = 1,default_list=None) -> list:
      """
      Prompt the user to enter multiple items, one per line.
      Input ends when the user enters an empty line.
      Returns a list of entered items.
      """
      console.print(f"[green]{prompt_text}[/green] (Enter empty line to finish)")
      items = []
      while True:
        item = Prompt.ask(f"{len(items)+1} [red] $ [/red]")
        if not item:
          if len(items) == 0 and default_list is not None:
            items = default_list
            console.print(f"[ok]Using default items: {', '.join(items)}[/ok]")
            return items

          if len(items) >= min_items:
            break
          else:
            console.print(f"[err]Please enter at least {min_items} item(s).[/err]")
            continue
        items.append(item)
      return items


    @staticmethod
    def choose_dir(prompt_text: str = "Select a directory", start_dir: str = None) -> str:
      """
      Prompt the user to either select a directory from a starting directory (default: current working directory)
      and its subdirectories (excluding hidden folders), or enter a directory path manually.
      Only searches up to 2 directory levels deep.
      Returns the selected or entered directory path as a string.
      """
      options = [
        "Choose from list",
        "Enter directory path manually"
      ]
      choice = Terminal.mcq(options, f"How would you like to select the directory")
      if choice == "Enter directory path manually":
        while True:
          dir_path = Terminal.ask("Enter directory path", required=True)
          if os.path.isdir(dir_path):
            return os.path.abspath(dir_path)
          else:
            Terminal.error("Invalid directory path. Please try again.")
      else:
        base_dir = start_dir if start_dir else os.getcwd()
        dir_list = []
        for root, dirs, _ in os.walk(base_dir):
          # Calculate depth relative to base_dir
          rel_path = os.path.relpath(root, base_dir)
          depth = 0 if rel_path == "." else rel_path.count(os.sep) + 1
          if depth > 2:
            # Don't descend further
            dirs[:] = []
            continue
          # Remove hidden directories in-place
          dirs[:] = [d for d in dirs if not d.startswith('.')]
          for d in dirs:
            dir_rel_path = os.path.relpath(os.path.join(root, d), base_dir)
            dir_list.append(dir_rel_path)
        # Always include the base directory itself
        dir_list.insert(0, ".")
        if not dir_list:
          Terminal.error("No directories found.")
          return None
        selected = Terminal.mcq(dir_list, prompt_text)
        return os.path.abspath(os.path.join(base_dir, selected))


    @staticmethod
    def choose_file(prompt_text: str = "Select a file", start_dir: str = None) -> str:
        """
        Prompt the user to either select a file from a directory (default: current working directory)
        and its subdirectories (excluding hidden folders), or enter a file path manually.
        Only searches up to 2 directory levels deep.
        Returns the selected or entered file path as a string.

        Args:
            prompt_text (str): The prompt to display.
            start_dir (str, optional): The directory to start searching from. Defaults to os.getcwd().
        """
        options = [
            "Choose from list",
            "Enter file path manually"
        ]
        choice = Terminal.mcq(options, f"{prompt_text}: How would you like to select the file?")
        if choice == "Enter file path manually":
            while True:
                file_path = Terminal.ask("Enter file path", required=True)
                if os.path.isfile(file_path):
                    return os.path.abspath(file_path)
                else:
                    Terminal.error("Invalid file path. Please try again.")
        else:
            base_dir = start_dir if start_dir else os.getcwd()
            file_list = []
            for root, dirs, files in os.walk(base_dir):
                # Calculate depth relative to base_dir
                rel_path = os.path.relpath(root, base_dir)
                depth = 0 if rel_path == "." else rel_path.count(os.sep) + 1
                if depth > 2:
                    # Don't descend further
                    dirs[:] = []
                    continue
                # Remove hidden directories in-place
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for f in files:
                    file_rel_path = os.path.relpath(os.path.join(root, f), base_dir)
                    file_list.append(file_rel_path)
            if not file_list:
                Terminal.error("No files found.")
                return None
            selected = Terminal.mcq(file_list, prompt_text)
            return os.path.abspath(os.path.join(base_dir, selected))

    @staticmethod
    def display_form(title: str, fields: list) -> None:
      """
      Display a beautiful form with a title and fields using a Rich table.
      Each field should be a dict with a single key-value pair.
      """
      table = Table(title=title, title_style="ok", show_header=False)
      table.add_column("Field", style="high", no_wrap=True)
      table.add_column("Value", style="white")
      for field in fields:
        for key, val in field.items():
          table.add_row(str(key).capitalize(), str(val))
      console.print(table)



    @staticmethod
    def ask_checkbox(name: str, message: str, choices: list) -> list:
        """
        Generic checkbox prompt using inquirer.

        Args:
            name (str): Internal name/key of the prompt.
            message (str): Message/question to show to user.
            choices (list): List of choices to select from.

        Returns:
            list: List of selected options.
        """
        questions = [
            inquirer.Checkbox(
                name,
                message=message,
                choices=choices,
            ),
        ]
        answers = inquirer.prompt(questions)
        return answers.get(name, [])
