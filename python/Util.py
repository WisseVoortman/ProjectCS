class STATE:
    STOPPED = bin(0)


class COMMANDS:
    ACK = bin(0)


class TextColors:
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36
    WHITE = 37


class BackgroundColors:
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    PURPLE = 45
    CYAN = 46
    WHITE = 47


# Might not be supported by all terminals
class TextStyles:
    NO_EFFECT = 0
    BOLD = 1
    UNDERLINE = 2
    NEGATIVE1 = 3
    NEGATIVE2 = 5


def color(text, text_color=TextColors.WHITE, background_color=BackgroundColors.BLACK, style=TextStyles.NO_EFFECT):
    return '\033[{0};{1};{2}m {3}\033[00m'.format(style, text_color, background_color, text)


DEBUG = True  # Enable debug, Implement manually
