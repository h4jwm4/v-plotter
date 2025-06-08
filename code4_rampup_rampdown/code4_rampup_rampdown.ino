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
  rampSpeed();

  delay(1000);

  digitalWrite(dirX, LOW); // Counterclockwise rotation
  rampSpeed();

  delay(1000);
}

void rampSpeed() {
  // Ramp up
  for (int speed = 2000; speed >= 200; speed -= 200) {
    rotateSteps(100, speed);
  }
  // Ramp down
  for (int speed = 200; speed <= 2000; speed += 200) {
    rotateSteps(100, speed);
  }
}

void rotateSteps(int steps, int speed) {
  for (int x = 0; x < steps; x++) {
    digitalWrite(stepX, HIGH);
    delayMicroseconds(speed);
    digitalWrite(stepX, LOW);
    delayMicroseconds(speed);
  }
}
