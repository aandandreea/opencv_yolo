from ultralytics import YOLO
import cv2
import time
import statistics
from pathlib import Path


class YOLOBenchmark:
    def __init__(
        self,
        model_path: str,
        image_path: str,
        imgsz: int = 640,
        warmup_runs: int = 10,
        benchmark_runs: int = 100,
        use_onnx: bool | None = None,
    ):
        self.model_path = Path(model_path)
        self.image_path = Path(image_path)
        self.imgsz = imgsz
        self.warmup_runs = warmup_runs
        self.benchmark_runs = benchmark_runs

        # If flag is not provided, infer from extension
        if use_onnx is None:
            self.use_onnx = self.model_path.suffix.lower() == ".onnx"
        else:
            self.use_onnx = use_onnx

        self.model = None
        self.image = None

    def load(self):
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        if not self.image_path.exists():
            raise FileNotFoundError(f"Image file not found: {self.image_path}")

        expected_suffix = ".onnx" if self.use_onnx else ".pt"
        if self.model_path.suffix.lower() != expected_suffix:
            raise ValueError(
                f"Model type mismatch: use_onnx={self.use_onnx}, "
                f"but file is '{self.model_path.suffix}'"
            )

        self.model = YOLO(str(self.model_path))
        self.image = cv2.imread(str(self.image_path))

        if self.image is None:
            raise ValueError(f"Could not load image: {self.image_path}")

    def warmup(self):
        for _ in range(self.warmup_runs):
            _ = self.model(self.image, imgsz=self.imgsz, verbose=False)

    def run(self) -> dict:
        if self.model is None or self.image is None:
            self.load()

        self.warmup()

        times = []

        for _ in range(self.benchmark_runs):
            start = time.perf_counter()
            _ = self.model(self.image, imgsz=self.imgsz, verbose=False)
            end = time.perf_counter()
            times.append((end - start) * 1000)  # ms

        avg_ms = statistics.mean(times)
        min_ms = min(times)
        max_ms = max(times)
        fps = 1000 / avg_ms

        return {
            "model_path": str(self.model_path),
            "model_type": "ONNX" if self.use_onnx else "PyTorch",
            "image_path": str(self.image_path),
            "imgsz": self.imgsz,
            "runs": self.benchmark_runs,
            "avg_ms": avg_ms,
            "min_ms": min_ms,
            "max_ms": max_ms,
            "fps": fps,
        }

    @staticmethod
    def print_results(results: dict):
        print(f"Model: {results['model_path']}")
        print(f"Type: {results['model_type']}")
        print(f"Image: {results['image_path']}")
        print(f"Image size: {results['imgsz']}")
        print(f"Runs: {results['runs']}")
        print(f"Average inference: {results['avg_ms']:.2f} ms")
        print(f"Min inference: {results['min_ms']:.2f} ms")
        print(f"Max inference: {results['max_ms']:.2f} ms")
        print(f"Theoretical FPS: {results['fps']:.2f}")


if __name__ == "__main__":
    MODEL_PATH = r"C:\Users\eoanc\opencv_yolo_test\runs\detect\yolo_mechanical_parts\yolo_parts_final\weights\best.pt"
    ONNX_MODEL_PATH = r"C:\Users\eoanc\opencv_yolo_test\runs\detect\yolo_mechanical_parts\yolo_parts_final\weights\best.onnx"
    IMAGE_PATH = r"C:\Users\eoanc\opencv_yolo_test\mechanical_parts_dataset\test\images\2f443tj_jpg.rf.0453633956bd83914f24ffcba5afbdcf.jpg"

    pt_benchmark = YOLOBenchmark(
        model_path=MODEL_PATH,
        image_path=IMAGE_PATH,
        imgsz=640,
        warmup_runs=10,
        benchmark_runs=100,
    )
    pt_results = pt_benchmark.run()
    pt_benchmark.print_results(pt_results)

    print("\n" + "-" * 40 + "\n")

    onnx_benchmark = YOLOBenchmark(
        model_path=ONNX_MODEL_PATH,
        image_path=IMAGE_PATH,
        imgsz=512,
        warmup_runs=10,
        benchmark_runs=100,
    )
    onnx_results = onnx_benchmark.run()
    onnx_benchmark.print_results(onnx_results)