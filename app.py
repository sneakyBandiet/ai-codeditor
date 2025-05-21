# app.py
import streamlit as st
import os
import datetime
from backend.chat_manager import ChatManager
from backend.execution_engine import ExecutionEngine
from tkinter import Tk, filedialog

from frontend.editor import show_editor
from frontend.chat import show_chat_interface
from frontend.execution import show_execution_area, show_file_actions
from frontend.file_browser import show_file_navigation
from frontend.search import show_search_bar

st.set_page_config(page_title="Code-Generator mit Claude", layout="wide")

def initialize_session():
    defaults = {
        "messages": [],
        "editor_code": "",
        "last_execution_result": None,
        "project_folder": None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def settings_sidebar():
    with st.sidebar:
        st.header("Einstellungen")
        input_api_key = st.text_input("Anthropic API-Schlüssel", value=os.getenv("ANTHROPIC_API_KEY", ""), type="password")
        if not input_api_key:
            st.error("Bitte gib einen gültigen Anthropic API-Schlüssel ein.")
        model = st.selectbox("Claude-Modell", ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"])
        auto_execute = st.checkbox("Code automatisch in Editor übernehmen", value=True)
        return input_api_key, model, auto_execute

def project_folder_sidebar():
    with st.sidebar:
        st.markdown("---")
        st.subheader("📁 Projektordner")
        if not st.session_state.project_folder:
            if st.button("📂 Projektordner auswählen"):
                try:
                    root = Tk()
                    root.withdraw()
                    root.attributes('-topmost', True)
                    folder_selected = filedialog.askdirectory()
                    root.destroy()
                    if folder_selected:
                        st.session_state.project_folder = folder_selected
                        st.rerun()
                except Exception:
                    st.error("Dateiauswahl nicht möglich: Stelle sicher, dass tkinter installiert ist und du eine lokale Umgebung nutzt.")
        else:
            st.success(f"Aktiv: `{st.session_state.project_folder}`")
            if st.button("❌ Projekt schließen"):
                st.session_state.project_folder = None
                st.session_state.current_file = None
                st.session_state.editor_code = ""
                st.session_state.last_execution_result = None
                st.rerun()

        st.markdown("---")
        st.subheader("📁 Projektdateien")
        if st.session_state.get("project_folder"):
            show_file_navigation(st.session_state.project_folder)

def main():
    initialize_session()
    input_api_key, model, auto_execute = settings_sidebar()
    project_folder_sidebar()
    show_search_bar()
    show_file_actions()

    chat_manager = ChatManager(input_api_key, model, "")
    engine = ExecutionEngine()

    if st.session_state.get("editor_code") is not None:
        show_editor()
        show_execution_area(engine)
    else:
        st.markdown("---")
        st.markdown("### 📂 Kein Projektordner geöffnet")
        st.markdown("> Wähle links einen Ordner aus, um Dateien zu laden und mit dem Editor zu arbeiten.")
        st.markdown("""
<div style="border: 1px solid #ccc; padding: 50px; text-align: center; color: #999;">
    <h2 style="color: #ccc;">Willkommen im Code-Editor</h2>
    <p style="color: #bbb;">Keine Datei geöffnet. Öffne einen Projektordner, um loszulegen.</p>
</div>
""", unsafe_allow_html=True)

    show_chat_interface(chat_manager, auto_execute)

if __name__ == "__main__":
    main()
