# ui/chat.py
import re
import streamlit as st

def show_chat_interface(chat_manager, auto_execute):
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