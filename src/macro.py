import time
import threading
import uuid
from enum import Enum, auto
from dataclasses import dataclass

from io_backend import IOBackend

@dataclass
class MacroStep:
    output_info: list[tuple[str, bool]]
    duration: int = 0

class TriggerMode(Enum):
    TOGGLE = auto()
    HOLD = auto()

@dataclass
class ProfileTrigger:
    inputs: set[str]
    mode: TriggerMode

class MacroProfile:
    backend: IOBackend

    uid: str
    steps: list[MacroStep]
    repeat_count: int
    trigger: ProfileTrigger | None

    _running_event: threading.Event
    _thread: threading.Thread | None

    def __init__(self, backend: IOBackend, uid: str) -> None:
        self.backend = backend

        self.uid = uid
        self.steps = []
        self.repeat_count = -1
        self.trigger = None

        self._active = False
        self._running_event = threading.Event()
        self._thread = None

    def _run_loop(self) -> None:
        repeat_num = 0
        active: set[str] = set()

        while self._running_event.is_set():
            if self.repeat_count > 0 and repeat_num >= self.repeat_count:
                break

            for step in self.steps:
                if not self._running_event.is_set():
                    break

                for out_id, out_mode in step.output_info:
                    if out_mode:
                        active.add(out_id)
                        self.backend.press(out_id)
                    else:
                        if out_id in active:
                            active.remove(out_id)

                        self.backend.release(out_id)

                if step.duration > 0:
                    time.sleep(step.duration / 1000)

            repeat_num += 1

        for out_id in active:
            self.backend.release(out_id)

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
    backend: IOBackend
    profiles: dict[str, MacroProfile]

    _active_inputs: set[str]

    def __init__(self, backend: IOBackend) -> None:
        self.backend = backend
        self.profiles = {}

        self._active_inputs = set()

        backend.listen(self.handle_input)

    def handle_input(self, in_id: str, in_mode: bool) -> None:
        first_press = in_mode and in_id not in self._active_inputs

        if in_mode:
            self._active_inputs.add(in_id)
        elif in_id in self._active_inputs:
            self._active_inputs.remove(in_id)

        for profile in self.profiles.values():
            if profile.trigger is None:
                continue

            trig_inputs = profile.trigger.inputs
            trig_mode = profile.trigger.mode

            if trig_mode == TriggerMode.TOGGLE:
                if first_press and in_id in trig_inputs and trig_inputs.issubset(self._active_inputs):
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

        profile = MacroProfile(self.backend, uid)
        self.profiles[uid] = profile

        return profile

    def delete_profile(self, uid: str) -> None:
        if uid in self.profiles:
            del self.profiles[uid]
