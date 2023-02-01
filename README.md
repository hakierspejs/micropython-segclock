# Micropython segment clock library

This library allows you to draw 7-segment digits clock on the given FrameBuffer.

Example of usage:
```python

from your_display_driver import Display
from frambuffer import FrameBuffer
from segclock import Clock

def main():
    fbuf = FrameFuffer()
    display = Display(fbuf)
    clock = Clock(
        fbuf,
        screen_width,
        screen_height,
    )

    clock.draw(3, 14)
    display.show()

```

Simple kitchen timer based on this library: https://github.com/hakierspejs/pico-ktimer
