import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from ultralytics import YOLO
import cv2 as cv
from datetime import datetime
from collections import defaultdict
import time
import numpy as np

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

video_path = "tr2.mov"
cap = cv.VideoCapture(video_path)

os.makedirs("violations", exist_ok=True)

object_y_hist = defaultdict(list)
saved_ids = set()

fps = cap.get(cv.CAP_PROP_FPS)
frame_count = 0
frame_skip = 5

# Save annotated video
output_path = "Annotated_Video.mp4"
fourcc = cv.VideoWriter_fourcc(*'mp4v')
width = 854
height = 480
output_fps = fps / frame_skip
out = cv.VideoWriter(output_path, fourcc, output_fps, (width, height))

# Red light check (adjust timing according to your video)
def is_red_light():
    current_pos_seconds = cap.get(cv.CAP_PROP_POS_MSEC) / 1000.0
    return current_pos_seconds > 3 # Adjust as needed

# Draw traffic light on frame
def draw_traffic_light(frame, red):
    cv.rectangle(frame, (800,10), (850,110), (50,50,50), -1)
    cv.rectangle(frame, (800,10), (850,110), (255,255,255), 2)
    cv.circle(frame, (825,35), 15, (0,0,255) if red else (0,0,50), -1)
    cv.circle(frame, (825,85), 15, (0,255,0) if not red else (0,50,0), -1)

violation_timers = {}
flash_duration = int(fps/frame_skip * 2)  # Flash for 2 seconds

def flash_vehicle(vehicle_id):
    if vehicle_id in violation_timers:
        time_since_violation = violation_timers[vehicle_id]
        if time_since_violation > flash_duration:
            return False
        flash_pattern = (time_since_violation // 2) % 2 == 0
        violation_timers[vehicle_id] += 1
        return flash_pattern
    return False

number_of_violations = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % frame_skip != 0:
        continue

    frame_resized = cv.resize(frame, (width, height))

    # Track vehicles
    results = model.track(frame_resized, persist=True, classes=[0,1,2,3,5,7,8,9,10,11,12])

    annotated_frame = results[0].plot()

    # Draw stop lines
    cv.line(annotated_frame, (10,300), (844,315), (0,0,255), 2)
    cv.line(annotated_frame, (844,0), (844,315), (0,0,255), 2)
    cv.line(annotated_frame, (10,0), (10,300), (0,0,255), 2)

    red = is_red_light()

    if results[0].boxes.id is not None:
        for box in results[0].boxes:
            if not hasattr(box, 'id') or box.id is None:
                continue
            vid = int(box.id)
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            center_y = int((y1 + y2)/2)

            object_y_hist[vid].append(center_y)
            if len(object_y_hist[vid]) >= 2:
                prev_y = object_y_hist[vid][-2]
                curr_y = object_y_hist[vid][-1]
                line_y = 315  # adjust according to your frame

                if red and prev_y < line_y and curr_y >= line_y and vid not in saved_ids:
                    number_of_violations += 1
                    violation_timers[vid] = 0
                    cropped = frame_resized[y1-5:y2+5, x1-5:x2+5]
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"violations/vehicle_{vid}_{timestamp}.jpg"
                    cv.imwrite(filename, cropped)
                    print(f"[VIOLATION] Vehicle {vid} saved at {filename}")
                    saved_ids.add(vid)

            if flash_vehicle(vid):
                cv.rectangle(annotated_frame, (x1, y1), (x2, y2), (0,0,255), 4)
                cv.putText(annotated_frame, "VIOLATION!", (x2-80, y2+25), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

    draw_traffic_light(annotated_frame, red)

    # Display counters
    cv.rectangle(annotated_frame, (5,4), (275,45), (255,255,255), -1)
    cv.putText(annotated_frame, f"Active Vehicle Count: {len(results[0].boxes) if results[0].boxes.id is not None else 0}", (25,20), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)
    cv.putText(annotated_frame, f"Violations: {number_of_violations}", (25,40), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)

    out.write(annotated_frame)
    cv.imshow("Vehicle Detection", annotated_frame)

    if cv.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
out.release()
cv.destroyAllWindows()