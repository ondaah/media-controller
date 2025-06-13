#include <Encoder.h>
#include <Button.h>

#define CLK 2
#define DT 3
#define SW 4
#define LED 13

Encoder encoder(CLK, DT);
Button swButton(SW);

long oldPosition = 0;

void setup()
{
    pinMode(LED, OUTPUT);
    swButton.begin();
    Serial.begin(9600);
}

void loop()
{
    long newPosition = encoder.read() / 4;
    if (newPosition != oldPosition)
    {
        Serial.print("e");
        Serial.println(newPosition);
        oldPosition = newPosition;
    }

    digitalWrite(LED, swButton.read() == Button::PRESSED ? HIGH : LOW);

    if (swButton.toggled())
        Serial.println(swButton.read() == Button::PRESSED ? "b1" : "b0");
}
