#include "types.h"

#include "mcp23017.h"

#include <functional>

typedef std::function<void(u8)> callback_function;

constexpr uint8_t D_PINS_LENGTH = 8;

// struct SN76489I2CInterface {
//     SN76489I2CInterface();

//     void send_byte(u8 value);

//     int m_i;
//     Mcp23017 mcp;
// };

struct SN76489 {
    void init(const u8 *data, u8 clock, u8 not_write_en, u8 ready);
    void send_byte(u8 value);
    void frequency(u8 channel, u16 frequency);
    void attenuator(u8 channel, u8 level);

    callback_function send_byte_callback;

    u8 pins_data[D_PINS_LENGTH];
    u8 pin_clock;
    u8 pin_not_write_en;
    u8 pin_ready;
};

struct SN76489AudioModule {
    SN76489AudioModule(u8 not_write_en, u8 i2c_sda, u8 i2c_scl);

    void init();
    void send_byte(u8 value);

    Mcp23017 mcp;
    SN76489 sn76489;

    u8 pin_not_write_en;
    u8 i2c_sda;
    u8 i2c_scl;
    u8 mcp_sn76489_data_pins[D_PINS_LENGTH];
};

u16 data_from_frequency(float frequency);
