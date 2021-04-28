# qtpynoisyboi_test.py --
#
# MOSI -- out A (PWM)
# MISO -- out B (PWM)
# A0   -- out C (DAC)
# RX   -- gate in 
# A1   -- knob in  A
# A2   -- knob in  B
# A3   -- knob in  C
# TX   -- button 1
# SCK  -- button 2

import time
import board
import neopixel
import pwmio
import analogio
import digitalio
from adafruit_debouncer import Debouncer
import random

import voltageio
import waveforms

do_calibration_setup = False

# determined experimentally
calibration = {
    "a": {
        -3.34: 65535,
        0.0: 43675,
        6.69:0,
    },
    "b": {
        -3.40: 65535,
        0.0: 43535,
        6.73: 0,
    },
    "c": {
        }
}

but1pin = digitalio.DigitalInOut(board.TX)
but1pin.pull = digitalio.Pull.UP
but1 = Debouncer(but1pin)
but2pin = digitalio.DigitalInOut(board.SCK)
but2pin.pull = digitalio.Pull.UP
but2 = Debouncer(but2pin)

knob_a = analogio.AnalogIn(board.A1)
knob_b = analogio.AnalogIn(board.A2)
knob_c = analogio.AnalogIn(board.A3)
        
out_a = pwmio.PWMOut(board.MOSI, frequency=25000, duty_cycle=0)
out_b = pwmio.PWMOut(board.MISO, frequency=25000, duty_cycle=0)
vout_a = voltageio.VoltageOut(calibration['a'])
vout_b = voltageio.VoltageOut(calibration['b'])

def set_out_a_duty(dc):
    out_a.duty_cycle = dc
def set_out_b_duty(dc):
    out_b.duty_cycle = dc
def set_out_a_volts(voltage):
    out_a.duty_cycle = vout_a.dac_for_voltage(voltage)
def set_out_b_volts(voltage):
    out_b.duty_cycle = vout_b.dac_for_voltage(voltage)

# calibration
if do_calibration_setup:
    print("Calibrate PWM DAC.")
    while True:
        print("Enter 'set_out_a_duty(65535)' and watch output on multimeter:")
        value = input().strip()
        eval(value)
        print('value:"',value,'"')
        time.sleep(0.1)
    


sin_wave = waveforms.Waveform('sin',steps=256)
rnd_wave = waveforms.Waveform('rnd',steps=16)

wave = sin_wave.wave
volt_offset = 0.0
volt_amplitude = 2.0
period = 1.0
dt = period / len(wave)

i=0
val = 0
wave_index=0
last_time = time.monotonic()

while True:
    but1.update()
    but2.update()
    period = utils.map_range(knob_a.value, 0,1023, 0.01, 10)
                             
    now = time.monotonic()
    if now > dt + last_time:
        last_time = now
        wave_index = (wave_index + 1) % len(wave)
        print("updated", wave_index)
    # get the wave value, scale it by amplitude and offsetit
    val = offset + amplitude * wave[wave_index]
    # convert to volts and send it out
    set_out_a_volts(val)
    

#note_volts = [0, 0.0833, 0.1666, 0.25, 0.333, 0.4166, 0.5, 0.5833, 0.6666, 0.75, 0.83333, 0.9166, 1]
#note_volts = [0,          0.1666, 0.25, 0.333,         0.5,         0.6666, 0.75, 0.83333, 1]
#note_vals = [1, 1.5, 2, 2.5]
#note_vals = [1, 2, 2.5, 3, 3.5, 4]

    #val = sin_wave.wave[i] # * amplitude
    #val = random.random() * 1
    #val = note_volts[random.randint(0,len(note_volts)-1)]
#    val = note_vals[j]
#    j = (j+1) % len(note_vals)

#j=0
    
# cvsa_index = 0
# cvsb_index = 2
# cvai=0
# cvbi=0
# cva_last = time.monotonic()
# cvb_last = time.monotonic()

# cvsa = cvs_list[cvsa_index]
# cvsb = cvs_list[cvsb_index]

# while True:
#     butt1.update()
#     now = time.monotonic()
#     if now > cva_last + rateA:
#         cva_last = now
#         cvai = (cvai + 1) % len(cvsa)
#         duty_cycle = int( cvsa[cvai] * 65535/100)
#         outA.duty_cycle = 65535 - duty_cycle
#     if now > cvb_last + rateB:
#         cvb_last = now
#         cvbi = (cvbi + 1) % len(cvsb)
#         duty_cycle = int( cvsb[cvbi] * 65535/100)
#         outB.duty_cycle = 65535 - duty_cycle
# #    rateA = 0.01 + (potAknob.value / 65535 / 2)
#     rateA = (potAknob.value / 65535 ) #/ len(cvsa))
#     rateB = 0.01 + (potBknob.value / 65535 / 2)
#     if butt1.fell: # pressed
#         print("push!")
#         cvsa_index = (cvsa_index + 1 ) % len(cvs_list)
#         cvsa = cvs_list[cvsa_index]
#         cvsai=0
        



# cv = 50
# while True:
#     duty_cycle = int(cv * 65535/100)
#     out1.duty_cycle = 65535 - duty_cycle
    
# cv_index = 0
# while True:
#     if but1.value == False: # pressed
#         print("push!")
#         cv_index = (cv_index + 1 ) % len(cvs_list)
#     cvs = cvs_list[ cv_index ]
    
#     for cv in cvs:
#         duty_cycle = int(cv * 65535/100)
#         out1.duty_cycle = 65535 - duty_cycle
#         out2.duty_cycle = duty_cycle
#         print("duty:",duty_cycle, out1.duty_cycle)
#         rate = 0.01 + (potAknob.value / 65535 / 2)
#         time.sleep(rate)
       

# # test knob to voltage output
# while True:
#     pos = potknob.value // 256
#     print("pos:",pos)
#     out1.duty_cycle = 65535 - potknob.value # inverting amplifier
#     time.sleep(0.01)


# # test simple triangle wave output
# i=0
# while True:
#     if i < 50:
#         out1.duty_cycle = int(i * 2 * 65535 / 100)  # Up
#     else:
#         out1.duty_cycle = 65535 - int((i - 50) * 2 * 65535 / 100)  # Down
#     i = (i + 1) % 100
#     time.sleep(0.001)
    
# while True:
#     for i in range(100):
#         if i < 50:
#             led.duty_cycle = int(i * 2 * 65535 / 100)  # Up
#         else:
#             out1.duty_cycle = 65535 - int((i - 50) * 2 * 65535 / 100)  # Down
# #        time.sleep(0.0001)

        
