const int stepX = 2;
const int dirX  = 5;
const int enPin = 8;

void setup() {
  pinMode(stepX, OUTPUT);
  pinMode(dirX, OUTPUT);
  pinMode(enPin, OUTPUT);

  digitalWrite(enPin, LOW);    // Enable motor driver
  digitalWrite(dirX, HIGH);    // Set direction
}

void loop() {
  // Accelerate
  for (int delayTime = 1000; delayTime > 200; delayTime -= 10) {
    stepPulse(delayTime);
  }

  // Constant speed (cruise)
  for (int i = 0; i < 100; i++) {
    stepPulse(200);
  }

  // Decelerate
  for (int delayTime = 200; delayTime < 1000; delayTime += 10) {
    stepPulse(delayTime);
  }

  delay(1000);

  // Reverse direction
  digitalWrite(dirX, LOW);
  delay(1000);

  // Repeat in reverse

  // Accelerate
  for (int delayTime = 1000; delayTime > 200; delayTime -= 10) {
    stepPulse(delayTime);
  }

  // Cruise
  for (int i = 0; i < 100; i++) {
    stepPulse(200);
  }

  // Decelerate
  for (int delayTime = 200; delayTime < 1000; delayTime += 10) {
    stepPulse(delayTime);
  }

  delay(2000);
}

// Sends a single step pulse with specified delay
void stepPulse(int delayMicro) {
  digitalWrite(stepX, HIGH);
  delayMicroseconds(delayMicro);
  digitalWrite(stepX, LOW);
  delayMicroseconds(delayMicro);
}
