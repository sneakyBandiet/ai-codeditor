# frontend/chat.py
import streamlit as st
from utils.markdown import extract_code_blocks
from backend.system_prompter import SystemPrompter


def show_chat_interface(chat_manager, auto_execute):
    """Render the AI chat interface, handle message input and output, and apply AI suggestions to the editor."""
    st.markdown("---")
    st.header("💬 Chat mit Claude")

    default_prompt = "You are a code assistant helping to debug Python code."
    task_prompt_options = {
        "🔧 Debugging": default_prompt,
        "⚙️ Optimierung": "You are a performance expert optimizing Python scripts.",
        "📚 Dokumentation": "You are a technical writer generating helpful docstrings and comments.",
        "🧪 Testgenerierung": "You are a QA assistant creating unit tests for the given code.",
        "💬 Freier Assistent": "You are a general code assistant."
    }
    selected_task = st.selectbox("🧠 Aktuelle Aufgabe", list(task_prompt_options.keys()))
    system_prompt = task_prompt_options[selected_task]

    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                code_blocks = extract_code_blocks(msg["content"])
                if code_blocks:
                    for idx, part in enumerate(code_blocks):
                        with st.expander(f"💡 Vorschlag {idx+1}", expanded=True):
                            st.code(part, language="python")
                            if st.button("📝 In Editor übernehmen", key=f"edit_{i}_{idx}"):
                                st.session_state.editor_code = part
                                folder = st.session_state.get("project_folder") or st.session_state.get("unsaved_folder")
                                current_file = st.session_state.get("current_file")
                                if folder and current_file:
                                    from backend.file_manager import FileManager
                                    FileManager(folder).save_file(current_file, part)
                                st.rerun()
                else:
                    st.markdown(msg["content"])
            else:
                st.markdown(msg["content"])

    if prompt := st.chat_input("Gib deinen Prompt ein."):
        current_file = st.session_state.get("current_file")
        editor_code = st.session_state.get("editor_code")

        # Build contextual system prompt
        prompter = SystemPrompter(base_prompt=system_prompt)
        file_summary = editor_code if editor_code else ""
        filename = current_file if current_file else None
        contextual_prompt = prompter.build_prompt(prompt, file_context=file_summary, filename=filename)

        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": contextual_prompt})

        with st.chat_message("assistant"):
            with st.spinner("Claude denkt nach..."):
                ai_response = chat_manager.send(st.session_state.messages)
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
