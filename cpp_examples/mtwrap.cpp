#include "mtwrap.h"
//#include <cstdint>
#include <boost/random/mersenne_twister.hpp>
#include <boost/random/uniform_int_distribution.hpp>
#include <boost/random/uniform_real_distribution.hpp>

static boost::random::mt19937 rng(42u);
static boost::random::uniform_int_distribution<> dist(1, 6);

extern "C" {
int roll_die(void)
{
    return dist(rng);
}

uint32_t mt_rand(void)
{
    return rng();
}
void mt_write_random(uint8_t *bytes, size_t len)
{
    while (len >= 4) {
        uint32_t tmp = mt_rand();
        memcpy(bytes, &tmp, sizeof(uint32_t));
        bytes += 4;
        len -= 4;
    }
    if (len) {
        uint32_t tmp = mt_rand();
        memcpy(bytes, &tmp, len);
    }
}

}
