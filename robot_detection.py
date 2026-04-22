import cv2
import time
import sqlite3
import requests
import json
import os
import platform
from ultralytics import YOLO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
MODEL_PATH = r"C:\Users\aand\opencv_yolo_test\runs\detect\yolo_mechanical_parts\yolo_parts_final\weights\best.pt"  # Update for Pi/Jetson
DATABASE_PATH = 'robot_data.db'
UPLOAD_URL = 'http://your-server.com/api/upload'  # Replace with actual server URL
CONFIDENCE_THRESHOLD = 0.8
CAMERA_INDEX = 0  # 0 for default webcam, or /dev/video0 on Linux

# Mock sensor functions (replace with real sensor code for Pi/Jetson)
def get_temperature():
    # Mock: return random temp between 20-30°C
    import random
    return round(20 + random.random() * 10, 2)

def get_radiation():
    # Mock: return random radiation level (e.g., in mSv/h)
    import random
    return round(random.random() * 0.1, 4)

# Database setup
def init_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            object_type TEXT,
            bounding_box TEXT,
            confidence REAL,
            temperature REAL,
            radiation REAL,
            uploaded INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Check network connectivity
def is_online():
    try:
        requests.get('http://www.google.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False

# Upload data to server
def upload_data():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM detections WHERE uploaded = 0')
    rows = cursor.fetchall()

    if not rows:
        logging.info("No new data to upload.")
        conn.close()
        return

    for row in rows:
        data = {
            'id': row[0],
            'timestamp': row[1],
            'object_type': row[2],
            'bounding_box': row[3],
            'confidence': row[4],
            'temperature': row[5],
            'radiation': row[6]
        }
        try:
            response = requests.post(UPLOAD_URL, json=data, timeout=10)
            if response.status_code == 200:
                cursor.execute('UPDATE detections SET uploaded = 1 WHERE id = ?', (row[0],))
                logging.info(f"Uploaded detection ID {row[0]}")
            else:
                logging.error(f"Upload failed for ID {row[0]}: {response.status_code}")
        except Exception as e:
            logging.error(f"Upload error for ID {row[0]}: {str(e)}")

    conn.commit()
    conn.close()

# Main detection loop
def run_detection():
    # Load model
    model = YOLO(MODEL_PATH)
    logging.info("Model loaded successfully.")

    # Initialize camera
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        logging.error("Cannot open camera.")
        return

    # Set camera properties for Pi/Jetson optimization
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    logging.info("Camera initialized. Starting detection loop...")

    frame_count = 0
    upload_interval = 60  # Upload every 60 seconds if online

    while True:
        ret, frame = cap.read()
        if not ret:
            logging.error("Failed to capture frame.")
            break

        start_time = time.time()

        # Run YOLO detection
        results = model(frame, imgsz=640, verbose=False)
        boxes = results[0].boxes

        detections = []
        if boxes is not None:
            for box in boxes:
                conf = float(box.conf)
                if conf < CONFIDENCE_THRESHOLD:
                    continue

                cls_id = int(box.cls)
                label = model.names[cls_id]
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append({
                    'label': label,
                    'bbox': [x1, y1, x2, y2],
                    'confidence': conf
                })

        # Collect sensor data
        temp = get_temperature()
        rad = get_radiation()

        # Store detections in database
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        for det in detections:
            bbox_str = json.dumps(det['bbox'])
            cursor.execute('''
                INSERT INTO detections (timestamp, object_type, bounding_box, confidence, temperature, radiation)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (timestamp, det['label'], bbox_str, det['confidence'], temp, rad))
            logging.info(f"Detection stored: {det['label']} at {timestamp}")

        conn.commit()
        conn.close()

        # Periodic upload check
        frame_count += 1
        if frame_count % (30 * upload_interval) == 0:  # Assuming 30 FPS
            if is_online():
                logging.info("Network available. Attempting upload...")
                upload_data()
            else:
                logging.info("Offline. Data buffered locally.")

        # Calculate and log FPS
        end_time = time.time()
        fps = 1 / (end_time - start_time)
        logging.info(f"Frame processed. FPS: {fps:.2f}, Detections: {len(detections)}")

        # Optional: Save annotated frame for debugging (remove for headless)
        # annotated = frame.copy()
        # for det in detections:
        #     cv2.rectangle(annotated, (det['bbox'][0], det['bbox'][1]), (det['bbox'][2], det['bbox'][3]), (0, 255, 0), 2)
        #     cv2.putText(annotated, f"{det['label']}: {det['confidence']:.2f}", (det['bbox'][0], det['bbox'][1] - 10),
        #                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        # cv2.imwrite(f"debug_frame_{frame_count}.jpg", annotated)

        # Exit condition (e.g., for testing; remove for continuous run)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC key
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Detect platform
    system = platform.system()
    if system == "Linux":
        logging.info("Running on Linux (Raspberry Pi/Jetson). Ensure camera permissions.")
    elif system == "Windows":
        logging.info("Running on Windows. Using webcam.")

    init_database()
    run_detection()