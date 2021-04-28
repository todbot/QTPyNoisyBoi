#!/usr/bin/env python3
#
#
# - There's a wave lookup table (lut) that contains a list of output values
# - Each step in the table is separated by 'cv_time' time
# - if 'cv_interp' is True, output interpolates to 
#
#

import time

lut64_sin = (0.500,0.549,0.598,0.645,0.691,0.736,0.778,0.817,0.854,0.887,0.916,0.941,0.962,0.978,0.990,0.998,1.000,0.998,0.990,0.978,0.962,0.941,0.916,0.887,0.854,0.817,0.778,0.736,0.691,0.645,0.598,0.549,0.500,0.451,0.402,0.355,0.309,0.264,0.222,0.183,0.146,0.113,0.084,0.059,0.038,0.022,0.010,0.002,0.000,0.002,0.010,0.022,0.038,0.059,0.084,0.113,0.146,0.183,0.222,0.264,0.309,0.355,0.402,0.451,)

lut = lut64_sin
lut_size = len(lut)

offset = 12345  # zero volt point
amplitude = 2  # volts
period = 0.1  # 10 Hz, variable
dt = period / lut_size

# copies ideas from Winterbloom_VoltageIO
# converts given voltages to (PWM) DAC values (0-65535)
# where the opamp is both amplifying and offset from zero volts
class VoltageOut:
    def __init__(self, calibration):
        self._analog_out = analog_out
        self._calibration = {}
        
    def dac_for_voltage(self, voltage):
        val = 3
        return val
    
    def _calibrated_value_for_voltage(self, voltage):
        if voltage in self._calibration:
            return self._calibration[voltage]

        low, high = _takeb_nearest_pair(self._calibration_keys, voltage)

        if high == low:
            normalized_offset = 0
        else:
            normalized_offset = (voltage - low) / (high - low)

        low_val = self._calibration[low]
        high_val = self._calibration[high]

        lerped = round(low_val + ((high_val - low_val) * normalized_offset))

        return min(lerped, 65535)
    

# from winterbloom_voltageio import VoltageOut
# vout = VoltageOut(None)
# vout.linear_calibration(-3,10)
# vout.voltage = 0
# print(vout._value)

while True:
    time.sleep(0.1)




# cvi=0
# cv_next = cv_lut[cvi]
# cv_last = cv_next

# curr_time = 0
# last_time = curr_time
# cv = cv_last
# cv_delta = 0

# while True:
#     time.sleep(0.1)
#     print("cv:", cv, "\tdelta:",cv_delta, "cv_next:",cv_next )
#     cv = cv + cv_delta
#     curr_time = curr_time + dt
#     if curr_time > cv_time + last_time:
#         last_time = curr_time
#         cvi = (cvi + 1) % len(cv_lut)
#         cv_last = cv_next
#         cv_next = cv_lut[cvi]
#         cv = cv_last
#         cv_delta = (cv_next - cv_last) * dt/cv_time
