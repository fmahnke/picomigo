from mktech import subprocess


def build() -> None:
    subprocess.run('mpremote soft-reset')

    subprocess.run('./bin/build')
