# Claude Code-Generator

Eine Streamlit-Anwendung, die die Anthropic Claude API nutzt, um Python-Code zu generieren.

## Installation

1. Klone dieses Repository
2. Aktiviere die virtuelle Umgebung:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
3. Installiere die Abhängigkeiten: `pip install -r requirements.txt`
4. Füge deinen Anthropic API-Schlüssel in die `.env` Datei ein
5. Starte die Anwendung: `streamlit run app.py`

## Funktionen

- Eingabe von User-Prompts für Code-Generierung
- Anpassbarer System-Prompt
- Auswahl verschiedener Claude-Modelle
- Chat-Verlauf wird während der Sitzung gespeichert
