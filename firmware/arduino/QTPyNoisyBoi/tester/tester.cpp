

/*
 *  Compile with:
 * gcc -o tester tester.cpp ../VoltageOut.cpp -I ..
 *
 */

#include "VoltageOut.h"
#include "CVMaker.h"

#include "stdio.h"

//voltage_calibration cals[3];
voltage_calibration cals_a[] =
    {
     {-3.34, 65535},
     {0.0, 43675},
     {6.69, 0}
    };

int main()
{
    printf("Hello there, %lu calibration entries\n", sizeof(cals_a)/sizeof(voltage_calibration));
    
    VoltageOut vo = VoltageOut(cals_a, sizeof(cals_a)/sizeof(voltage_calibration));

    printf("dac for 1.0V: %d\n", vo.dac_for_voltage(1.0));
    printf("dac for 2.0V: %d\n", vo.dac_for_voltage(2.0));
    printf("dac for 3.0V: %d\n", vo.dac_for_voltage(3.0));
    printf("dac for 4.0V: %d\n", vo.dac_for_voltage(4.0));
    printf("dac for 5.0V: %d\n", vo.dac_for_voltage(5.0));
    return 0;
}
