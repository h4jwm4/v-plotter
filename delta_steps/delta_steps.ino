#include <AccelStepper.h>

#define X_STEP 2
#define X_DIR 5
#define Y_STEP 3
#define Y_DIR 6
#define EN_PIN 8

AccelStepper stepperX(1, X_STEP, X_DIR);
AccelStepper stepperY(1, Y_STEP, Y_DIR);

void setup() {
  Serial.begin(115200);
  pinMode(EN_PIN, OUTPUT);
  digitalWrite(EN_PIN, LOW);

  stepperX.setMaxSpeed(1000);
  stepperX.setAcceleration(500);
  stepperY.setMaxSpeed(1000);
  stepperY.setAcceleration(500);
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    int commaIndex = input.indexOf(',');
    if (commaIndex > 0) {
      int dx = input.substring(0, commaIndex).toInt();
      int dy = input.substring(commaIndex + 1).toInt();
      
      stepperX.move(stepperX.distanceToGo() + dx);
      stepperY.move(stepperY.distanceToGo() + dy);
    }
  }

  stepperX.run();
  stepperY.run();
}
