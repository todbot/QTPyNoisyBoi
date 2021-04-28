#!/usr/bin/env python3


import math

#lut_size = 128

#out_min = 0
#out_max = 65535

# simple range mapper, like Arduino map()
def map_range(s, a, b):
    (a1, a2), (b1, b2) = a, b
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

def make_sin_lut( lut_size, out_min,out_max):
    str = "lut%d_sin = (" % lut_size
    for i in range(lut_size):
        dtheta = 2 * math.pi / lut_size
        l = math.sin(i * dtheta) 
        ld = map_range(l, (-1,1), (out_min,out_max) )
        if type(out_max) is float:
            str += "%1.3f," % ld
        else:
            str += "%d," % ld
    str += ")"
    return str


lut1 = make_sin_lut( 128, 0, 1.0)
print(lut1)
lut2 = make_sin_lut( 64, 0, 1.0)
print(lut2)
lut3 = make_sin_lut( 64, 0, 1023)
print(lut3)
