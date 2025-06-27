# mein_essensplaner/mein_essensplaner/config_loader.py - Der Hausmeister -> Läd meine configs
import yaml
import os

# 1. Globale Pfad Definitionen
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
CONFIG_FILE_PATH = os.path.join(PROJECT_ROOT, "config.yaml")
CREDENTIALS_FILE_PATH = os.path.join(PROJECT_ROOT, "credentials.yaml")

def load_config():
    "Lädt die Konfiguration aus der config.yaml Datei."
    try:
        with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"FEHLER: Konfigurationsdatei nicht gefunden: {CONFIG_FILE_PATH}")
        return None

def load_credentials():
    "Lädt die E-Mail-Zugangsdaten aus der credentials.yaml Datei."
    try:
        with open(CREDENTIALS_FILE_PATH, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"HINWEIS: credentials.yaml wurde nicht gefunden. E-Mail-Funktion ist deaktiviert.")
        return None

if __name__ == "__main__":
    print("--- Teste Konfigurationslader ---")
    config = load_config()
    creds = load_credentials()
    print(f"Konfiguration geladen: {'Ja' if config else 'Nein'}")
    print(f"Zugangsdaten geladen: {'Ja' if creds else 'Nein'}")