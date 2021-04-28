

# Copies ideas from Winterbloom_VoltageIO
# 

def _take_nearest_pair(values, target):
    """Given a sorted, monotonic list of values and a target value,
    returns the closest two pairs of numbers in the list
    to the given target. The first being the closest number
    less than the target, the second being the closest number
    greater than the target.

    For example::

        >>> _take_nearest_pair([1, 2, 3], 2.5)
        (2, 3)

    If the target is not part of the continuous range of the
    values, then both numbers will either be the minimum or
    maximum value in the list.

    For example::

        >>> _take_nearest_pair([1, 2, 3], 10)
        (3, 3)

    """
    low = values[0]
    high = values[0]

    for value in values:
        if value <= target and value >= low:
            low = value
        if value > target:
            high = value
            break
    else:
        # If we never found a value higher than
        # the target, the the target is outside
        # of the range of the list. Therefore,
        # the highest close number is also the
        # lowest close number.
        high = low

    return low, high


class VoltageOut:
    """Convert given voltages to (PWM) DAC values (0-65535)
    where the opamp is both amplifying, inverting, and offset from zero volts
    """
    
    def __init__(self, calibration):
        self._calibration = calibration
        self._calibration_keys = sorted(self._calibration.keys())
        
    def _calibrated_value_for_voltage(self, voltage):
        if voltage in self._calibration:
            return self._calibration[voltage]

        low, high = _take_nearest_pair(self._calibration_keys, voltage)

        if high == low:
            normalized_offset = 0
        else:
            normalized_offset = (voltage - low) / (high - low)

        low_val = self._calibration[low]
        high_val = self._calibration[high]

        lerped = round(low_val + ((high_val - low_val) * normalized_offset))

        return min(lerped, 65535)

    def dac_for_voltage(self, voltage):
        return self._calibrated_value_for_voltage(voltage)
    
