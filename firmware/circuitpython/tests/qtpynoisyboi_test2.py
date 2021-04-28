# qtpynoisyboi_test.py --
#
# MOSI -- out A (PWM)
# MISO -- out B (PWM)
# A0   -- out C (DAC)
# A1   -- in  A
# A2   -- in  B
# A3   -- in  C

import time
import board
#import neopixel
import pwmio
import analogio
import digitalio
from adafruit_debouncer import Debouncer

butt1pin = digitalio.DigitalInOut(board.TX)
butt1pin.pull = digitalio.Pull.UP
butt1 = Debouncer(butt1pin)


potAknob = analogio.AnalogIn(board.A1)

outA = pwmio.PWMOut(board.MOSI, frequency=25000, duty_cycle=0)
outB = pwmio.PWMOut(board.MISO, frequency=25000, duty_cycle=0)
#outA.duty_cycle = 0
outA.duty_cycle = 32768
#outA.duty_cycle = 65535

# test: check DC
#while True:   time.sleep(0.1); pass

#cvs = [ 100, 75, 50, 25, 0 ]
#cvs = [ 90, 75, 50, 25, 10,0 ]
#cvs = [ 48, 40, 30, 25 ]
rate = 0.1
cvs_list = [
    (90, 75, 50, 25, 10, 0),
    (100,0),
    ( 48, 40, 30, 25 ),
]
cvsa_index = 0
cvsb_index = 0
cvai=0
cvbi=0
cva_last = time.monotonic()
cvb_last = time.monotonic()

cvsa = cvs_list[cvsa_index]
cvsb = cvs_list[cvsb_index]

while True:
    butt1.update()
    now = time.monotonic()
    if now > cva_last + rate:
        cva_last = now
        cvai = (cvai + 1) % len(cvsa)
        duty_cycle = int( cvsa[cvai] * 65535/100)
        outA.duty_cycle = 65535 - duty_cycle
    rate = 0.01 + (potAknob.value / 65535 / 2)
    if butt1.fell: # pressed
        print("push!")
        cvsa_index = (cvsa_index + 1 ) % len(cvs_list)
        cvsa = cvs_list[cvsa_index]
        



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

        
