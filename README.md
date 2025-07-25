# build and install

## native modules

### sound module

```
cd pico-native/modules/sound

./do_build_module

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
