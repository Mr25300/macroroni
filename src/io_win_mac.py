from typing import cast, Callable

from pynput import mouse, keyboard

from io_backend import IOBackend, IOCallback

def pynput_to_id(pynput_id: mouse.Button | keyboard.Key | keyboard.KeyCode | None) -> str | None:
    if isinstance(pynput_id, mouse.Button):
        return f"m_{pynput_id.name}"
    elif isinstance(pynput_id, keyboard.Key):
        return f"k_{pynput_id.name}"
    elif isinstance(pynput_id, keyboard.KeyCode):
        if pynput_id.char is not None:
            return f"kc_{pynput_id.char}"
        elif pynput_id.vk is not None:
            return f"kv_{pynput_id.vk}"

    return None

def id_to_pynput(io_id: str | None) -> mouse.Button | keyboard.Key | keyboard.KeyCode | None:
    if io_id is None:
        return None

    if io_id.startswith("m_"):
        return getattr(mouse.Button, io_id.removeprefix("m_"))
    elif io_id.startswith("k_"):
        return getattr(keyboard.Key, io_id.removeprefix("k_"))
    elif io_id.startswith("kc_"):
        return keyboard.KeyCode.from_char(io_id.removeprefix("kc_"))
    elif io_id.startswith("kv_"):
        try:
            return keyboard.KeyCode.from_vk(int(io_id.removeprefix("kv_")))
        except Exception:
            pass

    return None

class IOWinMac(IOBackend):
    m_controller: mouse.Controller
    k_controller: keyboard.Controller
    m_listener: mouse.Listener
    k_listener: keyboard.Listener

    _callback: IOCallback | None

    def __init__(self) -> None:
        self.m_controller = mouse.Controller()
        self.k_controller = keyboard.Controller()

        def on_click(x: int, y: int, button: mouse.Button, pressed: bool) -> None:
            if self._callback is not None:
                self._callback(cast(str, pynput_to_id(button)), pressed)

        def on_press(key: keyboard.Key | keyboard.KeyCode | None) -> None:
            if self._callback is not None:
                out_id = pynput_to_id(key)

                print(out_id)

                if out_id is not None:
                    self._callback(out_id, True)

        def on_release(key: keyboard.Key | keyboard.KeyCode | None) -> None:
            if self._callback is not None:
                out_id = pynput_to_id(key)

                print(out_id)

                if out_id is not None:
                    self._callback(out_id, False)

        self.m_listener = mouse.Listener(on_click=on_click)
        self.k_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

        self.m_listener.start()
        self.k_listener.start()

        self._callback = None

    def press(self, out_id: str) -> None:
        pynput_id = id_to_pynput(out_id)

        if pynput_id is None:
            return

        if isinstance(pynput_id, mouse.Button):
            self.m_controller.press(pynput_id)
        else:
            self.k_controller.press(cast(keyboard.Key | keyboard.KeyCode, pynput_id))

    def release(self, out_id: str) -> None:
        pynput_id = id_to_pynput(out_id)

        if pynput_id is None:
            return

        if isinstance(pynput_id, mouse.Button):
            self.m_controller.release(pynput_id)
        else:
            self.k_controller.release(cast(keyboard.Key | keyboard.KeyCode, pynput_id))

    def listen(self, callback: IOCallback) -> None:
        self._callback = callback
