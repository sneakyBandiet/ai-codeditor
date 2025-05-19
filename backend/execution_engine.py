# backend/execution_engine.py

import io
import contextlib
import traceback

class ExecutionEngine:
    def run_code(self, code):
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        result = {"success": False, "output": "", "error": ""}

        with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
            try:
                local_vars = {}
                exec(code, {}, local_vars)
                result["success"] = True
            except Exception:
                result["error"] = traceback.format_exc()

        result["output"] = stdout_buffer.getvalue()
        if result["success"] and stderr_buffer.getvalue():
            result["output"] += "\nWarnings/Errors:\n" + stderr_buffer.getvalue()

        return result

    def create_error_feedback(self, code, error):
        return (
            "Ich habe versucht, diesen Code auszuführen:\n\n"
            f"```python\n{code}\n```\n\n"
            f"Aber es gab einen Fehler:\n\n```\n{error}\n```\n\n"
            "Kannst du den Code korrigieren und erklären, was das Problem war?"
        )