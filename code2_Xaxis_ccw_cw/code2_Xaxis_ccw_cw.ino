const int stepX = 2; // Pin for step signal
const int dirX  = 5; // Pin for direction signal
const int enPin = 8; // Pin to enable the motor driver

void setup() {
  pinMode(stepX, OUTPUT);
  pinMode(dirX, OUTPUT);
  pinMode(enPin, OUTPUT);

  digitalWrite(enPin, LOW); // Enable the motor driver
}

void loop() {
  // Clockwise Rotation
  digitalWrite(dirX, HIGH); // Set direction to clockwise
  rotateMotor();

  delay(1000); // Wait for 1 second

  // Counterclockwise Rotation
  digitalWrite(dirX, LOW); // Set direction to counterclockwise
  rotateMotor();

  delay(1000); // Wait for 1 second
}

void rotateMotor() {
  for (int x = 0; x < 800; x++) { // One full rotation
    digitalWrite(stepX, HIGH); // Generate a step pulse
    delayMicroseconds(1000);  // Hold HIGH for 1 millisecond

    digitalWrite(stepX, LOW);  // Step pulse ends
    delayMicroseconds(1000);   // Hold LOW for 1 millisecond
  }
}
