from tkinter import Tk, ttk

from macro import MacroManager, MacroProfile, MacroStep, ProfileTrigger, TriggerMode

class Window:
    macro: MacroManager
    root: Tk

    def __init__(self) -> None:
        self.macro = MacroManager()
        self.root = Tk()

    def run(self) -> None:
        self.root.mainloop()
