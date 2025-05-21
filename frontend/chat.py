# frontend/chat.py
import re
import streamlit as st
import json
import datetime
from backend.system_prompter import SystemPrompter

def show_chat_interface(chat_manager, auto_execute):
    st.header("💬 Chat mit Claude")

    # === Let user choose system prompt role dynamically ===
    default_prompt = "You are a helpful code assistant."
    task_prompt_options = {
        "📝 Benutzerdefiniert (aus Einstellungen)": default_prompt,
        "🔧 Debugging": "You are a Python expert helping to debug code safely.",
        "⚙️ Optimierung": "You are a performance expert optimizing Python scripts.",
        "📚 Dokumentation": "You are a technical writer generating helpful docstrings and comments.",
        "🧪 Testgenerierung": "You are a QA assistant creating unit tests for the given code.",
        "💬 Freier Assistent": "You are a general code assistant."
    }
    selected_task = st.selectbox("🧠 Aktuelle Aufgabe", list(task_prompt_options.keys()))
    selected_prompt = task_prompt_options[selected_task]

    prompter = SystemPrompter(base_prompt=selected_prompt)

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
        # === Optional: File context grounding ===
        file_context = None
        if "editor_code" in st.session_state and st.session_state.editor_code:
            file_context = prompter.summarize_code(st.session_state.editor_code)

        full_prompt = prompter.build_prompt(user_input, file_context=file_context)

        # === Store full grounded prompt as user message ===
        st.session_state.messages.append({"role": "user", "content": full_prompt})

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

    # === Export chat history with active system prompt ===
    if st.session_state.messages:
        st.markdown("---")
        export_data = {
            "system_prompt": selected_prompt,
            "model": "claude-*",
            "messages": st.session_state.messages,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        chat_json = json.dumps(export_data, indent=2)
        st.download_button("💾 Chatverlauf exportieren", chat_json, file_name="chat_history.json")
