# MIT License
#
# Copyright (c) 2023 Alex Ostrowski 
# Copyright (c) 2023 Stowarzyszenie Hakierspejs Łódź; hs-ldz.pl
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# SEGMENTS:
#     0
#   1   2
#     3
#   4   5
#     6
SEGMENT_0 = ((0, 0, 5, 1),)

SEGMENT_1 = ((0, 0, 1, 5),)

SEGMENT_2 = ((4, 0, 5, 5),)

SEGMENT_3 = ((0, 4, 5, 5),)

SEGMENT_4 = ((0, 4, 1, 9),)

SEGMENT_5 = ((4, 4, 5, 9),)

SEGMENT_6 = ((0, 8, 5, 9),)

DIGIT_0 = (
    SEGMENT_0,
    SEGMENT_1,
    SEGMENT_2,
    SEGMENT_4,
    SEGMENT_5,
    SEGMENT_6,
)

DIGIT_1 = (
    SEGMENT_2,
    SEGMENT_5,
)


DIGIT_2 = (
    SEGMENT_0,
    SEGMENT_2,
    SEGMENT_3,
    SEGMENT_4,
    SEGMENT_6,
)


DIGIT_3 = (
    SEGMENT_0,
    SEGMENT_2,
    SEGMENT_3,
    SEGMENT_5,
    SEGMENT_6,
)


DIGIT_4 = (
    SEGMENT_1,
    SEGMENT_2,
    SEGMENT_3,
    SEGMENT_5,
)


DIGIT_5 = (
    SEGMENT_0,
    SEGMENT_1,
    SEGMENT_3,
    SEGMENT_5,
    SEGMENT_6,
)


DIGIT_6 = (
    SEGMENT_0,
    SEGMENT_1,
    SEGMENT_3,
    SEGMENT_4,
    SEGMENT_5,
    SEGMENT_6,
)

DIGIT_7 = (
    SEGMENT_0,
    SEGMENT_2,
    SEGMENT_5,
)

DIGIT_8 = (
    SEGMENT_0,
    SEGMENT_1,
    SEGMENT_2,
    SEGMENT_3,
    SEGMENT_4,
    SEGMENT_5,
    SEGMENT_6,
)

DIGIT_9 = (
    SEGMENT_0,
    SEGMENT_1,
    SEGMENT_2,
    SEGMENT_3,
    SEGMENT_5,
    SEGMENT_6,
)

COLON = (
    ((0, 2, 1, 3),),
    ((0, 6, 1, 7),),
)

DIGITS = (
    DIGIT_0,
    DIGIT_1,
    DIGIT_2,
    DIGIT_3,
    DIGIT_4,
    DIGIT_5,
    DIGIT_6,
    DIGIT_7,
    DIGIT_8,
    DIGIT_9,
)

MIN_HEIGHT = 10  # px
MIN_WIDTH = (6 + 2) * 4 + 2 *3 - 2 # px


class Clock:
    class TooSmallDimensionsException(Exception):
        pass

    def __init__(
        self,
        fbuf,
        width,
        height,
        font_color=0b1,
        back_color=0b0,
        offset_x=0,
        offset_y=0,
        scale_x=1,
        scale_y=1,
    ):
        self.fbuf = fbuf
        self.width = width
        self.height = height
        if self.height < MIN_HEIGHT or self.width < MIN_WIDTH:
            message = (
                "Too small dimensions. "
                "Minimal width: {min_width}px, minimal height: {min_height}px".format(
                    min_width=MIN_WIDTH,
                    min_height=MIN_HEIGHT,
                )
            )
            raise self.TooSmallDimensionsException(message)
        self._state = (-1,) * 5
        self.font_color = font_color
        self.back_color = back_color
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.scale_x = scale_x
        self.scale_y = scale_y

        pen_width = 2 * self.scale_x  # px
        digit_width = 6 * self.scale_x  # px

        self.position_0 = offset_x # 0
        self.position_1 = offset_x + 1 * (digit_width + pen_width)
        self.position_2 = offset_x + 2 * (digit_width + pen_width)
        self.position_3 = offset_x + 2 * (digit_width + pen_width) + pen_width * 2
        self.position_4 = self.position_3 + digit_width + pen_width

    def _draw_digit(self, digit, position, color):
        x_crutch = 0
        for segment in digit:
            for rect in segment:
                x1, y1, x2, y2 = rect
                w = int(self.scale_x * (x2 - x1 + 1))
                h = int(self.scale_y * (y2 - y1 + 1))
                x = int(self.scale_x * x1) + position + self.offset_x
                y = int(self.scale_y * y1) + self.offset_y
                self.fbuf.rect(x, y, w, h, color, True)

    def draw(self, hour, minute, colon=True):
        current_state = (hour // 10, hour % 10, colon, minute // 10, minute % 10)

        if self._state[0] != current_state[0]:
            self._draw_digit(DIGITS[8], self.position_0, self.back_color)
            self._draw_digit(DIGITS[hour // 10], self.position_0, self.font_color)

        if self._state[1] != current_state[1]:
            self._draw_digit(DIGITS[8], self.position_1, self.back_color)
            self._draw_digit(DIGITS[hour % 10], self.position_1, self.font_color)

        if self._state[2] != current_state[2]:
            self._draw_digit(COLON, self.position_2, self.back_color)
            if colon:
                self._draw_digit(COLON, self.position_2, self.font_color)

        if self._state[3] != current_state[3]:
            self._draw_digit(DIGITS[8], self.position_3, self.back_color)
            self._draw_digit(DIGITS[minute // 10], self.position_3, self.font_color)

        if self._state[4] != current_state[4]:
            self._draw_digit(DIGITS[8], self.position_4, self.back_color)
            self._draw_digit(DIGITS[minute % 10], self.position_4, self.font_color)

        self._state = current_state
