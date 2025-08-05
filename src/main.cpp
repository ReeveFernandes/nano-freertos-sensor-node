#include <Arduino.h>
#include <Arduino_FreeRTOS.h>
#include <queue.h>
#include "bme280_driver.h"

QueueHandle_t sensorQ;
uint32_t sampleRate = 1000;   // ms

void sensorTask(void*){
  if(!bmeInit(0x77)){
    // Flash LED fast if sensor not found
    pinMode(LED_BUILTIN, OUTPUT);
    for(;;){ digitalWrite(LED_BUILTIN,!digitalRead(LED_BUILTIN));
             vTaskDelay(pdMS_TO_TICKS(1000)); }
  }
  for(;;){
    SensorMsg msg = bmeRead();
    xQueueSend(sensorQ, &msg, portMAX_DELAY);
    vTaskDelay(pdMS_TO_TICKS(sampleRate));
  }
}

void serialTask(void*){
  Serial.begin(115200);
  SensorMsg msg;
//   char buf[64];
  for(;;){
    if(xQueueReceive(sensorQ,&msg,portMAX_DELAY)==pdTRUE){
    //   snprintf(buf,sizeof(buf),
    //      "{\"T\":%.2f,\"H\":%.2f,\"P\":%.2f}\\n",
    //      msg.temp,msg.hum,msg.press);
    //   Serial.print(buf);
        Serial.print('{');
        Serial.print("\"T\":");  Serial.print(msg.temp, 2);
        Serial.print(",\"H\":"); Serial.print(msg.hum, 2);
        Serial.print(",\"P\":"); Serial.print(msg.press, 2);
        Serial.println('}');
    }
    // Non-blocking serial read for commands
    if(Serial.available()){
      String line = Serial.readStringUntil('\n');
      if(line.startsWith("{\"rate\":")){
        sampleRate = line.substring(8,line.length()-1).toInt();
      }
    }
  }
}

void setup(){
  sensorQ = xQueueCreate(4, sizeof(SensorMsg));
  xTaskCreate(sensorTask, "sens", 256, nullptr, 1, nullptr);
  xTaskCreate(serialTask, "seri", 256, nullptr, 1, nullptr);
}
void loop(){}