import json
import os
import subprocess
from handlers.pyprompt import Terminal
from handlers.config import getConfigData

pyp = Terminal()

def list():  
    try:
        config = getConfigData(".")
        cmd_groups = config.get("cmd", {})
        if not cmd_groups:
            pyp.error("No command groups found in cook.conf.json.")
            return
        
        # Convert keys to a Python list to avoid conflict with the built-in list() function
        cmd_group_names = [key for key in cmd_groups.keys()]
        
        # Use the show_list method to display command groups in the same format as license list
        pyp.show_list("Command List", cmd_group_names)
    except Exception as e:
        pyp.error(f"Error listing commands: {e}")

def run(group):
    try:
        config = getConfigData(".")
        print(config)
        cmd_groups = config.get("cmd", {})
        commands = cmd_groups.get(group)
        if not commands:
            pyp.error(f"No commands found for group '{group}'.")
            return

        pyp.good(f"Running commands in group: [high]{group}[/high]")
        for cmd in commands.get("cmd", []):
            pyp.high(f"→ Executing: {cmd}")
            os.system(cmd)
            pyp.good(f"✔ Command succeeded: {cmd}")

    except Exception as e:
        pyp.error(f"Error running commands: {e}")