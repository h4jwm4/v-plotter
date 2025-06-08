#include <AccelStepper.h>

// Motor interface: 1 = Driver (step/dir)
#define motorInterfaceType 1

// Define motor control pins
#define stepPin 2
#define dirPin 5
#define enPin 8

// Create an instance of AccelStepper
AccelStepper stepper(motorInterfaceType, stepPin, dirPin);

void setup() {
  pinMode(enPin, OUTPUT); 
  digitalWrite(enPin, LOW);  // Enable driver (LOW = enabled)

  stepper.setMaxSpeed(1000);       // Set max speed (steps per second)
  stepper.setAcceleration(200);    // Set acceleration (steps per second^2)
  stepper.moveTo(1000);            // Target position
}

void loop() {
  // If at target, go to opposite side
  if (stepper.distanceToGo() == 0) {
    stepper.moveTo(-stepper.currentPosition());
  }

  // Move motor one step
  stepper.run();
}
