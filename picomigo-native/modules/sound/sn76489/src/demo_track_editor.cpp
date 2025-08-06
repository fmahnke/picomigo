#include "hardware/i2c.h"
#include "mcp23017.h"
#include "pico/stdio.h"
#include "pico/time.h"

#include <cstdio>

static const int MCP_ALL_PINS_OUTPUT = 0x0000;
static const int MCP_ALL_PINS_OFF = 0x0000;
static const int MCP_ALTERNATE_PINS_ON = 0xaaaa;

#define I2C_GPIO_PIN_SDA 14
#define I2C_GPIO_PIN_SLC 15

Mcp23017 mcp1(i2c1, 0x20);

void setup_output(Mcp23017 mcp) {
    int result;

    result = mcp.setup(true, false);
    result = mcp.set_io_direction(MCP_ALL_PINS_OUTPUT);
}

int main() {
    stdio_init_all();
    sleep_ms(2000);
    printf("Starting up\n");

    i2c_init(i2c1, 400000);
    gpio_set_function(I2C_GPIO_PIN_SDA, GPIO_FUNC_I2C);
    gpio_set_function(I2C_GPIO_PIN_SLC, GPIO_FUNC_I2C);
    gpio_pull_up(I2C_GPIO_PIN_SDA);
    gpio_pull_up(I2C_GPIO_PIN_SLC);

    setup_output(mcp1);
    // mcp1.set_all_output_bits(MCP_ALTERNATE_PINS_ON);
    mcp1.set_all_output_bits(MCP_ALL_PINS_OFF);

    printf("Setting MCP(0x20) pin 4\n");
    mcp1.set_output_bit_for_pin(4, true);
    mcp1.set_output_bit_for_pin(1, true);
    mcp1.set_output_bit_for_pin(2, true);
    mcp1.set_output_bit_for_pin(3, true);
    mcp1.set_output_bit_for_pin(5, true);
    mcp1.set_output_bit_for_pin(7, true);
    mcp1.set_output_bit_for_pin(6, true);
    mcp1.set_output_bit_for_pin(8, true);
    mcp1.set_output_bit_for_pin(9, true);
    mcp1.set_output_bit_for_pin(10, true);
    mcp1.set_output_bit_for_pin(11, true);
    mcp1.flush_output();

    // mcp1.set_all_output_bits(MCP_ALL_PINS_OFF);
    return 0;
}
