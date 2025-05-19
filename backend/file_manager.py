# backend/file_manager.py

import os

class FileManager:
    def __init__(self, root="."):
        self.root = root

    def list_files(self, extensions=None):
        if extensions is None:
            extensions = [".py", ".js", ".html", ".txt"]
        files = []
        for fname in os.listdir(self.root):
            full_path = os.path.join(self.root, fname)
            if os.path.isfile(full_path) and any(fname.endswith(ext) for ext in extensions):
                files.append(fname)
        return sorted(files)

    def read_file(self, filename):
        path = os.path.join(self.root, filename)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def save_file(self, filename, content):
        path = os.path.join(self.root, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
