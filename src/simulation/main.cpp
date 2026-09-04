#include <Arduino.h>

#define GREEN_LED 25
#define RED_LED 26
#define BUZZER 27

void setup()
{
    pinMode(GREEN_LED, OUTPUT);
    pinMode(RED_LED, OUTPUT);
    pinMode(BUZZER, OUTPUT);

    digitalWrite(GREEN_LED, HIGH);
    digitalWrite(RED_LED, LOW);
    digitalWrite(BUZZER, LOW);
}

void loop()
{
    digitalWrite(GREEN_LED, HIGH);
    delay(1000);

    digitalWrite(GREEN_LED, LOW);
    digitalWrite(RED_LED, HIGH);
    delay(1000);

    digitalWrite(RED_LED, LOW);
}