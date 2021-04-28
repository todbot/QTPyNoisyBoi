import time
import board
#import neopixel
import pwmio
import analogio

potknob = analogio.AnalogIn(board.A1)

out1 = pwmio.PWMOut(board.RX, frequency=25000, duty_cycle=0)

#out1.duty_cycle = 0
out1.duty_cycle = 32768
#out1.duty_cycle = 65535

#while True:   time.sleep(0.1); pass

cvs = [ 100, 75, 50, 25, 0 ]
rate = 0.1

# cv = 50
# while True:
#     duty_cycle = int(cv * 65535/100)
#     out1.duty_cycle = 65535 - duty_cycle
    
while True:
    for cv in cvs:
        duty_cycle = int(cv * 65535/100)
        out1.duty_cycle = 65535 - duty_cycle
        print("duty:",duty_cycle, out1.duty_cycle)
        rate = 0.05 + (potknob.value / 65535 / 5)
        time.sleep(rate)
     

# test knob to voltage output
while True:
    pos = potknob.value // 256
    print("pos:",pos)
    out1.duty_cycle = 65535 - potknob.value # inverting amplifier
    time.sleep(0.01)


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

        
