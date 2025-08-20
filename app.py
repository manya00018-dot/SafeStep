from flask import Flask, render_template, request, jsonify
from twilio.rest import Client
import os, time
from flask import send_from_directory, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

emergency_contacts = []

@app.route('/')
def home():
    return render_template('index.html', contacts=emergency_contacts)

@app.route('/save_contacts', methods=['POST'])
def save_contacts():
    global emergency_contacts
    emergency_contacts = []
    for i in range(1, 4):
        num = request.form.get(f"contact{i}")
        if num:
            emergency_contacts.append(num)

    if request.form.get("police"):
        emergency_contacts.append("100")
    if request.form.get("ambulance"):
        emergency_contacts.append("108")

    return render_template('index.html', message="Contacts saved successfully!", contacts=emergency_contacts)

from flask import Flask, render_template, request, jsonify
from twilio.rest import Client

app = Flask(__name__)

# ------------------------------
# Twilio setup (replace with youeebr own)
TWILIO_ACCOUNT_SID = "ACac15728d7e401f5b80a4978d87736"
TWILIO_AUTH_TOKEN = "059dc16bcf4fbb29ab8a1e7e340e9333"
TWILIO_PHONE_NUMBER = "+17754297457"

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ------------------------------
# Store emergency contacts
emergency_contacts = []

# ------------------------------
# Home page: SOS + Voice + Contacts
@app.route('/')
def home():
    return render_template('index.html', contacts=emergency_contacts)

# ------------------------------
# Save contacts
@app.route('/save_contacts', methods=['POST'])
def save_contacts():
    global emergency_contacts
    emergency_contacts = []

    for i in range(1, 4):
        num = request.form.get(f"contact{i}")
        if num:
            emergency_contacts.append(num)

    # Optional official numbers
    if request.form.get("police"):
        emergency_contacts.append("100")
    if request.form.get("ambulance"):
        emergency_contacts.append("108")

    return render_template('index.html', message="Contacts saved successfully!", contacts=emergency_contacts)

# ------------------------------
# Trigger SOS: called by button or voice
@app.route('/sos', methods=['POST'])
def sos():
    data = request.get_json()
    lat = data.get('latitude')
    lon = data.get('longitude')

    location_text = f"🚨 EMERGENCY! Location: Latitude {lat}, Longitude {lon}"
    print(location_text)  # For debugging in terminal

    # Send SMS to all saved contacts
    for contact in emergency_contacts:
        try:
            client.messages.create(
                body=location_text,
                from_=TWILIO_PHONE_NUMBER,
                to=f"+91{contact}"  # Adjust country code if needed
            )
        except Exception as e:
            print(f"Error sending to {contact}: {e}")

    return jsonify({"status": "SOS received", "latitude": lat, "longitude": lon})

# ------------------------------
if __name__ == '__main__':
    app.run(debug=True)










from flask import Flask, request
from twilio.rest import Client

app = Flask(__name__)

@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.json
    location = data['location']

    account_sid = "your_twilio_sid"
    auth_token = "your_twilio_auth"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"🚨 Help! Current location: {location}",
        from_="+1234567890",  # Your Twilio number
        to="+916364339979"    # Trusted contact number
    )

    return {"status": "sent", "sid": message.sid}









EVIDENCE_DIR = os.path.join(os.path.dirname(__file__), "evidence")
os.makedirs(EVIDENCE_DIR, exist_ok=True)
@app.post("/upload_audio")
def upload_audio():
    f = request.files.get("audio")
    if not f:
        return jsonify({"error": "no file"}), 400
    # timestamped, safe filename
    ts = int(time.time())
    fname = secure_filename(f"sos_audio_{ts}.webm")
    path = os.path.join(EVIDENCE_DIR, fname)
    f.save(path)
    return jsonify({"url": url_for('get_evidence', filename=fname)})
    

@app.post("/upload_photo")
def upload_photo():
    f = request.files.get("photo")
    if not f:
        return jsonify({"error": "no file"}), 400
    ts = int(time.time())
    fname = secure_filename(f"sos_photo_{ts}.jpg")
    path = os.path.join(EVIDENCE_DIR, fname)
    f.save(path)
    return jsonify({"url": url_for('get_evidence', filename=fname)})


@app.get("/evidence/<path:filename>")
def get_evidence(filename):
    return send_from_directory(EVIDENCE_DIR, filename)









from flask import Flask, request
from twilio.rest import Client
import os

app = Flask(__name__)

# Twilio config (replace with your real values)
ACCOUNT_SID = "ACac15728d7e401f5b80a4978d87736"
AUTH_TOKEN = "059dc16bcf4fbb29ab8a1e7e340e9333"
FROM_WHATSAPP = "whatsapp:+14155238886"  # Twilio sandbox number
TO_WHATSAPP = "whatsapp:+916364339979"  # Your emergency contact

client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route("/sos_evidence", methods=["POST"])
def sos_evidence():
    if "file" not in request.files:
        return "No file received", 400

    file = request.files["file"]
    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    # Send WhatsApp message with audio
    message = client.messages.create(
        from_=FROM_WHATSAPP,
        to=TO_WHATSAPP,
        body="🚨 SOS! Evidence recording attached.",
        media_url=["https://your-server.com/" + filepath]  # must be accessible online
    )

    return "Evidence sent successfully ✅"










# --- Community Help (demo) ---
from flask import jsonify
import random

FAKE_NAMES = [
    "Asha", "Ravi", "Priya", "Kiran", "Neha", "Arjun", "Meera", "Vikram",
    "Anita", "Rahul", "Divya", "Sanjay"
]

def simulate_responders():
    # Create 3–4 random helpers with distance and ETA
    count = random.choice([3, 4])
    responders = []
    chosen = random.sample(FAKE_NAMES, count)
    for name in chosen:
        dist_km = round(random.uniform(0.3, 2.5), 1)     # 0.3–2.5 km
        eta_min = max(2, int(dist_km * random.uniform(3, 6)))  # rough ETA
        responders.append({
            "name": name,
            "distance_km": dist_km,
            "eta_min": eta_min
        })
    return responders

@app.route("/community_help", methods=["POST"])
def community_help():
    data = request.get_json(silent=True) or {}
    lat = data.get("latitude")
    lon = data.get("longitude")

    responders = simulate_responders()
    maps_url = None
    if lat is not None and lon is not None:
        maps_url = f"https://www.google.com/maps?q={lat},{lon}"

    return jsonify({
        "ok": True,
        "maps_url": maps_url,
        "responders": responders,
        "message": "Community help alert broadcast to nearby SafeStep users."
    })



@app.route("/community_help", methods=["POST"])
def community_help():
    responders = [
        {"name": "User A", "distance": "1.2 km"},
        {"name": "User B", "distance": "800 m"},
        {"name": "User C", "distance": "2 km"}
    ]
    return jsonify({
        "ok": True,
        "responders": responders
    })