# backend/chat_manager.py

import anthropic

class ChatManager:
    def __init__(self, api_key, model, system_prompt):
        self.api_key = api_key
        self.model = model
        self.system_prompt = system_prompt

    def send(self, messages):
        try:
            client = anthropic.Anthropic(api_key=self.api_key)  # Create client *inside* send()
            response = client.messages.create(
                model=self.model,
                system=self.system_prompt,
                messages=messages,
                max_tokens=4000
            )
            return response.content[0].text
        except Exception as e:
            return f"Fehler bei der Anfrage an Claude: {e}"
