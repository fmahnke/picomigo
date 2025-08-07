#include "sn76489.hpp"
#include "vgm_data.hpp"

#include "sn76489.pio.h"

#include "hardware/clocks.h"
#include "hardware/pio.h"
#include "pico/stdio.h"
#include "pico/time.h"

#include <hardware/gpio.h>
#include <stdio.h>

#define I2C_GPIO_PIN_SDA 14
#define I2C_GPIO_PIN_SLC 15

// constexpr uint32_t CLOCK_HZ = 1000000;
constexpr uint32_t CLOCK_HZ = 3579540;

const uint d_pins[D_PINS_LENGTH] = {0, 1, 2, 3, 4, 5, 6, 7};

// GG clock 3579540

static const uint clock_pin = 8;
static const uint not_write_en_pin = 9;
// static const uint ready_pin = 10;

bool use_i2c = true;

SN76489AudioModule
    audio_module(not_write_en_pin, I2C_GPIO_PIN_SDA, I2C_GPIO_PIN_SLC);

static SN76489 sn76489;

void pio_init() {
    printf("init PIO\n");

    // Choose PIO instance (0 or 1)
    PIO pio = pio0;

    // Get first free state machine in PIO 0
    uint sm = pio_claim_unused_sm(pio, true);

    // Add PIO program to PIO instruction memory. SDK will find location and
    // return with the memory offset of the program.
    uint offset = pio_add_program(pio, &sn76489_program);

    float clock_hz = (float) clock_get_hz(clk_sys);

    static const float pio_freq = (float) (CLOCK_HZ * 2);

    // Calculate the PIO clock divider
    float div = clock_hz / pio_freq;

    // Initialize the program using the helper function in our .pio file
    sn76489_program_init(pio, sm, offset, clock_pin, div);

    // Start running our PIO program in the state machine
    pio_sm_set_enabled(pio, sm, true);
}

// void sn76489_init() {
//     printf("init sn76489\n");

//     const u8 data_pins[] = {0, 1, 2, 3, 4, 5, 6, 7};

//     sn76489.init(data_pins, 8, 9, 10);
// }

void init() {
    stdio_init_all();

    // Wait for serial connection.

    sleep_ms(2000);

    printf("trace\n");

    // gpio_set_dir(not_write_en_pin, GPIO_OUT);
    // while (true) {
    //     gpio_put(not_write_en_pin, true);
    //     sleep_ms(500);
    //     gpio_put(not_write_en_pin, false);
    //     sleep_ms(500);
    // }

    pio_init();

    printf("init audio module\n");

    audio_module.init();

    // sn76489_init();
}

int main() {
    init();

    printf("loop\n");

    bool play = false;
    bool play2 = true;

    usize vgm_index = 10500;

    while (true) {
        uint64_t time_ms = time_us_64() / 1000.0f;

        if (time_ms > 12000) {
            // break;
        }

        if (play) {
            audio_module.sn76489.frequency(0, data_from_frequency(440.0f));
            audio_module.sn76489.attenuator(0, 0);
            // audio_module.sn76489.attenuator(1, 0xF);
            // audio_module.sn76489.attenuator(2, 0xF);
            // audio_module.sn76489.attenuator(3, 0xF);
        }

        if (play2) {
            if (vgm_index == vgm_data_len) {
                break;
            }

            // printf("vgm index %d/%d\n", vgm_index, vgm_data_len);

            u8 command = vgm_data[vgm_index];

            if (command == 0x00) {
                u8 data = vgm_data[vgm_index + 1];

                audio_module.send_byte(data);
            } else if (command == 0x01) {
                sleep_ms(17);
            }

            ++vgm_index;
        }

        // sleep_ms(1);
    }
}

u16 data_from_frequency(float frequency) {
    return CLOCK_HZ / (32 * frequency);
}
