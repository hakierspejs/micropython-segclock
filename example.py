import framebuf
from segclock import Clock


def main():
    # fbuf = ssd1306.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c)
    screen_width = 128
    screen_height = 32

    fbuf = framebuf.FrameBuffer(
        bytearray(screen_width*screen_height//8),  # 1 bit per pixel
        screen_width,
        screen_height,
        framebuf.MONO_HLSB
    )

    clock = Clock(
        fbuf,
        screen_width,
        screen_height,
        offset_x=1,
        offset_y=1,
        scale_x=3,
        scale_y=3,
    )

    clock.draw(3, 14)


if __name__ == "__main__":
    main()
