#include <Servo.h>

// Settings
unsigned long baudRate = 19200; // Baud Rate for serial communication

// Initializing variables
Servo servo;
unsigned short int oldAngle = 0;
unsigned short int angle = 0;

void setup() {

  // Initializing serial communication
  Serial.begin(baudRate);

  // Attaching servo
  servo.attach(9);
}

void loop() {

  servo.write(oldAngle);

  // Reading serial communications
  if (Serial.available() > 0) {
    
    angle = Serial.parseInt();

    // Validating serial data (from 1 to 181, 0's use causes problems)
    if (angle > 0 && angle <= 181) {

      // Issuing feedback (returns 1 if it changes, else 0)
      if (angle-1 != oldAngle) {
        oldAngle = angle-1;
        Serial.println("1");
      } else {
        Serial.println("0");
      }
    }

  }
}