#include <Wire.h>
#include <Adafruit_ADS1015.h>
#include <Adafruit_INA219.h>

Adafruit_INA219 ina219; // for Power Consumption Sensing
Adafruit_ADS1115 ads;  /* Use this for the 16-bit version */
//Adafruit_ADS1015 ads;     /* Use thi for the 12-bit version */

void setup(void) 
{
  Serial.begin(9600);
  

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

void loop(void) 
{


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
  Serial.println("");


  
  delay(1000);
}
