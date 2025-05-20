# frontend/execution.py
import streamlit as st

def show_execution_area(engine):
    st.markdown("---")
    st.markdown("---")
    with st.columns([0.15, 0.85])[0]:
        with st.expander("📁 Dateioptionen", expanded=False):
            if st.button("🆕 Neue Datei", use_container_width=True, key="new_file_btn"):
                st.session_state.editor_code = ""
                st.session_state.current_file = None
                st.success("Neue leere Datei erstellt.")
            if st.button("💾 Speichern", use_container_width=True, key="save_file_btn"):
                if "current_file" in st.session_state and st.session_state.current_file:
                    from backend.file_manager import FileManager
                    file_manager = FileManager(st.session_state.project_folder)
                    file_manager.save_file(st.session_state.current_file, st.session_state.editor_code)
                    st.success("Datei gespeichert.")
                else:
                    st.warning("Keine Datei ausgewählt.")

        new_filename = st.text_input("📄 Speichern unter...", value="", key="save_as_filename")
        if st.button("💾 Save As", use_container_width=True, key="save_as_btn"):
            if new_filename:
                from backend.file_manager import FileManager
                file_manager = FileManager(st.session_state.project_folder)
                file_manager.save_file(new_filename, st.session_state.editor_code)
                st.session_state.current_file = new_filename
                st.success(f"Datei gespeichert als '{new_filename}'")
            else:
                st.warning("Bitte gib einen Dateinamen ein.")

    with st.columns([0.15, 0.85])[0]:
        if st.button("▶️ Ausführen", use_container_width=True, type="primary", key="run_code_btn"):
            result = engine.run_code(st.session_state.editor_code)
            st.session_state.last_execution_result = result
            st.rerun()

    if st.session_state.last_execution_result:
        result = st.session_state.last_execution_result
        if result["success"]:
            st.success("✅ Code erfolgreich ausgeführt")
            st.text_area("Ausgabe:", value=result["output"], height=150, disabled=True, key="execution_output_area")
        else:
            st.error("❌ Fehler bei der Ausführung")
            st.text_area("Fehlermeldung:", value=result["error"], height=150, disabled=True, key="execution_error_area")
            if st.button("🔄 Fehler an Claude senden"):
                feedback = engine.create_error_feedback(st.session_state.editor_code, result["error"])
                st.session_state.messages.append({"role": "user", "content": feedback})
                st.session_state.last_execution_result = None
                st.rerun()
