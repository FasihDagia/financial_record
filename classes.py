import tkinter as tk
from tkinter import ttk

class AutocompleteCombobox(ttk.Combobox):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)
        self['values'] = self._completion_list
        self.bind('<KeyRelease>', self._handle_keyrelease)
        self.bind('<FocusOut>', lambda e: self.selection_clear())

    def _handle_keyrelease(self, event):
        if event.keysym in ["BackSpace", "Left", "Right", "Up", "Down", "Return", "Tab"]:
            return

        value = self.get()
        if value == '':
            self['values'] = self._completion_list
        else:
            data = [item for item in self._completion_list if value.lower() in item.lower()]
            self['values'] = data

        # Move the cursor to end of entry
        self.icursor(tk.END)