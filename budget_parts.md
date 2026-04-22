# Budget Parts List for Robotic YOLO Detection System

This document outlines a cost-effective parts list for building a budget version of the robotic mechanical parts detection system. The setup is designed to run the `robot_detection.py` script on a Raspberry Pi, providing a proof-of-concept for thesis work. All prices are approximate in USD (as of 2026) and may vary by region/vendor. Total estimated cost: **$150-250**.

## Core Components

### 1. Edge Device: Raspberry Pi 4 Model B (2GB RAM)
- **Purpose**: Runs the YOLO model, Python scripts, and handles data storage/upload.
- **Specifications**: Quad-core CPU, 2GB RAM, USB ports, Ethernet/Wi-Fi.
- **Why Budget**: Cheapest Pi model capable of real-time YOLO inference at low resolutions.
- **Price**: $35-45
- **Where to Buy**: Raspberry Pi official store, Amazon, or local electronics shops.
- **Alternatives**: 
  - Raspberry Pi Zero W ($15) for even lower cost, but may struggle with YOLO performance.
  - Raspberry Pi 5 (4GB RAM) if available at the same price—it's better due to faster CPU (Cortex-A76), improved thermal management, and PCIe for peripherals, offering smoother YOLO inference and multitasking.

### 2. MicroSD Card (32GB Class 10)
- **Purpose**: Stores the OS, Python environment, and database.
- **Specifications**: High-speed for smooth operation.
- **Price**: $5-10
- **Where to Buy**: Any electronics store.

### 3. Power Supply (5V 3A USB-C)
- **Purpose**: Powers the Raspberry Pi reliably.
- **Specifications**: Official Raspberry Pi PSU recommended.
- **Price**: $10-15
- **Where to Buy**: Raspberry Pi store or Amazon.

### 4. Camera: USB Webcam (1080p)
- **Purpose**: Captures video for YOLO detection.
- **Specifications**: 640x480 resolution at 30 FPS, plug-and-play with OpenCV.
- **Why Budget**: Basic webcams work well; no need for high-end cameras.
- **Price**: $10-20
- **Where to Buy**: Amazon, eBay, or office supply stores.
- **Alternatives**: Raspberry Pi Camera Module 3 ($25) for CSI connection, but USB is simpler for beginners.

## Sensors
S
### 5. Temperature Sensor: D18B20 Digital Temperature Sensor
- **Purpose**: Measures ambient temperature for environmental data.
- **Specifications**: Waterproof, 1-wire interface, -55°C to 125°C range.
- **Why Budget**: Inexpensive and easy to interface with Pi GPIO.
- **Price**: $5-10 (pack of 5 for $10-15)
- **Where to Buy**: Adafruit, SparkFun, or Amazon.
- **Notes**: Requires a 4.7kΩ resistor for pull-up.

### 6. Radiation Sensor: Geiger Counter Module (e.g., RadiationD v1.1)
- **Purpose**: Detects radiation levels for nuclear facility simulation.
- **Specifications**: Measures counts per minute (CPM), compatible with Arduino/Pi.
- **Why Budget**: Basic modules are affordable; for thesis, use as mock data source.
- **Price**: $20-40
- **Where to Buy**: eBay, AliExpress, or specialized radiation sensor vendors.
- **Notes**: May require calibration; for budget, simulate with software if real sensor is too costly.

## Accessories and Enclosures

### 7. GPIO Breakout Board and Jumper Wires
- **Purpose**: Connects sensors to Raspberry Pi GPIO pins.
- **Specifications**: 40-pin header, assorted male/female wires.
- **Price**: $5-10
- **Where to Buy**: Adafruit or Amazon.

### 8. Plastic Enclosure for Raspberry Pi
- **Purpose**: Protects the Pi from dust and minor damage.
- **Specifications**: Ventilated case with fan mount (optional).
- **Price**: $5-15
- **Where to Buy**: Raspberry Pi store or Amazon.

### 9. Optional: Basic Robotic Arm (Servo-Based)
- **Purpose**: Simulates robotic manipulation for positioning the camera.
- **Specifications**: 3-4 servo motors, Arduino-compatible (e.g., MeArm or DIY kit).
- **Why Budget**: Not essential for core detection; add for full robotic demo.
- **Price**: $20-50
- **Where to Buy**: Amazon, eBay, or robotics kits from SparkFun.
- **Notes**: Requires additional servo controller ($10-20) and power supply.

## Total Estimated Cost Breakdown
- **Core Components**: $60-90 (Pi + SD + Power + Camera)
- **Sensors**: $25-50 (Temperature + Radiation)
- **Accessories**: $15-35 (Breakout, enclosure, wires)
- **Optional Robotic Arm**: $30-70
- **Grand Total (without arm)**: $100-175
- **Grand Total (with arm)**: $130-245

## Assembly and Setup Notes
1. **Software Installation**: Flash Raspberry Pi OS Lite to SD card, install dependencies from `requirements.txt`, and transfer your scripts.
2. **Sensor Wiring**: Follow tutorials for DS18B20 (1-wire) and Geiger module (serial/I2C). Update `robot_detection.py` to read real sensor data instead of mocks.
3. **Testing**: Start with camera detection, then add sensors. Use a breadboard for prototyping.
4. **Power Considerations**: Ensure stable power; radiation sensors may need separate batteries.
5. **Safety**: For nuclear simulation, handle sensors carefully—consult guidelines for radiation devices.

## Notes for Nuclear Facility Adaptation
While this is a budget setup, for real nuclear use, components would need upgrading (e.g., radiation-hardened Pi alternatives at $500+). This version serves as a thesis prototype to demonstrate feasibility without full compliance costs.

For sourcing, check local makerspaces or university labs for discounts. If you need wiring diagrams or code snippets for sensor integration, let me know!