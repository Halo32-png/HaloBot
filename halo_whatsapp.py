from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pyttsx3
import requests

# Flask app
app = Flask(__name__)

# Voice engine setup
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Zira voice (female)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    reply = ""

    # Halo's responses
    if "hello" in incoming_msg:
        reply = "Hello Willdead! How can I help you today?"
    elif "weather" in incoming_msg:
        # Get weather online
        try:
            r = requests.get("https://wttr.in/?format=3")
            reply = "Here’s the weather: " + r.text
        except:
            reply = "I couldn’t fetch the weather right now."
    elif "open youtube" in incoming_msg:
        reply = "Opening YouTube on your laptop!"
    elif "bye" in incoming_msg:
        reply = "Goodbye Willdead, talk to you soon!"
    else:
        reply = "Halo here! I didn’t quite get that, but I’m listening."

    # Speak out loud on your laptop
    engine.say(reply)
    engine.runAndWait()

    # Send back to WhatsApp
    msg.body(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
