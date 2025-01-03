String incomingByte ;    

void setup() {

  Serial.begin(9600);

  pinMode(LED_BUILTIN, OUTPUT);

}
void loop() {

  if (Serial.available() > 0) {

  incomingByte = Serial.readStringUntil('\n');

    if (incomingByte == "lightsetup1") {

      digitalWrite(LED_BUILTIN, HIGH);

      Serial.write("Led on");

    }

    else if (incomingByte == "lightsetup2") {

      digitalWrite(LED_BUILTIN, LOW);

      Serial.write("Led off");

    }

        else if (incomingByte == "lightsetup3") {

      digitalWrite(LED_BUILTIN, HIGH);

      Serial.write("Led on");

    }


    else{

     Serial.write("invald input");

    }

  }

}

