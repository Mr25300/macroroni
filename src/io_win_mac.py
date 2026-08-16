from typing import cast, Callable

from pynput import mouse, keyboard

from io_backend import IOBackend, IOId

PYNPUT_MAP = {
    IOId.KEY_LSHIFT: keyboard.Key.shift_l,
    IOId.KEY_RSHIFT: keyboard.Key.shift_r,
    IOId.KEY_LCTRL: keyboard.Key.ctrl_l,
    IOId.KEY_RCTRL: keyboard.Key.ctrl_r,
    IOId.KEY_LALT: keyboard.Key.alt_l,
    IOId.KEY_RALT: keyboard.Key.alt_r,
    IOId.KEY_LMETA: keyboard.Key.cmd_l,
    IOId.KEY_RMETA: keyboard.Key.cmd_r,

    IOId.KEY_BACKSPACE: keyboard.Key.backspace,
    IOId.KEY_TAB: keyboard.Key.tab,
    IOId.KEY_CAPSLOCK: keyboard.Key.caps_lock,
    IOId.KEY_ENTER: keyboard.Key.enter,
    IOId.KEY_KP_ENTER: keyboard.Key.enter,
    IOId.KEY_KP_NUMLOCK: keyboard.Key.num_lock,
    IOId.KEY_SPACE: keyboard.Key.space,

    IOId.KEY_INSERT: keyboard.Key.insert,
    IOId.KEY_DELETE: keyboard.Key.delete,
    IOId.KEY_HOME: keyboard.Key.home,
    IOId.KEY_END: keyboard.Key.end,
    IOId.KEY_PAGEUP: keyboard.Key.page_up,
    IOId.KEY_PAGEDOWN: keyboard.Key.page_down,

    IOId.KEY_UP: keyboard.Key.up,
    IOId.KEY_DOWN: keyboard.Key.down,
    IOId.KEY_LEFT: keyboard.Key.left,
    IOId.KEY_RIGHT: keyboard.Key.right,

    IOId.KEY_ESC: keyboard.Key.esc,
    IOId.KEY_PRINT_SCREEN: keyboard.Key.print_screen,
    IOId.KEY_SCROLL_LOCK: keyboard.Key.scroll_lock,
    IOId.KEY_PAUSE: keyboard.Key.pause,

    IOId.KEY_F1: keyboard.Key.f1,
    IOId.KEY_F2: keyboard.Key.f2,
    IOId.KEY_F3: keyboard.Key.f3,
    IOId.KEY_F4: keyboard.Key.f4,
    IOId.KEY_F5: keyboard.Key.f5,
    IOId.KEY_F6: keyboard.Key.f6,
    IOId.KEY_F7: keyboard.Key.f7,
    IOId.KEY_F8: keyboard.Key.f8,
    IOId.KEY_F9: keyboard.Key.f9,
    IOId.KEY_F10: keyboard.Key.f10,
    IOId.KEY_F11: keyboard.Key.f11,
    IOId.KEY_F12: keyboard.Key.f12,
    IOId.KEY_F13: keyboard.Key.f13,
    IOId.KEY_F14: keyboard.Key.f14,
    IOId.KEY_F15: keyboard.Key.f15,
    IOId.KEY_F16: keyboard.Key.f16,
    IOId.KEY_F17: keyboard.Key.f17,
    IOId.KEY_F18: keyboard.Key.f18,
    IOId.KEY_F19: keyboard.Key.f19,
    IOId.KEY_F20: keyboard.Key.f20,

    IOId.KEY_VOLUME_MUTE: keyboard.Key.media_volume_mute,
    IOId.KEY_VOLUME_DOWN: keyboard.Key.media_volume_down,
    IOId.KEY_VOLUME_UP: keyboard.Key.media_volume_up,
    IOId.KEY_MEDIA_NEXT: keyboard.Key.media_next,
    IOId.KEY_MEDIA_PREV: keyboard.Key.media_previous,
    IOId.KEY_MEDIA_STOP: keyboard.Key.media_stop,
    IOId.KEY_MEDIA_PLAY_PAUSE: keyboard.Key.media_play_pause,

    IOId.MOUSE_LEFT: mouse.Button.left,
    IOId.MOUSE_RIGHT: mouse.Button.right,
    IOId.MOUSE_MIDDLE: mouse.Button.middle,
    IOId.MOUSE_X1: mouse.Button.button8,
    IOId.MOUSE_X2: mouse.Button.button9
}

PYNPUT_MAP_INV = {PYNPUT_MAP[key]: key for key in PYNPUT_MAP}
PYNPUT_CHAR_MAP_INV: dict[str, IOId] = {member.value: member for member in IOId if type(member.value) == str}

def toPynput(io_id: IOId) -> mouse.Button | keyboard.Key | keyboard.KeyCode:
    if io_id in PYNPUT_MAP:
        return PYNPUT_MAP[io_id]
    else:
        return keyboard.KeyCode.from_char(cast(str, io_id.value))

def fromPynput(pynput_id: mouse.Button | keyboard.Key | keyboard.KeyCode) -> IOId:
    if type(pynput_id) == keyboard.KeyCode:
        return PYNPUT_CHAR_MAP_INV[cast(str, pynput_id.char)]
    else:
        return PYNPUT_MAP_INV[pynput_id]

class PynputBackend(IOBackend):
    m_controller: mouse.Controller
    k_controller: keyboard.Controller
    m_listener: mouse.Listener
    k_listener: keyboard.Listener

    def __init__(self) -> None:
        self.m_controller = mouse.Controller()
        self.k_controller = keyboard.Controller()
        self.m_listener = mouse.Listener()
        self.k_listener = keyboard.Listener()

    def press(self, out_id: IOId) -> None:
        pynput_id = toPynput(out_id)

        pass

    def release(self, out_id: IOId) -> None:
        pynput_id = toPynput(out_id)

        pass

    def listen(self, callback: Callable[[IOId, bool], None]) -> None:
        pass
