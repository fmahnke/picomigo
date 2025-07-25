# Create an INTERFACE library for our C module.
add_library(usermod_picomigo_sound INTERFACE)

# Add our source files to the lib
target_sources(usermod_picomigo_sound INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/src/rp2/audio.c
    ${CMAKE_CURRENT_LIST_DIR}/src/rp2/sound.c
    ${CMAKE_CURRENT_LIST_DIR}/src/sound_mod.c
)

# Add the current directory as an include directory.
target_include_directories(usermod_picomigo_sound INTERFACE
    ${CMAKE_CURRENT_LIST_DIR})

# Link our INTERFACE library to the usermod target.
target_link_libraries(usermod INTERFACE usermod_picomigo_sound)

