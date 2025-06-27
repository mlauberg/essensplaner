# mein_essensplaner/mein_essensplaner/data_manager.py - Das Gedächnis
from tinydb import TinyDB, Query # TinyDB Biblothek einfache JSON-Datenbank
import os

class DataManager:
    def __init__(self, db_path="events_db.json"):

        # 1. Pfad für Datenbankdatei
        project_root = os.path.dirname(os.path.dirname(__file__))
        full_db_path = os.path.join(project_root, db_path)

        # 2. Datenbankverbindung öffnen
        self.db = TinyDB(full_db_path, indent=4, ensure_ascii=False)

        # 3. Tabelle auswählen
        self.events = self.db.table('events')

        # 4. Query Objekt vorbereiten
        self.EventQuery = Query()

    def get_event(self, date_str):
        # Sucht in der events Tabelle nach einem Dokument, bei dem das Feld 
        # 'date' = date_str und dann gibt es das erste gefundene Dokument zurück.
        return self.events.get(self.EventQuery.date == date_str)

    def update_event(self, date_str, event_data):
        # upsert ist eine Kombi aus update und insert.
        # 1. Es sucht im Dokument, wo 'date' = date_str ist.
        # 2. Wenn es eines findet, wird es mit den neuen 'event_data' geupdated.
        # 3. Wenn es keines findet, wird ein neues Dokument eingefügt.
        self.events.upsert({'date': date_str, **event_data}, self.EventQuery.date == date_str)

    def clear_event_override(self, date_str):
        # Dies wird verwendet, um eine Änderung zurückzusetzen. 
        removed_ids = self.events.remove(self.EventQuery.date == date_str)
        if removed_ids:
            print(f"Event-Überschreibung für {date_str} entfernt.")

    def close_db(self):
        self.db.close()


if __name__ == "__main__":
    print("Teste DataManager")
    from .config_loader import load_config
    import os
    
    config = load_config()
    if config:
        project_root = os.path.dirname(os.path.dirname(__file__))
        test_db_path = os.path.join(project_root, "test_db.json")

        dm = DataManager(db_path="test_db.json")
        dm.update_event("2025-01-01", {"status": "test"})
        print(f"Event am 2025-01-01: {dm.get_event('2025-01-01')}")
        dm.clear_event_override("2025-01-01")
        print(f"Event am 2025-01-01 nach Löschung: {dm.get_event('2025-01-01')}")
        dm.close_db()
        
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
            print("Test-DB gelöscht.")