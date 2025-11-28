import time

import umsgpack


def main() -> None:
    while True:
        print('tick')

        # obj = [1, 2, 3.14159]
        # s = umsgpack.dumps(obj)  # s is a bytes object
        # print(umsgpack.loads(s))  # Outcome [1, 2, 3.14159]

        time.sleep(1.0)


main()
