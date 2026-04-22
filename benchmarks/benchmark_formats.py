from ultralytics import YOLO

BEST_WEIGHTS = r"C:\Users\aand\opencv_yolo_test\runs\detect\yolo_mechanical_parts\yolo_parts_final\weights\best.pt"

model = YOLO(BEST_WEIGHTS)

# Try one image size first
metrics = model.benchmark(
    data="mechanical_parts_dataset/mech_parts_data.yaml",
    imgsz=640,
    half=False,
    device="cpu"   # use "0" for GPU on your laptop if available
)

print(metrics)