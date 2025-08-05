# Programming Conventions

# Style

## Functional programming

Prefer comprehensions and functional tools with lambda expressions over
iterations with for loops.

## Strings

Prefer single quotes around all string literals.

Use double quotes around a string literal that contains another string literal.
Example: `f"--dry-run {'\n'.join(files)}"`

### Whitespace

### Line spacing

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

# Typing

- Fully type all functions and methods; add a type annotation to every
  parameter and return value.

# Comments

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

# Language

We use Python version >= 3.12. Do not use any deprecated types or features.
