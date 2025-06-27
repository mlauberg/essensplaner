# Wöchentlicher Essensplaner

Eine einfache, wöchentliche Planungsanwendung. Die Anwendung wurde mit Python und dem `customtkinter`-Framework für die grafische Benutzeroberfläche entwickelt.

## Features

- **Wochenübersicht:** Zeigt eine Ansicht der aktuellen Woche.
- **Navigation:** Einfaches Blättern zu vorherigen und zukünftigen Wochen.
- **Standard-Termine:** Trägt automatisch einen täglichen Essestermin ein.
- **Termin-Management:**
  - **Absagen:** Termine können per Knopfdruck abgesagt werden.
  - **Verschieben:** Termine können innerhalb eines Rahmens von +/- 30 Minuten verschoben werden.
  - **Reset:** Geänderte Termine können auf den Standard zurückgesetzt werden.
- **Inaktive Vergangenheit:** Tage in der Vergangenheit können nicht mehr bearbeitet werden, um die Datenintegrität zu wahren.
- **E-Mail-Benachrichtigung:** Ein Wochenplan für die kommende Woche kann per Knopfdruck als E-Mail versendet werden.
- **Persistente Speicherung:** Alle Änderungen an Terminen werden in einer lokalen JSON-Datenbank gespeichert und bleiben nach einem Neustart erhalten.
- **Konfigurierbarkeit:** Standard-Terminzeiten und der Datenbankpfad sind über eine `config.yaml`-Datei anpassbar.

## Installation und Ausführung

### 1. Voraussetzungen

- Python 3.8+
- `pip` (Python package installer)
- Eine eingerichtete virtuelle Umgebung wird dringend empfohlen.

### 2. Setup

1. **Repository klonen oder herunterladen:**

    ```bash
    git clone [URL-des-Repositories]
    cd mein_essensplaner
    ```

2. **Virtuelle Umgebung erstellen und aktivieren:**

    ```bash
    python3 -m venv .venv

    # Virtuelle Umgebung aktivieren (macOS/Linux)
    source .venv/bin/activate
    ```

3. **Abhängigkeiten installieren:**

    ```bash
    pip install -r requirements.txt
    ```

4. **(Optional) E-Mail-Funktion konfigurieren:**
    - Erstelle eine Datei namens `credentials.yaml` im Projekt-Root-Verzeichnis (neben `config.yaml`).
    - Füge folgenden Inhalt ein und ersetze die Platzhalter mit den Daten deines E-Mail-Kontos (z.B. ein GMX-Konto, bei dem IMAP/POP3-Zugriff aktiviert ist):

      ```yaml
      sender_email: "deine.email@provider.de"
      password: "dein-passwort-oder-app-passwort"
      ```

    - **Wichtig:** Füge `credentials.yaml` zu deiner `.gitignore`-Datei hinzu, um zu verhindern, dass Zugangsdaten versioniert werden.

### 3. Anwendung starten

Stelle sicher, dass deine virtuelle Umgebung aktiv ist. Führe dann aus dem Projekt-Root-Verzeichnis den folgenden Befehl aus:

```bash
python3 -m mein_essensplaner.main
```

## Technische Details & Modularbeit-Anforderungen

### Verwendete Bibliotheken

Die Anwendung nutzt die folgenden 4 Bibliotheken:

1. **`customtkinter`**: Für die Erstellung der grafischen Benutzeroberfläche.
2. **`tinydb`**: Als leichte, dokumentenorientierte JSON-Datenbank zur persistenten Speicherung der Termindaten.
3. **`babel`**: Zur Übersetung von Datums- und Wochentagsanzeigen in Deutsch.
4. **`pyyaml`**: Zum Einlesen und Parsen der Konfigurationsdateien (`config.yaml`, `credentials.yaml`).

### Projektstruktur & Modulaufteilung

Das Projekt ist in **sechs logische Module** aufgeteilt, um eine Trennung der Zuständigkeiten (Separation of Concerns) zu gewährleisten:

- `mein_essensplaner/` (Paket-Ordner)
  - `main.py`: Haupteinstiegspunkt der Anwendung. Initialisiert alle Komponenten und startet die GUI.
  - `app_logic.py`: Enthält die Kern-Geschäftslogik (Event-Status verwalten, HTML-Plan generieren).
  - `data_manager.py`: Kümmert sich um alle Datenbankoperationen (Lesen, Schreiben, Löschen) mit `tinydb`.
  - `ui_components.py`: Definiert die Haupt-GUI-Klasse, das Layout und die Interaktions-Handler.
  - `config_loader.py`: Zentrales Modul zum Laden der `config.yaml` und `credentials.yaml`.
  - `email_sender.py`: Gekapselte Funktionalität zum Versenden von E-Mails via SMTP.
- `config.yaml`: Konfigurationsdatei für Standardwerte.
- `credentials.yaml`: _(Optional, nicht versioniert)_ Speichert E-Mail-Zugangsdaten.
- `events_db.json`: Datenbankdatei (automatisch erstellt).
- `README.md`: Diese Dokumentation.

### Hinweise zur Erfüllung der Modularbeit

- **Module:** Das Projekt besteht aus 6 Modulen, was die Anforderung von mindestens 5 Modulen erfüllt.
- **Bibliotheken:** Es werden 4 externe Bibliotheken verwendet.
- **Ausführbarkeit:** Das Programm ist über `main.py` ohne Parameter startbar.
- **`if __name__ == "__main__":`**: Jedes Modul enthält einen solchen Block, um die geforderte eigenständige Testbarkeit zu demonstrieren.
- **Code-Umfang:** Die Gesamtzeilenzahl des reinen Python-Codes erfüllt die Mindestanforderung von ca. 450 Zeilen. (Lines of Code: 447)
