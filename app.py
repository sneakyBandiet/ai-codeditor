# -*- coding: utf-8 -*-
import streamlit as st
import anthropic
from dotenv import load_dotenv
import os
import json
import datetime
import base64
import io
import contextlib
import traceback
import re

# Streamlit-Konfiguration
st.set_page_config(page_title="Code-Generator mit Claude", layout="wide")

# Session-State initialisieren
if "messages" not in st.session_state:
    st.session_state.messages = []
if "editor_code" not in st.session_state:
    st.session_state.editor_code = ""
if "last_execution_result" not in st.session_state:
    st.session_state.last_execution_result = None

# Umgebungsvariablen laden
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# Hilfsfunktionen
def get_download_link(chat_history):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_history_{timestamp}.json"
    chat_json = json.dumps(chat_history, indent=2)
    b64 = base64.b64encode(chat_json.encode()).decode()
    href = f'<a href="data:application/json;base64,{b64}" download="{filename}">Download Chat History (JSON)</a>'
    return href

def execute_python_code(code):
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    result = {"success": False, "output": "", "error": ""}
    
    with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
        try:
            local_vars = {}
            exec(code, {}, local_vars)
            result["success"] = True
        except Exception as e:
            result["error"] = traceback.format_exc()
    
    result["output"] = stdout_buffer.getvalue()
    if result["success"] and stderr_buffer.getvalue():
        result["output"] += "\nWarnings/Errors:\n" + stderr_buffer.getvalue()
    
    return result

def extract_python_code(text):
    code_blocks = []
    pattern = r"```python\s*(.*?)\s*```"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches

def create_error_feedback(code, error):
    return "Ich habe versucht, diesen Code auszuführen:\n\n```python\n" + code + "\n```\n\nAber es gab einen Fehler:\n\n```\n" + error + "\n```\n\nKannst du den Code korrigieren und erklären, was das Problem war?"

# Streamlit rerun Funktion (kompatibel mit älteren und neueren Versionen)
def rerun():
    try:
        st.rerun()
    except:
        try:
            st.experimental_rerun()
        except:
            st.warning("Konnte die Seite nicht neu laden. Bitte lade die Seite manuell neu.")

# Sidebar für Einstellungen
with st.sidebar:
    st.header("Einstellungen")
    
    # API-Schlüssel-Eingabe
    input_api_key = st.text_input("Anthropic API-Schlüssel", 
                                 value=api_key if api_key else "", 
                                 type="password")
    
    if input_api_key:
        api_key = input_api_key
    
    if not api_key:
        st.error("Bitte gib einen gültigen Anthropic API-Schlüssel ein.")
    
    # System-Prompt
    system_prompt = st.text_area(
        "System-Prompt",
        value="Du bist ein hilfreicher KI-Assistent, der Python-Code generiert. Gib immer gut kommentierten, funktionierenden Code zurück. Wenn du Fehlermeldungen erhältst, analysiere sie sorgfältig und verbessere deinen Code entsprechend.",
        height=200
    )
    
    # Modellauswahl
    model = st.selectbox(
        "Claude-Modell",
        ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
    )
    
    # Auto-execute option
    auto_execute = st.checkbox("Code automatisch in Editor übernehmen", value=True)
    
    # Export chat history
    if st.session_state.messages:
        st.markdown("---")
        st.subheader("Chat-Verlauf")
        
        export_data = {
            "system_prompt": system_prompt,
            "model": model,
            "messages": st.session_state.messages,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        download_link = get_download_link(export_data)
        st.markdown(download_link, unsafe_allow_html=True)
        
        if st.button("Chat-Verlauf löschen"):
            st.session_state.messages = []
            st.session_state.editor_code = ""
            st.session_state.last_execution_result = None
            rerun()

# Layout: Chat oben, Interpreter unten
st.title("Code-Generator mit Claude")

# Chat-Bereich
st.header("💬 Chat mit Claude")

# Chat-Verlauf anzeigen
for i, message in enumerate(st.session_state.messages):
    display_role = "assistant" if message["role"] not in ["user", "assistant"] else message["role"]
    
    with st.chat_message(display_role):
        # Extrahiere Python-Code-Blöcke vor der Anzeige
        if message["role"] == "assistant":
            content = message["content"]
            code_blocks = extract_python_code(content)
            
            # Wenn keine Code-Blöcke vorhanden sind, zeige den gesamten Inhalt an
            if not code_blocks:
                st.markdown(content)
            else:
                # Zeige den Text mit Code-Blöcken an
                content_parts = re.split(r"```python\s*|\s*```", content)
                
                for idx, part in enumerate(content_parts):
                    if idx % 2 == 0:  # Text
                        if part.strip():
                            st.markdown(part)
                    else:  # Code
                        code_idx = idx // 2
                        if code_idx < len(code_blocks):
                            st.code(code_blocks[code_idx], language="python")
                            
                            # Zeige den "In Editor übernehmen"-Button
                            if st.button(f"📝 In Editor übernehmen", key=f"edit_{i}_{code_idx}"):
                                st.session_state.editor_code = code_blocks[code_idx]
                                rerun()
        else:
            # Normale Anzeige für User-Nachrichten
            st.markdown(message["content"])

# User-Input
user_prompt = st.chat_input("Gib deinen Prompt ein...")

# Claude API-Anfrage
if api_key and user_prompt:
    client = anthropic.Anthropic(api_key=api_key)
    
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            api_messages = [msg for msg in st.session_state.messages 
                           if msg["role"] in ["user", "assistant"]]
            
            response = client.messages.create(
                model=model,
                max_tokens=4000,
                system=system_prompt,
                messages=api_messages
            )
            
            assistant_response = response.content[0].text
            message_placeholder.markdown(assistant_response)
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            # Wenn Auto-Execute aktiviert ist, übernehme den ersten Code-Block in den Editor
            if auto_execute:
                code_blocks = extract_python_code(assistant_response)
                if code_blocks:
                    st.session_state.editor_code = code_blocks[0]
            
            # Erzwinge ein Neuladen der Seite, um die Code-Blöcke korrekt anzuzeigen
            rerun()
            
        except Exception as e:
            error_message = f"Fehler bei der API-Anfrage: {str(e)}"
            message_placeholder.error(error_message)
            st.session_state.messages.append({"role": "system_error", "content": error_message})
            
elif user_prompt:
    st.error("Bitte gib einen gültigen API-Schlüssel in der Seitenleiste ein, um fortzufahren.")

# Trennlinie
st.markdown("---")

# Python-Interpreter-Bereich
st.header("🐍 Python-Interpreter")

# Editierbarer Code-Editor
st.session_state.editor_code = st.text_area("Python-Code bearbeiten:", 
                                           value=st.session_state.editor_code, 
                                           height=250)

# Ausführen-Button
if st.button("▶️ Code ausführen", use_container_width=True, type="primary"):
    if st.session_state.editor_code:
        # Code ausführen
        result = execute_python_code(st.session_state.editor_code)
        st.session_state.last_execution_result = result
        rerun()

# Ergebnis anzeigen
if st.session_state.last_execution_result:
    result = st.session_state.last_execution_result
    
    if result["success"]:
        st.success("✅ Code erfolgreich ausgeführt")
        if result["output"]:
            st.text_area("Ausgabe:", value=result["output"], height=150, disabled=True)
        else:
            st.info("Keine Ausgabe")
    else:
        st.error("❌ Fehler bei der Ausführung")
        st.text_area("Fehlermeldung:", value=result["error"], height=150, disabled=True)
        
        # Button zum Senden des Fehlers an Claude
        if st.button("🔄 Fehler an Claude senden"):
            feedback = create_error_feedback(st.session_state.editor_code, result["error"])
            st.session_state.messages.append({"role": "user", "content": feedback})
            st.session_state.last_execution_result = None
            rerun()