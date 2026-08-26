#include <Servo.h>

Servo sortServo;
const int servoPin = 9; 
char receivedChar;

int czas_podrozy_do_serwa = 1500; 
int czas_na_spadniecie = 2000;   

void setup() {
  Serial.begin(9600);
  sortServo.attach(servoPin);
  sortServo.write(90);
}

void loop() {
  if (Serial.available() > 0) {
    receivedChar = Serial.read();
    //Sruba
    if (receivedChar == '1') {
      delay(czas_podrozy_do_serwa);
      sortServo.write(55);
      delay(czas_na_spadniecie);
      sortServo.write(90); 
    } 
    //Wkret
    else if (receivedChar == '2') {
      delay(czas_podrozy_do_serwa);
      sortServo.write(130);
      delay(czas_na_spadniecie);
      sortServo.write(90); 
      
    }
  }
}