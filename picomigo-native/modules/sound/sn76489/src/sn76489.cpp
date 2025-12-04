#include "sn76489.hpp"

#include "pico/time.h"

#include <hardware/gpio.h>

#include <cstdio>
#include <cstring>

static const int MCP_ALL_PINS_OUTPUT = 0x0000;

SN76489AudioModule::SN76489AudioModule(
    u8 not_write_en,
    u8 i2c_sda,
    u8 i2c_scl
) :
  mcp(i2c1, 0x20),
  mcp_sn76489_data_pins{7, 6, 5, 12, 11, 10, 9, 8},
  pin_not_write_en(not_write_en),
  i2c_sda(i2c_sda),
  i2c_scl(i2c_scl) {}

void SN76489AudioModule::init() {
    i2c_init(i2c1, 400000);

    gpio_set_function(i2c_sda, GPIO_FUNC_I2C);
    gpio_set_function(i2c_scl, GPIO_FUNC_I2C);
    gpio_pull_up(i2c_sda);
    gpio_pull_up(i2c_scl);

    mcp.setup(true, false);
    mcp.set_io_direction(MCP_ALL_PINS_OUTPUT);
    mcp.set_all_output_bits(0);

    gpio_init(pin_not_write_en);
    gpio_set_dir(pin_not_write_en, GPIO_OUT);
    gpio_put(pin_not_write_en, false);

    sn76489.send_byte_callback = [this](u8 value) {
        return this->send_byte(value);
    };

    sn76489.init(0, 0, 0, 0);

    // mcp.set_output_bit_for_pin(0, 1);
    // mcp.set_output_bit_for_pin(1, 1);
    // mcp.set_output_bit_for_pin(2, 1);
    // mcp.set_output_bit_for_pin(3, 1);
    // mcp.set_output_bit_for_pin(4, 1);
    // mcp.set_output_bit_for_pin(5, 1);
    // mcp.set_output_bit_for_pin(6, 1);
    // mcp.set_output_bit_for_pin(7, 1);
    // mcp.set_output_bit_for_pin(8, 1);
    // mcp.set_output_bit_for_pin(9, 1);
    // mcp.set_output_bit_for_pin(10, 1);
    // mcp.set_output_bit_for_pin(11, 1);
    // mcp.set_output_bit_for_pin(12, 1);
    // mcp.set_output_bit_for_pin(13, 1);
    // mcp.set_output_bit_for_pin(14, 1);
    // mcp.set_output_bit_for_pin(15, 1);
    // mcp.flush_output();
}

void SN76489AudioModule::send_byte(u8 value) {
    // printf("send byte %08b\n", value);
    //
    //  for (usize i = 0; i < D_PINS_LENGTH; ++i) {
    //      printf("%d ", mcp_sn76489_data_pins[i]);
    //  }
    //  printf("\n");

    mcp.set_output_bit_for_pin(mcp_sn76489_data_pins[7], value & 1);
    mcp.set_output_bit_for_pin(mcp_sn76489_data_pins[6], value & 2);
    mcp.set_output_bit_for_pin(mcp_sn76489_data_pins[5], value & 4);
    mcp.set_output_bit_for_pin(mcp_sn76489_data_pins[4], value & 8);
    mcp.set_output_bit_for_pin(mcp_sn76489_data_pins[3], value & 16);
    mcp.set_output_bit_for_pin(mcp_sn76489_data_pins[2], value & 32);
    mcp.set_output_bit_for_pin(mcp_sn76489_data_pins[1], value & 64);
    mcp.set_output_bit_for_pin(mcp_sn76489_data_pins[0], value & 128);
    // gpio_put(pins_data[7], value & 1);
    // gpio_put(pins_data[6], value & 2);
    // gpio_put(pins_data[5], value & 4);
    // gpio_put(pins_data[4], value & 8);
    // gpio_put(pins_data[3], value & 16);
    // gpio_put(pins_data[2], value & 32);
    // gpio_put(pins_data[1], value & 64);
    // gpio_put(pins_data[0], value & 128);
    mcp.flush_output();

    gpio_put(pin_not_write_en, 0);

    sleep_us(100);

    gpio_put(pin_not_write_en, 1);
}

// SN76489I2CInterface::SN76489I2CInterface() :
//   mcp(i2c1, 0x20) {}

// void SN76489I2CInterface::send_byte(u8 value) {
//     gpio_put(pins_data[7], value & 1);
//     gpio_put(pins_data[6], value & 2);
//     gpio_put(pins_data[5], value & 4);
//     gpio_put(pins_data[4], value & 8);
//     gpio_put(pins_data[3], value & 16);
//     gpio_put(pins_data[2], value & 32);
//     gpio_put(pins_data[1], value & 64);
//     gpio_put(pins_data[0], value & 128);
// }

void SN76489::init(const u8 *data, u8 clock, u8 not_write_en, u8 ready) {
    memcpy(pins_data, data, sizeof(u8) * D_PINS_LENGTH);

    pin_clock = clock;
    pin_not_write_en = not_write_en;
    pin_ready = ready;

    // for (size_t i = 0; i < D_PINS_LENGTH; ++i) {
    //     gpio_init(pins_data[i]);
    //     gpio_set_dir(pins_data[i], GPIO_OUT);
    // }

    // gpio_set_dir(pin_not_write_en, GPIO_OUT);

    // gpio_init(pin_ready);
    // gpio_set_dir(pin_ready, GPIO_IN);

    // silence everything

    send_byte_callback(0b10011111);
    send_byte_callback(0b10111111);
    send_byte_callback(0b11011111);
    send_byte_callback(0b11111111);
}

// frequency = CLOCK_HZ / 32 * n
// n = CLOCK_HZ / (32 * frequency)

// write time 32 cycles == 32 us at 1 MHz clock

// void SN76489::send_byte(uint8_t value) {
//     gpio_put(pins_data[7], value & 1);
//     gpio_put(pins_data[6], value & 2);
//     gpio_put(pins_data[5], value & 4);
//     gpio_put(pins_data[4], value & 8);
//     gpio_put(pins_data[3], value & 16);
//     gpio_put(pins_data[2], value & 32);
//     gpio_put(pins_data[1], value & 64);
//     gpio_put(pins_data[0], value & 128);

//     gpio_put(pin_not_write_en, 0);

//     sleep_ms(1);

//     gpio_put(pin_not_write_en, 1);
// }

void SN76489::frequency(u8 channel, u16 frequency) {
    u8 first = (0b1 << 7) | (channel << 5) | (frequency & 0xF);
    u8 second = frequency >> 4;

    // printf(
    //     "note: %u, %010b, %08b, %08b\n",
    //     frequency,
    //     frequency,
    //     first,
    //     second
    // );

    send_byte_callback(first);
    send_byte_callback(second);
}

void SN76489::attenuator(u8 channel, u8 level) {
    u8 data = (0b1001 << 4) | (channel << 5) | (level & 0xF);

    send_byte_callback(data);
}
