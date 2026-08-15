import time
import threading
from typing import IO
import uuid
from enum import Enum
from dataclasses import dataclass

from pynput import mouse, keyboard

m_controller = mouse.Controller()
k_controller = keyboard.Controller()

class MacroStepType(Enum):
    BLANK = 0
    MOUSE = 1
    KEYBOARD = 2

IOIdentifier = mouse.Button | keyboard.Key | keyboard.KeyCode | str | None

@dataclass
class MacroStep:
    output_id: IOIdentifier
    output_mode: bool = True
    duration: int = 0

class MacroProfile:
    uid: str
    steps: list[MacroStep]
    repeat_count: int

    _running_event: threading.Event
    _thread: threading.Thread | None

    def __init__(self, uid: str) -> None:
        self.uid = uid
        self.steps = []
        self.repeat_count = 1
        self._running_event = threading.Event()
        self._thread = None

    def _run_loop(self) -> None:
        repeat_num = 0

        while repeat_num < self.repeat_count and self._running_event.is_set():
            for step in self.steps:
                if not self._running_event.is_set():
                    break

                if step.output_id is None:
                    pass
                elif type(step.output_id) == mouse.Button:
                    if step.output_mode:
                        m_controller.press(step.output_id)
                    else:
                        m_controller.release(step.output_id)
                else:
                    if step.output_mode:
                        k_controller.press(step.output_id)
                    else:
                        k_controller.release(step.output_id)

                if step.duration > 0:
                    time.sleep(step.duration / 1000)

            repeat_num += 1

    def run(self) -> None:
        self._running_event.set()

        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running_event.clear()

        if self._thread and self._thread.is_alive():
            self._thread.join()

class ProfileBindMode(Enum):
    TOGGLE = 0
    HOLD = 1
    START_STOP = 2

@dataclass
class ProfileBind:
    uid: str
    mode: ProfileBindMode
    start_keys: set[IOIdentifier]
    stop_keys: set[IOIdentifier] | None = None

class MacroManager:
    profiles: dict[str, MacroProfile]

    _active_input: set[IOIdentifier]

    def __init__(self) -> None:
        self.profiles = {}
        self._active_input = set()

        def on_press(key: keyboard.Key | keyboard.KeyCode | None) -> None:
            self.handle_input(key, True)

        def on_release(key: keyboard.Key | keyboard.KeyCode | None) -> None:
            self.handle_input(key, False)

        def on_click(x: int, y: int, button: mouse.Button, pressed: bool) -> None:
            self.handle_input(button, pressed)

        m_listener = mouse.Listener(on_click=on_click)
        k_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

        m_listener.start()
        k_listener.start()

    def handle_input(self, input_id: IOIdentifier, input_mode: bool) -> None:
        if input_id is None:
            return

        if input_mode:
            self._active_input.add(input_id)
        else:
            self._active_input.remove(input_id)



    def create_profile(self) -> MacroProfile:
        uid = str(uuid.uuid4())

        while uid in self.profiles:
            uid = str(uuid.uuid4())

        profile = MacroProfile(uid)
        self.profiles[uid] = profile

        return profile

    def delete_profile(self, uid: str) -> None:
        if uid in self.profiles:
            del self.profiles[uid]
