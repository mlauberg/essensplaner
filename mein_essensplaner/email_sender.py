# mein_essensplaner/mein_essensplaner/email_sender.py - Unser Postbote
import smtplib, ssl
from email.mime.text import MIMEText # Note: MIME ist das "Verpackungs- und Beschriftungssystem" für E-Mails
from email.mime.multipart import MIMEMultipart

def send_weekly_plan_email(sender_email, password, recipient_email, html_content, week_number):

    # 1. E-Mail-Container erstellen mit mime sonnst könnten wir nur text emails verschicken
    message = MIMEMultipart("alternative")
    
    # 2. E-Mail-Header
    message["Subject"] = f"Essensplan für die kommende Woche (KW {week_number})"
    message["From"] = sender_email
    message["To"] = recipient_email

    # 3  HTML-Inhalt an die E-Mail anhängen
    message.attach(MIMEText(html_content, "html", "utf-8"))
    
    context = ssl.create_default_context()
    try:
         # 4. Verbindung zum E-Mail-Server aufbauen (bei mir GMX)
        with smtplib.SMTP("mail.gmx.net", 587, timeout=10) as server:
            # 5. Verbindung verschlüsseln
            server.starttls(context=context)

            # 6. Einloggen und E-Mail versenden:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            print(f"E-Mail erfolgreich an {recipient_email} gesendet.")
            return True
    # Fehlerhandeling
    except (smtplib.SMTPException, ConnectionRefusedError, OSError) as e:
        print(f"E-Mail FEHLER: {e}")
        return False


if __name__ == "__main__":
    print("--- Teste E-Mail Sender (simuliert) ---")
    from .config_loader import load_credentials
    
    creds = load_credentials()
    if creds:
        print("Zugangsdaten gefunden, Test-Aufruf wäre möglich.")
    else:
        print("Keine Zugangsdaten, Test übersprungen.")