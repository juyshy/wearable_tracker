#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>

#include <Adafruit_10DOF.h>

/*
modified fromg here
https://github.com/adafruit/Adafruit_10DOF/blob/master/tester/tester.pde
*/

/* Assign a unique ID to the sensors */
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(30301);

 
void setup(void)
{
  Serial.begin(115200);
  Serial.println(F("Adafruit 10DOF Tester"));  
  
  /* Initialise the sensors */
  if(!accel.begin())
  {
    /* There was a problem detecting the ADXL345 ... check your connections */
    Serial.println(F("Ooops, no LSM303 detected ... Check your wiring!"));
    while(1);
  }
 
}

void loop(void)
{
  /* Get a new sensor event */
  sensors_event_t event;
   
  /* Display the results (acceleration is measured in m/s^2) */
  accel.getEvent(&event);  
  
  int val_x = event.acceleration.x * 100;
  int val_y = event.acceleration.y * 100;
  int val_z = event.acceleration.z * 100;
  Serial.print(val_x);
  Serial.print(" ");
  Serial.print(val_y);
  Serial.print(" ");
  Serial.print(val_z);
  Serial.print("\n");

  delay(100);
}
