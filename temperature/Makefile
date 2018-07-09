CC=gcc
IDIR =./lib
CFLAGS=-I$(IDIR) -static

TEM_HUM: main.c lib/common_dht_read.c lib/pi_2_dht_read.c lib/pi_2_mmio.c
	$(CC) -o TEM_HUM main.c lib/common_dht_read.c lib/pi_2_dht_read.c lib/pi_2_mmio.c $(CFLAGS)

.PHONY: clean

clean:
	rm -rf TEM_HUM
