import cv2
import csv
import os
from datetime import datetime
from ultralytics import YOLO
from collections import Counter

# Load YOLO model
model = YOLO('yolov8n.pt')


def run_webcam_detection(csv_filename="detections_log.csv"):
    # Open the webcam (0 is usually the built-in camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Press 'q' to quit and save.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 1. Run detection on the current frame
        results = model(frame, stream=True)

        detected_names = []
        for r in results:
            # Draw boxes on the screen so you can see what is happening
            annotated_frame = r.plot()

            for box in r.boxes:
                class_id = int(box.cls[0])
                label = model.names[class_id]
                detected_names.append(label)

        # 2. Display the live camera feed
        cv2.imshow("Webcam Detection", annotated_frame)

        # 3. Save to CSV every time an object is detected
        if detected_names:
            counts = Counter(detected_names)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            file_exists = os.path.isfile(csv_filename)
            with open(csv_filename, mode='a', newline='') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(['Timestamp', 'Object Name', 'Count'])

                for obj_name, count in counts.items():
                    writer.writerow([timestamp, obj_name, count])

        # Press 'q' to stop the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# RUN THE CAMERA
run_webcam_detection()