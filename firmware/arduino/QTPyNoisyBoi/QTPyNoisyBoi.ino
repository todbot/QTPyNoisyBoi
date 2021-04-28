/*
 * QTPyNoisyBoi  -- 3 Channel CV modulator for Eurorack modular synths
 *
 * 2021 - Tod Kurt / @todbot - github.com/todbot/qtpynoisyboi
 * 
 * # MOSI -- out A (PWM)  -- Arduino pin 10
 * # MISO -- out B (PWM)  -- Arduino pin 9
 * # A0   -- out C (DAC)  -- Arduino pin 0
 * # RX   -- gate in      -- Arduino pin 7
 * # A1   -- knob in  A   -- Arduino pin 1
 * # A2   -- knob in  B   -- Arduino pin 2
 * # A3   -- knob in  C   -- Arduino pin 3
 * # TX   -- button 1     -- Arduino pin 6
 * # SCK  -- button 2     -- Arduino pin 8
 *
 */

// Hmm, Seeed's pwm() function is awesome but glitchy
// I think because it's flipping the prescaler or changing without
// waiting for TCC ready?
// So for now I'll use this semi-homegrown 'analogWriteHF()' func
//#include "wiring_pwm.h"
#include "analogWriteHF.h"
#include "VoltageOut.h"
#include "calibration.h"

int outAPin = 10; // MOSI on QTPY  (TCC1)
int outBPin = 9;  // MISO on QTPY  (TCC0)
int outCPin = 0;  // A0 on QTPY

int gateInPin = 7; // RX on QTPY

int knobAPin = 1;  // A1 on QTPY
int knobBPin = 2;  // A2 on QTPY
int knobCPin = 3;  // A3 on QTPY

int but1Pin = 6;   // TX on QTPY
int but2Pin = 8;   // TX on QTPY

const uint32_t pwm_freq = 11720; // 

VoltageOut voutA = VoltageOut(cals_a, sizeof(cals_a)/sizeof(voltage_calibration));
VoltageOut voutB = VoltageOut(cals_b, sizeof(cals_b)/sizeof(voltage_calibration));
VoltageOut voutC = VoltageOut(cals_c, sizeof(cals_c)/sizeof(voltage_calibration));

void setup()
{
    delay(1000);
    Serial.begin(115200);
    Serial.println("Hello from QTPyNoisyBoi!");
    pinMode(outAPin, OUTPUT);
    pinMode(outBPin, OUTPUT);
    pinMode(outCPin, OUTPUT);
    
    pinMode(gateInPin, INPUT_PULLDOWN);
    pinMode(knobAPin, INPUT);
    pinMode(knobBPin, INPUT);
    pinMode(knobCPin, INPUT);
    pinMode(but1Pin, INPUT_PULLUP);
    pinMode(but2Pin, INPUT_PULLUP);
}

uint32_t dac_val = 512;  // 10-bit number

void loop() {
    //pwm(outAPin, pwm_freq, dac_val);  // ranges 0-1023
    //pwm(outBPin, pwm_freq, dac_val);  // ranges 0-1023
    analogWriteHF(outAPin, dac_val);  // ranges 0-1023
    analogWriteHF(outBPin, dac_val);  // ranges 0-1023
    analogWrite(outCPin, dac_val);    // actually analog, 0-1023
    //dac_val++;
    if( dac_val >= 1024 ) dac_val = 0;
    delay(5);
}

