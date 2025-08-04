#include "sn76489.hpp"

#include "pico/stdlib.h"

#include <hardware/gpio.h>

#include <cstring>

constexpr uint32_t CLOCK_HZ = 1000000;

void SN76489::init(const u8 *data, u8 clock, u8 not_write_en, u8 ready) {
    memcpy(pins_data, data, sizeof(u8) * D_PINS_LENGTH);

    pin_clock = clock;
    pin_not_write_en = not_write_en;
    pin_ready = ready;

    for (size_t i = 0; i < D_PINS_LENGTH; ++i) {
        gpio_init(pins_data[i]);
        gpio_set_dir(pins_data[i], GPIO_OUT);
    }

    // gpio_init(pin_clock);
    // gpio_set_dir(pin_clock, GPIO_OUT);

    gpio_init(pin_not_write_en);
    gpio_set_dir(pin_not_write_en, GPIO_OUT);

    gpio_init(pin_ready);
    gpio_set_dir(pin_ready, GPIO_IN);

    // silence everything else

    send_byte(0b10011111);
    send_byte(0b10111111);
    send_byte(0b11011111);
    send_byte(0b11111111);
}

// frequency = CLOCK_HZ / 32 * n
// n = CLOCK_HZ / (32 * frequency)

// write time 32 cycles == 32 us at 1 MHz clock

void SN76489::send_byte(uint8_t value) {
    gpio_put(pins_data[7], value & 1);
    gpio_put(pins_data[6], value & 2);
    gpio_put(pins_data[5], value & 4);
    gpio_put(pins_data[4], value & 8);
    gpio_put(pins_data[3], value & 16);
    gpio_put(pins_data[2], value & 32);
    gpio_put(pins_data[1], value & 64);
    gpio_put(pins_data[0], value & 128);

    gpio_put(pin_not_write_en, 0);

    sleep_ms(1);

    gpio_put(pin_not_write_en, 1);
}

u16 data_from_frequency(float frequency) {
    return CLOCK_HZ / (32 * frequency);
}
