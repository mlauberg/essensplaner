# mein_essensplaner/mein_essensplaner/app_logic.py - Das Gehirn 
from datetime import datetime, timedelta
from babel.dates import format_date

class AppLogic:
    def __init__(self, data_manager, config):
        self.data_manager = data_manager
        self.config = config
        self.default_meal = config.get('default_meal', {})

    # DATENABFRAGE LOGIK
    def get_event_details_for_day(self, date_obj):
        date_str = date_obj.strftime("%Y-%m-%d")
        stored_event = self.data_manager.get_event(date_str) # Delegiert die DB Abfrage

        if stored_event and stored_event.get('status') == 'cancelled':
            return {"name": "Abgesagt", "time_str": "", "status": "cancelled"}
        
        if stored_event and stored_event.get('status') == 'rescheduled':
            return {
                "name": self.default_meal.get('name', 'Event'),
                "time_str": f"{stored_event['start_time']} - {stored_event['end_time']}",
                "status": "rescheduled",
                "start_time": stored_event['start_time']
            }
        
        # FallbacK
        return {
            "name": self.default_meal.get('name', 'Essen'),
            "time_str": f"{self.default_meal.get('start_time')} - {self.default_meal.get('end_time')}",
            "status": "default",
            "start_time": self.default_meal.get('start_time')
        }

    # DATENMANIPULATIONS LOGIK
    def cancel_event(self, date_obj):
        self.data_manager.update_event(date_obj.strftime("%Y-%m-%d"), {"status": "cancelled"})

    def reset_to_default(self, date_obj):
        self.data_manager.clear_event_override(date_obj.strftime("%Y-%m-%d"))

    def reschedule_event(self, date_obj, new_start_time_str):
        try:
            # R1: Zeitformat muss hier stimmen.
            default_start_dt = datetime.strptime(self.default_meal.get('start_time'), "%H:%M")
            new_start_dt = datetime.strptime(new_start_time_str, "%H:%M")
            
            # R2: Die Verschiebung darf max. 30 Minuten betragen.
            if abs((new_start_dt - default_start_dt).total_seconds()) > 30 * 60:
                 return False
            
            # Berechnet die neue Endzeit
            duration = timedelta(minutes=self.default_meal.get('duration_minutes', 30))
            new_end_dt = new_start_dt + duration
            
            # Wenn alle Rs erfüllt sind, wird der write an DataManager gegeben.
            self.data_manager.update_event(date_obj.strftime("%Y-%m-%d"), { 
                "status": "rescheduled",
                "start_time": new_start_dt.strftime("%H:%M"),
                "end_time": new_end_dt.strftime("%H:%M")
            })
            return True
        except (ValueError, TypeError):
            return False
        
    # HTML GEN LOGIK
    def generate_weekly_plan_html(self, week_start_date):
        html = """
        <html><head><style>
              body { font-family: sans-serif; color: #333; } h2 { color: #0056b3; }
              ul { list-style-type: none; padding: 0; } li { margin: 10px 0; border-bottom: 1px solid #eee; padding-bottom: 10px; }
              .day { font-weight: bold; } .cancelled { color: #999; font-style: italic; }
              .rescheduled { color: #d9534f; font-weight: bold; }
        </style></head><body>
            <h2>Hallo Oma,</h2><p>hier ist der Essensplan für die kommende Woche:</p><ul>
        """
        # Geht alle Tage der Woche durch.
        for i in range(7):
            current_day = week_start_date + timedelta(days=i)
            # formatierung für deutsch
            day_name = format_date(current_day, "EEEE", locale='de_DE')
            # Ruft sich selbst auf, um die Daten für den Tag zu holen.
            event = self.get_event_details_for_day(current_day)
            
            # Ein Dictionary wird verwendet "map" 
            status_map = {
                "cancelled": f'<span class="cancelled">Fällt aus</span>',
                "rescheduled": f'<span class="rescheduled">Verschoben auf {event["time_str"]}</span>',
                "default": f'<span>Wie gewohnt um {event["time_str"]}</span>'
            }
            status_text = status_map.get(event['status'])
            
            html += f'<li><span class="day">{day_name}, {current_day.strftime("%d.%m.")}:</span> {status_text}</li>'

        html += "</ul><p>Liebe Grüße,<br>Dein Max</p></body></html>"
        return html

if __name__ == "__main__":
    print("Teste AppLogic")
    class MockDataManager:
        def __init__(self): self.events = {}
        def get_event(self, date_str): return self.events.get(date_str)
        def update_event(self, date_str, data): self.events[date_str] = data
        def clear_event_override(self, date_str): self.events.pop(date_str, None)
    
    mock_config = {'default_meal': {'name': 'Essen', 'start_time': '17:30', 'end_time': '18:00', 'duration_minutes': 30}}
    logic = AppLogic(MockDataManager(), mock_config)
    today = datetime.now().date()
    logic.cancel_event(today)
    details = logic.get_event_details_for_day(today)
    print(f"Status heute nach Absage: {details.get('status')}")
    if details.get('status') == 'cancelled':
        print("Test erfolgreich.")
    else:
        print("Test fehlgeschlagen.")
