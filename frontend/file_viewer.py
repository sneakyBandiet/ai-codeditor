# frontend/file_viewer.py
import streamlit as st

class FileViewer:
    """Provides UI for displaying and editing the content of a file in the code editor."""
    def render(self, filename, content):
        if filename:
            st.markdown(f"📄 Aktuelle Datei: `{filename}`")
        else:
            st.markdown("📄 Keine Datei geöffnet")

        return st.text_area(
            "📝 Code bearbeiten",
            value=content,
            height=st.session_state.get("editor_height", 400),
            key="editor_text_area"
        )
