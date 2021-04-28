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
import utils

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
volt_amplitude = 4.0
period = 1.0

i=0
val = 0
wave_index=0
last_time = time.monotonic()
period_time = time.monotonic()

wave_inc = 8

# let's declare our "dt" to always be 0.01 secs, THEN
# what wave part do I pick for given period
# 
dt = 0.001
wave_dt = period / len(wave)
#print("steps:",len(wave), "period:",period, "dt:",dt,"period_dt:",wave_dt, "wave_inc:",wave_inc)

base_dt = 0.001
dtcnt=0
while True:

    wave_dt = max(0, utils.map_range(knob_a.value, (65500,150), (0.001, 0.25)))
    volt_amplitude = utils.map_range(knob_b.value, (150,65500), (0.1,5) )
    # period = max(0, utils.map_range(knob_a.value, (150,65500), (0.1, 20)))
    # wave_dt = wave_inc * period / len(wave)

    #if wave_dt*2 < dt:
    #    wave_inc = 2*wave_inc
    #    wave_dt = 2*wave_dt

    wave_inc = max(1,utils.map_range(wave_dt, (0,0.1), (16,1))) # this is a float
    dt = wave_dt / wave_inc
    wave_inc = int(wave_inc)
    
    wave_index = (wave_index + wave_inc) % len(wave)
        
    print("steps:",len(wave), "wave_inc:",wave_inc,"period:",period, "wave_dt:",wave_dt, "dt:",dt)

    val = volt_offset + volt_amplitude * wave[wave_index]
    # convert to volts and send it out
    set_out_a_volts(val)

    
    time.sleep(dt)  # dt never changes
    


# while True:
# #    but1.update()
# #    but2.update()
#     #period = max(0, utils.map_range(knob_a.value, (150,65500), (0.001, 10)))
#     #dt = period / len(wave)
#     dt = max(0, utils.map_range(knob_a.value, (150,65500), (0.005,0.5)))
#     #print("dt:",dt)
#     if dt <= 0.01:
#         wave_inc = 16
#     elif dt > 0.01 and dt <= 0.02:
#         wave_inc = 8
#         time.sleep(dt/4)
#     elif dt > 0.02 and dt < 0.04:
#         wave_inc = 4
#         time.sleep(dt/3)
#     else:
#         wave_inc = 1
#         time.sleep(dt)

#     wave_index = (wave_index + wave_inc) % len(wave)
#     val = volt_offset + volt_amplitude * wave[wave_index]
#     # convert to volts and send it out
#     set_out_a_volts(val)

#     if wave_index==0:
#         overage = time.monotonic() - period_time
#         #print("updated: period:", period, "dt:",dt, "actual_period:",time.monotonic()-period_time, time.monotonic())
#         print("wave_inc:",wave_inc," dt:",dt, "actual_dt:",(time.monotonic()-period_time)/len(wave))
#         period_time = time.monotonic()
    
    # can't use this approach because time.montonic() only has 1-sec resolution 
    # now = time.monotonic()
    # if now > (last_time + dt):
    #     last_time = time.monotonic()
    #     wave_index = (wave_index + 1) % len(wave)
    #     if wave_index==0:
    #         print("updated: ", time.monotonic()-period_time)
    #         period_time = now
    # get the wave value, scale it by amplitude and offset it
    #val = 2 # volt_offset + volt_amplitude * wave[wave_index]
    #print(val)
    # convert to volts and send it out
    #set_out_a_volts(val)
    

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

        
