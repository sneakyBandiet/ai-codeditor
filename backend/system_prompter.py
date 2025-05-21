# backend/system_prompter.py

class SystemPrompter:
    def __init__(self, base_prompt="You are a code assistant helping to debug Python code."):
        self.base_prompt = base_prompt

    def build_prompt(self, user_input, file_context=None, extra_instructions=None):
        """
        Build a grounded system prompt for Claude based on user input, file context, and optional instructions.
        """
        parts = [f"# Systemrolle:\n{self.base_prompt}"]

        if extra_instructions:
            parts.append(f"# Zusatzinstruktionen:\n{extra_instructions.strip()}")

        if file_context:
            parts.append(f"# Dateikontext:\n{file_context.strip()[:5000]}")  # Cap to avoid prompt bloat

        parts.append(f"# Nutzeranfrage:\n{user_input.strip()}")

        return "\n\n".join(parts)

    def summarize_code(self, code):
        """Basic code summarization (optional stub)"""
        lines = code.strip().split("\n")
        summary = "\n".join(lines[:20])  # Simple start: return first 20 lines
        return summary

    def get_context_from_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return self.summarize_code(content)
        except Exception as e:
            return f"[Fehler beim Laden des Dateikontexts: {e}]"
