# backend/system_prompter.py

class SystemPrompter:
    """Builds system prompts for the AI, including file context and task-specific instructions."""
    def __init__(self, base_prompt="You are a code assistant helping to debug Python code."):
        self.base_prompt = base_prompt

    def build_prompt(self, user_input, file_context=None, filename=None, extra_instructions=None):
        """
        Build a grounded system prompt for Claude based on user input, file context, and optional instructions.
        """
        parts = [f"# Systemrolle:\n{self.base_prompt}"]

        if filename:
            parts.append(f"# Datei: {filename}")

        if extra_instructions:
            parts.append(f"# Zusatzinstruktionen:\n{extra_instructions.strip()}")

        if file_context:
            summary = self.summarize_code(file_context)
            parts.append(f"# Dateikontext (Zusammenfassung):\n{summary}")

        parts.append(f"# Nutzeranfrage:\n{user_input.strip()}")

        return "\n\n".join(parts)

    def summarize_code(self, code):
        """Basic code summarization: return first 20 non-empty lines."""
        lines = [line for line in code.strip().split("\n") if line.strip()]
        summary = "\n".join(lines[:20])
        return summary

    def get_context_from_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return self.summarize_code(content)
        except Exception as e:
            return f"[Fehler beim Laden des Dateikontexts: {e}]"
