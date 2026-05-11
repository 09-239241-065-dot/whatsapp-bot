from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    user_message = request.form.get("Body", "").strip()
    if not user_message:
        return "No message", 400
    try:
        response = model.generate_content(
            f"Rewrite this in professional English. Only return the improved version, nothing else: {user_message}"
        )
        enhanced = response.text.strip()
        reply = f"✅ *Professional English:*\n\n{enhanced}\n\n_Copy & send this_ 👆"
    except Exception as e:
        reply = "❌ Something went wrong. Try again."
    
    twilio_response = MessagingResponse()
    twilio_response.message(reply)
    return str(twilio_response)

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot is running!"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
