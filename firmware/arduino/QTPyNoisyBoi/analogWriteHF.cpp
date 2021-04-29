/**
 *
 */

// Heavy borrowing from:
// https://github.com/SaltyHash/BWO/blob/master/src/arduino/motor_control/wiring_analog_extras.cpp
// https://forum.seeedstudio.com/t/change-pwm-frequency/252579/3

#include "analogWriteHF.h"

#include <Arduino.h>
//#include <WMath.h>  // map()  why can't I include this?
#include <wiring_private.h>

#ifdef __cplusplus
//extern "C" {
#endif

// Wait for synchronization of registers between the clock domains
static __inline__ void syncTC_8(Tc* TCx) __attribute__((always_inline, unused));
static void syncTC_8(Tc* TCx) {
  while (TCx->COUNT8.STATUS.bit.SYNCBUSY);
}

// Wait for synchronization of registers between the clock domains
static __inline__ void syncTCC(Tcc* TCCx) __attribute__((always_inline, unused));
static void syncTCC(Tcc* TCCx) {
  while (TCCx->SYNCBUSY.reg & TCC_SYNCBUSY_MASK);
}

// copied from WMath.h because apparently I cannot figure out the preprocessor
long map(long x, long in_min, long in_max, long out_min, long out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

/* Right now, PWM output only works on the pins with
   hardware support.  These are defined in the appropriate
   variant.c file.  For the rest of the pins, we just return.

   This was copied from wiring_analog.c
   and modified to
   * set the PWM frequency to 20kHz.

   Args:
     value - Range is [0, 1023], unlike analogWrite(), which goes 0-255
*/
//void analogWriteHF(const uint32_t pin, uint32_t value, const uint32_t pwm_freq ) // an idea
void analogWriteHF(const uint32_t pin, uint32_t value)
{
  /*
    From the SAMD21 datasheet, page 642:

                  f{GCLK_TC}
      f{PWM_SS} = ----------
                  N(TOP + 1)

    Where:
    - f{PWM_SS} is the PWM frequency.
    - f{GCLK_TC} is the clock frequency (48MHz, in this case).
    - N is the prescaler value (16, in this case).
    - TOP is the max counter value (149, in this case).

    This gives f{PWM_SS} = 48MHz / (16(149 + 1)) = 20kHz.
  */
    /*
      or: resolution == TOP+1 = f{GCLK_TC} / N / f{PWM}
                              =  48e6 / 16 / 20e3 = 150
    */
    static const uint16_t TOP = 1023;  // 11.6hKHz @ DIV4
    //const static int TOP = 1024;  // 5.8 hKHz @ DIV8
    //static const int TOP = 746;  // 8 hKHz @ DIV8     // NOTE THIS IS 8-BIT with COUNT8 below
    //const static int TOP = 373;  // 8 hKHz @ DIV16
    //static const int TOP = 149;  // 20 kHz @ DIV16

  PinDescription pinDesc = g_APinDescription[pin];
  uint32_t attr = pinDesc.ulPinAttribute;

  if (!(attr & PIN_ATTR_PWM))
  {
    return;
  }

  //value = map(constrain(value, 0, 1023), 0, 1023, 0, TOP);
  value = map(constrain(value, 0, 1023), 0, 1023, 0, TOP);

  uint32_t tcNum = GetTCNumber(pinDesc.ulPWMChannel);
  uint8_t tcChannel = GetTCChannelNumber(pinDesc.ulPWMChannel);
  static bool tcEnabled[TCC_INST_NUM + TC_INST_NUM];

  if (attr & PIN_ATTR_TIMER)
  {
    pinPeripheral(pin, PIO_TIMER);
  }
  else if ((attr & PIN_ATTR_TIMER_ALT) == PIN_ATTR_TIMER_ALT)
  {
    //this is on an alt timer
    pinPeripheral(pin, PIO_TIMER_ALT);
  }
  else
  {
    return;
  }

  if (!tcEnabled[tcNum])
  {
    tcEnabled[tcNum] = true;
    uint16_t GCLK_CLKCTRL_IDs[] = {
      GCLK_CLKCTRL_ID(GCM_TCC0_TCC1), // TCC0
      GCLK_CLKCTRL_ID(GCM_TCC0_TCC1), // TCC1
      GCLK_CLKCTRL_ID(GCM_TCC2_TC3),  // TCC2
      GCLK_CLKCTRL_ID(GCM_TCC2_TC3),  // TC3
      GCLK_CLKCTRL_ID(GCM_TC4_TC5),   // TC4
      GCLK_CLKCTRL_ID(GCM_TC4_TC5),   // TC5
      GCLK_CLKCTRL_ID(GCM_TC6_TC7),   // TC6
      GCLK_CLKCTRL_ID(GCM_TC6_TC7),   // TC7
    };
    GCLK->CLKCTRL.reg = (uint16_t)(GCLK_CLKCTRL_CLKEN | GCLK_CLKCTRL_GEN_GCLK0 | GCLK_CLKCTRL_IDs[tcNum]);
    while (GCLK->STATUS.bit.SYNCBUSY == 1);
    
    // Set PORT
    if (tcNum >= TCC_INST_NUM)
    {
        //Serial.println("HERE IN 8-BIT TCx LAND");
      // -- Configure TC
      Tc *TCx = (Tc*) GetTC(pinDesc.ulPWMChannel);
      // Disable TCx
      TCx->COUNT8.CTRLA.bit.ENABLE = 0;
      syncTC_8(TCx);
      // Set Timer counter Mode to 8 bits, normal PWM, with prescale set to 1/16
      TCx->COUNT8.CTRLA.reg |= TC_CTRLA_MODE_COUNT8 | TC_CTRLA_WAVEGEN_NPWM | TC_CTRLA_PRESCALER(TC_CTRLA_PRESCALER_DIV4_Val);
      syncTC_8(TCx);
      // Set PER to a maximum counter value of TOP
      TCx->COUNT8.PER.reg = TOP;
      syncTC_8(TCx);
      // Set the initial value
      TCx->COUNT8.CC[tcChannel].reg = (uint32_t) value;
      syncTC_8(TCx);
      // Enable TCx
      TCx->COUNT8.CTRLA.bit.ENABLE = 1;
      syncTC_8(TCx);
    }
    else
    {
        //Serial.println("HERE IN 16-BIT TCCx LAND");
      // -- Configure TCC
      Tcc *TCCx = (Tcc*) GetTC(pinDesc.ulPWMChannel);
      // Disable TCCx
      TCCx->CTRLA.bit.ENABLE = 0;
      syncTCC(TCCx);

      TCCx->CTRLA.reg |= TCC_CTRLA_PRESCALER(TCC_CTRLA_PRESCALER_DIV4_Val);
      syncTCC(TCCx);

      // Set TCCx as normal PWM
      TCCx->WAVE.reg |= TCC_WAVE_WAVEGEN_NPWM;
      syncTCC(TCCx);
      // Set the initial value
      TCCx->CC[tcChannel].reg = (uint32_t) value;
      syncTCC(TCCx);
      // Set PER to a maximum counter value of TOP
      TCCx->PER.reg = TOP;
      syncTCC(TCCx);
      // Enable TCCx
      TCCx->CTRLA.bit.ENABLE = 1;
      syncTCC(TCCx);
    }
  }
  else
  {
    if (tcNum >= TCC_INST_NUM)
    {
        //Serial.println("HERE IN OTHER 8-BIT TCx LAND"); 
      Tc *TCx = (Tc*) GetTC(pinDesc.ulPWMChannel);
      TCx->COUNT8.CC[tcChannel].reg = (uint32_t) value; 
      syncTC_8(TCx);
    }
    else
    {
        //Serial.println("HERE IN OTHER 16-BIT TCCx LAND"); 
      Tcc *TCCx = (Tcc*) GetTC(pinDesc.ulPWMChannel);
      TCCx->CTRLBSET.bit.LUPD = 1;
      syncTCC(TCCx);
      TCCx->CCB[tcChannel].reg = (uint32_t) value;
      syncTCC(TCCx);
      TCCx->CTRLBCLR.bit.LUPD = 1;
      syncTCC(TCCx);
    }
  }
}


#ifdef __cplusplus
//}
#endif
