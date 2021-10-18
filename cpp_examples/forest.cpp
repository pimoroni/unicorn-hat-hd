#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <time.h>
#include <errno.h> // for ENOMEM
#include <signal.h>
#include "mtwrap.h"

// port of forest-fire.py to C/C++

// recommended by kernel documentation
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/types.h>
#include <linux/spi/spidev.h>

const char *dev_file = "/dev/spidev0.0";
const uint32_t max_speed_hz = 9000000;
const uint8_t SOF = 0x72;

// forest is oversampled.
const uint32_t scale = 3;
const uint32_t neighborhood = 3;

// 3 color channels, 3x scale for 2 dimensions
#define PANEL_LEN 16
#define SCALE_LEN 3
#define GRID_LEN  (PANEL_LEN * SCALE_LEN)
#define FOREST_LEN (PANEL_LEN*PANEL_LEN*SCALE_LEN*SCALE_LEN)
#define IMAGE_LEN (PANEL_LEN * PANEL_LEN * 3)

typedef struct {
    uint8_t t[FOREST_LEN];
} forest_s;

enum {
    F_SPACE = 0,
    F_TREE  = 1,
    F_FIRE  = 2,
};

const uint32_t fps_target = 12;
const uint32_t p_initial = 0.055 * UINT32_MAX;
const uint32_t p_plant = 0.001 * UINT32_MAX;
const uint32_t p_combust = 0.00005 * UINT32_MAX;

#define MIN(x,y) ({ \
    typeof(x) _x = (x);     \
    typeof(y) _y = (y);     \
    (void) (&_x == &_y);    \
    _x < _y ? _x : _y; })
#define MAX(x,y) ({ \
    typeof(x) _x = (x);     \
    typeof(y) _y = (y);     \
    (void) (&_x == &_y);    \
    _x > _y ? _x : _y; })

forest_s *new_forest(void)
{
    return (forest_s *) calloc(sizeof(forest_s), 1);
}

uint8_t count_neighbors(size_t x, size_t y) {
    // first eliminate symmetry
    if (x >= GRID_LEN/2) x = GRID_LEN - x - 1;
    if (y >= GRID_LEN/2) y = GRID_LEN - y - 1;
    // diagonal flip
    if (x < y) {
        size_t tmp = x;
        x = y;
        y = tmp;
    }
    // corner has 8, inside corner has 15, middle is 24
    bool equal = x == y;
    // corners
    if (equal) {
        if (x == 0) return 8;
        if (x == 1) return 15;
        return 24;
    }
    bool offby = x == (y + 1);
    if (offby) {
        if (y == 0) return 11;
        if (y == 1) return 19;
    }
    bool twoby = x == (y + 2);
    if (twoby) {
        if (y == 0) return 14;
        if (y == 1) return 19;
    }
    // edges
    if (y == 0) return 14;
    if (y == 1) return 19;
    // none of the above
    return 24;
}

// from Adafruit, gamma correction table for LEDs
const uint8_t gamma8[] = {
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255 };

uint8_t rescale(uint32_t accumulant, uint32_t neighbors)
{
  uint32_t frac = (255*accumulant + neighbors/2)/neighbors;
  if (frac >= 255) return 255;
	return frac;
}

void average_forest(uint8_t image[IMAGE_LEN], forest_s *forest)
{
  for (int i = 0; i < PANEL_LEN; ++i) {
    for (int j = 0; j < PANEL_LEN; ++j) {
      size_t oidx = 3 * (i * PANEL_LEN + j);
      ssize_t x = i * SCALE_LEN + SCALE_LEN/2;
      ssize_t y = j * SCALE_LEN + SCALE_LEN/2;
      uint32_t ncnt = count_neighbors(x, y);
      uint32_t ncnt_check = 0;
      uint32_t burning = 0;
      uint32_t trees = 0;
      uint32_t space = 0;
      const int xis = MAX(x - SCALE_LEN + 1, (ssize_t) 0);
      const int xie = MIN(x + SCALE_LEN, (ssize_t) GRID_LEN);
      const int yis = MAX(y - SCALE_LEN + 1, (ssize_t) 0);
      const int yie = MIN(y + SCALE_LEN, (ssize_t) GRID_LEN);
      for (int xi = xis; xi < xie; ++xi)
        for (int yi = yis; yi < yie; ++yi) {
					if ((yi == y) && (xi == x)) continue;
          ++ncnt_check;
          uint8_t fdata = forest->t[xi + GRID_LEN * yi];
          if (fdata == F_FIRE) ++burning;
          else if (fdata == F_TREE) ++trees;
          else ++space;
        }

      image[oidx + 0] = rescale(burning, ncnt);
      image[oidx + 1] = gamma8[rescale(trees, ncnt)];
      image[oidx + 2] = 0;
    }
  }
}

bool burning_neighbors(forest_s *cf, int i)
{
	ssize_t x = i % GRID_LEN;
	ssize_t y = i / GRID_LEN;
	const int xis = MAX(x - SCALE_LEN + 1, (ssize_t) 0);
	const int xie = MIN(x + SCALE_LEN, (ssize_t) GRID_LEN);
	const int yis = MAX(y - SCALE_LEN + 1, (ssize_t) 0);
	const int yie = MIN(y + SCALE_LEN, (ssize_t) GRID_LEN);
	for (int xi = xis; xi < xie; ++xi)
		for (int yi = yis; yi < yie; ++yi)
			if (cf->t[xi + GRID_LEN * yi] == F_FIRE) return true;

	return false;
}

void initialize_forest(forest_s *cf)
{
	memset(cf, 0, sizeof(forest_s));
	for (int i = 0; i < FOREST_LEN; i++) {
		bool will_grow = mt_rand() < p_initial;
		if (will_grow)
			cf->t[i] = F_TREE;
		else
			cf->t[i] = F_SPACE;
	}
}

void update_forest(forest_s *ff, forest_s *cf)
{
    memset(ff, 0, sizeof(forest_s));
    for (int i = 0; i < FOREST_LEN; i++) {
        if (cf->t[i] == F_SPACE) {
            bool will_grow = mt_rand() < p_plant;
            if (will_grow) {
                ff->t[i] = F_TREE;
            } else {
                ff->t[i] = F_SPACE;
						}
        } else if (cf->t[i] == F_FIRE) {
            ff->t[i] = F_SPACE;
        } else { // cf->t[i] == F_TREE
            bool will_burn = mt_rand() < p_combust;
            will_burn |= burning_neighbors(cf, i);
            if (will_burn) {
                ff->t[i] = F_FIRE;
            } else {
                ff->t[i] = F_TREE;
            }
        }
    }
}

static void increment_frametime(struct timespec *ts, int fps)
{
	const long nanoframe = (1000000000L + fps/2)/fps;	
	const long wrap = ts->tv_nsec + nanoframe;
	if (wrap >= 1000000000L) {
		ts->tv_nsec = wrap - 1000000000L;
		++ts->tv_sec;
	} else {
		ts->tv_nsec = wrap;
	}
}

static void control_time_delta(void)
{
	static struct timespec prev;
	struct timespec now = {0};
	int ret = clock_gettime(CLOCK_MONOTONIC, &now);
	if (ret != 0) return;
	if (prev.tv_sec == 0) {
		prev = now;
	}
	increment_frametime(&prev,  fps_target);
	long ldelta = prev.tv_nsec - now.tv_nsec;
	long lsecs = 0;
	while (prev.tv_sec > now.tv_sec) {
		now.tv_sec += 1;
		lsecs += 1;
	}
	if (ldelta < 0) {
		if (lsecs) {
			ldelta += 1000000000;
			--lsecs;
		} else {
			printf("Timing anomaly: %ld, %ld, %ld, %ld, %ld.\n", ldelta, prev.tv_sec, prev.tv_nsec, now.tv_sec, now.tv_nsec);
		}
	}
	struct timespec vs = {lsecs, ldelta};
	nanosleep(&vs, NULL);
}

static int spi_fd = 0;

int show_image(uint8_t image_pkt[IMAGE_LEN + 1])
{
    struct spi_ioc_transfer xfer = {0};
    uint8_t *rxbuf = NULL;
    rxbuf = (uint8_t *) malloc(IMAGE_LEN + 1);
    if (rxbuf == NULL) return -ENOMEM;
    xfer.len = IMAGE_LEN + 1;
    image_pkt[0] = SOF;
    xfer.tx_buf = (uintptr_t) &image_pkt[0];
    xfer.rx_buf = (uintptr_t) rxbuf;
    xfer.delay_usecs = 0;
    xfer.speed_hz = max_speed_hz;
    xfer.bits_per_word = 8;
    int retval = ioctl(spi_fd, SPI_IOC_MESSAGE(1), &xfer);
    if (retval != IMAGE_LEN + 1) {
    	printf("Got result %d from ioctl()\n", retval);
    }
    free(rxbuf);
    return 0;
}

int spidev_init(void)
{
    spi_fd = open(dev_file, O_RDWR);
    if (spi_fd < 0) {
        printf("Unable to open spidev: %d\n", spi_fd);
        spi_fd = 0;
        return -1;
    }
        
    return 0;
}

bool running = true;
void cleanup(int signal)
{
	if (!spi_fd) return;
	uint8_t image_pkt[IMAGE_LEN + 1] = {0};
	image_pkt[0] = SOF;
	show_image(image_pkt);
	running = false;
	close(spi_fd);
	return;
}

int main(int argc, char **argv)
{
    spidev_init();
    // register cleanup handler to close SPI bus.
    signal(SIGINT, cleanup);

    uint8_t image_pkt[IMAGE_LEN + 1] = {0};
    image_pkt[0] = SOF;
    forest_s a_forest = {0};
    forest_s b_forest = {0};
    forest_s *fut_forest = &b_forest;
    forest_s *cur_forest = &a_forest;
		initialize_forest(cur_forest);
    uint8_t *image = &image_pkt[1];
    uint32_t frames = 0;
    
    while (running) {
        update_forest(fut_forest, cur_forest);
        forest_s *tmp_forest = cur_forest;
        cur_forest = fut_forest;
        fut_forest = tmp_forest;;
        average_forest(image, cur_forest);
        show_image(image_pkt);
        control_time_delta();
        ++frames;
        // stop if we lose the SPI bus.
        if (!spi_fd && (frames >= 5)) running = false;
    }
    return 0;
}
