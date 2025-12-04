#include "sn76489.hpp"
#include "vgm_lunar_last_boss.hpp"

#include "sn76489.pio.h"

#include "hardware/clocks.h"
#include "hardware/pio.h"
#include "pico/assert.h"
#include "pico/stdio.h"
#include "pico/time.h"

#include <cfenv>
#include <hardware/gpio.h>

#include <cmath>
#include <stdio.h>

#define I2C_GPIO_PIN_SDA 14
#define I2C_GPIO_PIN_SLC 15

// constexpr uint32_t CLOCK_HZ = 1000000;
constexpr uint32_t CLOCK_HZ = 3579540;

constexpr uint32_t SAMPLE_RATE = 44100;
constexpr float SPEED = 1.10f;

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

u32 milliseconds_from_samples(u32 sample_count) {
    return std::lround((double) sample_count / (SAMPLE_RATE * SPEED) * 1000);
}

u32 microseconds_from_samples(u32 sample_count) {
    return std::lround((double) sample_count / (SAMPLE_RATE * SPEED) * 1000000);
}

int main() {
    init();

    printf("loop\n");

    bool play = false;
    bool play2 = true;

    usize vgm_index = 0;

    std::fesetround(FE_TONEAREST);

    while (true) {
        uint64_t time_ms = time_us_64() / 1000.0f;

        if (time_ms > 15000) {
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
            u8 command_size = 0;
            u8 data[2] = {vgm_data[vgm_index + 1], vgm_data[vgm_index + 2]};

            // printf(
            //     "%u command: %02x  %02x %02x\n",
            //     vgm_index,
            //     command,
            //     data[0],
            //     data[1]
            // );

            if (command == 0x00) {
                command_size = 2;

                u8 data = vgm_data[vgm_index + 1];

                audio_module.send_byte(data);
            } else if (command == 0x01) {
                command_size = 1;

                sleep_us(microseconds_from_samples(735));
            } else if (command == 0x4F) {
                command_size = 1;

                // no op
            } else if (command == 0x61) {
                command_size = 3;

                u16 data =
                    (vgm_data[vgm_index + 2] << 8) | vgm_data[vgm_index + 1];

                sleep_us(microseconds_from_samples(data));
            } else {
                printf(
                    "unsupported command: 0x%02x (%u)\n",
                    command,
                    vgm_index
                );

                hard_assertion_failure();
            }

            hard_assert(command_size != 0);

            vgm_index += command_size;
        }

        // sleep_ms(1);
    }
}

u16 data_from_frequency(float frequency) {
    return CLOCK_HZ / (32 * frequency);
}
