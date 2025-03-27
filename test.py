import tkinter as tk

def on_mouse_scroll(event):
    """Enable smooth scrolling with mouse wheel."""
    canvas.yview_scroll(-1 * (event.delta // 120), "units")  

def create_company(root):
    global canvas  

    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("600x700")
    root.title("Create Company")

    # Title label
    tk.Label(root, text="Create Company Profile", font=("Helvetica", 22, "bold")).pack(padx=10, pady=10)

    # Main Frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Canvas (removes border)
    canvas = tk.Canvas(main_frame, highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbar
    scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    # Scrollable Frame inside Canvas
    scrollable_frame = tk.Frame(canvas)

    # Create window inside canvas with adjustable width
    frame_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Force frame resizing inside canvas
    def update_scroll_region():
        scrollable_frame.update_idletasks()  # Make sure frame size is updated
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(frame_window, width=canvas.winfo_width())  # Adjust width dynamically

    # Bind frame changes to scroll region update
    scrollable_frame.bind("<Configure>", lambda e: update_scroll_region())

    # Input Frame
    input_frame = tk.Frame(scrollable_frame)
    input_frame.pack(pady=10, fill=tk.X)

    # Function to remove "Optional" placeholder text
    def remove_optional(event, entry):
        if entry.get() == "Optional":
            entry.delete(0, tk.END)
            entry.config(fg="black")

    # Labels and Entry Fields
    tk.Label(input_frame, text="Company Name:", font=("Helvetica", 10)).grid(row=0, column=0, padx=5, pady=10)
    name_entry = tk.Entry(input_frame, font=("Helvetica", 10))
    name_entry.grid(row=0, column=1, padx=5, pady=10)

    tk.Label(input_frame, text="Phone No:", font=("Helvetica", 10)).grid(row=0, column=2, padx=5, pady=10)
    phone_entry = tk.Entry(input_frame, font=("Helvetica", 10))
    phone_entry.grid(row=0, column=3, padx=5, pady=10)

    tk.Label(input_frame, text="Telephone No:", font=("Helvetica", 10)).grid(row=1, column=0, padx=5, pady=10)
    telephone_default = tk.StringVar(value="Optional")
    telephone_entry = tk.Entry(input_frame, font=("Helvetica", 10), fg="grey", textvariable=telephone_default)
    telephone_entry.bind("<FocusIn>", lambda event: remove_optional(event, telephone_entry))
    telephone_entry.grid(row=1, column=1, padx=5, pady=10)

    tk.Label(input_frame, text="Email:", font=("Helvetica", 10)).grid(row=1, column=2, padx=5, pady=10)
    email_entry = tk.Entry(input_frame, font=("Helvetica", 10))
    email_entry.grid(row=1, column=3, padx=5, pady=10)

    tk.Label(input_frame, text="Address:", font=("Helvetica", 10)).grid(row=2, column=0, padx=10, pady=10)
    address_entry = tk.Text(input_frame, font=("Helvetica", 10), width=50, height=5)
    address_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=10)

    # Scroll Update (Force Refresh)
    root.update_idletasks()
    update_scroll_region()

    # Bind Mouse Scrolling
    root.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * (event.delta // 120), "units"))
    root.bind_all("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))  # Linux Scroll Up
    root.bind_all("<Button-5>", lambda event: canvas.yview_scroll(1, "units")) 