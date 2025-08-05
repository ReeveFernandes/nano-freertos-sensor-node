#pragma once
#include <Arduino.h>
struct SensorMsg { float temp, hum, press; };
bool bmeInit(uint8_t addr = 0x76);
SensorMsg bmeRead();