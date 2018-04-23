
// declare functions
float getTemperature(float);
float getPressure(float);
float getHumidity(float);

void acquire_data(void);

//global variables
float current_temperature;
float current_pressure;
float current_humidity;

void setup() {
  // start serial port at 9600:
  Serial.begin(9600);
  while (!Serial)
  {
     //wait for serial port to connect
  }
  current_temperature = 20;
  current_pressure = 989.6;
  current_humidity = 79.5;
  
}

void loop() {
  randomSeed((long) (current_temperature * current_pressure * current_humidity));
  // check for serial input:
  if(Serial.available() > 0)
  {
    byte incoming_byte = Serial.read();
    if (incoming_byte == '1')
    {
      acquire_data();
    }
              
  }
}

void acquire_data(void)
{
  current_temperature = getTemperature(current_temperature);
  current_pressure = getPressure(current_pressure);
  current_humidity = getHumidity(current_humidity);
  Serial.print(current_temperature);
  Serial.print(",");
  Serial.print(current_pressure);
  Serial.print(",");
  Serial.println(current_humidity);  
}

// functions to simulate bme280
float getTemperature(float current_temp)
{
  float temperature;
  float max_temp = 38.5;
  float min_temp = -27.2;
  float max_variation = 5;
  long temp_variation = random((max_variation)+1);
  long variation_direction = random(2);
  
  if (variation_direction < 1)
  {
    temperature = current_temp - temp_variation;
    if (temperature < min_temp)
    {
      temperature = min_temp;
    }
  }
  else
  {
    temperature = current_temp + temp_variation;
    if (temperature > max_temp)
    {
      temperature = max_temp;
    }
  }
  return temperature;
   
  
}
float getPressure(float current_press)
{
  float pressure;
  float max_press = 1053.6;
  float min_press = 925.6;
  float max_variation = 10;
  long press_variation = random((max_variation)+1);
  long variation_direction = random(2);
  
  if (variation_direction < 1)
  {
    pressure = current_press - press_variation;
    if (pressure < min_press)
    {
      pressure = min_press;
    }
  }
  else
  {
    pressure = current_press + press_variation;
    if (pressure > max_press)
    {
      pressure = max_press;
    }
  }
  return pressure;
}
float getHumidity(float current_hum)
{
  float humidity;
  float max_hum = 90;
  float min_hum = 69;
  float max_variation = 5;
  long hum_variation = random((max_variation)+1);
  long variation_direction = random(2);
  
  if (variation_direction < 1)
  {
    humidity = current_hum - hum_variation;
    if (humidity < min_hum)
    {
      humidity = min_hum;
    }
  }
  else
  {
    humidity = current_hum + hum_variation;
    if (humidity > max_hum)
    {
      humidity = max_hum;
    }
  }
  return humidity;
}

