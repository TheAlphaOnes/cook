import gitignorefile
import os
from handlers import pyprompt
from collections import defaultdict
from handlers.const import COOK_INVISIBLE_FF
pyp = pyprompt.Terminal()

def get_all_files_and_folders(root_folder, exclude_list=None):
  if exclude_list is None:
    exclude_list = []

  exclude_list = exclude_list+COOK_INVISIBLE_FF
  gitignore_path = os.path.join(root_folder, ".gitignore")
  matches = None
  if os.path.isfile(gitignore_path):
    matches = gitignorefile.parse(gitignore_path)

  items = []
  for dirpath, dirnames, filenames in os.walk(root_folder):
    if matches and matches(dirpath):
      continue
    if any(os.path.abspath(dirpath).startswith(os.path.abspath(ex)) for ex in exclude_list):
      continue
    items.append(dirpath)
    for filename in filenames:
      full_path = os.path.join(dirpath, filename)
      if matches and matches(full_path):
        continue
      if any(os.path.abspath(full_path).startswith(os.path.abspath(ex)) for ex in exclude_list):
        continue
      items.append(full_path)
  return items

def get_lines_of_code_per_file(file_paths):
  loc_per_file = {}
  for path in file_paths:
    if os.path.isfile(path):
      try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
          loc = sum(1 for line in f if line.strip())
          loc_per_file[path] = loc
      except Exception:
        loc_per_file[path] = None
  return loc_per_file

def summarize_by_extension(loc_dict):
  ext_loc = defaultdict(int)
  for file, lines in loc_dict.items():
    if file == 'TOTAL' or lines is None:
      continue
    _, ext = os.path.splitext(file)
    if ext:
      ext_loc["*"+ext] += lines
    else:
      ext_loc[os.path.basename(file)] += lines
  return ext_loc

def line_of_code(path_dir,exclude_list=None):

  file_list = get_all_files_and_folders(path_dir,exclude_list)
  loc = get_lines_of_code_per_file(file_list)
  total_loc = sum(v for v in loc.values() if v is not None)

  ext_loc = dict(summarize_by_extension(loc))

  pyp.display_form(title='Line Of Code',fields=[{k: v} for k, v in ext_loc.items()] )
  pyp.high(f"Total Line Of Code: {total_loc}")

