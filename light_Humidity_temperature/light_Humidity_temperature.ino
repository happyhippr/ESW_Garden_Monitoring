////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Include Libraries
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#include <Wire.h>                 //light sensor
#include <Adafruit_Sensor.h>      // Light Sensor 
#include "Adafruit_TSL2591.h"     // Light Sensor
#include <DHT.h>                  // Temp/Humidity Sensor
#include <DHT_U.h>                // Temp/Humidity Sensor
#include <Adafruit_ADS1015.h>    // used to sense thermocouple temperatures
#include <Adafruit_INA219.h>      // used to sense this computers power consumption



// Create variables / object instances
Adafruit_TSL2591 tsl = Adafruit_TSL2591(2591); // pass in a number for the sensor identifier (for your use later)
#define DHTPIN 12     // Digital pin connected to the DHT sensor 
#define DHTTYPE    DHT11     // DHT 11
DHT_Unified dht(DHTPIN, DHTTYPE);
uint32_t delayMS;
Adafruit_INA219 ina219; // for Power Consumption Sensing
Adafruit_ADS1115 ads;  /* Use this for the 16-bit version */
//Adafruit_ADS1015 ads;     /* Use thi for the 12-bit version */


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
  tsl.setGain(TSL2591_GAIN_LOW);    // 1x gain (bright light)
  //tsl.setGain(TSL2591_GAIN_MED);      // 25x gain
  //tsl.setGain(TSL2591_GAIN_HIGH);   // 428x gain
  
  // Changing the integration time gives you a longer time over which to sense light
  // longer timelines are slower, but are good in very low light situtations!
  tsl.setTiming(TSL2591_INTEGRATIONTIME_100MS);  // shortest integration time (bright light)
  //tsl.setTiming(TSL2591_INTEGRATIONTIME_200MS);
  //tsl.setTiming(TSL2591_INTEGRATIONTIME_300MS);
  // tsl.setTiming(TSL2591_INTEGRATIONTIME_400MS);
  // tsl.setTiming(TSL2591_INTEGRATIONTIME_500MS);
  // tsl.setTiming(TSL2591_INTEGRATIONTIME_600MS);  // longest integration time (dim light)

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
}

// measure and then print all signals
void printSignalNamesAndValues(void){
  
  
  
  
  
  //////////////////////////////////////////////////////////////////////////
  /// Measure the temperatures using the ADC and the Thermocouple amplifiers
  double adc0, adc1, adc2, adc3;
  // take some samples and average them
  int count = 10;
  double sum = 0.0;
  double sum2 = 0.0;
  for (int i = 1; i < count+1; i++) {
    sum += ads.readADC_SingleEnded(0);
    sum2 += ads.readADC_SingleEnded(1);
    delay(50);
  }
  sum = sum / count;
  sum2 = sum2/count;
  // Create the scale factor to convert a 16bit int into a 5V double decimal value
  double scale_factor = (5.07/27200.0);
  sum = sum*scale_factor;
  sum2 = sum2*scale_factor;
  // Convert Decimal voltage to temperature in C
  double Temp1 =  (sum - 1.25) / 0.005;
  double Temp2 =  (sum2 - 1.25) / 0.005;


  //////////////////////////////////////////////////////////////////////
  // Measure the input supply power consumped
  float shuntvoltage = 0;
  float supply_voltage = 0;
  float Supply_Current = 0;
  float loadvoltage = 0;
  float power_mW = 0;
  shuntvoltage = ina219.getShuntVoltage_mV();
  supply_voltage = ina219.getBusVoltage_V();
  Supply_Current = (ina219.getCurrent_mA())/1000.0;
  power_mW = (ina219.getPower_mW())/1000.0;
  loadvoltage = supply_voltage + (shuntvoltage / 1000.0);

  ////////////////////////////////////////////////////////////////////
  // Print the results
  Serial.print("Greenhouse_Temp(C):");Serial.print(Temp1);Serial.print(",");
  Serial.print("Outside_Temp(C):");Serial.print(Temp2);Serial.print(",");
  Serial.print("Supply_Voltage(V):"); Serial.print(supply_voltage); Serial.print(",");
  Serial.print("Supply_Current(A):"); Serial.print(Supply_Current);Serial.print(",");
  Serial.print("Supply_Power(W):"); Serial.print(power_mW);Serial.print(",");
  
  
  
  
  

    ///////////////////////////////
  // Extract & Print Lux Reading
  // More advanced data read example. Read 32 bits with top 16 bits IR, bottom 16 bits full spectrum
  // That way you can do whatever math and comparisons you want!
  uint32_t lum = tsl.getFullLuminosity();
  uint16_t ir, full;
  ir = lum >> 16;
  full = lum & 0xFFFF;
  Serial.print(F("IR_spectrum:")); Serial.print(ir);  Serial.print(F(","));
  Serial.print(F("Full_spectrum:")); Serial.print(full); Serial.print(F(","));
  Serial.print(F("Visible_spectrum:")); Serial.print(full - ir); Serial.print(F(","));
  Serial.print(F("Lux:")); Serial.print(tsl.calculateLux(full, ir), 6);Serial.print(",");

  ////////////////////////////////
  // Print Humidity & Temp Reading
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    //Serial.print(F("Error reading temperature!, "));
  }
  else {
    Serial.print(F("Temperature(C):"));
    Serial.print(event.temperature);
    //Serial.print("C");
    Serial.print(",");
  }
  // Print Humidity
  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
   // Serial.println(F("Error reading humidity!, "));
  }
  else {
    Serial.print(F("Humidity(%):"));
    Serial.print(event.relative_humidity);
    //Serial.print("%");
   
  }
  

  Serial.println();
}



void printSignalNames(void){
  Serial.println("Lux,Temperature(C),Humidity(%)");
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
  
  
  
  /////////////////////////////////////////////////////////
  // Setup for thermocouple temp sensing and power consumption sensing
  // Setting the gain/range of your ADC for temp sensing
  //                                                                ADS1015  ADS1115
  //                                                                -------  -------
  ads.setGain(GAIN_TWOTHIRDS);  // 2/3x gain +/- 6.144V    1 bit = 3mV      0.1875mV (default)
  // ads.setGain(GAIN_ONE);        // 1x gain   +/- 4.096V  1 bit = 2mV      0.125mV
  // ads.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  // ads.setGain(GAIN_FOUR);       // 4x gain   +/- 1.024V  1 bit = 0.5mV    0.03125mV
  // ads.setGain(GAIN_EIGHT);      // 8x gain   +/- 0.512V  1 bit = 0.25mV   0.015625mV
  // ads.setGain(GAIN_SIXTEEN);    // 16x gain  +/- 0.256V  1 bit = 0.125mV  0.0078125mV
  ads.begin();
  ina219.begin();
  
  
  
  
}

/**************************************************************************/
/*
    Arduino loop function, called once 'setup' is complete (your own code
    should go here)
*/
/**************************************************************************/
void loop(void) 
{ 

  if(Serial.available()>0){
    char input = char(Serial.read());

    if(input=='1'){
      printSignalNames();
    }
    else if(input=='2'){
      printSignalNamesAndValues();
    } 
   
    
  }
  //printMeasuredValues();
  // delay(1000);
  
}
