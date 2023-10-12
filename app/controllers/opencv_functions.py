import cv2
import os
import mediapipe as mp

# from deepface import DeepFace

# Initialize mediapipe face detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)
face_mesh = mp.solutions.face_mesh.FaceMesh()
# Initialize mediapipe face detection and pose estimation
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(
    min_detection_confidence=0.2, min_tracking_confidence=0.5
)
face_match = False
image_path = os.path.abspath("../static/images/reference.jpg")
print(image_path)
reference_img = cv2.imread(image_path)


def detect_faces(frame):
    # Process the frame and get the face detection results
    results = face_detection.process(frame)
    if results.detections:
        for face in results.detections:
            # Draw the face detection annotations on the frame
            mp_drawing.draw_detection(frame, face)

    num_faces = len(results.detections) if results.detections else 0
    cv2.putText(
        frame,
        f"No of Face: {num_faces}",
        (10, 30),
        cv2.FONT_HERSHEY_COMPLEX_SMALL,
        1,
        (0, 255, 0),
        1,
        cv2.LINE_AA,
    )


def generate_frames():
    # Initialize the OpenCV camera capture
    camera = cv2.VideoCapture(0)
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode the frame as JPEG
            detect_faces(frame)
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()

        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
