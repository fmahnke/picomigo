import re
from subprocess import PIPE
from typing import cast

from mktech import subprocess
from mktech.error import Err, Ok
from mktech.log import log
from mktech.os import ensure_dir, environ, working_directory
from mktech.path import Path
from mktech.subprocess import Capture, run


def main(path: Path | None, verbose: int) -> None:
    if path is None:
        path = working_directory()

    files = path.rglob('*')

    cpp_files = list(filter(lambda x: x.suffix in ['.cpp', '.c', '.h'], files))

    excludes = [
        'src/rp2/snd_drum.h',
        'src/rp2/snd_synth_loop.h',
    ]

    cpp_files = list(filter(lambda x: str(x) not in excludes, cpp_files))

    print(f'checking {len(cpp_files)} files')

    if verbose > 0:
        print('\n'.join([str(it) for it in cpp_files]))

    for it in cpp_files:
        _clangd_check(it)


def _clangd_check(path: Path) -> None:
    build_dir = Path(environ('BUILD_DIR'))

    output_dir = build_dir / 'clang'

    match ensure_dir(output_dir):
        case Err(_):
            raise NotImplementedError
        case Ok(_):
            pass

    out_name = str(path).replace('/', '-')

    print(f'clangd check {path} -> {out_name}')

    stderr = Capture()

    args = (
        '--enable-config'
        """ --query-driver='/usr/bin/arm-none-eabi-*,/usr/bin/gcc*,/usr/bin/g++*'"""
    )

    result = run(f'clangd {args} --check={path}', stderr=stderr)

    output = cast(str, stderr.text)

    assert isinstance(output, str)

    _ = Path(output_dir / out_name).write_text(output)

    _errors(path, output)


def _errors(path: Path, output: str) -> None:
    lines = output.split('\n')

    for it in lines:
        match = re.search('Line', it)

        if match is None:
            match = re.search('compilation database', it)

        if match is not None:
            log.debug(match)

            print(f'{path}: {it}')
