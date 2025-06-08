#include <AccelStepper.h>
#include <Servo.h>

#define X_STEP 2
#define X_DIR 5
#define Y_STEP 3
#define Y_DIR 6
#define EN_PIN 8

Servo myServo;
AccelStepper stepperX(1, X_STEP, X_DIR);
AccelStepper stepperY(1, Y_STEP, Y_DIR);

long targetX = 0, targetY = 0;
int servoAngle = -1;
bool moving = false; // New flag to track motion status

void setup() {
  myServo.attach(9);  // Servo on pin 9

  Serial.begin(115200);
  pinMode(EN_PIN, OUTPUT);
  digitalWrite(EN_PIN, LOW);

  stepperX.setMaxSpeed(5000);
  stepperX.setAcceleration(500);
  stepperY.setMaxSpeed(5000);
  stepperY.setAcceleration(500);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    data.trim(); // Remove newline and whitespace

    // Inside loop() after checking Serial.available()
    if (data.startsWith("SPEED:")) {
      float scale = data.substring(6).toFloat();
      scale = constrain(scale, 0.2, 5.0); // Limit between 0.2x and 5x
      stepperX.setMaxSpeed(5000 * scale);
      stepperX.setAcceleration(500 * scale);
      stepperY.setMaxSpeed(5000 * scale);
      stepperY.setAcceleration(500 * scale);
      Serial.print("UPDATED SPEED SCALE: ");
      Serial.println(scale, 2);
    }
    // --- Handle "S:angle" format ---
    if (data.startsWith("S:")) {
      servoAngle = data.substring(2).toInt();
      if (servoAngle >= 0 && servoAngle <= 180) {
        myServo.write(servoAngle);
      }
    }
    // --- Handle "X,Y,S" or "X,Y" format ---
    else {
      int firstComma = data.indexOf(',');
      int secondComma = data.indexOf(',', firstComma + 1);

      if (firstComma > 0 && secondComma > firstComma) {
        targetX = data.substring(0, firstComma).toInt();
        targetY = data.substring(firstComma + 1, secondComma).toInt();
        servoAngle = data.substring(secondComma + 1).toInt();

        if (servoAngle >= 0 && servoAngle <= 180) {
          myServo.write(servoAngle);
        }

        stepperX.moveTo(targetX);
        stepperY.moveTo(targetY);
        moving = true;
      }
      else if (firstComma > 0) {
        targetX = data.substring(0, firstComma).toInt();
        targetY = data.substring(firstComma + 1).toInt();

        stepperX.moveTo(targetX);
        stepperY.moveTo(targetY);
        moving = true;
      }
    }
  }

  stepperX.run();
  stepperY.run();

  // Check if movement just finished
  if (moving && stepperX.distanceToGo() == 0 && stepperY.distanceToGo() == 0) {
    Serial.print("DONE: ");
    Serial.print(targetX);
    Serial.print(", ");
    Serial.println(targetY);
    moving = false;
  }
}
