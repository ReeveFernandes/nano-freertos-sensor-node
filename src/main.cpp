#include <Arduino.h>
#include <Arduino_FreeRTOS.h>
#include <task.h>

void fastBlink(void*){
  pinMode(LED_BUILTIN, OUTPUT);
  for(;;){ digitalWrite(LED_BUILTIN, HIGH); vTaskDelay(pdMS_TO_TICKS(250));
           digitalWrite(LED_BUILTIN, LOW ); vTaskDelay(pdMS_TO_TICKS(250)); }
}
void slowBlink(void*){
  pinMode(LED_BUILTIN, OUTPUT);
  for(;;){ digitalWrite(LED_BUILTIN, HIGH); vTaskDelay(pdMS_TO_TICKS(500));
           digitalWrite(LED_BUILTIN, LOW ); vTaskDelay(pdMS_TO_TICKS(500)); }
}
void setup(){
  xTaskCreate(fastBlink, "fast", 128, NULL, 1, NULL);
  xTaskCreate(slowBlink, "slow", 128, NULL, 1, NULL);
}
void loop(){}   // not used with FreeRTOS