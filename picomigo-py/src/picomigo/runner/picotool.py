from mktech import subprocess
from mktech.error import Err, Error, Ok, Result
from mktech.log import log


def load(args: str) -> Result[None, Error]:
    log.debug('test')

    result = subprocess.run(f'picotool load {args}')

    if result.exit_code != 0:
        return Err(Error('TODO'))

    return Ok(None)


def reboot(args: str = '') -> Result[None, Error]:
    result = subprocess.run(f'picotool reboot {args}')

    if result.exit_code != 0:
        return Err(Error('TODO'))

    return Ok(None)
