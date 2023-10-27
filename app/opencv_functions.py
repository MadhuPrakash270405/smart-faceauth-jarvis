import cv2
import numpy as np
import face_recognition
from controllers.audio_functions import text_to_voice, voice_to_text


def load_image(path, color_conversion=cv2.COLOR_BGR2RGB):
    try:
        image = cv2.imread(path)
        if image is None:
            raise FileNotFoundError(f"Image file not found at {path}")
        if color_conversion:
            image = cv2.cvtColor(image, color_conversion)
        return image
    except Exception as e:
        print(f"Error loading image: {e}")
        return None


def load_reference_image(path):
    image = load_image(path)
    if image is not None:
        try:
            return face_recognition.face_encodings(image)[0]
        except IndexError:
            print("No faces found in the reference image.")
            return None
    return None


def detect_faces(frame, known_face_encodings):
    match_found = False
    try:
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(image_rgb)
        face_encodings = face_recognition.face_encodings(image_rgb, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding
            )
            if True in matches:
                print("Match Found")
                match_found = True
                break
    except Exception as e:
        print(f"Error in face detection: {e}")
    return match_found


def perform_voice_verification():
    try:
        text_to_voice("You are almost Verified, What's the Voice Code??")
        audio_trans = voice_to_text()
        transcription = audio_trans.get("transcription")
        if transcription and transcription.lower() == "america":
            text_to_voice("Hi Madhu, How is your day??")
        else:
            print("Voice verification failed.")
    except Exception as e:
        print(f"Error in voice verification: {e}")


def process_frame(frame, background_img, mask):
    try:
        frame = cv2.flip(frame, 1)
        circular_frame = cv2.bitwise_and(frame, frame, mask=mask)
        start_x = (background_img.shape[1] - circular_frame.shape[1]) // 2
        start_y = (background_img.shape[0] - circular_frame.shape[0]) // 2
        roi = background_img[
            start_y : start_y + circular_frame.shape[0],
            start_x : start_x + circular_frame.shape[1],
        ]
        roi_outer = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mask))
        merged_roi = cv2.add(roi_outer, circular_frame)
        background_img[
            start_y : start_y + circular_frame.shape[0],
            start_x : start_x + circular_frame.shape[1],
        ] = merged_roi
        return background_img
    except Exception as e:
        print(f"Error in processing frame: {e}")
        return background_img


def create_circular_mask(frame):
    try:
        mask = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)
        center_coordinates = (frame.shape[1] // 2, frame.shape[0] // 2)
        radius = min(center_coordinates)
        mask = cv2.circle(mask, center_coordinates, radius, 255, -1)
        return mask
    except Exception as e:
        print(f"Error in creating mask: {e}")
        return np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)


def main():
    background_img = load_image("./static/images/background.png", None)
    if background_img is None:
        return

    known_face_encoding = load_reference_image("./static/images/2845381.jpg")
    if known_face_encoding is None:
        return

    known_face_encodings = [known_face_encoding]

    try:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 15)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    except Exception as e:
        print(f"Error initializing camera: {e}")
        return

    frame_count = 0
    process_every_n_frames = 5

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (640, 480))
            mask = create_circular_mask(frame)
            frame_count += 1

            if frame_count % process_every_n_frames == 0:
                match_found = detect_faces(frame, known_face_encodings)
                if match_found:
                    perform_voice_verification()
                    break

            background_img = process_frame(frame, background_img, mask)
            cv2.imshow("SMART AUTHENTICATION SYSTEM", background_img)

            if cv2.waitKey(25) & 0xFF == ord("q"):
                break
    except Exception as e:
        print(f"Error during main loop: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
