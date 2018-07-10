#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdbool.h>
#include "common_dht_read.h"

void usage(const char *argv) {
	fprintf(stderr, "Usage: %s [-o]\n", argv);
	exit(-1);
}

int main(int argc, const char *argv[])
{
        int opt;
	int pin = 5;
	int sensor = DHT22;
	int res;
	float humidity, temperature;

        bool infinite = true;

        while ((opt = getopt(argc, (char * const*)argv, "o")) != -1) {
                switch(opt) {
                case 'o':
                        infinite = false;
                        break;
                default:
                        usage(argv[0]);
                }
        }

	do {
		fprintf(stdout, "Staring getting humidity and temperature: ");
		res = pi_2_dht_read(sensor, pin, &humidity, &temperature);
		if (res != DHT_SUCCESS) {
			fprintf(stderr, "Error Getting the humidity and temperature\n");
			if (! infinite) exit(-1);
		} else {
			fprintf(stdout, "humidity = %f, temperature = %f\n", humidity, temperature);
		}

		if (infinite) sleep(5);
	} while (infinite);

	return 0;
}
