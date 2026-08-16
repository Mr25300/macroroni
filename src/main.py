import time

from pynput import keyboard, mouse

from macro import MacroManager, MacroProfile, MacroStep, ProfileTrigger, TriggerMode

if __name__ == "__main__":
    manager = MacroManager()
    profile = manager.create_profile()

    profile.steps = [MacroStep(keyboard.Key.backspace, True, 1), MacroStep(keyboard.Key.backspace, False, 1)]
    profile.trigger = ProfileTrigger({keyboard.KeyCode.from_char("a")}, TriggerMode.HOLD)

    time.sleep(100000)
