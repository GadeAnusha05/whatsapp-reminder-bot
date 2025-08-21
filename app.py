from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "almond" in incoming_msg:
        msg.body("✅ Reminder: Soak almonds at 10 PM and eat them in the morning 🌙☀️")
    else:
        msg.body("👋 Hi! I am your Almond Reminder Bot. Type 'almond' to get your reminder.")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
