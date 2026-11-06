from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
from pathlib import Path
import math
import json

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
    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "success": False,
                "message": "Invalid JSON data"
            }), 400

        if data.get("consent") is not True:
            return jsonify({
                "success": False,
                "message": "Location sharing requires consent"
            }), 403

        latitude = float(data.get("latitude"))
        longitude = float(data.get("longitude"))
        accuracy = float(data.get("accuracy", 0))

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

        record = {
            "timestamp": datetime.now().astimezone().isoformat(),
            "latitude": latitude,
            "longitude": longitude,
            "accuracy": accuracy,
            "map": (
                f"https://www.google.com/maps?q="
                f"{latitude},{longitude}"
            )
        }

        with DATA_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record) + "\n")

        return jsonify({
            "success": True,
            "message": "Location received successfully"
        })

    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Invalid location values"
        }), 400

    except OSError:
        return jsonify({
            "success": False,
            "message": "Could not save location data"
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8080,
        debug=False
    )
