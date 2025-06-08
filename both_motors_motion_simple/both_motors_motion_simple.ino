const int stepX = 2;
const int dirX  = 5;

const int stepY = 3;
const int dirY  = 6;

const int enPin = 8;

void setup() {
  pinMode(stepX, OUTPUT);
  pinMode(dirX, OUTPUT);

  pinMode(stepY, OUTPUT);
  pinMode(dirY, OUTPUT);

  pinMode(enPin, OUTPUT);

  digitalWrite(enPin, LOW);    // Enable motor driver
  digitalWrite(dirX, HIGH);    // X direction
  digitalWrite(dirY, HIGH);    // Y direction
}

void loop() {
  // Accelerate forward
  for (int delayTime = 1000; delayTime > 200; delayTime -= 10) {
    stepBoth(delayTime);
  }

  // Cruise
  for (int i = 0; i < 100; i++) {
    stepBoth(200);
  }

  // Decelerate
  for (int delayTime = 200; delayTime < 1000; delayTime += 10) {
    stepBoth(delayTime);
  }

  delay(1000);

  // Reverse direction
  digitalWrite(dirX, LOW);
  digitalWrite(dirY, LOW);
  delay(1000);

  // Accelerate backward
  for (int delayTime = 1000; delayTime > 200; delayTime -= 10) {
    stepBoth(delayTime);
  }

  // Cruise
  for (int i = 0; i < 100; i++) {
    stepBoth(200);
  }

  // Decelerate
  for (int delayTime = 200; delayTime < 1000; delayTime += 10) {
    stepBoth(delayTime);
  }

  delay(2000);
}

// Steps both motors with same delay
void stepBoth(int delayMicro) {
  digitalWrite(stepX, HIGH);
  digitalWrite(stepY, HIGH);
  delayMicroseconds(delayMicro);

  digitalWrite(stepX, LOW);
  digitalWrite(stepY, LOW);
  delayMicroseconds(delayMicro);
}
