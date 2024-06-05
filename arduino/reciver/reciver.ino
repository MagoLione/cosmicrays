 // Settings
 unsigned short int pin = 7; // Input Pin
 unsigned long baudRate = 19200; // Baud Rate for serial communication

 // Initializing variables
 int pOS;

void setup() {
  // Initializing serial communication
  Serial.begin(baudRate);
  
  // Initializing input pin
  pinMode(pin, INPUT);
}

void loop() {

  // Reading the pin state
  int pinState = digitalRead(pin);
  
  // Validating input
  if (pinState != pOS) {
    if (pinState == HIGH) {

      // Informing that a CosmicRay has been received.
      Serial.println("0");
    }
    pOS = pinState;
  }
}
