#include <OneWire.h>
#include <DallasTemperature.h>
#include <SoftwareSerial.h>

OneWire ds18x20[] = {7, 3, 10, 9, 6, 4, 8, 5, 2};
const int oneWireCount = sizeof(ds18x20) / sizeof(OneWire);
DallasTemperature sensor[oneWireCount];
DeviceAddress deviceAddress;
void setup(void) {
  Serial.begin(9600);
}

void loop(void) {
  if (Serial.available()) {
    if (Serial.read() == 'r')
      func();
  }
}

void func(void) {
  for (int i = 0; i < oneWireCount; i++) {
    ;
    sensor[i].setOneWire(&ds18x20[i]);
    sensor[i].begin();
    if (sensor[i].getAddress(deviceAddress, 0)) sensor[i].setResolution(deviceAddress, 12);
  }

  for (int i = 0; i < oneWireCount; i++) {
    sensor[i].requestTemperatures();
    float temperature = sensor[i].getTempCByIndex(0);
    if (temperature > 27) {
      Serial.write("2");
    }
    else Serial.write("1");
  }

 // for (int i = 0; i < oneWireCount; i++) {
   // float temperature = sensor[i].getTempCByIndex(0);
  //  if (temperature > 27) {
 //     Serial.write("2");
 //   }
 //   else Serial.write("1");
//  }
}
