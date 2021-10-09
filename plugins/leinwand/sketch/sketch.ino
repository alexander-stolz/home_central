int pinUp = 12;
int pinDown = 11;
int pinStop = 10;
bool movingUp = false;
bool movingDown = false;
long pos = 0;
long maxPos = 37400;

void setup()
{
  pinMode(pinUp, OUTPUT);
  pinMode(pinDown, OUTPUT);
  pinMode(pinStop, OUTPUT);
  digitalWrite(pinUp, LOW);
  digitalWrite(pinDown, LOW);
  digitalWrite(pinStop, LOW);
  Serial.begin(9600);
}

void loop()
{
  delay(100);
  if (movingUp)
  {
    pos -= 100;
    pos = max(pos, 0);
    if (pos == 0)
    {
      delay(300);
      pressButton(pinStop);
      movingUp = false;
    }
  }
  if (movingDown)
  {
    pos += 100;
    pos = min(pos, maxPos);
    if (pos == maxPos)
    {
      pressButton(pinStop);
      movingDown = false;
    }
  }
  if (Serial.available() > 0)
  {
    int inByte = Serial.read();
    // pause
    if (inByte == 1)
    {
      Serial.println(pos);
      Serial.println(movingUp);
      Serial.println(movingDown);
    }
    // up
    else if (inByte == 2)
    {
      pressButton(pinUp);
      if (not movingDown)
      {
        movingUp = true;
        if (pos == 0)
        {
          pos = maxPos;
        }
        else
        {
          pos -= 500;
        }
      }
      movingDown = false;
    }
    // down
    else if (inByte == 3)
    {
      pressButton(pinDown);
      if (not movingUp)
      {
        movingDown = true;
        pos += 500;
      }
      movingUp = false;
    }
  }
}

void pressButton(int pin)
{
  digitalWrite(pin, HIGH);
  delay(500);
  digitalWrite(pin, LOW);
}
