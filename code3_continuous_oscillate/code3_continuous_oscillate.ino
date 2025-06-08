const int stepX = 2;
const int dirX  = 5;
const int enPin = 8;

void setup() {
  pinMode(stepX, OUTPUT);
  pinMode(dirX, OUTPUT);
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW); // Enable the motor driver
}

void loop() {
  // Oscillate back and forth
  for (int i = 0; i < 5; i++) { // Repeat 5 oscillations
    digitalWrite(dirX, HIGH); // Clockwise rotation
    rotateSteps(400);         // Half rotation
    delay(500);               // Pause

    digitalWrite(dirX, LOW); // Counterclockwise rotation
    rotateSteps(400);        // Half rotation
    delay(500);              // Pause
  }
  delay(2000); // Pause before repeating
}

void rotateSteps(int steps) {
  for (int x = 0; x < steps; x++) {
    digitalWrite(stepX, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepX, LOW);
    delayMicroseconds(1000);
  }
}
