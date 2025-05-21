# frontend/editor.py
from frontend.file_viewer import FileViewer
import streamlit as st

def show_editor():
    viewer = FileViewer()

    if "open_files" not in st.session_state:
        st.session_state.open_files = []

    current_file = st.session_state.get("current_file")
    if current_file and current_file not in st.session_state.open_files:
        st.session_state.open_files.append(current_file)

    open_files = st.session_state.open_files

    if open_files:
        col1, col2 = st.columns([4, 1])
        with col1:
            selected = st.radio("🗂️ Geöffnete Dateien:", open_files, index=open_files.index(current_file), horizontal=True, key="tab_switch")
        with col2:
            if st.button("❌ Datei schließen"):
                if current_file in open_files:
                    st.session_state.open_files.remove(current_file)
                    if st.session_state.open_files:
                        st.session_state.current_file = st.session_state.open_files[0]
                    else:
                        st.session_state.current_file = None
                        st.session_state.editor_code = ""
                    st.rerun()

        st.session_state.current_file = selected
        folder = st.session_state.get("project_folder") or st.session_state.get("unsaved_folder")
        if folder:
            from backend.file_manager import FileManager
            file_manager = FileManager(folder)
            content = file_manager.read_file(selected)
            updated_code = viewer.render(selected, content)
            st.session_state.editor_code = updated_code
    else:
        st.info("Keine Datei geöffnet.")
