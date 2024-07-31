import tkinter as tk
from tkinter import simpledialog, filedialog
from datetime import datetime
import json
import os

def load_names():
    if os.path.exists("anest_names.json"):
        with open("anest_names.json", "r") as file:
            return json.load(file)
    return ["Dr. Smith", "Dr. Johnson", "Dr. Williams"]

def save_names():
    with open("GUI/anest_names.json", "w") as file:
        json.dump(anest_names, file)

def add_new_name():
    new_name = simpledialog.askstring("Input", "Enter the new Anest. Name:")
    if new_name and new_name not in anest_names:
        anest_names.append(new_name)
        save_names()
        menu = option_menu["menu"]
        menu.add_command(label=new_name, command=tk._setit(selected_name, new_name))
        selected_name.set(new_name)

def select_files():
    file_paths = filedialog.askopenfilenames(
        title="Select .seq files",
        filetypes=[("SEQ files", "*.seq")],
        multiple=True
    )
    for file_path in file_paths:
        if len(file_listbox.get(0, tk.END)) < 10:
            file_listbox.insert(tk.END, file_path)
        else:
            break

def update_time_date():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    time_label.config(text=current_time)
    root.after(1000, update_time_date)

def close_app():
    root.destroy()

def save_inputs():
    inputs = {
        "anest_name": selected_name.get(),
        "signature_time": {
            "hour": hour_spinbox.get(),
            "minute": minute_spinbox.get()
        },
        "helper": helper_var.get(),
        "seq_files": list(file_listbox.get(0, tk.END))
    }
    with open("GUI/user_inputs.json", "w") as file:
        json.dump(inputs, file, indent=4)
    print("Inputs saved to user_inputs.json")

def create_window():
    global option_menu, selected_name, anest_names, file_listbox, time_label, root
    global hour_spinbox, minute_spinbox, helper_var
    
    anest_names = load_names()

    root = tk.Tk()
    root.title("Interactive App Window")
    root.attributes('-fullscreen', True)

    container = tk.Frame(root, padx=20, pady=20, bg="#f0f0f0")
    container.pack(expand=True, fill='both')

    canvas = tk.Canvas(container, bg="#f0f0f0")
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    time_label = tk.Label(scrollable_frame, font=('Helvetica', 12), bg="#f0f0f0")
    time_label.grid(row=0, column=2, padx=10, pady=10, sticky='e')

    label = tk.Label(scrollable_frame, text="Select or Add Anest. Name", font=('Helvetica', 16, 'bold'), bg="#f0f0f0")
    label.grid(row=1, column=0, columnspan=2, pady=10, sticky='w')

    selected_name = tk.StringVar(root)
    selected_name.set(anest_names[0])

    option_menu = tk.OptionMenu(scrollable_frame, selected_name, *anest_names)
    option_menu.config(width=20, font=('Helvetica', 12), bg="#d3d3d3")
    option_menu.grid(row=2, column=0, pady=5, sticky='w')

    add_button = tk.Button(scrollable_frame, text="Add New Name", command=add_new_name, font=('Helvetica', 12), bg="#4caf50", fg="white")
    add_button.grid(row=2, column=1, pady=5, padx=5, sticky='w')

    time_label_desc = tk.Label(scrollable_frame, text="Signature Time", font=('Helvetica', 16, 'bold'), bg="#f0f0f0")
    time_label_desc.grid(row=3, column=0, columnspan=2, pady=10, sticky='w')

    time_frame = tk.Frame(scrollable_frame, bg="#f0f0f0")
    time_frame.grid(row=4, column=0, columnspan=2, pady=5, sticky='w')
    
    hour_label = tk.Label(time_frame, text="Hour:", font=('Helvetica', 12), bg="#f0f0f0")
    hour_label.pack(side=tk.LEFT)
    hour_spinbox = tk.Spinbox(time_frame, from_=0, to=23, width=2, format="%02.0f", font=('Helvetica', 12))
    hour_spinbox.pack(side=tk.LEFT, padx=5)
    
    minute_label = tk.Label(time_frame, text="Minute:", font=('Helvetica', 12), bg="#f0f0f0")
    minute_label.pack(side=tk.LEFT)
    minute_spinbox = tk.Spinbox(time_frame, from_=0, to=59, width=2, format="%02.0f", font=('Helvetica', 12))
    minute_spinbox.pack(side=tk.LEFT, padx=5)

    helper_var = tk.BooleanVar()
    helper_check = tk.Checkbutton(scrollable_frame, text="Helper", variable=helper_var, font=('Helvetica', 12), bg="#f0f0f0")
    helper_check.grid(row=5, column=0, columnspan=2, pady=10, sticky='w')

    file_label = tk.Label(scrollable_frame, text=".seq Files Dump (up to 10 files):", font=('Helvetica', 16, 'bold'), bg="#f0f0f0")
    file_label.grid(row=6, column=0, columnspan=2, pady=10, sticky='w')

    file_listbox = tk.Listbox(scrollable_frame, width=50, height=10, font=('Helvetica', 12), bg="#ffffff")
    file_listbox.grid(row=7, column=0, columnspan=2, pady=5, sticky='w')

    file_button = tk.Button(scrollable_frame, text="Add Files", command=select_files, font=('Helvetica', 12), bg="#2196f3", fg="white")
    file_button.grid(row=8, column=0, columnspan=2, pady=5, padx=5, sticky='w')

    save_button = tk.Button(scrollable_frame, text="Save Inputs", command=save_inputs, font=('Helvetica', 12), bg="#ff9800", fg="white")
    save_button.grid(row=9, column=0, columnspan=2, pady=10, sticky='w')

    close_button = tk.Button(scrollable_frame, text="Close App", command=close_app, font=('Helvetica', 12), bg="#f44336", fg="white")
    close_button.grid(row=10, column=0, columnspan=2, pady=10, sticky='w')

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    update_time_date()

    root.mainloop()

if __name__ == "__main__":
    create_window()
