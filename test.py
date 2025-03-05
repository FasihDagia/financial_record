import tkinter as tk

def change_color(*args):
    """Change text color to black when user types."""
    reason_entry.config(fg="black")

def remove_default_text(event):
    """Remove the default 'Optional' text when any key is pressed."""
    if reason_entry.get() == "Optional":
        reason_entry.delete(0, tk.END)  # Clear the entry box
        reason_entry.config(fg="black")  # Set text color to black

root = tk.Tk()
input_frame = tk.Frame(root)
input_frame.pack(pady=20)

tk.Label(input_frame, text="Reason:", font=("Helvetica", 10)).grid(row=4, column=0, pady=10)

# Create StringVar and set default value
reason_default = tk.StringVar(value="Optional")

# Bind the function to detect changes in the StringVar
reason_default.trace_add("write", change_color)

# Create Entry widget
reason_entry = tk.Entry(input_frame, width=20, textvariable=reason_default, fg='grey')
reason_entry.grid(row=4, column=1, pady=10)

# Bind keypress event to remove default text
reason_entry.bind("<KeyPress>", remove_default_text)

root.mainloop()
