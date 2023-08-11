import os

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if not (d.startswith('.') or d == 'venv')]  # Ignore directories starting with a dot or named "venv"
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}|____{}'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}|____{}'.format(subindent, f))

directory_path = "."  # Replace with your directory path
list_files(directory_path)
