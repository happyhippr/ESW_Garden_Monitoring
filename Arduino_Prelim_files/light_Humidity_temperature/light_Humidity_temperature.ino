////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Include Libraries
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#include <Wire.h>                 //light sensor
#include <Adafruit_Sensor.h>      // Light Sensor 
#include "Adafruit_TSL2591.h"     // Light Sensor

#include <DHT.h>                  // Temp/Humidity Sensor
#include <DHT_U.h>                // Temp/Humidity Sensor



// Create variables / object instances
Adafruit_TSL2591 tsl = Adafruit_TSL2591(2591); // pass in a number for the sensor identifier (for your use later)
#define DHTPIN 12     // Digital pin connected to the DHT sensor 
#define DHTTYPE    DHT11     // DHT 11
DHT_Unified dht(DHTPIN, DHTTYPE);
uint32_t delayMS;



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Define User Functions
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**************************************************************************/
/*
    Configures the gain and integration time for the TSL2591 Light Sensor
*/
/**************************************************************************/
void configureSensor(void) // setup Light sensor
{
  // You can change the gain on the fly, to adapt to brighter/dimmer light situations
  //tsl.setGain(TSL2591_GAIN_LOW);    // 1x gain (bright light)
  //Serial.println("trying to set gain");
  tsl.setGain(TSL2591_GAIN_MED);      // 25x gain
  //tsl.setGain(TSL2591_GAIN_HIGH);   // 428x gain
  
  // Changing the integration time gives you a longer time over which to sense light
  // longer timelines are slower, but are good in very low light situtations!
  //tsl.setTiming(TSL2591_INTEGRATIONTIME_100MS);  // shortest integration time (bright light)
  // tsl.setTiming(TSL2591_INTEGRATIONTIME_200MS);
  tsl.setTiming(TSL2591_INTEGRATIONTIME_300MS);
  // tsl.setTiming(TSL2591_INTEGRATIONTIME_400MS);
  // tsl.setTiming(TSL2591_INTEGRATIONTIME_500MS);
  // tsl.setTiming(TSL2591_INTEGRATIONTIME_600MS);  // longest integration time (dim light)

  /* Display the gain and integration time for reference sake */  
  //Serial.println(F("------------------------------------"));
  //.print  (F("Gain:         "));
  tsl2591Gain_t gain = tsl.getGain();
  switch(gain)
  {
    case TSL2591_GAIN_LOW:
      //Serial.println(F("1x (Low)"));
      break;
    case TSL2591_GAIN_MED:
      //Serial.println(F("25x (Medium)"));
      break;
    case TSL2591_GAIN_HIGH:
      //Serial.println(F("428x (High)"));
      break;
    case TSL2591_GAIN_MAX:
      //Serial.println(F("9876x (Max)"));
      break;
  }
  //Serial.print  (F("Timing:       "));
  //Serial.print((tsl.getTiming() + 1) * 100, DEC); 
  //Serial.println(F(" ms"));
  //Serial.println(F("------------------------------------"));
  //Serial.println(F(""));
}















/**************************************************************************/
/*
    Program entry point for the Arduino sketch
*/
/**************************************************************************/
void setup(void) 
{
  Serial.begin(9600);
  /////////////////////////////////////////////////////
  ////// Setup for Light Sensor //////////////////
  if (!tsl.begin()) 
  {
    Serial.println(F("No sensor found ... check your wiring?"));
    while(true){};
  } 
  configureSensor();


  /////////////////////////////////////////////////////////
  // Setup for Temp & Humidity Sensing
  dht.begin();
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  dht.humidity().getSensor(&sensor);
  delayMS = sensor.min_delay / 1000;
  
}

/**************************************************************************/
/*
    Arduino loop function, called once 'setup' is complete (your own code
    should go here)
*/
/**************************************************************************/
void loop(void) 
{

  while(!Serial.available()>0){
    char input = char(Serial.read());

    if(input = '1'){
      Serial.println("111.222,1213423.0,");
    }
    else if(input = '2'){
      Serial.println("printing signal names");
    }
    
  }


   /*
  ///////////////////////////////
  // Extract & Print Lux Reading
  uint32_t lum = tsl.getFullLuminosity();
  uint16_t ir, full;
  ir = lum >> 16;
  full = lum & 0xFFFF;
  Serial.print(F("Lux: ")); Serial.print(tsl.calculateLux(full, ir), 6);Serial.print(", ");

  ////////////////////////////////
  // Print Humidity & Temp Reading
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.print(F("Error reading temperature!, "));
  }
  else {
    Serial.print(F("Temperature: "));
    Serial.print(event.temperature);
    Serial.print(F("°C"));
    Serial.print(", ");
  }
  // Print Humidity
  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println(F("Error reading humidity!, "));
  }
  else {
    Serial.print(F("Humidity: "));
    Serial.print(event.relative_humidity);
    Serial.print(F("%"));
    Serial.print(", ");
  }



  Serial.println();
  */



  

  //delay(1000);
}
