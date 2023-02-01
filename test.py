import framebuf
from segclock import Clock
import unittest


class SegClockTestCase(unittest.TestCase):

    @staticmethod
    def _bytes_to_bytearray(value):
        return bytearray(
            b''.join(map(
                lambda x: int.to_bytes(x, 1, 'big'), 
                value
            ))
        )

    def test__clock_initialization(self):
        fbuf = None  # mock
        clock = Clock(fbuf, 100, 100)

    def test__clock_init__too_small_screen__raise_exc(self):
        fbuf = None  # mock
        try:
            Clock(fbuf, 100, 100)
        except Exception as e:
            self.assertIsInstance(e, Clock.TooSmallDimensionsException)

    def test__clock_draw__minimal_dimentions__correct_clock_state_after_drawing(self):
        data = bytearray(40*10//8)
        fbuf = framebuf.FrameBuffer(data, 40, 10, framebuf.MONO_HLSB)
        clock = Clock(fbuf, 40, 10)
        clock.draw(13, 29)

        self.assertEqual(
            clock._state, 
            (1, 3, 1, 2, 9),
        )

    def test__clock_draw__minimal_dimentions__correct_fbuf_values(self):
        data = bytearray(40*10//8)
        fbuf = framebuf.FrameBuffer(data, 40, 10, framebuf.MONO_HLSB)
        clock = Clock(fbuf, 40, 10)
        clock.draw(88, 88)

        correct_result = self._bytes_to_bytearray((
            0b11111100, 0b11111100, 0b00001111, 0b11001111, 0b11000000,
            0b11111100, 0b11111100, 0b00001111, 0b11001111, 0b11000000,
            0b11001100, 0b11001100, 0b11001100, 0b11001100, 0b11000000,
            0b11001100, 0b11001100, 0b11001100, 0b11001100, 0b11000000,

            0b11111100, 0b11111100, 0b00001111, 0b11001111, 0b11000000,
            0b11111100, 0b11111100, 0b00001111, 0b11001111, 0b11000000,
            0b11001100, 0b11001100, 0b11001100, 0b11001100, 0b11000000,
            0b11001100, 0b11001100, 0b11001100, 0b11001100, 0b11000000,

            0b11111100, 0b11111100, 0b00001111, 0b11001111, 0b11000000,
            0b11111100, 0b11111100, 0b00001111, 0b11001111, 0b11000000,
        ))

        self.assertEqual(
            data, 
            correct_result,
        )

    def test__clock_draw__without_colon__correct_fbuf_values(self):
        data = bytearray(40*10//8)
        fbuf = framebuf.FrameBuffer(data, 40, 10, framebuf.MONO_HLSB)
        clock = Clock(fbuf, 40, 10)
        clock.draw(88, 88, False)

        correct_result = self._bytes_to_bytearray((
            0b11111100, 0b11111100, 0b00001111, 0b11001111, 0b11000000,
            0b11111100, 0b11111100, 0b00001111, 0b11001111, 0b11000000,
            0b11001100, 0b11001100, 0b00001100, 0b11001100, 0b11000000,
            0b11001100, 0b11001100, 0b00001100, 0b11001100, 0b11000000,

            0b11111100, 0b11111100, 0b00001111, 0b11001111, 0b11000000,
            0b11111100, 0b11111100, 0b00001111, 0b11001111, 0b11000000,
            0b11001100, 0b11001100, 0b00001100, 0b11001100, 0b11000000,
            0b11001100, 0b11001100, 0b00001100, 0b11001100, 0b11000000,

            0b11111100, 0b11111100, 0b00001111, 0b11001111, 0b11000000,
            0b11111100, 0b11111100, 0b00001111, 0b11001111, 0b11000000,
        ))

        self.assertEqual(
            data, 
            correct_result,
        )


if __name__ == '__main__':
    unittest.main()
