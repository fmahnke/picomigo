#include "hardware/gpio.h"
#include "pico/binary_info.h"
#include "pico/stdlib.h"

#include "audio.h"

#include "snd_drum.h"
#include "snd_synth_loop.h"

#include <stdio.h>

#define SOUND_PIN 2
#define BTN_PIN 16
#define LED_PIN 25

#define TODO
#define PLAY

#ifdef TODO
static void blink_led(void) {
    static uint64_t last_blink = 0;

    uint64_t cur_time = time_us_64();
    if (last_blink + 500000 < cur_time) {
        gpio_xor_mask(1 << LED_PIN);
        last_blink = cur_time;
    }
}

void sound_init(void) {
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);

    gpio_init(BTN_PIN);
    gpio_set_dir(BTN_PIN, false);
    gpio_pull_up(BTN_PIN);
    blink_led();
#ifdef PLAY

    audio_init(SOUND_PIN, 22050);
    int id = audio_play_loop(snd_synth_loop, sizeof(snd_synth_loop), 80);
    printf("playing synth loop as %d\n", id);

    uint64_t btn_press_time = 0;
    while (1) {
        sleep_ms(20);

        gpio_init(0);
        gpio_set_dir(0, GPIO_OUT);
        gpio_put(0, true);

        gpio_init(LED_PIN);
        gpio_set_dir(LED_PIN, GPIO_OUT);
        gpio_put(LED_PIN, false);

        // blink_led();

        if (gpio_get(BTN_PIN) == 0) {
            uint64_t cur_time = time_us_64();
            if (btn_press_time + 300000 < cur_time) {
                btn_press_time = cur_time;
                int id = audio_play_once(snd_drum, sizeof(snd_drum));
                printf("playing drums as %d\n", id);
                if (id >= 0) {
                    audio_source_set_volume(id, 1024);
                }
            }
        }

        audio_mixer_step();
    }
#endif
}
#else  // #if TODO

void sound_init(void) {
    gpio_init(0);
    gpio_set_dir(0, GPIO_OUT);
    gpio_put(0, true);

    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);

    gpio_init(BTN_PIN);
    gpio_set_dir(BTN_PIN, false);
    gpio_pull_up(BTN_PIN);

    // blink_led();

    gpio_put(LED_PIN, true);

    while (true) {}
}

#endif
