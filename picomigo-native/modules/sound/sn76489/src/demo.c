#include "hardware/clocks.h"
#include "hardware/pio.h"
#include "pico/stdio.h"
#include "pico/stdlib.h"
#include "sn76489.pio.h"
#include <hardware/gpio.h>
#include <stdio.h>

#define D_PINS_LENGTH 8
#define CLOCK_HZ 1000000

const uint d_pins[D_PINS_LENGTH] = {0, 1, 2, 3, 4, 5, 6, 7};

static const uint clock_pin = 8;
static const uint not_write_en_pin = 9;
static const uint ready_pin = 10;

// frequency = CLOCK_HZ / 32 * n
// n = CLOCK_HZ / (32 * frequency)

uint16_t data_from_frequency(float frequency) {
    return CLOCK_HZ / (32 * frequency);
}

void send_byte(uint8_t value) {
    gpio_put(d_pins[7], value & 1);
    gpio_put(d_pins[6], value & 2);
    gpio_put(d_pins[5], value & 4);
    gpio_put(d_pins[4], value & 8);
    gpio_put(d_pins[3], value & 16);
    gpio_put(d_pins[2], value & 32);
    gpio_put(d_pins[1], value & 64);
    gpio_put(d_pins[0], value & 128);

    gpio_put(not_write_en_pin, 0);

    sleep_ms(1);

    gpio_put(not_write_en_pin, 1);
}

int main() {
    // pico pins
    // 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

    // write time 32 cycles == 32 us at 1 MHz clock

    static const float pio_freq = 2000000;

    stdio_init_all();

    for (size_t i = 0; i < D_PINS_LENGTH; ++i) {
        gpio_init(d_pins[i]);
        gpio_set_dir(d_pins[i], GPIO_OUT);
    }

    gpio_init(clock_pin);
    gpio_set_dir(clock_pin, GPIO_OUT);

    gpio_init(not_write_en_pin);
    gpio_set_dir(not_write_en_pin, GPIO_OUT);

    gpio_init(ready_pin);
    gpio_set_dir(ready_pin, GPIO_IN);

    // Choose PIO instance (0 or 1)
    PIO pio = pio0;

    // Get first free state machine in PIO 0
    uint sm = pio_claim_unused_sm(pio, true);

    // Add PIO program to PIO instruction memory. SDK will find location and
    // return with the memory offset of the program.
    uint offset = pio_add_program(pio, &sn76489_program);

    float clock_hz = (float) clock_get_hz(clk_sys);

    // Calculate the PIO clock divider
    float div = clock_hz / pio_freq;

    // Initialize the program using the helper function in our .pio file
    sn76489_program_init(pio, sm, offset, clock_pin, div);

    // Start running our PIO program in the state machine
    pio_sm_set_enabled(pio, sm, true);

    size_t step = 0;

    sleep_ms(2000);

    // Do nothing
    while (true) {
        uint64_t time_ms = time_us_64() / 1000.0f;

        if (time_ms > 5000) {
            break;
        }

        uint16_t note = data_from_frequency(440.0f);

        uint8_t first = (0b1000 << 4) | (note & 0xF);
        uint8_t second = note >> 4;

        if (step == 0) {
            printf("note: %u, %010b, %08b, %08b\n", note, note, first, second);
        }

        step += 1;

        if (step == 1000) {
            step = 0;
        }

        send_byte(first);
        send_byte(second);

        // update ch 1 attenuator max

        send_byte(0b10010001);

        // silence noise

        send_byte(0b10111111);
        send_byte(0b11011111);
        send_byte(0b11111111);

        // while (true) {};

        sleep_ms(1);
        /*
        printf(
            "Clock Hz: %.02f, pio freq: %.02f, div: %.02f\n",
            clock_hz,
            pio_freq,
            div
        );

        sleep_ms(1000);
        */
    }
}
