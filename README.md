FreeRTOS-Based Sensor Node with Arduino Uno & BME280

📌 Overview

This project demonstrates a real-time sensor node built using:
	•	Arduino Uno
	•	BME280 Environmental Sensor (I2C)
	•	FreeRTOS (via PlatformIO)
	•	JSON-formatted UART output

It utilizes FreeRTOS tasks for concurrency and includes basic error handling for I2C communication.

⸻

🔧 Hardware Requirements
	•	Arduino Uno (or compatible clone)
	•	BME280 I2C sensor module
	•	Breadboard + jumper wires
	•	USB cable

⸻

🧰 Software Requirements
	•	PlatformIO CLI
	•	Python 3 (for PlatformIO)
	•	macOS, Linux, or Windows

⸻

🚀 Getting Started

1. Clone the Project

git clone https://github.com/yourusername/nano-freertos-sensor-node.git
cd nano-freertos-sensor-node

2. Initialize PlatformIO

pio project init --board uno --project-option="framework=arduino"

3. Install Required Libraries

pio lib install "Adafruit BME280 Library"
pio lib install "FreeRTOS"

4. Upload to Board

Make sure your Arduino Uno is connected via USB:

pio run -t upload --upload-port /dev/cu.usbserial-XXXX

Replace XXXX with the actual port. Use pio device list to find it.

5. Monitor Output

pio device monitor -b 115200 --port /dev/cu.usbserial-XXXX

You should see:

{"T":24.15,"H":48.32,"P":1001.88}
{"T":24.12,"H":48.40,"P":1002.01}


⸻

🧠 Architecture
	•	Task 1: Reads data from BME280 sensor
	•	Task 2: Serializes and outputs data in JSON
	•	Queue: Shared message buffer between the two tasks

⸻

🐞 Common Issues
	•	Upload Fails (stk500_recv()):
	•	Try pressing RESET during upload
	•	Switch to uno_old_bootloader in platformio.ini
	•	No Sensor Found:
	•	Check SDA/SCL wiring (A4/A5 on Uno)
	•	Try I2C scanner sketch
	•	Output Shows ?:
	•	AVR printf doesn’t support floats. Use Serial.print() instead.

⸻

📁 Project Structure

nano-freertos-sensor-node/
├── include/              # Header files (optional)
├── lib/                  # Custom libraries (if needed)
├── src/
│   └── main.cpp          # Main application logic
├── platformio.ini        # PlatformIO build config
└── README.md             # Project overview


⸻

📈 Future Improvements
	•	Add command parsing via UART
	•	Add MQTT output via WiFi microcontroller
	•	Port to ESP32 or STM32

⸻

🤝 Credits

Created by Reeve Fernandes — inspired by real embedded debugging and hands-on hardware work.

⸻

📜 License

MIT License. See LICENSE file for details.
