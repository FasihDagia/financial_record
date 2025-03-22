import tkinter as tk
from tkinter import ttk

def on_combobox_keyrelease(event):
    typed_value = combobox.get()
    # Filter options based on the typed value
    filtered_options = [item for item in combobox_values if typed_value.lower() in item.lower()]
    
    # Update the combobox with the filtered options
    combobox['values'] = filtered_options

# Create the main window
root = tk.Tk()
root.title("Searchable ComboBox Example")

# Define the list of options
combobox_values = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Grapes", "Kiwi", "Lemon", "Mango", "Orange"]

# Create the combobox widget
combobox = ttk.Combobox(root, values=combobox_values)

# Bind the key release event to filter options as user types
combobox.bind("<KeyRelease>", on_combobox_keyrelease)

# Set the combobox width and pack it
combobox.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()
