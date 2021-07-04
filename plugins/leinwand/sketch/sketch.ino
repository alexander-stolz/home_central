int pinUp = 12;
int pinDown = 11;
bool movingUp = false;
bool movingDown = false;
long pos = 0;
long maxPos = 37000;

void setup() {
  pinMode(pinUp, OUTPUT);
  pinMode(pinDown, OUTPUT);
  digitalWrite(pinUp, LOW);
  digitalWrite(pinDown, LOW);
  Serial.begin(9600);
}

void loop() {
  delay(100);
  if (movingUp) {
    pos -= 100;
    pos = max(pos + 1000, 0);
    if (pos == 0) {
      pressButton(pinDown);
      movingUp = false;
    }
  }
  if (movingDown) {
    pos += 100;
    pos = min(pos, maxPos);
    if (pos == maxPos) {
      pressButton(pinUp);
      movingDown = false;
    }
  }
  if (Serial.available() > 0) {
    int inByte = Serial.read();
    // pause
    if (inByte == 1) {
      if (movingUp) {
        pressButton(pinDown);
        movingUp = false;
      }
      if (movingDown) {
        pressButton(pinUp);
        movingUp = false;
      }
    }
    // up
    else if (inByte == 2) {
      pressButton(pinUp);
      if (not movingDown) {
        movingUp = true;
      }
      else {
        pos += 500;
      }
      movingDown = false;
    }
    // down
    else if (inByte == 3) {
      pressButton(pinDown);
      if (not movingUp) {
        movingDown = true;
      }
      else {
        //pos -= 500;
      }
      movingUp = false;
    }
  }
}

void pressButton(int pin) {
  digitalWrite(pin, HIGH);
  delay(500);
  digitalWrite(pin, LOW);
}
