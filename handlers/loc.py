import os
import gitignorefile
from collections import defaultdict

from handlers import pyprompt
from handlers.const import COOK_INVISIBLE_FF,NON_CODE_EXTENSIONS

# Initialize terminal prompt
pyp = pyprompt.Terminal()

# Extensions for media files, binary files, and other non-code files to exclude


def is_code_file(file_path):
    """Check if a file is likely to contain code (not a binary/media file)."""
    _, ext = os.path.splitext(file_path.lower())

    # Exclude files with non-code extensions
    if ext in NON_CODE_EXTENSIONS:
        return False

    # Additional check: try to detect binary files by reading a small sample
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)  # Read first 1KB
            # If there are null bytes, it's likely a binary file
            if b'\x00' in chunk:
                return False
    except Exception:
        # If we can't read the file, assume it's not a code file
        return False

    return True


def get_all_files_and_folders(root_folder, exclude_list=None):
    """Get all files and folders in a directory, respecting .gitignore and exclude list."""
    if exclude_list is None:
        exclude_list = []

    exclude_list = exclude_list + COOK_INVISIBLE_FF
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
    """Count lines of code for each file, excluding empty lines and non-code files."""
    loc_per_file = {}

    for path in file_paths:
        if os.path.isfile(path):
            # Only count lines for code files, skip media/binary files
            if not is_code_file(path):
                continue

            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    loc = sum(1 for line in f if line.strip())
                    loc_per_file[path] = loc
            except Exception:
                loc_per_file[path] = None

    return loc_per_file


def summarize_by_extension(loc_dict):
    """Group line counts by file extension."""
    ext_loc = defaultdict(int)

    for file, lines in loc_dict.items():
        if file == 'TOTAL' or lines is None:
            continue

        _, ext = os.path.splitext(file)
        if ext:
            ext_loc["*" + ext] += lines
        else:
            ext_loc[os.path.basename(file)] += lines

    return ext_loc


def line_of_code(path_dir, exclude_list=None):
    """
    Count lines of code in a directory, excluding media files, binary files,
    and other non-code files (images, videos, audio, archives, etc.).

    Args:
        path_dir (str): Directory path to analyze
        exclude_list (list, optional): Additional paths to exclude

    Returns:
        None: Displays results using pyprompt
    """
    file_list = get_all_files_and_folders(path_dir, exclude_list)
    loc = get_lines_of_code_per_file(file_list)
    total_loc = sum(v for v in loc.values() if v is not None)

    ext_loc = dict(summarize_by_extension(loc))

    pyp.display_form(
        title='Line Of Code',
        fields=[{k: v} for k, v in ext_loc.items()]
    )
    pyp.high(f"Total Line Of Code: {total_loc}")

