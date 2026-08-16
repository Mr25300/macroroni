import time
import threading
import uuid
from enum import Enum
from dataclasses import dataclass

from pynput import mouse, keyboard

m_controller = mouse.Controller()
k_controller = keyboard.Controller()

IOIdentifier = mouse.Button | keyboard.Key | keyboard.KeyCode | None

@dataclass
class MacroStep:
    output_id: IOIdentifier
    output_mode: bool = True
    duration: int = 0

class TriggerMode(Enum):
    TOGGLE = 0
    HOLD = 1

@dataclass
class ProfileTrigger:
    inputs: set[IOIdentifier]
    mode: TriggerMode

class MacroProfile:
    uid: str
    steps: list[MacroStep]
    repeat_count: int
    trigger: ProfileTrigger | None

    _running_event: threading.Event
    _thread: threading.Thread | None

    def __init__(self, uid: str) -> None:
        self.uid = uid
        self.steps = []
        self.repeat_count = -1
        self.trigger = None

        self._active = False
        self._running_event = threading.Event()
        self._thread = None

    def _run_loop(self) -> None:
        repeat_num = 0
        m_active: set[mouse.Button] = set()
        k_active: set[keyboard.Key | keyboard.KeyCode] = set()

        while self._running_event.is_set():
            if self.repeat_count > 0 and repeat_num >= self.repeat_count:
                break

            for step in self.steps:
                if not self._running_event.is_set():
                    break

                if step.output_id is None:
                    pass
                elif type(step.output_id) == mouse.Button:
                    if step.output_mode:
                        m_active.add(step.output_id)
                        m_controller.press(step.output_id)
                    else:
                        m_active.remove(step.output_id)
                        m_controller.release(step.output_id)
                else:
                    if step.output_mode:
                        k_active.add(step.output_id)
                        k_controller.press(step.output_id)
                    else:
                        k_active.remove(step.output_id)
                        k_controller.release(step.output_id)

                if step.duration > 0:
                    time.sleep(step.duration / 1000)

            repeat_num += 1

        for k_id in m_active:
            m_controller.release(k_id)

        for k_id in k_active:
            k_controller.release(k_id)

        self._running_event.clear()

    def run(self) -> None:
        if self._running_event.is_set():
            return

        self._running_event.set()

        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if not self._running_event.is_set():
            return

        self._running_event.clear()

        if self._thread and self._thread.is_alive():
            self._thread.join()

    def toggle(self) -> None:
        if self._running_event.is_set():
            self.stop()
        else:
            self.run()

class MacroManager:
    profiles: dict[str, MacroProfile]

    _active_inputs: set[IOIdentifier]

    def __init__(self) -> None:
        self.profiles = {}

        self._active_inputs = set()

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

        first_press = input_mode and input_id not in self._active_inputs

        if input_mode:
            self._active_inputs.add(input_id)
        elif input_id in self._active_inputs:
            self._active_inputs.remove(input_id)

        for profile in self.profiles.values():
            if profile.trigger is None:
                continue

            trig_inputs = profile.trigger.inputs
            trig_mode = profile.trigger.mode

            if trig_mode == TriggerMode.TOGGLE:
                if first_press and input_id in trig_inputs and trig_inputs.issubset(self._active_inputs):
                    profile.toggle()
            else:
                if trig_inputs.issubset(self._active_inputs):
                    profile.run()
                else:
                    profile.stop()

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
