#include <Servo.h>

// sensor distance ~ 20 cm

// angle constants
#define MAX_POS_PAN 10
#define MAX_NEG_PAN -10
#define MAX_POS_TILT 20
#define MAX_NEG_TILT -12

/*30 cm = 1.88
 *35 cm = 1.61
 *40 cm = 1.42
 *45 cm = 1.30
 *50 cm = 1.13
 *55 cm = 1.00
 *60 cm = 0.94
 *65 cm = 0.86
 *70 cm = 0.79
 *75 cm = 0.73
 *
 *Distance = x/1
 *Voltage = 1023x/5
 *
 *equation
 *11786*x + -5.39 
 *R^2 = 0.998
 */

Servo panServo;
Servo tiltServo;

// set IR sensor and servo pins
const int IRPin = A0;
const int panServoPin = 9;
const int tiltServoPin = 10;

int IRVal;
bool running = true;

// SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP
void setup() {
  // begin serial monitor
  int baudRate = 9600;
  Serial.begin(baudRate);
  
  // attach servos to pins
  panServo.attach(panServoPin);
  tiltServo.attach(tiltServoPin);

  // center servos and pause
  panServo.write(90);
  tiltServo.write(90);
  
  // wait 1 second before the scanning starts
  delay(1000);
}

// LOOP LOOP LOOP LOOP LOOP LOOP LOOP
void loop() {
  // put your main code here, to run repeatedly:
  if (running) {
    for (int i = 90 + MAX_POS_PAN; i >= 90 + MAX_NEG_PAN; i--) {
      panServo.write(i);
      for (int j = 90 + MAX_POS_TILT; j >= 90 + MAX_NEG_TILT; j--) {
        tiltServo.write(j);
        IRVal = analogRead(IRPin);
        Serial.print(IRVal);   Serial.print(",");
        Serial.print(i);       Serial.print(",");
        Serial.println(j);
        delay(300);
      }
    }
    running = false;

    // short delay after scanning and recenter mount
    delay(500);
    tiltServo.write(90);
    panServo.write(90);
  }
}
