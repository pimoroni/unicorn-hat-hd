#include <stdint.h>
#include <unistd.h>
#include <string.h>

extern "C" {
int roll_die(void);
uint32_t mt_rand(void);
void mt_write_random(uint8_t *bytes, size_t len);
}
