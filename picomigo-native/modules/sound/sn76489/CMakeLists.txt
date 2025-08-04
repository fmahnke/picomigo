cmake_minimum_required(VERSION 4.0)

include(defaults.cmake)
# include(pico_sdk_import.cmake)
include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)
include($ENV{PICO_SDK_PATH}/tools/CMakeLists.txt)

project(picomigo_sound_sn76489 C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

pico_sdk_init()

add_executable(
    picomigo_sound_sn76489_demo

    src/demo.cpp
)

target_compile_definitions(
    picomigo_sound_sn76489_demo PRIVATE

    PICO_ENTER_USB_BOOT_ON_EXIT=1
)

# Create C header file with the name <pio program>.pio.h
pico_generate_pio_header(
    picomigo_sound_sn76489_demo

    ${CMAKE_CURRENT_LIST_DIR}/src/sn76489.pio
)

# Create map/bin/hex/uf2 files
pico_add_extra_outputs(picomigo_sound_sn76489_demo)

# Link to pico_stdlib (gpio, time, etc. functions)
target_link_libraries(
    picomigo_sound_sn76489_demo

    pico_stdlib
    hardware_pio
)

# target_link_libraries(
#     picomigo_sound_sn76489_demo
# 
#     picomigo_sound_sn76489
#     pico_stdlib
# 
#     # TODO might need these
# 
#     # pico_base
#     # hardware_dma
#     # hardware_pwm
#     # hardware_gpio
# )
# 
# add_library(
#     picomigo_sound_sn76489
# 
#     src/rp2/audio.c
#     src/rp2/sound.c
# )
# 
# target_link_libraries(
#     picomigo_sound_sn76489
# 
#     pico_stdlib
#     hardware_dma
#     hardware_pwm
# )
# 
pico_enable_stdio_usb(picomigo_sound_sn76489_demo 1)
# pico_add_extra_outputs(picomigo_sound_sn76489_demo)
