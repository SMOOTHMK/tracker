from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
from urllib.parse import quote
import logging
import os
import math

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/style.css")
def style():
    return send_from_directory(BASE_DIR, "style.css")

@app.route("/script.js")
def script():
    return send_from_directory(BASE_DIR, "script.js")

@app.route("/collect", methods=["POST"])
def collect():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"success": False, "message": "Invalid location data."}), 400

    try:
        lat = float(data["latitude"])
        lon = float(data["longitude"])
        accuracy = float(data["accuracy"])

        if not all(math.isfinite(x) for x in [lat, lon, accuracy]):
            raise ValueError()

        if not (-90 <= lat <= 90 and -180 <= lon <= 180 and accuracy >= 0):
            raise ValueError()

    except (KeyError, TypeError, ValueError, OverflowError):
        return jsonify({"success": False, "message": "Invalid coordinates."}), 400

    ip = request.remote_addr or "Unavailable"
    browser = str(data.get("browser", "Unavailable"))[:1000]
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    map_link = "https://www.google.com/maps?q=" + quote(f"{lat},{lon}")

    entry = (
        "\n========================================\n"
        "               TRACKER                  \n"
        "========================================\n"
        f"Time       : {time}\n"
        f"IP Address : {ip}\n"
        f"Latitude   : {lat}\n"
        f"Longitude  : {lon}\n"
        f"Accuracy   : {accuracy} metres\n"
        f"Browser    : {browser}\n"
        f"Google Map : {map_link}\n"
        "========================================\n"
    )

    file_path = os.path.join(BASE_DIR, "location.txt")

    try:
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(entry)
    except OSError:
        return jsonify({"success": False, "message": "Could not save location."}), 500

    logging.info("A consented location record was saved.")

    return jsonify({
        "success": True,
        "message": "Location submitted successfully.",
        "map": map_link
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
