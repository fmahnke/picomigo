import os
import sys
from unittest.discover import discover_main

import tests

tmod = __import__('tests')
print(dir(tmod))

print(tmod)
print(tmod.__path__)

tests_path = tests.__path__

assert isinstance(tests_path, str)

tests_files = os.listdir(tests_path)

test_paths = list(
    filter(lambda x: x.startswith('test_') and x.endswith('.py'), tests_files)
)

test_modules = [f"tests.{it.split('.py')[0]}" for it in test_paths]

# unittest.__main__ expects to be called from command line, so add an extra
# argument to fake it.

sys.argv.append('')
sys.argv.extend(test_modules)

discover_main()
