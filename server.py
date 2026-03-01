from flask import Flask, request, jsonify
from flask_cors import CORS
import qrcode
import base64
from io import BytesIO
from datetime import datetime
import json

app = Flask(__name__)
CORS(app) 

# Temporary "database"
attendance_data = []



@app.route("/generateQR", methods=["POST"])
def generate_qr():
    session_id = str(int(datetime.now().timestamp()))  
    qr_payload = json.dumps({"sessionId": session_id})

    qr_img = qrcode.make(qr_payload)
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return jsonify({"qrImage": f"data:image/png;base64,{qr_base64}", "sessionId": session_id})


@app.route("/markAttendance", methods=["POST"])
def mark_attendance():
    data = request.get_json()
    user_id = data.get("userId")
    session_id = data.get("sessionId")

    if not user_id or not session_id:
        return jsonify({"error": "Missing userId or sessionId"}), 400

    record = {
        "userId": user_id,
        "sessionId": session_id,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    attendance_data.append(record)
    return jsonify({"message": "Attendance marked!", "record": record})


@app.route("/getAttendance", methods=["GET"])
def get_attendance():
    return jsonify(attendance_data)


if __name__ == "__main__":
    app.run(port=5000)
