import yagmail
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
DESTINATAIRE = os.getenv("DESTINATAIRE")

def send_email(message):
    try:
        yag = yagmail.SMTP(EMAIL, PASSWORD)
        yag.send(to=DESTINATAIRE, subject="Alerte Bourse", contents=message)
        print(f"Email envoyé: {message}")
    except Exception as e:
        print(f"Erreur envoi mail : {e}")
