
from flask import Flask, request, jsonify
from datetime import datetime
from urllib.parse import quote
import logging
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "TRACKER Running"

@app.route("/collect", methods=["POST"])
def collect():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Required location data is missing."
        }), 400

    if not all(key in data for key in ["latitude", "longitude", "accuracy"]):
        return jsonify({
            "success": False,
            "message": "Required location data is missing."
        }), 400

    try:
        if any(isinstance(data[key], bool) for key in ["latitude", "longitude", "accuracy"]):
            raise ValueError()

        lat = float(data["latitude"])
        lon = float(data["longitude"])
        accuracy = float(data["accuracy"])

        if not all(map(lambda x: x == x and abs(x) != float("inf"), [lat, lon, accuracy])):
            raise ValueError()

        if (
            lat < -90 or lat > 90 or
            lon < -180 or lon > 180 or
            accuracy < 0
        ):
            raise ValueError()

    except (TypeError, ValueError, OverflowError):
        return jsonify({
            "success": False,
            "message": "Invalid coordinate values."
        }), 400

    ip = request.remote_addr or "Unavailable"
    browser = str(data.get("browser", "Unavailable"))[:1000]
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    map_link = "https://www.google.com/maps?q=" + quote(f"{lat},{lon}")

    entry = "\n"
    entry += "========================================\n"
    entry += "               TRACKER                  \n"
    entry += "========================================\n"
    entry += f"Time       : {time}\n"
    entry += f"IP Address : {ip}\n"
    entry += f"Latitude   : {lat}\n"
    entry += f"Longitude  : {lon}\n"
    entry += f"Accuracy   : {accuracy} metres\n"
    entry += f"Browser    : {browser}\n"
    entry += f"Google Map : {map_link}\n"
    entry += "========================================\n"

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "location.txt")

    try:
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(entry)

    except OSError:
        return jsonify({
            "success": False,
            "message": "Could not save location.txt."
        }), 500

    logging.info(entry)

    return jsonify({
        "success": True,
        "map": map_link
    })


if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=False)
