from ultralytics import YOLO

BEST_WEIGHTS = r"C:\Users\aand\opencv_yolo_test\runs\detect\yolo_mechanical_parts\yolo_parts_final\weights\best.pt"

def export_for_raspberry():
    model = YOLO(BEST_WEIGHTS)
    model.export(format="onnx", imgsz=512)
    print("ONNX export complete.")

def export_for_jetson():
    model = YOLO(BEST_WEIGHTS)
    model.export(format="engine", imgsz=640, half=True)
    print("TensorRT export complete.")

if __name__ == "__main__":
    export_for_raspberry()
    # export_for_jetson()