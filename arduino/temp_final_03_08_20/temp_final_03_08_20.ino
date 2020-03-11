//Use these packages
#include <OneWire.h>
#include <DallasTemperature.h>

//Data wire plugged into digital pin 2 on Arduino
#define ONE_WIRE_BUS 2

// Setup a oneWire instance to communicate with any OneWire device
OneWire oneWire(ONE_WIRE_BUS);

// Pass oneWire reference to DallasTemperature library
DallasTemperature sensors(&oneWire);

int deviceCount = 0;
float tempC;

//Initialize the bus and detects all DS18B20s in it.
void setup(void)
{
  sensors.begin();  // Start up the library
  Serial.begin(9600);

  // locate devices on the bus
  Serial.print("Locating devices...");
  Serial.print("Found ");
  deviceCount = sensors.getDeviceCount();
  Serial.print(deviceCount, DEC);
  Serial.println(" devices.");
  Serial.println("");
}

void loop(void)
{
  // Send command to all the sensors for temperature conversion
  sensors.requestTemperatures();

  // Display temperature from each sensor, loop from i = 0 to i < devicecount
  for (int i = 0;  i < deviceCount;  i++)
  {
    Serial.print("Sensor ");
    Serial.print(i + 1);
    Serial.print(" : ");
    tempC = sensors.getTempCByIndex(i);
    Serial.print(tempC); //Degrees Celcius
    Serial.print("C  |  ");
    Serial.print(DallasTemperature::toFahrenheit(tempC)); //Degrees Fahrenheit
    Serial.println("F");
  }

  Serial.println("");
  delay(1000);
}

// Plug power to 5V, ground to GND, and the middle wire (purple) to pin 2 (or whatever pin set above)
//Remember to install the <OneWire.h> and <DallasTemperature.h> packages, or simply use the files I included in this folder.
//If shows error "bad file descripter" or "failed to send command to serial port,
//Go to Tools > Port > Arduino Mega 2560 , or change to whatever arduino is being used.
