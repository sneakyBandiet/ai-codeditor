# frontend/execution.py
import streamlit as st
from backend.debug_logger import DebugLogger
import os
import tkinter as tk
from tkinter import filedialog
from backend.file_manager import FileManager

def show_file_actions():
    with st.expander("📁 Dateioptionen", expanded=False):
        if st.button("📂 Datei öffnen", use_container_width=True, key="open_file_btn"):
            try:
                root = tk.Tk()
                root.withdraw()
                root.attributes("-topmost", True)
                file_path = filedialog.askopenfilename(filetypes=[("Python/Text Dateien", "*.py *.txt"), ("Alle Dateien", "*.*")])
                root.destroy()
                if file_path:
                    folder = os.path.dirname(file_path)
                    file_name = os.path.basename(file_path)
                    file_manager = FileManager(folder)
                    content = file_manager.read_file(file_name)
                    st.session_state.editor_code = content
                    st.session_state.current_file = file_name
                    st.session_state.unsaved_folder = folder
                    st.success(f"Datei geöffnet: {file_name}")
                else:
                    st.warning("Öffnen abgebrochen.")
            except Exception as e:
                st.error(f"Fehler beim Öffnen der Datei: {e}")
        filetype = st.radio("Dateityp wählen:", [".py", ".txt"], horizontal=True)

        if st.button("🆕 Neue Datei", use_container_width=True, key="new_file_btn"):
            try:
                root = tk.Tk()
                root.withdraw()
                root.attributes("-topmost", True)
                file_path = filedialog.asksaveasfilename(defaultextension=filetype, filetypes=[("Ausgewählter Typ", f"*{filetype}")])
                root.destroy()
                if file_path:
                    folder = os.path.dirname(file_path)
                    file_name = os.path.basename(file_path)
                    file_manager = FileManager(folder)
                    file_manager.save_file(file_name, "")  # leere Datei erstellen
                    st.session_state.unsaved_folder = folder  # not treated as project folder
                    st.session_state.current_file = file_name
                    st.session_state.editor_code = file_manager.read_file(file_name)
                    st.success(f"Neue Datei erstellt: {file_name}")
                    return
                    st.session_state.unsaved_folder = folder  # not treated as project folder
                    st.success(f"Neue Datei erstellt: {file_name}")
                else:
                    st.warning("Erstellung abgebrochen.")
            except Exception as e:
                st.error(f"Fehler beim Erstellen der Datei: {e}")

        if st.button("💾 Speichern", use_container_width=True, key="save_file_btn"):
            save_dir = st.session_state.get("project_folder") or st.session_state.get("unsaved_folder")
            if st.session_state.get("current_file") and save_dir:
                file_manager = FileManager(save_dir)
                file_manager.save_file(st.session_state.current_file, st.session_state.editor_code)
                st.success("Datei gespeichert.")
            else:
                st.warning("Keine Datei ausgewählt.")

        if st.button("💾 Save As", use_container_width=True, key="save_as_btn"):
            try:
                root = tk.Tk()
                root.withdraw()
                root.attributes("-topmost", True)
                file_path = filedialog.asksaveasfilename(defaultextension=".py")
                root.destroy()
                if file_path:
                    folder = os.path.dirname(file_path)
                    file_name = os.path.basename(file_path)
                    file_manager = FileManager(folder)
                    file_manager.save_file(file_name, st.session_state.editor_code)
                    st.session_state.current_file = file_name
                    st.session_state.unsaved_folder = folder
                    st.success(f"Datei gespeichert als '{file_name}'")
                else:
                    st.warning("Speichern abgebrochen.")
            except Exception as e:
                st.error(f"Speichern fehlgeschlagen: {e}")

def show_execution_area(engine):
    logger = DebugLogger()

    with st.columns([0.15, 0.85])[0]:
        if st.button("▶️ Ausführen", use_container_width=True, type="primary", key="run_code_btn"):
            result = engine.run_code(st.session_state.editor_code)
            st.session_state.last_execution_result = result
            st.rerun()

    if st.session_state.last_execution_result:
        result = st.session_state.last_execution_result
        if result["success"]:
            formatted = logger.log_output(result["output"])
            st.success("✅ Code erfolgreich ausgeführt")
            st.text_area("Ausgabe:", value=formatted, height=150, disabled=True, key="execution_output_area")
        else:
            formatted = logger.log_error(result["error"])
            st.error("❌ Fehler bei der Ausführung")
            st.text_area("Fehlermeldung:", value=formatted, height=150, disabled=True, key="execution_error_area")
            if st.button("🔄 Fehler an Claude senden"):
                feedback = engine.create_error_feedback(st.session_state.editor_code, result["error"])
                st.session_state.messages.append({"role": "user", "content": feedback})
                st.session_state.last_execution_result = None
                st.rerun()
