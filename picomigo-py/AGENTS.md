# Repository Guidelines

## Project Structure & Module Organization
- `src/picomigo/`: Library code and CLI entrypoint (`picomigo.cli:main`);
  embedded-facing modules live under `src/picomigo/pico/`.
- `src/picomigo/examples/`: Ready-to-run MicroPython examples; invoke with
  `mpremote run src/picomigo/examples/<example>.py`.
- `tests/`: Pytest suite; add new files as `test_*.py`.
- `lib/`: Vendored MicroPython helpers; keep pristine unless upstreaming a fix.
- `rshell_build` & `_build*`: Scripts/artifacts used to copy firmware onto
  boards.

## Build, Test, and Development Commands
- Install deps once: `uv sync` (uses Python ≥3.13).
- Lint: `uv run nox -s lint` (flake8 over `src` and `tests`).
- Type check: `uv run nox -s typing` (basedpyright; mypy config is present but
- off in nox).
- Tests + coverage: `uv run nox -s tests` (pytest via coverage; combines
  parallel data).
- Flash/copy to board: `rshell -f rshell_build`.
- Run an example on a device: `mpremote run src/picomigo/examples/led.py`.
- Run main module quickly: `mpremote exec "import main"`.

## Coding Style & Naming Conventions
- Type everything (functions, methods, module globals); `mypy.ini` is `strict`
  and `pyrightconfig.json` is `recommended`.
- Keep module/class/function names lowercase_with_underscores; constants
  UPPER_SNAKE.
- Place a blank line after assignments or control blocks; avoid blank lines
  between `if/elif/else` branches.

## Testing Guidelines
- Framework: pytest; tests live in `tests/` and should be named
  `test_<feature>.py` with functions `test_*`.
- Fast feedback: run `uv run pytest tests/test_cli.py` when touching the CLI.
- Coverage: `nox -s tests` reports total coverage; keep or raise coverage when
  adding features. Parallel runs combine via `.coverage.*` files.
- Hardware-dependent examples should include a guard or be excluded from
  automated runs.

# Programming Conventions

## Style

### Functional programming

Prefer comprehensions and functional tools with lambda expressions over
iterations with for loops.

### Strings

Prefer single quotes around all string literals.

Use double quotes around a string literal that contains another string literal.
Example: `f"--dry-run {'\n'.join(files)}"`

### Whitespace

Keep lines to a maximum of 80 characters, including terminating newline.

#### Line spacing

- In general, leave one blank line between top level module statements or
  statements in a function or method.
  - Put a blank line after any control flow or loop statement.
  - Put a blank line after a variable declaration or assignment.
- Do not leave blank lines in between the arms of match statements
  or the branches of if/elif/else constructs.

Example:

```
def my_function(arg: ArgObject) -> Result[int, Error]:
    # There is a blank line in between this comment and the statement following
    # it. There's also a blank line between the next two statements.

    v = arg.v

    result = oper(v)

    # There's no blank line in between the match result and its case
    # statements.

    match result:
        case Err(e):
            # But there are blank lines between the statements within each of
            # the match arms.

            log.error(f'fatal error: {e}')

            return Err(Error(e))
        case Ok(v):
            log.info(f'success: {v}')

            return Ok(v)
```

## Typing

- Make all code satisfy `basedpyright` in `recommended` mode.
- Fully type all functions and methods; add a type annotation to every
  parameter and return value.
- Type all class attributes and class instance attributes.

## Comments

Use comments to express intent and rationale where necessary. Comments are
useful to clarify a failure to express these things clearly in the code itself.

- When possible, write self-documenting code that expresses to the reader what
  it does using descriptive names.
- When a piece of code is expressive enough on its own, don't add a comment
  that tells the reader what it does; that's redundant.
- When a piece of code doesn't clearly express what it does, then add a
  comment that explains it's function (but prefer refactoring the code to be
  self-documenting, if that's feasible).
- When it's not clear from the surrounding context *why* a piece of code is
  necessary, then add a comment explaining the rationale behind it.

## Language

We use Python version >= 3.13. Do not use any deprecated types or features.
