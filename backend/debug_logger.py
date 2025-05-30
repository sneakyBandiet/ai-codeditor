# backend/debug_logger.py

class DebugLogger:
    """Formats and logs output and error messages for code execution.""" 
    
    def __init__(self):
        self.logs = []

    def log_output(self, output):
        self.logs.append({"type": "output", "content": output})
        return self.format_output(output)

    def log_error(self, error):
        self.logs.append({"type": "error", "content": error})
        return self.format_error(error)

    def format_output(self, output):
        return f"✅ Ausgabe:\n{output.strip()}"

    def format_error(self, error):
        return f"❌ Fehler:\n{error.strip()}"

    def export_logs(self):
        return self.logs