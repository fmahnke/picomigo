import sys
import time


def main():
    while True:
        _ = sys.stdout.write('t')
        _ = sys.stdout.write('\r\n')

        ch = sys.stdin.read(1)

        print(f'ch={ch}')

        if ch == 'q':
            sys.exit()

        time.sleep(1)


main()
