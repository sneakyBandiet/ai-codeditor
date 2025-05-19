# app.py
# -*- coding: utf-8 -*-
import streamlit as st
from dotenv import load_dotenv
import os
import re
import json
import datetime
from backend.chat_manager import ChatManager
from backend.execution_engine import ExecutionEngine
from backend.file_manager import FileManager

# === Konfiguration & Init ===
st.set_page_config(page_title="Code-Generator mit Claude", layout="wide")
load_dotenv()

# === Session State ===
if "messages" not in st.session_state:
    st.session_state.messages = []
if "editor_code" not in st.session_state:
    st.session_state.editor_code = ""
if "last_execution_result" not in st.session_state:
    st.session_state.last_execution_result = None

# === API & Settings Sidebar ===
with st.sidebar:
    st.header("Einstellungen")

    input_api_key = st.text_input("Anthropic API-Schlüssel", value=os.getenv("ANTHROPIC_API_KEY", ""), type="password")
    if not input_api_key:
        st.error("Bitte gib einen gültigen Anthropic API-Schlüssel ein.")
    model = st.selectbox("Claude-Modell", ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"])
    system_prompt = st.text_area("System-Prompt", value="Du bist ein hilfreicher KI-Assistent, der Python-Code generiert...", height=200)
    auto_execute = st.checkbox("Code automatisch in Editor übernehmen", value=True)

    if st.session_state.messages:
        st.markdown("---")
        st.subheader("Chat-Verlauf")
        export_data = {
            "system_prompt": system_prompt,
            "model": model,
            "messages": st.session_state.messages,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        chat_json = json.dumps(export_data, indent=2)
        b64 = json.dumps(export_data).encode("utf-8")
        st.download_button("Chat-Verlauf herunterladen", chat_json, file_name="chat_history.json")
        if st.button("Chat-Verlauf löschen"):
            st.session_state.clear()
            st.rerun()

# === Hauptinhalt ===
st.title("Code-Generator mit Claude")
chat_manager = ChatManager(input_api_key, model, system_prompt)
engine = ExecutionEngine()

# === File Navigation ===
st.sidebar.subheader("Dateien im Projekt")
project_dir = st.sidebar.text_input("Projektordner", value=".")
file_manager = FileManager(root=project_dir)

try:
    files = file_manager.list_files()
    selected_file = st.sidebar.selectbox("Datei auswählen", files)

    if selected_file:
        file_content = file_manager.read_file(selected_file)
        st.session_state.editor_code = file_content
        st.session_state.current_file = selected_file
except Exception as e:
    st.sidebar.error(f"Fehler beim Laden der Dateien: {e}")

# === Code Editor ===
if "current_file" in st.session_state:
    st.markdown(f"📄 Aktuelle Datei: `{st.session_state.current_file}`")

st.session_state.editor_code = st.text_area(
    "Python-Code bearbeiten:",
    value=st.session_state.editor_code,
    height=250,
    key="editor_text_area"
)


if st.button("💾 Speichern", use_container_width=True):
    try:
        if "current_file" in st.session_state:
            file_manager.save_file(st.session_state.current_file, st.session_state.editor_code)
            st.success("Datei gespeichert.")
        else:
            st.warning("Keine Datei ausgewählt.")
    except Exception as e:
        st.error(f"Fehler beim Speichern: {e}")


# === Chat anzeigen ===
st.header("💬 Chat mit Claude")
for i, msg in enumerate(st.session_state.messages):
    role = "assistant" if msg["role"] not in ["user", "assistant"] else msg["role"]
    with st.chat_message(role):
        content = msg["content"]
        if role == "assistant":
            code_blocks = re.findall(r"```python\s*(.*?)\s*```", content, re.DOTALL)
            if not code_blocks:
                st.markdown(content)
            else:
                parts = re.split(r"```python\s*|\s*```", content)
                for idx, part in enumerate(parts):
                    if idx % 2 == 0:
                        st.markdown(part)
                    else:
                        st.code(part, language="python")
                        if st.button("📝 In Editor übernehmen", key=f"edit_{i}_{idx}"):
                            st.session_state.editor_code = part
                            st.rerun()
        else:
            st.markdown(content)

user_input = st.chat_input("Gib deinen Prompt ein...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        reply = chat_manager.send([m for m in st.session_state.messages if m["role"] in ["user", "assistant"]])
        placeholder.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

        if auto_execute:
            match = re.search(r"```python\s*(.*?)\s*```", reply, re.DOTALL)
            if match:
                st.session_state.editor_code = match.group(1)
        st.rerun()

# === Code Execution Bereich ===
st.markdown("---")
st.header("🐍 Python-Interpreter")
st.session_state.editor_code = st.text_area("Python-Code bearbeiten:", value=st.session_state.editor_code, height=250)

if st.button("▶️ Code ausführen", use_container_width=True, type="primary"):
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
