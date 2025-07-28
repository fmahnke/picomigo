function(external_target)
    set(oneValueArgs PATH)
    set(multiValueArgs DEPENDS)

    cmake_parse_arguments(
        PARSE_ARGV 0 arg "" "${oneValueArgs}" "${multiValueArgs}"
    )

    set(name ${arg_UNPARSED_ARGUMENTS})

    set(build_tool_options)

    if(
        DEFINED CMAKE_RULE_MESSAGES AND NOT CMAKE_RULE_MESSAGES
        AND CMAKE_GENERATOR STREQUAL Ninja
    )
        # Non-Makefile generators ignore CMAKE_RULE_MESSAGES, so simulate it
        # by adding --quiet to the build tool's command line.

        # For ninja, this removes the "[x/xx] Building..." and
        # "[x/xx] <command>" lines.

        list(APPEND build_tool_options -- --quiet)
    endif()

    set(source_dir ${CMAKE_CURRENT_SOURCE_DIR}/${arg_PATH})

    ExternalProject_Add(
        ${name}
        DEPENDS ${arg_DEPENDS}
        PREFIX ${name}
        SOURCE_DIR ${source_dir}
        BUILD_ALWAYS TRUE

        # TODO add -Werror=dev, --warn-uninitialized for projects that support
        # them.

        CMAKE_ARGS
            -Werror=deprecated
            -C "${propagated_cache_path}"

        BUILD_COMMAND cmake --build . ${build_tool_options}

        # INSTALL_COMMAND ""

        INSTALL_COMMAND cmake --install . --prefix=/usr/local
    )
endfunction()

# Create a .cmake cache file with the variables we want to propagate to
# external projects.

set(propagated_cache_path "${CMAKE_BINARY_DIR}/propagated_cache.cmake")

function(propagate_cache_vars)
    set(
        propagated_cache_vars

        CMAKE_CXX_INCLUDE_WHAT_YOU_USE
        CMAKE_INSTALL_MESSAGE
        CMAKE_MESSAGE_LOG_LEVEL
        CMAKE_MODULE_PATH
        CMAKE_RULE_MESSAGES
        CMAKE_TOOLCHAIN_FILE
        CMAKE_VERBOSE_MAKEFILE
        CMAKE_EXPORT_COMPILE_COMMANDS
        PICO_SDK_PATH
        PICO_BOARD
        PICO_PLATFORM
    )

    get_cmake_property(CACHE_VARS CACHE_VARIABLES)

    file(WRITE "${propagated_cache_path}" "# Propagated cache variables\n")

    foreach(CACHE_VAR ${CACHE_VARS})
        list(FIND propagated_cache_vars ${CACHE_VAR} index)

        if(NOT index EQUAL -1)
            get_property(
                CACHE_VAR_HELPSTRING CACHE ${CACHE_VAR} PROPERTY HELPSTRING
            )

            file(
                APPEND "${propagated_cache_path}"
                "set(${CACHE_VAR} \n\"${${CACHE_VAR}}\"\n CACHE STRING \"No help, variable specified on the command line.\" FORCE)\n"
            )
        endif()
    endforeach()
endfunction()

