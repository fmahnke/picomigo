cmake_minimum_required(VERSION 4.0)

include(pico_sdk_import.cmake)

project(picomigo_sound_project C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

pico_sdk_init()

add_executable(
    picomigo_sound_demo

    src/demo.c
)

target_link_libraries(
    picomigo_sound_demo

    picomigo_sound
    pico_stdlib
)

add_library(
    picomigo_sound

    src/rp2/audio.c
    src/rp2/sound.c
)

target_link_libraries(
    picomigo_sound

    pico_stdlib
    hardware_dma
    hardware_pwm
)

pico_enable_stdio_usb(picomigo_sound_demo 1)
pico_add_extra_outputs(picomigo_sound_demo)
