import time

import machine
import vl53l0x

# Initialize I2C bus and sensor.
i2c = machine.I2C(0, scl=5, sda=4, freq=400000)

print(f'i2c: {i2c}')

vl53 = vl53l0x.VL53L0X(i2c)

# Optionally set the timing budget. A timing budget of 20 milliseconds
# results in faster but less accurate measurements.
# For more accuracy set the timing budget to 200 milliseconds.
# The default is around 33 milliseconds.
# vl53.measurement_timing_budget = 20000  # microseconds
vl53.measurement_timing_budget = 200000  # microseconds

# Optionally start continuous measurement mode.
vl53.start_continuous()

while True:
    print("Range: {0}mm".format(vl53.range))
    time.sleep(0.1)
