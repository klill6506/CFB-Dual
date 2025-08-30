# CFB Dual-Model Handicapping System

This project provides a **college football handicapping model** with two configurations:
- **Aggressive Model** → lower thresholds, more plays
- **Conservative Model** → higher thresholds, fewer but stronger plays

The app is built with **FastAPI** and can be deployed to **Render** (or run locally).

---

## 🚀 Features
- Two independent configs: `config_aggressive.yaml` and `config_conservative.yaml`
- Injuries, situational spots, matchups, explosiveness, weather, and home field
- Option to compare both models at once
- Web API endpoint for easy integration with a GPT or other apps

---

## 📦 Requirements
Python 3.10+  
Install dependencies:
```bash
pip install -r requirements.txt
