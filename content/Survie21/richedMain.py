import os
try: import requests, termcolor, rich
except ImportError: os.system("python -m pip install rich requests termcolor")

import requests
import json
from termcolor import cprint
from rich.progress import Progress, SpinnerColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
import sys

# Configuration des colonnes de la barre de progression
progress_columns = (
    SpinnerColumn(),
    "[progress.description]{task.description}",
    BarColumn(),
    TaskProgressColumn(),
    "Remaining:",
    TimeRemainingColumn(),
)

# URL des fichiers
Json_url = "https://gustoon.github.io/content/Survie21/mods.json"
ModsFolderUrl = "https://gustoon.github.io/content/Survie21/"

# Gestion du chemin via argument ou input
if len(sys.argv) > 1:
    local_mods_path = os.path.abspath(sys.argv[1])
    with open("path.txt", "w") as f:
        f.write(local_mods_path)
else:
    if not os.path.exists("path.txt"):
        local_mods_path = os.path.abspath(input("Enter the path to the mods folder: "))
        with open("path.txt", "w") as f:
            f.write(local_mods_path)
    else:
        with open("path.txt", "r") as f:
            local_mods_path = os.path.abspath(f.read().strip())

if not os.path.exists(local_mods_path):
    os.makedirs(local_mods_path)
    print("Directory " + local_mods_path + " created")

print("Downloading JSON file from " + Json_url)
jsonResponse = requests.get(Json_url)
print("Download completed with status " + str(jsonResponse.status_code))
with open("mods.json", "wb") as f:
    f.write(jsonResponse.content)

json_file_path = "./mods.json"
mods_url = ModsFolderUrl

with open(json_file_path, "r") as json_file:
    json_obj = json.load(json_file)

print("Mods will be saved in " + local_mods_path)

# Téléchargement avec barre de progression
total = sum(len(value) for value in json_obj.values())

with Progress(*progress_columns) as progress:
    task = progress.add_task("[cyan]Téléchargement des mods...", total=total)
    for value in json_obj.values():
        for element in value:
            local_file_path = os.path.join(local_mods_path, element)
            if not os.path.isfile(local_file_path):
                response = requests.get(mods_url + element)
                with open(local_file_path, "wb") as f:
                    f.write(response.content)
            progress.update(task, advance=1)

# Suppression des fichiers obsolètes avec barre
existing_files = os.listdir(local_mods_path)
expected_files = [element for value in json_obj.values() for element in value]
to_delete = [f for f in existing_files if f not in expected_files]

with Progress(*progress_columns) as progress:
    task = progress.add_task("[red]Suppression des fichiers obsolètes...", total=len(to_delete))
    for filename in to_delete:
        file_path = os.path.join(local_mods_path, filename)
        os.remove(file_path)
        progress.update(task, advance=1)

cprint("FINISHED", "green")
sys.exit(0)