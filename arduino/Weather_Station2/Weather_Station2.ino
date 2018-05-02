

#include <Wire.h>
#include <cactus_io_BME280_I2C.h>
#include <RTClib.h>

// Create the BME280 object
BME280_I2C bme;              // I2C using default 0x77 
RTC_DS3231 rtc;

char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};


void setup() {
  Serial.begin(9600);

  if (!bme.begin()) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }
  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);
  }
  if (rtc.lostPower()) {
    // following line sets the RTC to the date & time this sketch was compiled
    rtc.adjust(DateTime(2018,4,18,13,49,0));
    // This line sets the RTC with an explicit date & time, for example to set
    // January 21, 2014 at 3am you would call:
    // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
  }
  bme.setTempCal(-1);
  
  
}

void loop() {
    bme.readSensor();
    DateTime now = rtc.now();
    float Pressure = bme.getPressure_MB();
    float Humidity = bme.getHumidity();
    float Temperature = bme.getTemperature_C();
    Serial.print(daysOfTheWeek[now.dayOfTheWeek()]); Serial.print("\t");
    Serial.print(now.hour(), DEC); Serial.print("\t");
    Serial.print(Temperature); Serial.print("\t");
    Serial.print(Pressure); Serial.print("\t");
    Serial.print(Humidity); Serial.println();
    
    // add a 2 second delay to slow down the output
    delay(5000);
}
