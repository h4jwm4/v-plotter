#define stepPin 2
#define dirPin 5
#define enPin 8

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(enPin, OUTPUT);
  
  digitalWrite(enPin, LOW);   // Enable driver
  digitalWrite(dirPin, HIGH); // Set direction
}

void loop() {
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(1000);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(1000);
}
