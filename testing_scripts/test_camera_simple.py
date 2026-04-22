from ultralytics import YOLO
import cv2

model = YOLO(r"C:\Users\aand\opencv_yolo_test\runs\detect\yolo_mechanical_parts\yolo_parts_final\weights\best.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, imgsz=640)
    boxes = results[0].boxes
    names = model.names

    annotated = frame.copy()

    if boxes is not None:
        for box in boxes:
            cls_id = int(box.cls)
            label = names[cls_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
            text = f"{label}"
            cv2.putText(annotated, text, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("YOLOv8 Mechanical Parts", annotated)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
