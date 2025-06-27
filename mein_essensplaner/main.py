# mein_essensplaner/mein_essensplaner/main.py - Mein Zündschlüssel
import customtkinter as ctk
from .config_loader import load_config
from .data_manager import DataManager
from .app_logic import AppLogic
from .ui_components import App
import os

def run_app():
    # 1. Meine Konfiguration laden
    config = load_config()
    if not config:
        print("Fehler: config.yaml nicht gefunden oder fehlerhaft.")
        return
    
    # 2. Module initialisieren ("Dependency Injection")
    data_manager = DataManager(db_path=config.get('data_file')) # DataManager braucht den Pfad aus der Config.
    app_logic = AppLogic(data_manager, config) # Logik braucht den DataManager und die Config.

    # 3. UI erstellen und mit der Logik verbinden
    app = App(app_logic, config)

    # 4. Sauberes Beenden - WICHTIG!
    app.protocol("WM_DELETE_WINDOW", lambda: (data_manager.close_db(), app.destroy()))

    # 5. Anwendung starten
    app.mainloop() # Startet hier meine Endlosschleife für die UI

if __name__ == "__main__":
    print(f"Starte Essensplaner aus: {os.getcwd()}")
    run_app()