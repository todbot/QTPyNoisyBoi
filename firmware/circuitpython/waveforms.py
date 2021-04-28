

# - Generate LUTs for sin, tri, saw, squ
# - Given period, determine time.sleep dt for each LUT element (dx)
# - Given period overrun (CirPy too slow), adjust dt
# - If overrun too high, start subdividing LUT (e.g 256-element LUT to 64-elem)

import math
import utils

def make_sin_lut( lut_size, out_min,out_max):
    lut = [0] * lut_size
    for i in range(lut_size):
        dtheta = 2 * math.pi / lut_size
        l = math.sin(i * dtheta) 
        ld = utils.map_range(l, (-1,1), (out_min,out_max) )
        lut[i] = ld
        # if type(out_max) is float:
        #     str += "%1.3f," % ld
        # else:
        #     str += "%d," % ld
    return lut


class Waveform:
    def __init__(self, wave_type, steps=64, min_val=0,max_val=1):
        self._type = wave_type
        if wave_type == 'sin':
            self.wave = make_sin_lut(steps, min_val,max_val)
        elif wave_type == 'rnd':
            self.wave = [min_val,max_val] # no
        elif wave_type == 'squ':
            print("NO SQU");
        else:
            print("NO NO NO")
            



