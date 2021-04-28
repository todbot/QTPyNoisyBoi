/* TODO: This header. */

#pragma once

#include <stdint.h>

#ifdef __cplusplus
//extern "C" {
#endif

/* Args:
     value - Range is [0, 1023], unlike analogWrite()
*/
void analogWriteHF(const uint32_t pin, uint32_t value);


#ifdef __cplusplus
//}
#endif
