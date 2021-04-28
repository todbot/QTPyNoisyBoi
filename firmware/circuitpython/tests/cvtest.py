#!/usr/bin/env python3
#
#
# - There's a wave lookup table (lut) that contains a list of output values
# - Each step in the table is separated by 'cv_time' time
# - if 'cv_interp' is True, output interpolates to 
#
#

import time

#cv_lut = (100,0,100,0)
cv_lut = (100,50,25,0)
cv_time = 0.01 # seconds
cv_interp = True

dt = 0.001
cvi=0
cv_next = cv_lut[cvi]
cv_last = cv_next

curr_time = 0
last_time = curr_time
cv = cv_last
cv_delta = 0

while True:
    time.sleep(0.1)
    print("cv:", cv, "\tdelta:",cv_delta, "cv_next:",cv_next )
    cv = cv + cv_delta
    curr_time = curr_time + dt
    if curr_time > cv_time + last_time:
        last_time = curr_time
        cvi = (cvi + 1) % len(cv_lut)
        cv_last = cv_next
        cv_next = cv_lut[cvi]
        cv = cv_last
        cv_delta = (cv_next - cv_last) * dt/cv_time
