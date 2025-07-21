import sys

import pico
from pico import logger
from pico.logger import log


async def main():
    print('\nlevel: default (DEBUG)\n')

    log.debug('message 1')
    log.info('message 2')
    log.warning('message 3')
    log.error('message 4')

    log.add(level=logger.DEBUG)

    print('\nlevel: DEBUG\n')

    log.debug('message 5')
    log.info('message 6')
    log.warning('message 7')
    log.error('message 8')

    log.add(level=logger.INFO)

    print('\nlevel: INFO\n')

    log.debug('message x')
    log.info('message 9')
    log.warning('message 10')
    log.error('message 11')

    log.add(level=logger.WARNING)

    print('\nlevel: WARNING\n')

    log.debug('message x')
    log.info('message x')
    log.warning('message 12')
    log.error('message 13')

    log.add(level=logger.ERROR)

    print('\nlevel: ERROR\n')

    log.debug('message x')
    log.info('message x')
    log.warning('message x')
    log.error('message 14')

    sys.exit()


pico.run(main)
