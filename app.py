from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ WhatsApp Reminder Bot is Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    # Get incoming message
    incoming_msg = request.values.get("Body", "").strip().lower()
    # Prepare Twilio response
    response = MessagingResponse()
    msg = response.message()

    # Logic for replies
    if "remind me" in incoming_msg:
        msg.body("⏰ Reminder received! I will notify you at the set time.")
    elif "time" in incoming_msg:
        now = datetime.now().strftime("%H:%M:%S")
        msg.body(f"🕒 Current time: {now}")
    else:
        msg.body("Hi! I'm your WhatsApp Reminder Bot. Send 'remind me' or 'time'.")

    return str(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
