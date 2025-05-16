import os
try: import requests, termcolor
except ImportError: os.system("python -m pip install requests termcolor") # Install requests and termcolor if not installed

import requests
import json
from termcolor import cprint
import sys

Json_url = "https://gustoon.github.io/content/Survie21/mods.json" # URL for JSON file
ModsFolderUrl = "https://gustoon.github.io/content/Survie21/" # Base Url for mods

# Lecture ou demande du chemin local des mods
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
open("mods.json", "wb").write(jsonResponse.content)
json_file_path = "./mods.json"
mods_url = ModsFolderUrl
with open(json_file_path, "r") as json_file:
    json_obj = json.load(json_file)
print("Mods will be saved in " + local_mods_path)
total = sum(len(value) for value in json_obj.values())
count = 0
for value in json_obj.values():
    for element in value:
        local_file_path = os.path.join(local_mods_path, element)
        if not os.path.isfile(local_file_path):
            print(element + " does not exist, downloading...")
            response = requests.get(mods_url + element)
            print("Download completed with status " + str(response.status_code))
            with open(local_file_path, "wb") as f:
                f.write(response.content)
                f.close()
            count += 1
            cprint(f"Percent : {count / total * 100}", "yellow")
        else:
            count += 1
            print(element + " already exists at " + local_file_path)
            cprint(f"Percent : {count / total * 100}", "yellow")
for filename in os.listdir(local_mods_path):
    local_file_path = os.path.join(local_mods_path, filename)
    if not any(filename == element for value in json_obj.values() for element in value):
        print(filename + " is not present in the JSON, deleting...")
        os.remove(local_file_path)
    else:
        print(filename + " exists at " + local_file_path)

cprint("FINISHED", "green")
sys.exit(0)