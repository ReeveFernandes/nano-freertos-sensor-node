#!/usr/bin/env python3
"""
Bridge: Serial JSON from your board  ->  MQTT (Mosquitto) topic.

- Reads newline-delimited JSON from a serial port (e.g., PlatformIO Monitor output).
- Accepts either short keys T/H/P or long keys temp/hum/press.
- Publishes numeric fields to MQTT topic (default: sensors/bme280) on localhost:1883.

Usage examples:
  python serial_to_mqtt.py
  python serial_to_mqtt.py --port /dev/tty.usbmodem1234
  python serial_to_mqtt.py --mqtt-host 127.0.0.1 --topic sensors/lab/bme280 --quiet

Tip: Close PlatformIO Serial Monitor before running this (only one program can use the port).
"""

import argparse
import json
import sys
import time
import glob
from typing import Optional

import serial                    # pyserial
import paho.mqtt.client as mqtt  # paho-mqtt


# ---- Helpers ---------------------------------------------------------------

def autodetect_port() -> Optional[str]:
    """
    Try to find a likely USB serial device (macOS patterns).
    Extend with Linux patterns if needed (e.g., /dev/ttyACM* /dev/ttyUSB*).
    """
    candidates = sorted(
        glob.glob("/dev/tty.usbmodem*") +  # common for ARM boards on macOS
        glob.glob("/dev/tty.usbserial*")   # common for USB-serial adapters
    )
    return candidates[0] if candidates else None


def to_float(x) -> Optional[float]:
    """Coerce anything to float; return None if it can't be parsed."""
    try:
        return float(x)
    except Exception:
        return None


# ---- CLI args --------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Serial -> MQTT bridge")
    p.add_argument("--port", default=autodetect_port(),
                   help="Serial port (auto-detected if possible; run `ls /dev/tty.*` to list)")
    p.add_argument("--baud", type=int, default=115200,
                   help="Serial baud rate (must match your firmware)")
    p.add_argument("--mqtt-host", default="localhost",
                   help="MQTT broker host (our Mosquitto runs on the host at localhost)")
    p.add_argument("--mqtt-port", type=int, default=1883,
                   help="MQTT broker port")
    p.add_argument("--topic", default="sensors/bme280",
                   help="MQTT topic to publish JSON to")
    p.add_argument("--quiet", action="store_true",
                   help="Reduce console output")
    return p.parse_args()


# ---- Main ------------------------------------------------------------------

def main() -> int:
    args = parse_args()

    # 1) Serial setup ---------------------------------------------------------
    if not args.port:
        print("No serial port auto-detected.\n"
              "Run: ls /dev/tty.*  and pass --port /dev/tty.usbmodemXXXX",
              file=sys.stderr)
        return 1

    print(f"Serial: {args.port} @ {args.baud}")
    try:
        ser = serial.Serial(args.port, args.baud, timeout=1)
    except Exception as e:
        print(f"ERROR opening serial {args.port}: {e}", file=sys.stderr)
        return 2

    # 2) MQTT setup -----------------------------------------------------------
    print(f"MQTT:   {args.mqtt_host}:{args.mqtt_port} → topic '{args.topic}'")
    client = mqtt.Client()
    try:
        client.connect(args.mqtt_host, args.mqtt_port, keepalive=60)
        client.loop_start()  # background network loop
    except Exception as e:
        print(f"ERROR connecting to MQTT {args.mqtt_host}:{args.mqtt_port}: {e}", file=sys.stderr)
        return 3

    # 3) Read/convert/publish loop -------------------------------------------
    try:
        while True:
            # Read one line of text from the serial port
            raw = ser.readline().decode("utf-8", "ignore").strip()
            if not raw:
                continue

            # Expect a JSON object per line from your firmware
            try:
                obj = json.loads(raw)
            except Exception:
                if not args.quiet:
                    print("skip (not JSON):", raw[:100])
                continue

            # Accept either {T,H,P} or {temp,hum,press}; coerce to floats
            temp  = to_float(obj.get("temp",  obj.get("T")))
            hum   = to_float(obj.get("hum",   obj.get("H")))
            press = to_float(obj.get("press", obj.get("P")))

            # If any field is missing or non-numeric, skip this line
            if None in (temp, hum, press):
                if not args.quiet:
                    print("skip (missing numeric fields):", raw[:100])
                continue

            # Build normalized payload and publish to MQTT
            out = {"temp": temp, "hum": hum, "press": press}
            client.publish(args.topic, json.dumps(out), qos=0, retain=False)

            if not args.quiet:
                print("MQTT ←", out)

    except KeyboardInterrupt:
        print("\nExiting…")

    # 4) Cleanup --------------------------------------------------------------
    try:
        client.loop_stop()
        client.disconnect()
    except Exception:
        pass

    try:
        ser.close()
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())