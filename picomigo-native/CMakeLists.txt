cmake_minimum_required(VERSION 4.0)

project(picomigo-native VERSION 0.1.0)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

include(ExternalProject)

include(mk)

external_target(
    pico_sdk PATH lib/pico-sdk
)
