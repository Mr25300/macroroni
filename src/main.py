import time

from pynput import keyboard, mouse

from io_win_mac import IOWinMac
from macro import MacroManager, MacroProfile, MacroStep, ProfileTrigger, TriggerMode

if __name__ == "__main__":
    io = IOWinMac()

    macro = MacroManager(io)
    profile = macro.create_profile()

    profile.steps = [
        MacroStep([("kc_1", True), ("kc_1", False)], 1000)
    ]
    profile.trigger = ProfileTrigger({"kc_a"}, TriggerMode.TOGGLE)

    time.sleep(100000)
