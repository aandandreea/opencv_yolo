# Software cu AI pentru detectarea componentelor mecanice din reactoare nucleare în timp real

## Descriere

Sistem software bazat pe inteligență artificială pentru detecția în timp real a componentelor mecanice (rulmenți, șuruburi, roți dințate, piulițe), conceput pentru inspecție robotică autonomă în medii nucleare, unde automatizarea reduce expunerea umană la radiații.

Proiectul are trei componente care lucrează împreună:

1. **Model AI** – model YOLOv8n antrenat pe un dataset propriu de piese mecanice.
2. **Robot edge (Raspberry Pi)** – rulează inferența local, salvează detecțiile în SQLite și le sincronizează către server când există conectivitate.
3. **Dashboard web (Java / Spring Boot)** – primește datele de la robot și le afișează în timp real.

```
 Cameră ──► Robot edge (YOLOv8n + SQLite) ──HTTP POST/JSON──► Server Spring Boot (H2) ──► Dashboard web
              inferență locală, offline-first                    /api/upload, /api/images       http://localhost:8080
```

## Funcționalități

- Detecție în timp real a 4 clase: `Bearing`, `Bolt`, `Gear`, `Nut`
- Inferență complet locală, pe dispozitive edge cu resurse limitate
- Stocare locală (SQLite) și sincronizare ulterioară, pentru funcționare chiar și fără rețea
- Export al modelului în format ONNX
- Scripturi de benchmark pentru compararea formatelor (PyTorch vs ONNX)
- Dashboard web cu temă întunecată, 5 secțiuni: Dashboard, Detections, Map View, Metrics, Robot Images
- Hartă interactivă bazată pe planul unui reactor nuclear PWR
- Panou de radiație cu praguri și badge-uri de status (NORMAL / ELEVATED / HIGH / ALARM)
- Galerie de imagini primite de la camera robotului (upload multipart, lightbox)
- Automatizarea build-ului cu Makefile

## Tehnologii

| Zonă | Tehnologii |
|---|---|
| AI / Inferență | Python, Ultralytics YOLOv8, OpenCV, ONNX Runtime |
| Edge | Raspberry Pi, SQLite |
| Backend | Java 11, Spring Boot 2.7.18, Spring MVC, Spring Data JPA, Hibernate, H2 |
| Frontend | HTML, Bootstrap 5.3.2, Chart.js 4.4.1, Font Awesome 6.5.1 |
| Build | Maven, GNU Make |

## Dataset

Dataset personalizat, adnotat în format YOLO și configurat prin `mechanical_parts_dataset/mech_parts_data.yaml`.

| Subset | Imagini | Etichete |
|---|---|---|
| Train | 1799 | 1799 |
| Val | 225 | 225 |
| Test | 225 | 225 |

Distribuția claselor în setul de antrenament: Bearing 1680, Bolt 2074, Gear 2086, Nut 2544.

## Antrenare

Pornind de la `yolov8n.pt` (preantrenat pe COCO), prin transfer learning și fine-tuning:

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
model.train(
    data="mechanical_parts_dataset/mech_parts_data.yaml",
    epochs=50,
    imgsz=640,
    batch=16,
    lr0=0.001,
    project="yolo_mechanical_parts",
    name="yolo_parts_final",
    exist_ok=True
)
```

## Rezultate (epoca 50)

| Metrică | Valoare |
|---|---|
| Precision | 0.8663 |
| Recall | 0.7782 |
| mAP@50 | 0.8599 |
| mAP@50-95 | 0.7038 |

Cel mai mare mAP@50 (0.8621) a fost atins la epoca 45, iar precizia maximă (0.9084) la epoca 36.

## Instalare și rulare

### 1. Model AI

```bash
pip install ultralytics opencv-python onnxruntime requests
```

Test pe cameră web:

```bash
python testing_scripts/test_camera.py
```

Rularea pe robot (detecție + stocare SQLite + upload automat către server):

```bash
python robot_detection.py
```

Export în ONNX:

```bash
python export_scripts/export_model.py
```

Benchmark:

```bash
python benchmarks/benchmark_inference.py
python benchmarks/benchmark_formats.py
```

> Pragul de încredere folosit pentru afișarea detecțiilor este 0.8 (80%).

### 2. Dashboard-ul web (Java / Spring Boot)

Cerințe: JDK 11 și Maven.

```bash
make build   # compilează și creează JAR-ul executabil
make run     # pornește aplicația
make         # build + run
make stop    # oprește instanța curentă
make clean   # șterge directorul target/
```

Aplicația pornește pe **http://localhost:8080**. Baza de date H2 este în memorie și este populată automat la pornire (metrici, coordonate, detecții și imagini de exemplu).

## API REST

| Endpoint | Descriere |
|---|---|
| `GET /api/data` | Lista detecțiilor |
| `POST /api/upload` | Primește detecții (JSON) de la robot |
| `POST /api/data/reset` | Resetează detecțiile |
| `GET /api/metrics`, `GET /api/metrics/by-name/{name}` | Metrici de mediu (temperatură, umiditate, radiație) |
| `GET /api/coordinates`, `GET /api/coordinates/by-map/{ref}` | Coordonatele de pe planul reactorului |
| `GET /api/images`, `GET /api/images/{id}/data` | Imaginile robotului |
| `POST /api/images`, `DELETE /api/images/{id}` | Upload (multipart) / ștergere imagine |

## Structura proiectului

> Ajustează după structura reală a repository-ului.

```
.
├── mechanical_parts_dataset/   # dataset (train / val / test) + mech_parts_data.yaml
├── main.py                     # antrenarea modelului
├── testing_scripts/            # teste pe cameră web
├── export_scripts/             # export ONNX
├── benchmarks/                 # benchmark PyTorch vs ONNX
├── robot_detection.py          # inferență edge + SQLite + upload
├── runs/detect/                # rezultate antrenare și ponderi (best.pt)
└── src/main/java/com/example/metricsapp/
    ├── controller/             # controlere REST
    ├── models/                 # entități JPA
    ├── repositories/           # Spring Data JPA
    ├── services/               # logica de business
    └── utils/                  # DataInitializer
```

## Limitări

- Dataset de dimensiuni limitate; mai multă diversitate ar crește robustețea
- Reflexiile metalice și condițiile de iluminare pot genera predicții eronate
- Baza H2 este in-memory (datele se pierd la repornire)
- Prototip / proof-of-concept, necertificat conform standardelor de siguranță nucleară

## Direcții viitoare

- Extinderea dataset-ului cu mai multe clase și imagini din medii industriale reale
- Cuantizare și compresie (INT8, FP16) pentru dispozitive low-power
- Autentificare (Spring Security) pentru dashboard
- Integrare cu protocoale industriale (MQTT, OPC-UA)
- Migrare de la H2 la PostgreSQL / MySQL
- Notificări în timp real (WebSocket / SSE) pentru alerte de radiație
- Testare și certificare conform IEC 61513 și IEEE 603

## Referințe

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [OpenCV](https://opencv.org/)
- [ONNX Runtime](https://onnxruntime.ai/)
- IAEA, *Considerations for Deploying Artificial Intelligence Applications in the Nuclear Power Industry*, NR-T-1.26, 2025

## Licență

Adaugă aici licența aleasă (de ex. MIT).
