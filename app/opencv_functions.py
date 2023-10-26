import cv2
import numpy as np
import face_recognition

from controllers.audio_functions import text_to_voice, voice_to_text


# Read the background image
background_img = cv2.imread("./static/images/background.png")
# Load reference image and convert to RGB
reference_image = cv2.imread("./static/images/2845381.jpg")
reference_rgb = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB)
reference_image_encoding = face_recognition.face_encodings(reference_rgb)[0]
# Load the tick mark image
tick_mark_img = cv2.imread(
    "./static/images/checked.png", -1
)  # -1 for alpha channel (transparency)

# Create a list of all known face encodings
known_face_encodings = [reference_image_encoding]


def detect_faces(frame):
    match_found = False
    try:
        # Convert the BGR image to RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(
            face_locations, face_encodings
        ):
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding
            )
            if True in matches:
                print("Match Found")
                match_found = True
                break  # Assuming you only need one match
    except Exception as e:
        print(f"Error:{e}")
    return frame, match_found


if __name__ == "__main__":
    # Set up video capture
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        # If the video has finished, break
        if not ret:
            break
        # Resize frame if necessary
        desired_height = int(background_img.shape[0] / 2)
        aspect_ratio = frame.shape[1] / frame.shape[0]
        desired_width = int(desired_height * aspect_ratio)
        frame = cv2.resize(frame, (desired_width, desired_height))
        # Create a binary mask with a filled white circle
        mask = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)
        center_coordinates = (frame.shape[1] // 2, frame.shape[0] // 2)
        radius = min(center_coordinates)
        color = 255
        thickness = -1
        mask = cv2.circle(mask, center_coordinates, radius, color, thickness)
        frame, match_found = detect_faces(frame.copy())
        frame = cv2.flip(frame, 1)
        # Extract the circular region of the video frame
        circular_frame = cv2.bitwise_and(frame, frame, mask=mask)
        # Calculate the position to place the frame in the center
        start_x = (background_img.shape[1] - circular_frame.shape[1]) // 2
        start_y = (background_img.shape[0] - circular_frame.shape[0]) // 2
        # Extract the region from the background image
        roi = background_img[
            start_y : start_y + circular_frame.shape[0],
            start_x : start_x + circular_frame.shape[1],
        ]
        # Use the inverse mask to extract only the outer region of the ROI
        roi_outer = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mask))

        # Merge the outer region of the ROI with the circular frame
        merged_roi = cv2.add(roi_outer, circular_frame)
        # Replace the ROI in the background image
        background_img[
            start_y : start_y + circular_frame.shape[0],
            start_x : start_x + circular_frame.shape[1],
        ] = merged_roi

        # Display the image
        cv2.imshow("SMART AUTHENTICATION SYSTEM", background_img)
        if match_found:
            print("MATCH FOUND")
        # Press 'q' to exit the loop
        if (cv2.waitKey(25) & 0xFF == ord("q")) or match_found:
            break
    cap.release()
    cv2.destroyAllWindows()
    text_to_voice("Hi Boss, Welcome How may I help you today")
    audio_trans = voice_to_text()
    print(audio_trans)
