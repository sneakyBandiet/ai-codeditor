# frontend/file_browser.py
import os
import streamlit as st
from backend.file_manager import FileManager

class FileViewer:
    def __init__(self, root_path):
        self.file_manager = FileManager(root=root_path)

    def render_tree(self, directory=None, base=""):
        if "expanded_dirs" not in st.session_state:
            st.session_state.expanded_dirs = set()

        if directory is None:
            directory = self.file_manager.root

        base_indent = "&nbsp;&nbsp;&nbsp;" * base.count(os.sep)
        entries = sorted(os.listdir(directory))
        for entry in entries:
            full_path = os.path.join(directory, entry)
            rel_path = os.path.relpath(full_path, self.file_manager.root)
            if os.path.isdir(full_path):
                folder_id = rel_path.replace(os.sep, '__')
                is_expanded = folder_id in st.session_state.expanded_dirs
                unique_key = f"folder_{folder_id}_{hash(full_path)}"
                toggle = st.checkbox(f"{base_indent}📁 {entry}", value=is_expanded, key=unique_key)
                if toggle:
                    st.session_state.expanded_dirs.add(folder_id)
                    self.render_tree(full_path, base=rel_path)
                else:
                    st.session_state.expanded_dirs.discard(folder_id)
            elif os.path.isfile(full_path):
                file_key = f"file_{rel_path.replace(os.sep, '__')}_{hash(full_path)}"
                if st.button(f"{base_indent}📄 {entry}", key=file_key):
                    file_content = self.file_manager.read_file(rel_path)
                    st.session_state.editor_code = file_content
                    st.session_state.current_file = rel_path


def show_file_navigation(project_folder):
    viewer = FileViewer(project_folder)
    viewer.render_tree()
