# backend/file_manager.py
import os

class FileManager:
    def __init__(self, root="."):
        self.root = root

    def list_files(self, extensions=None):
        if extensions is None:
            extensions = [".py", ".js", ".html", ".txt"]
        files = []
        for dirpath, _, filenames in os.walk(self.root):
            for fname in filenames:
                if any(fname.endswith(ext) for ext in extensions):
                    full_path = os.path.relpath(os.path.join(dirpath, fname), self.root)
                    files.append(full_path)
        return sorted(files)

    def read_file(self, filename):
        filepath = os.path.join(self.root, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    def save_file(self, filename, content):
        filepath = os.path.join(self.root, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
