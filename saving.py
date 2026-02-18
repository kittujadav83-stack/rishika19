import cv2
import csv
import os
from datetime import datetime
from ultralytics import YOLO
from collections import Counter

# 1. Load the YOLO model
model = YOLO('yolov8n.pt')


def run_detection_and_save():
    # Use 0 for webcam. If you have an image, replace 0 with 'image_name.jpg'
    source = 0

    cap = cv2.VideoCapture(source)
    csv_filename = "detections_log.csv"

    print("Starting Webcam... Press 'q' to stop.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 2. Run Object Detection
        results = model(frame)

        detected_names = []
        for r in results:
            annotated_frame = r.plot()  # Creates the box around objects
            for box in r.boxes:
                class_id = int(box.cls[0])
                label = model.names[class_id]
                detected_names.append(label)

        # 3. If objects are found, save to CSV
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
                    print(f"Saved: {obj_name} ({count})")

        # Show the live video
        cv2.imshow("Object Detection", annotated_frame)

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_detection_and_save()