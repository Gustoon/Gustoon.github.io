import os

indexTextStart = """<!DOCTYPE html>
<html>
<head><title>Index of {folderPath}</title></head>
<body>
    <h2>Index of {folderPath}</h2>
    <hr>
    <ul>
        <li>
            <a href='../'>../</a>
        </li>
"""
indexTextEnd = """
    </ul>
</body>
</html>
"""

def index_folder(folderPath):
    print("Indexing: " + folderPath + '/')
    # Getting the content of the folder
    files = os.listdir(folderPath)
    # If Root folder, correcting folder name
    root = folderPath
    if folderPath == '.':
        root = 'Root'
    indexText = indexTextStart.format(folderPath=root)
    for file in files:
        full_path = os.path.join(folderPath, file)
        # Skip index.html files and "Survie21" directory
        if file == 'index.html' or file == 'Survie21':
            continue
        indexText += f"\t\t<li>\n\t\t\t<a href='{file}'>{file}</a>\n\t\t</li>\n"
        # Recursive call to continue indexing
        if os.path.isdir(full_path):
            index_folder(full_path)
    indexText += indexTextEnd
    # Create or override previous index.html
    with open(os.path.join(folderPath, 'index.html'), "w") as index:
        index.write(indexText)

# Indexing root directory (script location)
index_folder('.')
