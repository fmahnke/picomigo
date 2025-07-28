cmake_minimum_required(VERSION 4.0)

project(picomigo-native VERSION 0.1.0)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

include(ExternalProject)

include(mk)

set(PICO_SDK_PATH "${CMAKE_CURRENT_LIST_DIR}/lib/pico-sdk" CACHE PATH "")
set(PICO_PLATFORM rp2350 CACHE STRING "")
set(PICO_BOARD pico2_w CACHE STRING "")

propagate_cache_vars()

external_target(
    pico_sdk PATH lib/pico-sdk
)

external_target(
    modules_sound PATH modules/sound
)
