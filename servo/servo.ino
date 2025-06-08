#include <Servo.h>

Servo myServo;

void setup() {
  myServo.attach(9);  // Attach servo signal wire to D9
  Serial.begin(9600);
  Serial.println("Servo test started...");
}

void loop() {
  // Sweep from 0 to 180
  for (int pos = 0; pos <= 180; pos += 1) {
    myServo.write(pos);
    delay(10);
  }

  delay(500);  // Pause at 180

  // Sweep from 180 to 0
  for (int pos = 180; pos >= 0; pos -= 1) {
    myServo.write(pos);
    delay(10);
  }

  delay(500);  // Pause at 0
}