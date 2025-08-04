#include "types.h"

constexpr uint8_t D_PINS_LENGTH = 8;

struct SN76489 {
    void init(const u8 *data, u8 clock, u8 not_write_en, u8 ready);
    void send_byte(u8 value);
    void frequency(u8 channel, u16 frequency);
    void attenuator(u8 channel, u8 level);

    u8 pins_data[D_PINS_LENGTH];
    u8 pin_clock;
    u8 pin_not_write_en;
    u8 pin_ready;
};

u16 data_from_frequency(float frequency);
