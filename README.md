# Pinout

| #  |     GP |  i2c |  SPI | UART |  ADC | Description    | Use |
| -- | ------ | ---- | ---- | ---- | ---- | -------------- | --- |
|  1 |    GP0 | SDA0 |  RX0 |  TX0 | ---- |                |     |
|  2 |    GP1 | SCL0 | CSn0 |  RX0 | ---- |                |     |
|  3 |    GND | ---- | ---- | ---- | ---- |                |     |
|  4 |    GP2 | SDA1 | SCK0 | ---- | ---- |                |     |
|  5 |    GP3 | SCL1 |  TX0 | ---- | ---- |                |     |
|  6 |    GP4 | SDA0 |  RX0 |  TX1 | ---- |                |     |
|  7 |    GP5 | SDL0 | CSn0 |  RX1 | ---- |                |     |
|  8 |    GND | ---- | ---- | ---- | ---- |                |     |
|  9 |    GP6 | SDA1 | SCK0 | ---- | ---- |                |     |
| 10 |    GP7 | SCL1 |  TX0 | ---- | ---- |                |     |
| 11 |    GP8 | SDA0 |  RX1 |  TX1 | ---- |                |     |
| 12 |    GP9 | SCL0 | CSn1 |  RX1 | ---- |                |     |
| 13 |    GND | ---- | ---- | ---- | ---- |                |     |
| 14 |   GP10 | SDA1 | SCK1 | ---- | ---- |                |     |
| 15 |   GP11 | SCL1 |  TX1 | ---- | ---- |                |     |
| 16 |   GP12 | SDA0 |  RX1 |  TX0 | ---- |                |     |
| 17 |   GP13 | SCL0 | CSn1 |  RX0 | ---- |                |     |
| 18 |    GND | ---- | ---- | ---- | ---- |                |     |
| 19 |   GP14 | SDA1 | SCK1 | ---- | ---- | Push button 1  |  GP |
| 20 |   GP15 | SCL1 |  TX1 | ---- | ---- | Push button 0  |  GP |
| 21 |   GP16 | SDA0 |  RX0 |  TX0 | ---- |                |     |
| 22 |   GP17 | SCL0 | CSn0 |  RX0 | ---- | Encoder out 1  |  GP |
| 23 |    GND | ---- | ---- | ---- | ---- |                |     |
| 24 |   GP18 | SDA1 | SCK0 | ---- | ---- | Encoder out 0  |  GP |
| 25 |   GP19 | SCL1 |  TX0 | ---- | ---- | Encoder button |  GP |
| 26 |   GP20 | SDA0 | ---- | ---- | ---- |                |     |
| 27 |   GP21 | SCL0 | ---- | ---- | ---- |                |     |
| 28 |    GND | ---- | ---- | ---- | ---- |                |     |
| 29 |   GP22 | ---- | ---- | ---- | ---- |                |     |
| 30 |    RUN | ---- | ---- | ---- | ---- |                |     |
| 31 |   GP26 | SDA1 | ---- | ---- | ADC0 | Potentiometer  | ADC |
| 32 |   GP27 | SCL1 | ---- | ---- | ADC1 |                |     |
| 33 |    GND | ---- | ---- | ---- | AGND |                |     |
| 34 |   GP28 | ---- | ---- | ---- | ADC2 |                |     |
| 35 |    --- | ---- | ---- | ---- | VREF |                |     |
| 36 |    3V3 | ---- | ---- | ---- | ---- |                |     |
| 37 | 3V3_EN | ---- | ---- | ---- | ---- |                |     |
| 38 |    GND | ---- | ---- | ---- | ---- |                |     |
| 39 |   VSYS | ---- | ---- | ---- | ---- |                |     |
| 40 |   VBUS | ---- | ---- | ---- | ---- |                |     |

# setup development environment

## sync python environment

```
cd picomigo-py
uv sync
```

## prepare micropython

```
cd $UPYTHON_PATH/mpy-cross
make
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
