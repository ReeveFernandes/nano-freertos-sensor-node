#include "bme280_driver.h"
#include <Adafruit_BME280.h>

static Adafruit_BME280 bme;

bool bmeInit(uint8_t addr){
  return bme.begin(addr);           // returns true on success
}

SensorMsg bmeRead(){
  SensorMsg m;
  m.temp  = bme.readTemperature();          // °C
  m.hum   = bme.readHumidity();             // %
  m.press = bme.readPressure()/100.0F;      // hPa
  return m;
}