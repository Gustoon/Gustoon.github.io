import os
import json

# Fonction pour déterminer si un fichier doit être inclus dans la liste en fonction de son nom
def should_include_file(file_name):
    return file_name.endswith(".jar")

# Chemin d'accès au répertoire à scanner pour les fichiers
dir_path = input("path to mods -> ")

# Liste de fichiers à inclure dans le fichier JSON
file_list = []

# Itération sur chaque fichier dans le répertoire
for file_name in os.listdir(dir_path):
    # Vérifier si le fichier doit être inclus dans la liste
    if should_include_file(file_name):
        file_list.append(file_name)

# Objet JSON à écrire dans le fichier
json_obj = {
    "files": file_list
}

# Chemin d'accès au fichier JSON
json_file_path = "mods.json"

# Écriture de l'objet JSON dans le fichier
with open(json_file_path, "w") as json_file:
    json.dump(json_obj, json_file, indent=4)