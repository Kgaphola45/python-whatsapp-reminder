import os
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime
import time

# Load Twilio credentials from .env
load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

# Path to reminders file
REMINDERS_FILE = "reminders.txt"

def send_whatsapp(message, phone):
    """Send a WhatsApp message via Twilio"""
    client.messages.create(
        body=message,
        from_="whatsapp:+14155238886",  
        to=f"whatsapp:{phone}"
    )
    print(f"✅ Reminder sent to {phone}: {message}")

def load_reminders():
    """Load reminders from reminders.txt"""
    reminders = []
    with open(REMINDERS_FILE, "r") as file:
        for line in file:
            if line.strip() == "":
                continue
            parts = line.strip().split("|")
            if len(parts) == 3:
                message = parts[0].strip()
                time_str = parts[1].strip()   # HH:MM
                phone = parts[2].strip()
                reminders.append({
                    "message": message,
                    "time": time_str,
                    "phone": phone
                })
    return reminders

def main():
    print("⏰ WhatsApp Reminder Script Started")
    reminders = load_reminders()

    while True:
        now = datetime.now()
        now_time = now.strftime("%H:%M")
        now_day = now.strftime("%A")        # e.g., "Monday"
        now_date = now.strftime("%Y-%m-%d") # e.g., "2026-05-14"
        current_minute = now.minute

        for reminder in reminders:
            time_str = reminder["time"]
            
            # Check for matches
            if time_str == now_time:
                send_whatsapp(reminder["message"], reminder["phone"])
            elif time_str == f"{now_day} {now_time}":
                send_whatsapp(reminder["message"], reminder["phone"])
            elif time_str == f"{now_date} {now_time}":
                send_whatsapp(reminder["message"], reminder["phone"])
            elif time_str.startswith("*/"):
                try:
                    interval = int(time_str[2:])
                    if current_minute % interval == 0:
                        send_whatsapp(reminder["message"], reminder["phone"])
                except ValueError:
                    pass
        
        # Wait 60 seconds before checking again
        time.sleep(60)

if __name__ == "__main__":
    main()