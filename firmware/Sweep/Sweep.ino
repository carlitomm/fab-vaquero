// Sweep
// by BARRAGAN <http://barraganstudio.com> 
// This example code is in the public domain.


#include <Servo.h>
int incoming;
float errorX;
float u;
float kpLarge = 0.055;
float kpMiddle = 0.030;
float kpShort = 0.010;
float absoluteError;

Servo myservo;  // create servo object to control a servo 
// a maximum of eight servo objects can be created 

float pos = 90;    // variable to store the servo position 

void setup() 
{ 
  Serial.begin(115200);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo.write(pos); 
} 

void loop() 
{ 
  if(Serial.available() > 0)
  {
    incoming = Serial.read();
    if (incoming  ==  'l')
    { 
      errorX = Serial.parseFloat();
      absoluteError = abs(errorX);


      if ( absoluteError > 80)
      {
        u = kpLarge * errorX;
      }
      
      if ( absoluteError <= 80 && absoluteError > 20)
      {
        u = kpMiddle * errorX;
      }
      if ( absoluteError <= 20 )
      {
        u = kpShort * errorX;
      }

      if( absoluteError > 2)
      {
        if (errorX > 0){
          //pos = pos - 5;
          pos = pos - u;        
          myservo.write(pos);             
          //delay(2);
          
          //limpia la entrada
          Serial.flush();    
          incoming = Serial.read();      
        }
        if (errorX < 0){
          //pos = pos + 5;
          pos = pos - u;        
          myservo.write(pos);              
          //delay(2);
          
          //limpia la entrada 
          Serial.flush();
          incoming = Serial.read();          
        }
      } 
    } 
  }


} 
















