# mein_essensplaner/mein_essensplaner/ui_components.py - Das Gesicht
import customtkinter as ctk # customtkinter für die UI
from datetime import date, timedelta, datetime
from babel.dates import format_date, get_day_names # Bable für das übersetzten des Datums in Deutsch
from .app_logic import AppLogic
from .email_sender import send_weekly_plan_email
from .config_loader import load_credentials

class App(ctk.CTk):
    def __init__(self, app_logic, config):
        super().__init__()
        
        # Speichert die übergebenen Logik- und Konfigurationsobjekte. -> So kann die UI auf die logik und die Einstellungen zugreifen.
        self.app_logic = app_logic
        self.config = config

        # Fenstereinstellungen
        self.title("Wöchentlicher Essensplaner")
        self.geometry("900x600") 
        ctk.set_appearance_mode("System")

        # Initialisiert den Kalender mit der aktuellen Woche
        self.current_week_start = date.today() - timedelta(days=date.today().weekday())
        self.day_cards = [] # Eine leere Liste, um die 7 Tageskarten-Widgets zu speichern
        self.credentials = load_credentials() # Lädt E-Mail-Zugangsdaten beim Start

        # Ruft die Methoden auf, die das Fenster mit Daten füllen
        self._create_widgets()
        self.update_week_display()

    def _create_day_card(self, parent):
        "Helper-Funktion, die eine einzelne Tageskarte erstellt und zurückgibt."
        card = {"container": ctk.CTkFrame(parent, border_width=1)}
        
        card["container"].grid_columnconfigure(0, weight=1)
        card["container"].grid_rowconfigure(0, weight=0)  
        card["container"].grid_rowconfigure(1, weight=0)  
        card["container"].grid_rowconfigure(2, weight=0)  
        card["container"].grid_rowconfigure(3, weight=0)  
        card["container"].grid_rowconfigure(4, weight=1)
        card["container"].grid_rowconfigure(5, weight=0)

        # Erstellung der Widgets
        card["name_label"] = ctk.CTkLabel(card["container"], font=ctk.CTkFont(size=14, weight="bold"))
        card["date_label"] = ctk.CTkLabel(card["container"], font=ctk.CTkFont(size=11))
        card["event_name_label"] = ctk.CTkLabel(card["container"], wraplength=115, font=ctk.CTkFont(size=13))
        card["event_time_label"] = ctk.CTkLabel(card["container"], wraplength=115, font=ctk.CTkFont(size=11))
        card["button_frame"] = ctk.CTkFrame(card["container"], fg_color="transparent")

        # Platziere die Widgets mit .grid()
        card["name_label"].grid(row=0, column=0, pady=(10,0), padx=5, sticky="ew")
        card["date_label"].grid(row=1, column=0, pady=(0,10), padx=5, sticky="ew")
        card["event_name_label"].grid(row=2, column=0, pady=(5,0), padx=5, sticky="ew")
        card["event_time_label"].grid(row=3, column=0, pady=(0,5), padx=5, sticky="ew")
        card["button_frame"].grid(row=5, column=0, pady=(5,10), padx=10, sticky="ew")
        
        return card

    def _create_widgets(self):
        # 1. Header-Bereich (Navigationsleiste oben)
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(pady=10, padx=10, fill="x", side="top")
        # Navigations- und E-Mail-Buttons
        ctk.CTkButton(header_frame, text="< Vorherige Woche", command=self.show_prev_week).pack(side="left")
        
        email_button = ctk.CTkButton(header_frame, text="Plan an Oma senden", command=self.handle_send_email, fg_color="SeaGreen", hover_color="DarkSeaGreen")
        email_button.pack(side="left", padx=20)
        if not self.credentials:
            email_button.configure(state="disabled", text="E-Mail nicht konfiguriert")

        self.week_label = ctk.CTkLabel(header_frame, text="", font=ctk.CTkFont(size=17, weight="bold"))
        self.week_label.pack(side="left", expand=True)

        ctk.CTkButton(header_frame, text="Nächste Woche >", command=self.show_next_week).pack(side="right")

        # 2. Hauptcontainer für die 7 Tageskarten
        days_container = ctk.CTkFrame(self)
        days_container.pack(pady=10, padx=10, fill="both", expand=True)
        days_container.grid_columnconfigure(list(range(7)), weight=1, uniform="day_col")
        days_container.grid_rowconfigure(0, weight=1)

        # 3. Erstellt die 7 Tageskarten in einer Schleife      
        for i in range(7):
            card = self._create_day_card(days_container) # Ruft die Helper-Funktion auf
            card["container"].grid(row=0, column=i, padx=4, pady=5, sticky="nsew") # nsew = north-south-east-west
            self.day_cards.append(card) # Speichert die Karte

    def update_week_display(self):
        start = self.current_week_start
        self.week_label.configure(text=f"KW {start.isocalendar()[1]}: {start.strftime('%d.%m')} - {(start + timedelta(days=6)).strftime('%d.%m.%Y')}")

        # Bereitet Daten vor (Wochentagsnamen, heutiges Datum)
        day_names_map = get_day_names('abbreviated', locale='de_DE')
        day_names = [day_names_map[i].replace('.', '') for i in range(7)]
        today = date.today()

        # Geht durch jede der 7 Tageskarten die bei mir gespeichert sind
        for i, card in enumerate(self.day_cards):
            current_day = start + timedelta(days=i)
            # Holt sich die aktuellen Event-Daten aus der Logik-Schicht!
            event = self.app_logic.get_event_details_for_day(current_day)
            is_past = current_day < today

            # 1. Aktualisiert die Texte der Labels
            card["name_label"].configure(text=day_names[current_day.weekday()].upper())
            card["date_label"].configure(text=format_date(current_day, 'd. MMM', locale='de_DE'))
            card["event_name_label"].configure(text=event['name'])
            card["event_time_label"].configure(text=event['time_str'])

            # 2. Wendet die Style an (Farben und z.B Rahmen)
            default_style = {"fg_color": ctk.ThemeManager.theme["CTkFrame"]["fg_color"], "border_width": 1, "border_color": ctk.ThemeManager.theme["CTkFrame"]["border_color"], "text_color": ctk.ThemeManager.theme["CTkLabel"]["text_color"]}
            status_styles = {
                "cancelled": {"fg_color": ("gray85", "gray25"), "text_color": ("gray50", "gray60")},
                "rescheduled": {"fg_color": ("#FFF9C4", "#FFB300"), "text_color": "black", "border_color": ("#FF8F00", "#FFB300")},
                "past": {"fg_color": ("gray90", "gray20"), "text_color": ("gray60", "gray50"), "border_color": ("gray70", "gray40")},
                "today": {"border_width": 2, "border_color": ctk.ThemeManager.theme["CTkButton"]["fg_color"]}
            }
            
            style = default_style.copy()
            # Wendet den Style an anhänig vom Zustand (Vergangen, abgesagt ...)
            if is_past: style.update(status_styles["past"])
            if event['status'] in status_styles: style.update(status_styles[event['status']])
            if current_day == today: style.update(status_styles["today"])
            
            card["container"].configure(fg_color=style["fg_color"], border_width=style["border_width"], border_color=style["border_color"])
            card["event_name_label"].configure(text_color=style["text_color"])
            card["event_time_label"].configure(text_color=style["text_color"])

            # 3. Aktualisiert die Buttons (löscht alte, erstellt neue)
            for widget in card["button_frame"].winfo_children(): widget.destroy()
            button_state = "disabled" if is_past else "normal"
            btn_font = ctk.CTkFont(size=12)

            if event['status'] != 'cancelled':
                ctk.CTkButton(card["button_frame"], text="Abmelden", command=lambda d=current_day: self.handle_action('cancel', d), fg_color=("#E57373", "#C62828"), hover_color=("#EF9A9A", "#E53935"), font=btn_font, state=button_state).pack(pady=3, fill="x")
                ctk.CTkButton(card["button_frame"], text="Verschieben", command=lambda d=current_day: self.handle_action('reschedule', d), font=btn_font, state=button_state).pack(pady=3, fill="x")
            if event['status'] != 'default':
                ctk.CTkButton(card["button_frame"], text="Reset", command=lambda d=current_day: self.handle_action('reset', d), fg_color="grey35", hover_color="grey50", font=btn_font, state=button_state).pack(pady=3, fill="x")

    # Methoden: die durch Button Klicks aufgerufen werden
    def show_prev_week(self): self.current_week_start -= timedelta(weeks=1); self.update_week_display()
    def show_next_week(self): self.current_week_start += timedelta(weeks=1); self.update_week_display()
    
    def handle_action(self, action, date_obj):
        if date_obj < date.today():
            self.show_error_dialog("Vergangene Termine können nicht geändert werden.")
            return
        
        # Delegiert die Arbeit an meine Logik-Schicht
        if action == 'cancel': self.app_logic.cancel_event(date_obj)
        elif action == 'reset': self.app_logic.reset_to_default(date_obj)
        elif action == 'reschedule':
            dialog = ctk.CTkInputDialog(text=f"Neue Startzeit (HH:MM) für {date_obj.strftime('%d.%m.')}:", title="Essen verschieben")
            new_time = dialog.get_input()
            if new_time and not self.app_logic.reschedule_event(date_obj, new_time):
                self.show_error_dialog("Verschieben fehlgeschlagen.\nUngültige Zeit oder außerhalb des Rahmens.")
        
        self.update_week_display() # Wichtig! Aktualisiert die Anzeige nach jeder Aktion!

    def handle_send_email(self):
        if not self.credentials:
            self.show_error_dialog("E-Mail-Zugangsdaten nicht in\ncredentials.yaml gefunden.")
            return

        today = date.today()
        days_until_next_monday = (7 - today.weekday()) % 7 or 7
        next_week_start = today + timedelta(days=days_until_next_monday)
        
        week_number = next_week_start.isocalendar()[1]
        html_content = self.app_logic.generate_weekly_plan_html(next_week_start)

        dialog = ctk.CTkInputDialog(text=f"Soll der Plan für KW {week_number} wirklich \nan omagon51@gmail.com gesendet werden?", title="Bestätigung")
        if dialog.get_input() is not None:
            success = send_weekly_plan_email(
                sender_email=self.credentials['sender_email'],
                password=self.credentials['password'],
                recipient_email="omagon51@gmail.com",
                html_content=html_content,
                week_number=week_number
            )
            msg = "E-Mail wurde erfolgreich versendet!" if success else "E-Mail konnte nicht gesendet werden.\nÜberprüfe die Terminal-Ausgabe."
            self.show_error_dialog(msg)

    def show_error_dialog(self, message):
        dialog = ctk.CTkToplevel(self)
        dialog.geometry("350x150")
        dialog.title("Hinweis")
        dialog.transient(self)
        dialog.grab_set()
        dialog.attributes("-topmost", True)
        ctk.CTkLabel(dialog, text=message, wraplength=300, justify="center").pack(expand=True, padx=20, pady=10)
        ctk.CTkButton(dialog, text="OK", command=dialog.destroy, width=100).pack(pady=(0, 15))
        self.after(50, lambda: self._center_toplevel(dialog))

    def _center_toplevel(self, toplevel_window):
        try:
            self.update_idletasks()
            main_x, main_y, main_width, main_height = self.winfo_x(), self.winfo_y(), self.winfo_width(), self.winfo_height()
            dialog_width, dialog_height = 350, 150 
            x = main_x + (main_width - dialog_width) // 2
            y = main_y + (main_height - dialog_height) // 2
            toplevel_window.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        except Exception: 
            pass

if __name__ == "__main__":
    print("Teste UI (simuliert)")
    class MockLogic:
        def get_event_details_for_day(self, _): 
            return {'name': 'Test', 'time_str': '12:00', 'status': 'default'}
    class MockConfig(dict):
        def get(self, key, default=None): 
            return self.get(key, default)
    
    try:
        app = App(MockLogic(), MockConfig(default_meal={}))
        print("UI-Test: App-Instanz konnte erstellt werden.")
    except Exception as e:
        print(f"Fehler beim Instanziieren der App: {e}")