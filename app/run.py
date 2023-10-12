from flask import Flask, Response, request, render_template, jsonify
from flask_cors import CORS
import base64
import os

from controllers.opencv_functions import generate_frames

# from video_functions.liveness_detection import detect_faces

app = Flask(__name__)
app.static_folder = "static"
CORS(app)


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(debug=True)
