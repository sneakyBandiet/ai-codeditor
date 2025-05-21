# Claude Code-Editor mit KI-Unterstützung

Eine moderne, leichtgewichtige Streamlit-Anwendung zum Schreiben, Ausführen und Verbessern von Code mit Unterstützung durch die Anthropic Claude API.

## 🛠️ Installation

1. Klone dieses Repository
2. Aktiviere die virtuelle Umgebung:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
3. Installiere die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```
4. Erstelle eine `.env` Datei und füge deinen Anthropic API-Schlüssel ein:
   ```env
   ANTHROPIC_API_KEY=dein_schlüssel
   ```
5. Starte die Anwendung:
   ```bash
   streamlit run app.py
   ```

## 🚀 Funktionen

### 💻 Code-Editor & Datei-Handling
- Projektordner durchsuchen und Dateien öffnen/speichern
- Unterstützung für `.py`, `.txt`, `.md`, `.json`
- Tabs für mehrere geöffnete Dateien mit Drag & Drop
- Editorhöhe anpassbar

### 💬 KI-Chat mit Claude
- Verschiedene Rollen (Debugging, Dokumentation, Testgenerierung, usw.)
- System-Prompts dynamisch auswählbar
- Dateiinhalt automatisch im Prompt eingebettet (mit optionaler Zusammenfassung)
- Claude schlägt Codeänderungen vor, die direkt übernommen werden können

### 🔍 Internet-Recherche
- Eingebaute Websuche (Serper API)
- Ergebnisse können Claude als Kontext übergeben werden

### 🧪 Code-Ausführung & Debugging
- Python-Code ausführen via `subprocess`
- Konsolen-Output und Fehlermeldungen werden angezeigt
- Fehler können automatisch an Claude zur Analyse gesendet werden

### 🧱 Architektur
Die Architektur folgt einem modularen Aufbau:

- `frontend/` – UI-Komponenten für Editor, Chat, Datei-Explorer, Suche, etc.
- `backend/` – Kernfunktionen wie ChatManager, ExecutionEngine, DebugLogger, FileManager, SystemPrompter
- `utils/` – Hilfsfunktionen (z.B. Markdown-Extraktion)
- `docs/architecture.md` – Enthält ein Mermaid-Diagramm der Systemarchitektur

## 📂 Architekturdiagramm (Mermaid)
Das vollständige Architekturdiagramm findest du in [`docs/architecture.md`](docs/architecture.md).

## 🧪 Beispiel-Start
```bash
streamlit run app.py
```

## ⚠️ Voraussetzungen
- Python 3.10+
- Internetverbindung für Claude API und Websuche (Serper)

---

> Entwickelt für das AI-Modul an der FHGR – 2025
