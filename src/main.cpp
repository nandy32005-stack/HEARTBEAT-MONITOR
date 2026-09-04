#include <Arduino.h>
#include <Wire.h>
#include <MAX30105.h>
#include <heartRate.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// ==========================================
// HEARTBEAT MONITOR WITH ALERT SYSTEM
// ESP32 + MAX30102 + OLED
// ==========================================

// ---------- OLED Configuration ----------

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

Adafruit_SSD1306 display(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    &Wire,
    OLED_RESET
);

// ---------- MAX30102 ----------

MAX30105 particleSensor;

// ---------- GPIO Configuration ----------

const int GREEN_LED = 25;
const int RED_LED = 26;
const int BUZZER = 27;

// ---------- Educational Thresholds ----------

const int LOW_THRESHOLD = 60;
const int HIGH_THRESHOLD = 100;

// ---------- BPM Variables ----------

const byte RATE_SIZE = 8;

byte rates[RATE_SIZE];
byte rateSpot = 0;

long lastBeat = 0;

float beatsPerMinute = 0;
int beatAvg = 0;

// ---------- Display Timing ----------

unsigned long lastDisplayUpdate = 0;

const unsigned long DISPLAY_INTERVAL = 500;

// ==========================================
// SETUP
// ==========================================

void setup()
{
    Serial.begin(115200);

    delay(1000);

    Serial.println();
    Serial.println("======================================");
    Serial.println(" HEARTBEAT MONITOR WITH ALERT SYSTEM");
    Serial.println("======================================");
    Serial.println();

    // ---------- GPIO ----------

    pinMode(GREEN_LED, OUTPUT);
    pinMode(RED_LED, OUTPUT);
    pinMode(BUZZER, OUTPUT);

    digitalWrite(GREEN_LED, LOW);
    digitalWrite(RED_LED, LOW);
    digitalWrite(BUZZER, LOW);

    // ---------- I2C ----------

    Wire.begin(21, 22);

    // ---------- OLED ----------

    if (!display.begin(
            SSD1306_SWITCHCAPVCC,
            0x3C))
    {
        Serial.println("ERROR: OLED not detected!");

        while (true)
        {
            delay(1000);
        }
    }

    display.clearDisplay();

    display.setTextColor(SSD1306_WHITE);

    display.setTextSize(1);
    display.setCursor(20, 10);
    display.println("HEARTBEAT");

    display.setCursor(25, 25);
    display.println("MONITOR");

    display.setCursor(20, 45);
    display.println("Initializing...");

    display.display();

    delay(1500);

    // ---------- MAX30102 ----------

    if (!particleSensor.begin(
            Wire,
            I2C_SPEED_FAST))
    {
        Serial.println("ERROR: MAX30102 not detected!");

        display.clearDisplay();

        display.setCursor(10, 20);
        display.setTextSize(1);
        display.println("MAX30102 ERROR");

        display.setCursor(10, 40);
        display.println("Check wiring");

        display.display();

        while (true)
        {
            delay(1000);
        }
    }

    Serial.println("MAX30102 detected.");

    // ---------- Sensor Configuration ----------

    particleSensor.setup();

    particleSensor.setPulseAmplitudeRed(0x0A);
    particleSensor.setPulseAmplitudeIR(0x0A);

    particleSensor.setPulseAmplitudeGreen(0);

    Serial.println("Sensor initialized.");
    Serial.println();

    Serial.println("Place your finger gently");
    Serial.println("on the MAX30102 sensor.");
    Serial.println();
}

// ==========================================
// UPDATE ALERT SYSTEM
// ==========================================

void updateAlert(int bpm)
{
    // No valid BPM
    if (bpm <= 0)
    {
        digitalWrite(GREEN_LED, LOW);
        digitalWrite(RED_LED, LOW);
        digitalWrite(BUZZER, LOW);

        return;
    }

    // ---------- LOW ----------

    if (bpm < LOW_THRESHOLD)
    {
        digitalWrite(GREEN_LED, LOW);
        digitalWrite(RED_LED, HIGH);

        tone(BUZZER, 1000);
    }

    // ---------- HIGH ----------

    else if (bpm > HIGH_THRESHOLD)
    {
        digitalWrite(GREEN_LED, LOW);
        digitalWrite(RED_LED, HIGH);

        tone(BUZZER, 1500);
    }

    // ---------- NORMAL ----------

    else
    {
        digitalWrite(GREEN_LED, HIGH);
        digitalWrite(RED_LED, LOW);

        noTone(BUZZER);
    }
}

// ==========================================
// UPDATE OLED DISPLAY
// ==========================================

void updateDisplay(int bpm)
{
    display.clearDisplay();

    display.setTextColor(SSD1306_WHITE);

    // ---------- Title ----------

    display.setTextSize(1);

    display.setCursor(20, 0);
    display.println("HEART MONITOR");

    // ---------- BPM ----------

    display.setTextSize(2);

    display.setCursor(5, 18);

    display.print("BPM:");

    if (bpm > 0)
    {
        display.print(bpm);
    }
    else
    {
        display.print("--");
    }

    // ---------- Status ----------

    display.setTextSize(1);

    display.setCursor(5, 45);

    if (bpm <= 0)
    {
        display.println("STATUS: WAITING");
    }

    else if (bpm < LOW_THRESHOLD)
    {
        display.println("STATUS: LOW");
    }

    else if (bpm > HIGH_THRESHOLD)
    {
        display.println("STATUS: HIGH");
    }

    else
    {
        display.println("STATUS: NORMAL");
    }

    display.display();
}

// ==========================================
// LOOP
// ==========================================

void loop()
{
    long irValue = particleSensor.getIR();

    // ======================================
    // CHECK SENSOR CONTACT
    // ======================================

    if (irValue < 50000)
    {
        beatsPerMinute = 0;
        beatAvg = 0;

        digitalWrite(GREEN_LED, LOW);
        digitalWrite(RED_LED, LOW);

        noTone(BUZZER);

        if (millis() - lastDisplayUpdate >=
            DISPLAY_INTERVAL)
        {
            updateDisplay(0);

            lastDisplayUpdate = millis();
        }

        Serial.println("Waiting for finger...");

        delay(100);

        return;
    }

    // ======================================
    // HEARTBEAT DETECTION
    // ======================================

    if (checkForBeat(irValue))
    {
        long delta =
            millis() - lastBeat;

        lastBeat = millis();

        beatsPerMinute =
            60.0 / (delta / 1000.0);

        // Accept reasonable BPM range

        if (beatsPerMinute > 20 &&
            beatsPerMinute < 220)
        {
            rates[rateSpot++] =
                (byte)beatsPerMinute;

            rateSpot %= RATE_SIZE;

            beatAvg = 0;

            for (byte x = 0;
                 x < RATE_SIZE;
                 x++)
            {
                beatAvg += rates[x];
            }

            beatAvg /= RATE_SIZE;
        }

        Serial.println("--------------------------------");

        Serial.print("Instant BPM: ");

        Serial.println(beatsPerMinute);

        Serial.print("Average BPM: ");

        Serial.println(beatAvg);

        Serial.println("--------------------------------");
    }

    // ======================================
    // ALERT SYSTEM
    // ======================================

    if (beatAvg > 0)
    {
        updateAlert(beatAvg);
    }

    // ======================================
    // OLED UPDATE
    // ======================================

    if (millis() - lastDisplayUpdate >=
        DISPLAY_INTERVAL)
    {
        updateDisplay(beatAvg);

        lastDisplayUpdate = millis();
    }

    delay(20);
}