import asyncio

import pico


async def main():
    display = pico.display()

    # Texts to display
    texts = [
        "Hello, World!",
        "Mutex Firmware",
        "Raspberry Pi Pico",
        "MicroPython Rocks!"
    ]
    index = 0

    while True:
        # Clear the display
        display.fill(0)  # pyright: ignore[reportFunctionMemberAccess]

        # Display the current text
        display.text(  # pyright: ignore[reportFunctionMemberAccess]
            texts[index], 0, 0
        )
        display.show()  # pyright: ignore[reportFunctionMemberAccess]

        # Move to the next text
        index += 1
        if index >= len(texts):
            index = 0  # Reset to the first text after the last one

        # Wait for 1 second before updating the text
        await asyncio.sleep(1)


pico.run(main)
