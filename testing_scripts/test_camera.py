from ultralytics import YOLO
import cv2
import time

model = YOLO(r"C:\Users\aand\opencv_yolo_test\runs\detect\yolo_mechanical_parts\yolo_parts_final\weights\best.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    start = time.time()

    # Run model WITHOUT built-in filtering (we'll do it manually)
    results = model(frame, imgsz=640)

    boxes = results[0].boxes
    names = model.names

    # Create a copy for drawing
    annotated = frame.copy()

    if boxes is not None:
        for box in boxes:
            conf = float(box.conf)

            # ✅ Skip detections below 80%
            if conf < 0.8:
                continue

            cls_id = int(box.cls)
            label = names[cls_id]

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Draw bounding box
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Draw label + confidence
            text = f"{label}: {conf:.2f}"
            cv2.putText(annotated, text, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Print to console (optional)
            print(f"{label}: {conf:.2f}")

    end = time.time()
    fps = 1 / (end - start)

    # Show FPS
    cv2.putText(annotated, f"FPS: {fps:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("YOLOv8 Mechanical Parts", annotated)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()