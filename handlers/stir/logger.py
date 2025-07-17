from enum import Enum

class Color(Enum):
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def log(color: Color, message: str):
    """Print a colored log message"""
    print(f"{color.value}{message}{Color.RESET.value}")

def info(message: str):
    """Print an info message"""
    log(Color.CYAN, f"{message}")

def success(message: str):
    """Print a success message"""
    log(Color.GREEN, f"{message}")

def warning(message: str):
    """Print a warning message"""
    log(Color.YELLOW, f"{message}")

def error(message: str):
    """Print an error message"""
    log(Color.RED, f"{message}")

def debug(message: str):
    """Print a debug message"""
    log(Color.MAGENTA, f"{message}")