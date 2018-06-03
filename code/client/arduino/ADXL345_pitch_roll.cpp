/*
    ADXL345 Triple Axis Accelerometer. Pitch & Roll calculation
    Read more: http://www.jarzebski.pl/arduino/czujniki-i-sensory/3-osiowy-akcelerometr-adxl345.html
    GIT: https://github.com/jarzebski/Arduino-ADXL345
    Web: http://www.jarzebski.pl
    (c) 2014 by Korneliusz Jarzebski
    modified by VeniZhang
*/

#include <Wire.h>
#include "ADXL345.h"
#define MAX 15
#include <math.h>
#include <SoftwareSerial.h>
#define COUNT 5
SoftwareSerial BluetoothSerial(10, 11); // RX, TX
char recv_char, sent_char;
String sent_data = "";
String recv_data = "";
bool isSame = 0;
char tmp = 'x';
char dirction = 'X';
ADXL345 accelerometer;
int count = 0;



void setup(void) 
{
    pinMode(6, OUTPUT);
    pinMode(5, OUTPUT);
    digitalWrite(6, HIGH);
    digitalWrite(5, LOW);
    Serial.begin(9600);
    BluetoothSerial.begin(9600);
    while (!BluetoothSerial)
   {
   }
  // Initialize ADXL345
    Serial.println("Initialize ADXL345");
    if (!accelerometer.begin())
    {
        Serial.println("Could not find a valid ADXL345 sensor, check wiring!");
        delay(500);
    }
  // Set measurement range
  // +/-  2G: ADXL345_RANGE_2G
  // +/-  4G: ADXL345_RANGE_4G
  // +/-  8G: ADXL345_RANGE_8G
  // +/- 16G: ADXL345_RANGE_16G
     accelerometer.setRange(ADXL345_RANGE_16G);
}
void loop(void) 
{
  // Read normalized values
    Vector norm = accelerometer.readNormalize();

  // Low Pass Filter to smooth out data. 0.1 - 0.9
    Vector filtered = accelerometer.lowPassFilter(norm, 0.5);

  // Calculate Pitch & Roll
    int pitch = -(atan2(norm.XAxis, sqrt(norm.YAxis*norm.YAxis + norm.ZAxis*norm.ZAxis))*180.0)/M_PI;
    int roll  = (atan2(norm.YAxis, norm.ZAxis)*180.0)/M_PI;

  // Calculate Pitch & Roll (Low Pass Filter)
    int fpitch = -(atan2(filtered.XAxis, sqrt(filtered.YAxis*filtered.YAxis + filtered.ZAxis*filtered.ZAxis))*180.0)/M_PI;
    int froll  = (atan2(filtered.YAxis, filtered.ZAxis)*180.0)/M_PI;

  // Output
  /*
  Serial.print(" Pitch = ");
  Serial.print(pitch);
  Serial.print(" Roll = ");
  Serial.print(roll);

  // Output (filtered)
  Serial.print(" (filter)Pitch = ");
  Serial.print(fpitch);
  Serial.print(" (filter)Roll = ");
  Serial.print(froll);
  Serial.println();
  */
      if(pitch > MAX)
      {
          dirction = 'L';
      }
      else if (pitch < -MAX)
      {
          dirction = 'R';
      }
      else if(froll > MAX)
      {
          dirction = 'U';
      }
      else if (froll < -MAX)
     {
        dirction = 'D';
     }
     if(tmp == dirction)
         {
          isSame = 1;
          if (tmp == 'U')
              {
                count ++;
              }
          else 
            count = 0;
         }
     else 
     {
         isSame = 0;
         count = 0;
     }
     tmp = dirction;
     if(!isSame || count > COUNT)
     {  
        if (count <= COUNT)
        {
            Serial.println(dirction);
            BluetoothSerial.write(dirction);
        }
        else
          {
              
             Serial.println('K');
             BluetoothSerial.write('K');
             count = 0;
             delay(100);

          }
        BluetoothSerial.write('\n');
        BluetoothSerial.flush();
     }


}
