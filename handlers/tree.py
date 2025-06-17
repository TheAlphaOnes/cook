import os
import pathlib
import sys

from rich import print
from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from rich.tree import Tree
import gitignorefile
from handlers.const import COOK_INVISIBLE_FF



def should_exclude(path, exclude_list, matches):
  abs_path = os.path.abspath(str(path))
  for ex in exclude_list:
    if abs_path.startswith(os.path.abspath(ex)):
      return True
  if matches and matches(str(path)):
    return True
  return False

def walk_directory_with_gitignore(directory: pathlib.Path, tree: Tree,my_exclude_list=[]) -> None:
  exclude_list = COOK_INVISIBLE_FF.copy()

  exclude_list = exclude_list + my_exclude_list

  gitignore_path = directory / ".gitignore"
  matches = None
  if gitignore_path.is_file():
    matches = gitignorefile.parse(str(gitignore_path))

  def _walk(path, tree):
    paths = sorted(
      path.iterdir(),
      key=lambda p: (p.is_file(), p.name.lower()),
    )
    for p in paths:
      if p.name.startswith("."):
        continue
      if should_exclude(p, exclude_list, matches):
        continue
      if p.is_dir():
        style = "dim" if p.name.startswith("__") else ""
        branch = tree.add(
          f"[bold magenta]:open_file_folder: [link file://{p}]{escape(p.name)}",
          style=style,
          guide_style=style,
        )
        _walk(p, branch)
      else:
        text_filename = Text(p.name, "green")
        text_filename.highlight_regex(r"\..*$", "bold red")
        text_filename.stylize(f"link file://{p}")
        file_size = p.stat().st_size
        text_filename.append(f" ({decimal(file_size)})", "blue")
        icon =  "📄"
        tree.add(Text(icon) + text_filename)

  _walk(directory, tree)



def show_tree_for_directory(dir_path,my_exclude_list):
  abs_dir = os.path.abspath(dir_path)
  tree = Tree(
    f":open_file_folder: [link file://{abs_dir}]{abs_dir}",
    guide_style="bold bright_blue",
  )
  walk_directory_with_gitignore(pathlib.Path(abs_dir), tree,my_exclude_list=my_exclude_list)
  print(tree)

