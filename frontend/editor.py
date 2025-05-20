# ui/editor.py
import streamlit as st

def show_editor():
    st.markdown("---")
    st.header("🐍 Python-Editor & Ausführung")

    if "current_file" in st.session_state:
        st.markdown(f"📄 Aktuelle Datei: `{st.session_state.current_file}`")

    editor_input = st.text_area("📝 Code bearbeiten", value=st.session_state.editor_code, height=300, key="editor_text_area")

    uploaded_file = st.file_uploader("📥 Datei hierher ziehen zum Hochladen und Bearbeiten", type=["py", "txt", "html", "js"])
    if uploaded_file is not None:
        uploaded_code = uploaded_file.read().decode("utf-8")
        st.session_state.editor_code = uploaded_code
        st.session_state.current_file = uploaded_file.name
        st.success(f"Datei '{uploaded_file.name}' hochgeladen und in den Editor geladen.")

    st.session_state.editor_code = editor_input