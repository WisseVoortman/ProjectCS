class STATE:
    STOPPED = 0
    RUNNING = 1


class COMMANDS:
    ACK = 0
    SEND_TEMP = 1
    SEND_LIGHT = 2
    SET_LIGHT = 3
    SET_AUTO = 4
    SET_MAN = 5
    ROLL_OUT = 6
    ROLL_IN = 7
    SET_TEMP = 8

    NOP = 127


class COLORS:
    GRAY = 90
    RED = 31
    LIME = 92
    YELLOW = 93
    BLUE = 94
    PINK = 95
    CYAN = 96
    BLACK = 97
    DEFAULT = 00


class TextStyle:
    DEFAULT = 0
    UNDERLINE = 4
    HIGHLIGHT = 7


def color(text, _color=COLORS.DEFAULT, style=TextStyle.DEFAULT):
    return '\033[{0};{1}m{2}\033[0;m'.format(style, _color, text)


DEBUG = True  # Enable debug, Implement manually
