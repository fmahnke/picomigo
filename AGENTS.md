# Repository Guidelines

## Project Structure & Module Organization
- `picomigo-py/`: MicroPython/Python library, CLI entrypoint, and examples
  (`src/picomigo/examples/`); tests live in `tests/`.
- `picomigo-native/`: C/CMake native modules for Pico; `modules/sound/`
  contains the sound driver; `_build/` holds build artifacts.
- `doc/`: Pinouts and written design notes. Hardware CAD lives in `kicad/` and
  `diylc/`.
- `container/`, `data/`, `Dockerfile*`: Packaging and container setup; avoid
  editing unless you are changing build images.

## Build, Test, and Development Commands
- Python env: `cd picomigo-py && uv sync` to install deps for Python ≥3.12.
- Lint: `uv run nox -s lint` (flake8 over `src` and `tests`).
- Type check: `uv run nox -s typing` (basedpyright).
- Tests + coverage: `uv run nox -s tests` (pytest via coverage; combines
  parallel data).
- Run an example on hardware:
  `uv run mpremote run src/picomigo/examples/led.py`.
- Copy library to board: `uv run rshell -f rshell_build`.
- Build all native modules: `cd picomigo-native && ./build_all`
  (`CLEAN=1 ./build_all` for a fresh build).
- Build sound module only:
  `cd picomigo-native/modules/sound && ./do_build sound`;
  flash demo: `./do_build sound_install`.
- Prepare MicroPython toolchain (if needed):
  `cd $UPYTHON_PATH/mpy-cross && make`.

## Coding Style & Naming Conventions
- C/CMake: mirror Pico SDK style; keep `CMakeLists.txt` minimal and prefer
  `static inline` helpers over macros. Do not version `_build/` outputs.

## Testing Guidelines
- Hardware-impacting changes: include or update an example and document
  required wiring; avoid CI-only tests that need a board.

## Commit & Pull Request Guidelines
- Commit subjects follow `scope: message` (e.g., `doc: add pinout`,
  `typing: lint/types`), imperative, ≤72 chars.
- PRs: describe intent and behavior change, link issues, and list commands
  executed (`nox -s lint typing tests`). Attach screenshots or serial logs for
  firmware/UI changes.
- Keep generated artifacts out of git (`_build/`, `.coverage*`, UF2 binaries);
- vendored `lib/` edits require justification in the PR notes.

## Hardware & Flashing Notes
- Target hardware: Raspberry Pi Pico / Pico W (MicroPython). Test on physical
  boards before merging firmware-related changes.
- Target boards: Raspberry Pi Pico / Pico W. Ensure serial permissions before
  running `picotool`, `mpremote`, or `rshell`.
- Flash UF2 images with `picotool load -f <uf2> && picotool reboot`; wait a
  couple of seconds before running examples. Document pin usage changes in PRs
  that affect wiring.
- USB tools required: `mpremote` and `rshell` (installed via project
  dependencies). If on macOS/Linux, ensure you have serial permissions before
  flashing.
