# picomigo

## Copy library to board

```bash
rshell -f rshell_build
```

## Run examples

```bash
mpremote run src/picomigo/examples/<example>.py
```

## Run main

```bash
mpremote exec 'import main'
```

## Test

src/picomigo/examples/input.py
src/picomigo/pico/pico/modules/display/st7789/examples/scroll.py
src/picomigo/examples/led2.py

src/picomigo/examples/led.py
src/picomigo/examples/potentiometer.py
src/picomigo/examples/rotary_encoder.py
src/picomigo/pico/pico/modules/display/ssd1306/examples/hello.py

## Development

Install with `pdm`:

```bash
pdm install
```
