from ultralytics import YOLO

def train_yolo():
    # Încarcă modelul YOLOv8 pre-antrenat
    model = YOLO("yolov8n.pt")  # sau yolov8s.pt pentru mai multă precizie

    # Antrenează modelul pe dataset-ul tău
    model.train(
        data="mechanical_parts_dataset/mech_parts_data.yaml",
        epochs=50,
        imgsz=640,
        batch=16,
        lr0=0.001,          # inițial learning rate
        lrf=0.01,           # factor de reducere finală (opțional)
        project="yolo_mechanical_parts",
        name="yolo_parts_final",
        exist_ok=True
    )

    # Export în ONNX după antrenare
    model.export(format="onnx")
    print("Training finished! Model exported to ONNX.")

def test():
    model = YOLO(
        r"C:\Users\eoanc\opencv_yolo_test\runs\detect\yolo_mechanical_parts\yolo_parts_final\weights\best.pt"
    )

    metrics = model.val(
        data="mechanical_parts_dataset/mech_parts_data.yaml",
        split="test"
    )

    print("mAP50-95:", metrics.box.map)
    print("mAP50:", metrics.box.map50)
    print("Precision:", metrics.box.mp)
    print("Recall:", metrics.box.mr)

if __name__ == "__main__":
    # train_yolo()
    test()