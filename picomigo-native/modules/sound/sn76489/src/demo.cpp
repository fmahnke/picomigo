#include "sn76489.hpp"

#include "hardware/clocks.h"
#include "hardware/pio.h"
#include "pico/stdio.h"
#include "pico/time.h"
#include "sn76489.pio.h"
#include <hardware/gpio.h>
#include <stdio.h>

const uint d_pins[D_PINS_LENGTH] = {0, 1, 2, 3, 4, 5, 6, 7};

static const uint clock_pin = 8;
static const uint not_write_en_pin = 9;
static const uint ready_pin = 10;

int main() {
    // pico pins
    // 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

    // write time 32 cycles == 32 us at 1 MHz clock

    stdio_init_all();

    // Wait for serial connection.

    sleep_ms(2000);

    printf("init PIO\n");

    // Choose PIO instance (0 or 1)
    PIO pio = pio0;

    // Get first free state machine in PIO 0
    uint sm = pio_claim_unused_sm(pio, true);

    // Add PIO program to PIO instruction memory. SDK will find location and
    // return with the memory offset of the program.
    uint offset = pio_add_program(pio, &sn76489_program);

    float clock_hz = (float) clock_get_hz(clk_sys);

    static const float pio_freq = 2000000;

    // Calculate the PIO clock divider
    float div = clock_hz / pio_freq;

    // Initialize the program using the helper function in our .pio file
    sn76489_program_init(pio, sm, offset, clock_pin, div);

    // Start running our PIO program in the state machine
    pio_sm_set_enabled(pio, sm, true);

    printf("init sn76489\n");

    const u8 data_pins[] = {0, 1, 2, 3, 4, 5, 6, 7};

    SN76489 sn76489;
    sn76489.init(data_pins, 8, 9, 10);

    size_t step = 0;

    printf("loop\n");

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

        sn76489.send_byte(first);
        sn76489.send_byte(second);

        // update ch 1 attenuator max

        sn76489.send_byte(0b10010001);

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
