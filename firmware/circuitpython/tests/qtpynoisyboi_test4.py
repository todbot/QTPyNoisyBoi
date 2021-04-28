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
potBknob = analogio.AnalogIn(board.A2)

outA = pwmio.PWMOut(board.MOSI, frequency=25000, duty_cycle=0)
outB = pwmio.PWMOut(board.MISO, frequency=25000, duty_cycle=0)
#outA.duty_cycle = 0
outA.duty_cycle = 32768
#outA.duty_cycle = 65535

# test: check DC
#while True:   time.sleep(0.1); pass

lut_sin = (32767,34375,35979,37575,39160,40729,42279,43806,45307,46777,48213,49613,50972,52287,53554,54772,55937,57046,58097,59086,60012,60873,61665,62388,63040,63619,64124,64552,64905,65180,65377,65495,65535,65495,65377,65180,64905,64552,64124,63619,63040,62388,61665,60873,60012,59086,58097,57046,55937,54772,53554,52287,50972,49613,48213,46777,45307,43806,42279,40729,39160,37575,35979,34375,32767,31159,29555,27959,26374,24805,23255,21728,20227,18757,17321,15921,14562,13247,11980,10762,9597,8488,7437,6448,5522,4661,3869,3146,2494,1915,1410,982,629,354,157,39,0,39,157,354,629,982,1410,1915,2494,3146,3869,4661,5522,6448,7437,8488,9597,10762,11980,13247,14562,15921,17321,18757,20227,21728,23255,24805,26374,27959,29555,31159,)

cvA
#cvs = [ 100, 75, 50, 25, 0 ]
#cvs = [ 90, 75, 50, 25, 10,0 ]
#cvs = [ 48, 40, 30, 25 ]
rateA = 0.1
rateB = 0.1
cvs_list = [
    lut_sin,
    (90, 75, 50, 25, 10, 0),
    (100,0),
    (48, 40, 30, 25 ),
]

cvsa_index = 0
cvsb_index = 2
cvai=0
cvbi=0
cva_last = time.monotonic()
cvb_last = time.monotonic()

cvsa = cvs_list[cvsa_index]
cvsb = cvs_list[cvsb_index]

while True:
    butt1.update()
    now = time.monotonic()
    if now > cva_last + rateA:
        cva_last = now
        cvai = (cvai + 1) % len(cvsa)
        duty_cycle = int( cvsa[cvai] * 65535/100)
        outA.duty_cycle = 65535 - duty_cycle
    if now > cvb_last + rateB:
        cvb_last = now
        cvbi = (cvbi + 1) % len(cvsb)
        duty_cycle = int( cvsb[cvbi] * 65535/100)
        outB.duty_cycle = 65535 - duty_cycle
#    rateA = 0.01 + (potAknob.value / 65535 / 2)
    rateA = (potAknob.value / 65535 ) #/ len(cvsa))
    rateB = 0.01 + (potBknob.value / 65535 / 2)
    if butt1.fell: # pressed
        print("push! rateA:",rateA)
        cvsa_index = (cvsa_index + 1 ) % len(cvs_list)
        cvsa = cvs_list[cvsa_index]
        cvsai=0
        



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

        
