from flask import Flask, jsonify, render_template, Response
import cv2
from controllers.weather_functions import weather_for_one_week
from controllers.audio_functions import voice_to_text


app = Flask(__name__)


@app.route("/start_listening", methods=["POST"])
def start_listening():
    voice_command = voice_to_text()
    if voice_command:
        if "weather" in voice_command.get("transcription", ""):
            weather_details = weather_for_one_week()
            return jsonify(
                {
                    "transcription": voice_command.get("transcription", ""),
                    "weather": weather_details,
                }
            )
    return jsonify(voice_command)


if __name__ == "__main__":
    app.run(debug=True)
