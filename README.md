# setup development environment

## sync python environment

```
cd picomigo-py
uv sync
```

# build and install

## native modules

### all

```
cd picomigo-native; ./build_all
```

### sound module

```
cd picomigo-native/modules/sound

./do_build sound
```

### sound module (upython)

```
cd picomigo-native/modules/sound

./do_build sound_module

picotool load -f $UPYTHON_BUILD_PATH/firmware.uf2 && picotool reboot && sleep 2; mpremote run py/demo.py
```

# TODO

- main board schematic
- power LED

## software

- serial user interface

## peripherals

- place level shifter

## audio

- place buzzer

## display

- display module

## LED

- LED module schematic

## power

- place 3.3 V/5 V power supply
- Schottky diode/MOSFET for Pico external power


# ideas

- continuity/resistance check
- current/voltage sensor
- microphone sensor
- battery tester
- cable tester
- cable speed tester
- cable data transfer speed tester
