/**
 * 
 * A very primitive port of wntrblm's Winterbloom_VoltageIO Python library:
 * https://github.com/wntrblm/Winterbloom_VoltageIO
 *
 */

#include <stdint.h>

struct voltage_calibration {
    float voltage;
    uint16_t dac_val;
};
  
class VoltageOut {

public:
    VoltageOut();
    VoltageOut(voltage_calibration cals[], int num_cals);
    
    uint16_t dac_for_voltage(float voltage);
    
private:
    voltage_calibration* cals;
    int num_cals;

    uint16_t _calibrated_value_for_voltage(float voltage);
   
};
