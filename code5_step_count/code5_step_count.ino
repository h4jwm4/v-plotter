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
  digitalWrite(dirX, HIGH); // Clockwise rotation
  rotateSteps(200); // Quarter rotation
  delay(1000);

  rotateSteps(400); // Half rotation
  delay(1000);

  rotateSteps(800); // Full rotation
  delay(1000);

  digitalWrite(dirX, LOW); // Counterclockwise rotation
  rotateSteps(800); // Full rotation
  delay(1000);
}

void rotateSteps(int steps) {
  for (int x = 0; x < steps; x++) {
    digitalWrite(stepX, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepX, LOW);
    delayMicroseconds(1000);
  }
}
