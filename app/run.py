from flask import Flask, jsonify, render_template, Response
from concurrent.futures import ThreadPoolExecutor
import cv2
from controllers.weather_functions import weather_for_one_week
from controllers.audio_functions import voice_to_text

from controllers.opencv_functions import detect_faces


app = Flask(__name__)


def generate_frames():
    # Initialize the OpenCV camera capture
    camera = cv2.VideoCapture(0)
    # Set default refresh rate
    refresh_rate = 30
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set the width to 640 pixels
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set the height to 480 pixels
    camera.set(cv2.CAP_PROP_FPS, 10)  # Set the frame rate to 10 FPS
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode the frame as JPEG
            frame = cv2.flip(frame, 1)
            detect_faces(frame)
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()

        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/")
def home_page():
    return render_template("face_detection.html")


@app.route("/audio")
def audio_route():
    return render_template("audio_transcription.html")


@app.route("/weather")
def weather_route():
    return render_template("weather_widget.html")


@app.route("/video_feed")
def video_feed():
    global refresh_rate
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
        content_type="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/set_refresh_rate/<int:rate>")
def set_refresh_rate(rate):
    global refresh_rate
    refresh_rate = rate
    return "Refresh rate set to " + str(rate) + " FPS."


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
