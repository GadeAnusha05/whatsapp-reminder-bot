from flask import Flask, request
from twilio.rest import Client
from apscheduler.schedulers.background import BackgroundScheduler
from twilio.twiml.messaging_response import MessagingResponse
import os
from datetime import datetime

app = Flask(__name__)

# Twilio credentials from environment variables
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_client = Client(account_sid, auth_token)
twilio_number = os.environ.get("TWILIO_NUMBER")  # e.g. "whatsapp:+14155238886"

# Your WhatsApp number
my_number = os.environ.get("MY_NUMBER")  # e.g. "whatsapp:+917893835478"

# Scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Night reminder: soak almonds at 9:10 PM daily
scheduler.add_job(
    lambda: twilio_client.messages.create(
        body="⏰ Time to soak your almonds 🥜",
        from_=twilio_number,
        to=my_number
    ),
    trigger='cron',
    hour=21,
    minute=10
)

# Morning reminder: eat soaked almonds at 7:30 AM daily
scheduler.add_job(
    lambda: twilio_client.messages.create(
        body="🌞 Good morning! Time to eat your soaked almonds 🥜",
        from_=twilio_number,
        to=my_number
    ),
    trigger='cron',
    hour=7,
    minute=30
)

@app.route("/")
def home():
    return "✅ WhatsApp Almond Reminder Bot is Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip().lower()
    response = MessagingResponse()
    msg = response.message()

    if "soak almonds" in incoming_msg:
        msg.body("⏰ Night reminder to soak almonds is set at 9:10 PM daily!")
    elif "eat almonds" in incoming_msg:
        msg.body("🌞 Morning reminder to eat soaked almonds is set at 7:30 AM daily!")
    elif "time" in incoming_msg:
        now = datetime.now().strftime("%H:%M:%S")
        msg.body(f"🕒 Current time: {now}")
    else:
        msg.body("Hi! Send 'soak almonds', 'eat almonds' or 'time' to get reminders.")

    return str(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
