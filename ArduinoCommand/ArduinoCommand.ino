String incomingByte;
const int buttonPin1 = 5;
const int buttonPin2 = 4;
const int buttonPin3 = 3;
const int buttonPin4 = 2;

const int lightPin1 = 6;
const int lightPin2 = 7;
const int lightPin3 = 8;
const int lightPin4 = 9;

int lightStates[4] = {LOW, LOW, LOW, LOW}; // Initial state of the lights
int buttonStates[4] = {LOW, LOW, LOW, LOW}; // Initial state of the buttons
int lastButtonStates[4] = {LOW, LOW, LOW, LOW}; // To remember the last state of the buttons

void setup() {
  Serial.begin(9600);
  pinMode(lightPin1, OUTPUT);
  pinMode(lightPin2, OUTPUT);
  pinMode(lightPin3, OUTPUT);
  pinMode(lightPin4, OUTPUT);
  pinMode(buttonPin1, INPUT);
  pinMode(buttonPin2, INPUT);
  pinMode(buttonPin3, INPUT);
  pinMode(buttonPin4, INPUT);
}

void loop() {
  // Read the state of each button
  buttonStates[0] = digitalRead(buttonPin1);
  buttonStates[1] = digitalRead(buttonPin2);
  buttonStates[2] = digitalRead(buttonPin3);
  buttonStates[3] = digitalRead(buttonPin4);

  // Toggle the lights if the button state has changed to HIGH
  for (int i = 0; i < 4; i++) {
    if (buttonStates[i] == HIGH && lastButtonStates[i] == LOW) {
      lightStates[i] = !lightStates[i];
      digitalWrite(lightPin1 + i, lightStates[i]);
    }
    lastButtonStates[i] = buttonStates[i];
  }

  if (Serial.available() > 0) {
    incomingByte = Serial.readStringUntil('\n');
    if (incomingByte == "lightsetup1") {
      lightStates[0] = HIGH;
      lightStates[1] = HIGH;
      lightStates[2] = HIGH;
      lightStates[3] = HIGH;
      for (int i = 0; i < 4; i++) {
        digitalWrite(lightPin1 + i, lightStates[i]);
      }
      Serial.write("Led on");
    } else if (incomingByte == "lightsetup2") {
      lightStates[0] = HIGH;
      lightStates[1] = LOW;
      lightStates[2] = HIGH;
      lightStates[3] = LOW;
      for (int i = 0; i < 4; i++) {
        digitalWrite(lightPin1 + i, lightStates[i]);
      }
      Serial.write("Led off");
    } else if (incomingByte == "lightsetup3") {
      lightStates[0] = LOW;
      lightStates[1] = HIGH;
      lightStates[2] = HIGH;
      lightStates[3] = LOW;
      for (int i = 0; i < 4; i++) {
        digitalWrite(lightPin1 + i, lightStates[i]);
      }
      Serial.write("Led on");
    } else {
      Serial.write("invalid input");
    }
  }
}
