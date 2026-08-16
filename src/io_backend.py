from typing import Callable
from abc import ABC, abstractmethod
from enum import Enum, auto

class IOId(Enum):
    KEY_LSHIFT = auto()
    KEY_RSHIFT = auto()
    KEY_LCTRL = auto()
    KEY_RCTRL = auto()
    KEY_LALT = auto()
    KEY_RALT = auto()
    KEY_LMETA = auto()
    KEY_RMETA = auto()

    KEY_A = "a"
    KEY_B = "b"
    KEY_C = "c"
    KEY_D = "d"
    KEY_E = "e"
    KEY_F = "f"
    KEY_G = "g"
    KEY_H = "h"
    KEY_I = "i"
    KEY_J = "j"
    KEY_K = "k"
    KEY_L = "l"
    KEY_M = "m"
    KEY_N = "n"
    KEY_O = "o"
    KEY_P = "p"
    KEY_Q = "q"
    KEY_R = "r"
    KEY_S = "s"
    KEY_T = "t"
    KEY_U = "u"
    KEY_V = "v"
    KEY_W = "w"
    KEY_X = "x"
    KEY_Y = "y"
    KEY_Z = "z"

    KEY_0 = "0"
    KEY_1 = "1"
    KEY_2 = "2"
    KEY_3 = "3"
    KEY_4 = "4"
    KEY_5 = "5"
    KEY_6 = "6"
    KEY_7 = "7"
    KEY_8 = "8"
    KEY_9 = "9"

    KEY_GRAVE = "`"
    KEY_MINUS = "-"
    KEY_EQUAL = "="
    KEY_BACKSPACE = auto()
    KEY_TAB = auto()
    KEY_CAPSLOCK = auto()

    KEY_LEFTBRACE = "["
    KEY_RIGHTBRACE = "]"
    KEY_BACKSLASH = "\\"
    KEY_SEMICOLON = ";"
    KEY_APOSTROPHE = "'"
    KEY_ENTER = auto()

    KEY_COMMA = ","
    KEY_DOT = "."
    KEY_SLASH = "/"
    KEY_SPACE = auto()

    KEY_INSERT = auto()
    KEY_DELETE = auto()
    KEY_HOME = auto()
    KEY_END = auto()
    KEY_PAGEUP = auto()
    KEY_PAGEDOWN = auto()

    KEY_UP = auto()
    KEY_DOWN = auto()
    KEY_LEFT = auto()
    KEY_RIGHT = auto()

    KEY_ESC = auto()
    KEY_PRINT_SCREEN = auto()
    KEY_SCROLL_LOCK = auto()
    KEY_PAUSE = auto()

    KEY_F1 = auto()
    KEY_F2 = auto()
    KEY_F3 = auto()
    KEY_F4 = auto()
    KEY_F5 = auto()
    KEY_F6 = auto()
    KEY_F7 = auto()
    KEY_F8 = auto()
    KEY_F9 = auto()
    KEY_F10 = auto()
    KEY_F11 = auto()
    KEY_F12 = auto()
    KEY_F13 = auto()
    KEY_F14 = auto()
    KEY_F15 = auto()
    KEY_F16 = auto()
    KEY_F17 = auto()
    KEY_F18 = auto()
    KEY_F19 = auto()
    KEY_F20 = auto()

    KEY_KP_NUMLOCK = auto()
    KEY_KP_SLASH = "/"
    KEY_KP_ASTERISK = "*"
    KEY_KP_MINUS = "-"
    KEY_KP_PLUS = "+"
    KEY_KP_ENTER = auto()
    KEY_KP_DOT = "."

    KEY_KP_0 = "0"
    KEY_KP_1 = "1"
    KEY_KP_2 = "2"
    KEY_KP_3 = "3"
    KEY_KP_4 = "4"
    KEY_KP_5 = "5"
    KEY_KP_6 = "6"
    KEY_KP_7 = "7"
    KEY_KP_8 = "8"
    KEY_KP_9 = "9"

    KEY_VOLUME_MUTE = auto()
    KEY_VOLUME_DOWN = auto()
    KEY_VOLUME_UP = auto()
    KEY_MEDIA_NEXT = auto()
    KEY_MEDIA_PREV = auto()
    KEY_MEDIA_STOP = auto()
    KEY_MEDIA_PLAY_PAUSE = auto()

    MOUSE_LEFT = auto()
    MOUSE_RIGHT = auto()
    MOUSE_MIDDLE = auto()
    MOUSE_X1 = auto()
    MOUSE_X2 = auto()

    MOUSE_SCROLL_UP = auto()
    MOUSE_SCROLL_DOWN = auto()
    MOUSE_SCROLL_LEFT = auto()
    MOUSE_SCROLL_RIGHT = auto()

class IOBackend(ABC):
    @abstractmethod
    def press(self, out_id: IOId) -> None:
        pass

    @abstractmethod
    def release(self, out_id: IOId) -> None:
        pass

    @abstractmethod
    def listen(self, callback: Callable[[IOId, bool], None]) -> None:
        pass
