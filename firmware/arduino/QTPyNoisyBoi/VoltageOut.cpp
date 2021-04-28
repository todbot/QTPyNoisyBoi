/**
 * 
 * A very primitive port of wntrblm's Winterbloom_VoltageIO Python library:
 * https://github.com/wntrblm/Winterbloom_VoltageIO
 *
 */

#include "VoltageOut.h"

#include <stdlib.h>
#include <stdio.h>  // debug

//wtf
#ifndef min
#define min(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a < _b ? _a : _b; })
#endif
/*
    """Given a sorted, monotonic list of values and a target value,
    returns the index of lowest of closest two pairs of numbers in the list
    to the given target. The first being the closest number
    less than the target, the second being the closest number
    greater than the target.
    For example::
        >>> _take_nearest_pair([1, 2, 3], 2.5)
        (2, 3)
*/
void _take_nearest_voltage_pair(float target, voltage_calibration cals[], int num_cals, int* lo_i, int* hi_i )
{
    *lo_i = 0; *hi_i = 0;
    float low = cals[*lo_i].voltage;
    //float high = cals[*lo_i].voltage;
    for( int i=0; i< num_cals; i++) {
        float value = cals[i].voltage;
        if( value <= target && value >= low ) {
            low = value;
            *lo_i = i;
        }
        if( value > target ) {
            //high = value;
            *hi_i = i;
            return;
        }
    }
    //high = low; // if all else fails return highest
    *hi_i = *lo_i;
}

uint16_t VoltageOut::_calibrated_value_for_voltage(float voltage)
{
    for( int i=0; i<num_cals; i++) {
        if( cals[i].voltage == voltage ) { return cals[i].dac_val; }
    }

    int low_i, high_i;
    _take_nearest_voltage_pair(voltage, cals, num_cals, &low_i, &high_i);
    //printf("li:%d, hi:%d\n",low_i, high_i);
    float low_voltage = cals[low_i].voltage;
    float high_voltage = cals[high_i].voltage;
    //printf("low_voltage:%f, high_voltage:%f\n",low_voltage, high_voltage);

    float normalized_offset = 0;
    if( high_i != low_i ) {
        normalized_offset = (voltage - low_voltage) / (high_voltage - low_voltage);
    }
    //printf("normalized_offset: %f\n", normalized_offset);
    
    uint16_t low_val = cals[low_i].dac_val;
    uint16_t high_val = cals[high_i].dac_val;
    //printf("low_val:%d, high_val:%d\n",low_val, high_val);
    
    uint16_t lerped = low_val + (((float)high_val - low_val) * normalized_offset);
    //printf("lerped:%d\n", lerped);
    
    return min(lerped, (uint16_t)65535);
}

VoltageOut::VoltageOut()
{
    
}

/*
 * Given a list of calibration (voltage,dac) values, construct an object that returns
 * appropriate DAC values.
 *
 */
VoltageOut::VoltageOut(voltage_calibration some_cals[], int some_num_cals)
{
    cals = some_cals; // FIXME: copy in?x
    num_cals = some_num_cals;
}

/*
 */
uint16_t VoltageOut::dac_for_voltage(float voltage) {
    
    return _calibrated_value_for_voltage(voltage);
}



