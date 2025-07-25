# Location of top-level MicroPython directory
MPY_DIR = /home/boss/src/lib/micropython/micropython

BUILD = _build

# Name of module
MOD = sound

# Source files (.c or .py)
SRC = src/sound.c

# Architecture to build for (x86, x64, armv6m, armv7m, xtensa, xtensawin, rv32imc)
ARCH = armv7emsp

MPY_LD_FLAGS += -l $(BUILD)/libpicomigo_audio.a

LINK_RUNTIME = 0

# Include to get the rules for compiling and linking the module
include $(MPY_DIR)/py/dynruntime.mk
