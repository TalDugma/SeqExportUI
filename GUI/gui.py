import tkinter as tk
from tkinter import simpledialog, filedialog
from datetime import datetime
import json
import os
import Tal

USER_INPUTS_FILE = "data\\user_inputs.json"
ANEST_NAMES = "data\\anest_names.json"
OUTPUT_FOLDER = "C:\\Users\\User\\Desktop\\TEST"

def clear_cases():
    if os.path.exists(USER_INPUTS_FILE):
        with open(USER_INPUTS_FILE, "w") as file:
            json.dump([], file, indent=4)
        update_display_listbox()
        tk.messagebox.showinfo("Clear Cases", "All cases cleared.")

def get_DATA_TIME_folder(seq_file_path):
    name= os.path.basename(seq_file_path)
    year = (name[:4])[-2:]
    month = name[5:7]
    day = name[8:10]
    return f"DATA_{year}-{month}-{day}"

def clear_sequences():
    file_listbox.delete(0, tk.END)
    tk.messagebox.showinfo("Clear Sequences", "All sequences cleared.")

def delete_selected_input():
    selected_index = display_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        if os.path.exists(USER_INPUTS_FILE):
            with open(USER_INPUTS_FILE, "r") as file:
                data = json.load(file)
            if isinstance(data, list) and index < len(data):
                # Remove the selected entry
                del data[index]
                with open(USER_INPUTS_FILE, "w") as file:
                    json.dump(data, file, indent=4)
                # Update the display listbox
                update_display_listbox()
                print(f"Input at index {index+1} deleted.")


def load_names():
    if os.path.exists(ANEST_NAMES):
        with open(ANEST_NAMES, "r") as file:
            return json.load(file)
    return ["Dr. Smith", "Dr. Johnson", "Dr. Williams"]

def save_names():
    with open(ANEST_NAMES, "w") as file:
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

def call_batch_processor(seq_files,data):
    seq_list = []
    for file in seq_files:
        seq_list.append(file)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    for seq in seq_list:
        DATA_folder = os.path.join(OUTPUT_FOLDER,get_DATA_TIME_folder(seq))
        os.makedirs(DATA_folder,exist_ok=True)
        with open( os.path.join(DATA_folder, "data.json"), "w") as file:
            json.dump(data, file, indent=4)
        try:
            Tal.main([seq],DATA_folder)  

            tk.messagebox.showinfo("Batch Processor", f"Batch processing completed! \n Outputs saved to:\n {OUTPUT_FOLDER}")
        except:
            tk.messagebox.showinfo("Batch Processor", "Batch processing failed!")


def run_batch_processor():
    response = tk.messagebox.askyesno("Confirmation", "Are you sure you want to run the batch processor?")
    if response:
        # Perform the batch processing action here
        with open(USER_INPUTS_FILE,'r') as file:
            data = json.load(file)
            if not isinstance(data, list):
                data = []
            if data==[]:
                tk.messagebox.showinfo("Batch Processor", "Fill cases input!") 
                return 
            seq_files = file_listbox.get(0, tk.END)
            if len(seq_files)==0:
                tk.messagebox.showinfo("Batch Processor", "Add .seq files!") 
                return
            tk.messagebox.showinfo("Batch Processor", "Batch processing started.")
            call_batch_processor(seq_files,data)
    else:
        tk.messagebox.showinfo("Batch Processor", "Batch processing canceled.")
def update_time_date():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    time_label.config(text=current_time)
    root.after(1000, update_time_date)

def close_app():
    if os.path.exists(USER_INPUTS_FILE):
        os.remove(USER_INPUTS_FILE)
    
    with open(USER_INPUTS_FILE, "w") as file:
        json.dump([], file, indent=4)
        
    root.destroy()

def save_inputs():
    new_entry = {
        "anest_name": selected_name.get(),
        "signature_time": {
            "hour": hour_spinbox.get(),
            "minute": minute_spinbox.get()
        },
        "helper": helper_var.get(),
    }
    file_path = USER_INPUTS_FILE
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
    else:
        data = []
    if not isinstance(data, list):
        data = []
    data.append(new_entry)
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    
    # Update the display listbox
    update_display_listbox()
    print("Inputs saved to user_inputs.json")

def update_display_listbox():
    file_path = USER_INPUTS_FILE
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
        display_listbox.delete(0, tk.END)
        for i,entry in enumerate(data):
            display_listbox.insert(tk.END, f"CASE {i+1}: {entry['anest_name']} - {entry['signature_time']['hour']}:{entry['signature_time']['minute']} - Helper: {entry['helper']}")

def create_window1():
    global option_menu, selected_name, anest_names, file_listbox, time_label, root
    global hour_spinbox, minute_spinbox, helper_var, display_listbox
    
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

    label = tk.Label(scrollable_frame, text="Fill Case Information", font=('Helvetica', 16, 'bold'), bg="#f0f0f0")
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
    
    save_button = tk.Button(scrollable_frame, text="Save Case", command=save_inputs, font=('Helvetica', 12), bg="#ff9800", fg="white")
    save_button.grid(row=6, column=0, columnspan=2, pady=10, sticky='w')

    clear_cases_button = tk.Button(scrollable_frame, text="Clear Cases", command=clear_cases, font=('Helvetica', 12), bg="#f44336", fg="white")
    clear_cases_button.grid(row=8, column=3, padx=20, pady=5, sticky='w')

    file_label = tk.Label(scrollable_frame, text=".seq Files Dump (up to 10 files):", font=('Helvetica', 16, 'bold'), bg="#f0f0f0")
    file_label.grid(row=7, column=0, columnspan=2, pady=10, sticky='w')

    file_listbox = tk.Listbox(scrollable_frame, width=50, height=10, font=('Helvetica', 12), bg="#ffffff")
    file_listbox.grid(row=8, column=0, columnspan=2, pady=5, sticky='w')

    file_button = tk.Button(scrollable_frame, text="Add Files", command=select_files, font=('Helvetica', 12), bg="#2196f3", fg="white")
    file_button.grid(row=9, column=0, columnspan=2, pady=5, padx=5, sticky='w')
    
    # Display listbox for showing saved inputs on the right
    display_listbox = tk.Listbox(scrollable_frame, width=50, height=20, font=('Helvetica', 12), bg="#ffffff")
    display_listbox.grid(row=0, column=3, rowspan=10, padx=20, pady=10, sticky='nw')
    # Delete button to remove selected inputs
    delete_button = tk.Button(scrollable_frame, text="Delete Selected Input", command=delete_selected_input, font=('Helvetica', 12), bg="#f44336", fg="white")
    delete_button.grid(row=8, column=3, padx=20, pady=5, sticky='nw')
    
    clear_sequences_button = tk.Button(scrollable_frame, text="Clear Sequences", command=clear_sequences, font=('Helvetica', 12), bg="#f44336", fg="white")
    clear_sequences_button.grid(row=10, column=0, columnspan=2, pady=5, sticky='w')

    close_button = tk.Button(scrollable_frame, text="Close App", command=close_app, font=('Helvetica', 12), bg="#f44336", fg="white")
    close_button.grid(row=0, column=0, columnspan=2, pady=10, sticky='w')

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    run_button = tk.Button(scrollable_frame, text="Run Batch Processor", font=('Helvetica', 20, 'bold'), bg="#4caf50", fg="white", command=run_batch_processor)
    run_button.grid(row=10, column=3, columnspan=2, pady=20, sticky='n')
    # Load and display the logo in the bottom right corner
    # logo_path = "my_app/data/logo.png"  # Replace with the actual path to your logo
    # logo_image = tk.PhotoImage(file=logo_path)
    # logo_label = tk.Label(scrollable_frame, image=logo_image, bg="#f0f0f0")
    # logo_label.image = logo_image  # Keep a reference to avoid garbage collection
    # logo_label.grid(row=11, column=11, padx=20, pady=10, sticky='se')

    update_time_date()
    update_display_listbox()

    root.mainloop()
def create_window():
    global option_menu, selected_name, anest_names, file_listbox, time_label, root
    global hour_spinbox, minute_spinbox, helper_var, display_listbox
    
    anest_names = load_names()

    root = tk.Tk()
    root.title("Interactive App Window")
    root.attributes('-fullscreen', True)

    # Container for the entire application
    container = tk.Frame(root, padx=20, pady=20, bg="#f0f0f0")
    container.pack(expand=True, fill='both')
    # Big title
    title_label = tk.Label(container, text="Scalpel's Great Sequence Export System", 
                           font=('Helvetica', 32, 'bold'), fg="#333333", bg="#f0f0f0")
    title_label.pack(pady=(0, 20))  # Adjust the second value in pady for space between the title and the logo

    # Load and place the logo
    # logo_image = tk.PhotoImage(file="data/logo.png")
    # logo_label = tk.Label(container, image=logo_image, bg="#f0f0f0")
    # logo_label.image = logo_image  # Keep a reference to avoid garbage collection
    # logo_label.pack(pady=10)  # Adjust padding as needed

    # Canvas and scrollbar for scrollable content
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

    # Time Display
    time_label = tk.Label(scrollable_frame, font=('Helvetica', 12), bg="#f0f0f0")
    time_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

    # Case Information Section
    case_info_frame = tk.LabelFrame(scrollable_frame, text="Case Information", font=('Helvetica', 16, 'bold'), bg="#f0f0f0", padx=10, pady=10)
    case_info_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky='nw')

    selected_name = tk.StringVar(root)
    selected_name.set(anest_names[0])

    option_menu = tk.OptionMenu(case_info_frame, selected_name, *anest_names)
    option_menu.config(width=20, font=('Helvetica', 12), bg="#d3d3d3")
    option_menu.grid(row=0, column=0, pady=5, sticky='w')

    add_button = tk.Button(case_info_frame, text="Add New Name", command=add_new_name, font=('Helvetica', 12), bg="#4caf50", fg="white")
    add_button.grid(row=0, column=1, pady=5, padx=5, sticky='w')

    time_label_desc = tk.Label(case_info_frame, text="Signature Time", font=('Helvetica', 16, 'bold'), bg="#f0f0f0")
    time_label_desc.grid(row=1, column=0, columnspan=2, pady=10, sticky='w')

    time_frame = tk.Frame(case_info_frame, bg="#f0f0f0")
    time_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky='w')

    hour_label = tk.Label(time_frame, text="Hour:", font=('Helvetica', 12), bg="#f0f0f0")
    hour_label.pack(side=tk.LEFT)
    hour_spinbox = tk.Spinbox(time_frame, from_=0, to=23, width=2, format="%02.0f", font=('Helvetica', 12))
    hour_spinbox.pack(side=tk.LEFT, padx=5)

    minute_label = tk.Label(time_frame, text="Minute:", font=('Helvetica', 12), bg="#f0f0f0")
    minute_label.pack(side=tk.LEFT)
    minute_spinbox = tk.Spinbox(time_frame, from_=0, to=59, width=2, format="%02.0f", font=('Helvetica', 12))
    minute_spinbox.pack(side=tk.LEFT, padx=5)

    helper_var = tk.BooleanVar()
    helper_check = tk.Checkbutton(case_info_frame, text="Helper", variable=helper_var, font=('Helvetica', 12), bg="#f0f0f0")
    helper_check.grid(row=3, column=0, columnspan=2, pady=10, sticky='w')

    save_button = tk.Button(case_info_frame, text="Save Case", command=save_inputs, font=('Helvetica', 12), bg="#ff9800", fg="white")
    save_button.grid(row=4, column=0, columnspan=2, pady=10, sticky='w')

    # Files Section
    file_frame = tk.LabelFrame(scrollable_frame, text="Files Management", font=('Helvetica', 16, 'bold'), bg="#f0f0f0", padx=10, pady=10)
    file_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='nw')

    file_label = tk.Label(file_frame, text=".seq Files Dump (up to 10 files):", font=('Helvetica', 12), bg="#f0f0f0")
    file_label.grid(row=0, column=0, pady=10, sticky='w')

    file_listbox = tk.Listbox(file_frame, width=50, height=10, font=('Helvetica', 12), bg="#ffffff")
    file_listbox.grid(row=1, column=0, pady=5, sticky='w')

    file_button = tk.Button(file_frame, text="Add Files", command=select_files, font=('Helvetica', 12), bg="#2196f3", fg="white")
    file_button.grid(row=2, column=0, pady=5, sticky='w')

    clear_sequences_button = tk.Button(file_frame, text="Clear Sequences", command=clear_sequences, font=('Helvetica', 12), bg="#f44336", fg="white")
    clear_sequences_button.grid(row=3, column=0, pady=5, sticky='w')

  
    # Display listbox for showing saved inputs on the right
    display_frame = tk.LabelFrame(scrollable_frame, text="Saved Cases", font=('Helvetica', 16, 'bold'), bg="#f0f0f0", padx=10, pady=10)
    display_frame.grid(row=1, column=2, rowspan=3, padx=20, pady=10, sticky='nw')
    clear_cases_button = tk.Button(display_frame, text="Clear Cases", command=clear_cases, font=('Helvetica', 12), bg="#f44336", fg="white")
    clear_cases_button.grid(row=2, column=0,padx=20, pady=5, sticky='w')

    display_listbox = tk.Listbox(display_frame, width=50, height=20, font=('Helvetica', 12), bg="#ffffff")
    display_listbox.grid(row=0, column=0, padx=20, pady=10, sticky='nw')

    delete_button = tk.Button(display_frame, text="Delete Selected Case", command=delete_selected_input, font=('Helvetica', 12), bg="#f44336", fg="white")
    delete_button.grid(row=1, column=0, padx=20, pady=5, sticky='nw')

    # Run Batch Processor button
    run_button = tk.Button(scrollable_frame, text="Run Batch Processor", font=('Helvetica', 20, 'bold'), bg="#4caf50", fg="white", command=run_batch_processor)
    run_button.grid(row=4, column=2, padx=20, pady=20, sticky='n')

    # Close App button at the bottom
    close_button = tk.Button(scrollable_frame, text="Close App", command=close_app, font=('Helvetica', 12), bg="#f44336", fg="white")
    close_button.grid(row=5, column=2, pady=10, sticky='se')

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    update_time_date()
    update_display_listbox()

    root.mainloop()
def create_window3():
    global option_menu, selected_name, anest_names, file_listbox, time_label, root
    global hour_spinbox, minute_spinbox, helper_var, display_listbox
    
    anest_names = load_names()

    root = tk.Tk()
    root.title("Interactive App Window")
    root.attributes('-fullscreen', True)

    # New color scheme
    primary_bg_color = "#2c3e50"  # Dark Blue
    secondary_bg_color = "#34495e"  # Slightly lighter dark blue
    highlight_color = "#e74c3c"  # Vivid Red
    button_color = "#16a085"  # Turquoise
    font_color = "#ecf0f1"  # Light Gray
    listbox_bg_color = "#ffffff"  # White
    listbox_font_color = "#2c3e50"  # Dark Blue for text

    container = tk.Frame(root, padx=20, pady=20, bg=primary_bg_color)
    container.pack(expand=True, fill='both')

    canvas = tk.Canvas(container, bg=primary_bg_color)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=primary_bg_color)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    time_label = tk.Label(scrollable_frame, font=('Helvetica', 12), fg=font_color, bg=primary_bg_color)
    time_label.grid(row=0, column=2, padx=10, pady=10, sticky='e')

    label = tk.Label(scrollable_frame, text="Fill Case Information", font=('Helvetica', 18, 'bold'), fg=font_color, bg=primary_bg_color)
    label.grid(row=1, column=0, columnspan=2, pady=10, sticky='w')

    selected_name = tk.StringVar(root)
    selected_name.set(anest_names[0])

    option_menu = tk.OptionMenu(scrollable_frame, selected_name, *anest_names)
    option_menu.config(width=20, font=('Helvetica', 12), bg=secondary_bg_color, fg=font_color, highlightbackground=secondary_bg_color, highlightthickness=0)
    option_menu.grid(row=2, column=0, pady=5, sticky='w')

    add_button = tk.Button(scrollable_frame, text="Add New Name", command=add_new_name, font=('Helvetica', 12), bg=button_color, fg=font_color)
    add_button.grid(row=2, column=1, pady=5, padx=5, sticky='w')

    time_label_desc = tk.Label(scrollable_frame, text="Signature Time", font=('Helvetica', 16, 'bold'), fg=font_color, bg=primary_bg_color)
    time_label_desc.grid(row=3, column=0, columnspan=2, pady=10, sticky='w')

    time_frame = tk.Frame(scrollable_frame, bg=primary_bg_color)
    time_frame.grid(row=4, column=0, columnspan=2, pady=5, sticky='w')
    
    hour_label = tk.Label(time_frame, text="Hour:", font=('Helvetica', 12), fg=font_color, bg=primary_bg_color)
    hour_label.pack(side=tk.LEFT)
    hour_spinbox = tk.Spinbox(time_frame, from_=0, to=23, width=2, format="%02.0f", font=('Helvetica', 12))
    hour_spinbox.pack(side=tk.LEFT, padx=5)
    
    minute_label = tk.Label(time_frame, text="Minute:", font=('Helvetica', 12), fg=font_color, bg=primary_bg_color)
    minute_label.pack(side=tk.LEFT)
    minute_spinbox = tk.Spinbox(time_frame, from_=0, to=59, width=2, format="%02.0f", font=('Helvetica', 12))
    minute_spinbox.pack(side=tk.LEFT, padx=5)

    helper_var = tk.BooleanVar()
    helper_check = tk.Checkbutton(scrollable_frame, text="Helper", variable=helper_var, font=('Helvetica', 12), fg=font_color, bg=primary_bg_color)
    helper_check.grid(row=5, column=0, columnspan=2, pady=10, sticky='w')
    
    save_button = tk.Button(scrollable_frame, text="Save Case", command=save_inputs, font=('Helvetica', 12), bg=highlight_color, fg=font_color)
    save_button.grid(row=6, column=0, columnspan=2, pady=10, sticky='w')

    clear_cases_button = tk.Button(scrollable_frame, text="Clear Cases", command=clear_cases, font=('Helvetica', 12), bg=highlight_color, fg=font_color)
    clear_cases_button.grid(row=8, column=3, padx=20, pady=5, sticky='w')

    file_label = tk.Label(scrollable_frame, text=".seq Files Dump (up to 10 files):", font=('Helvetica', 16, 'bold'), fg=font_color, bg=primary_bg_color)
    file_label.grid(row=7, column=0, columnspan=2, pady=10, sticky='w')

    file_listbox = tk.Listbox(scrollable_frame, width=50, height=10, font=('Helvetica', 12), bg=listbox_bg_color, fg=listbox_font_color)
    file_listbox.grid(row=8, column=0, columnspan=2, pady=5, sticky='w')

    file_button = tk.Button(scrollable_frame, text="Add Files", command=select_files, font=('Helvetica', 12), bg=button_color, fg=font_color)
    file_button.grid(row=9, column=0, columnspan=2, pady=5, padx=5, sticky='w')
    
    display_listbox = tk.Listbox(scrollable_frame, width=50, height=20, font=('Helvetica', 12), bg=listbox_bg_color, fg=listbox_font_color)
    display_listbox.grid(row=0, column=3, rowspan=10, padx=20, pady=10, sticky='nw')

    delete_button = tk.Button(scrollable_frame, text="Delete Selected Input", command=delete_selected_input, font=('Helvetica', 12), bg=highlight_color, fg=font_color)
    delete_button.grid(row=8, column=3, padx=20, pady=5, sticky='nw')
    
    clear_sequences_button = tk.Button(scrollable_frame, text="Clear Sequences", command=clear_sequences, font=('Helvetica', 12), bg=highlight_color, fg=font_color)
    clear_sequences_button.grid(row=10, column=0, columnspan=2, pady=5, sticky='w')

    close_button = tk.Button(scrollable_frame, text="Close App", command=close_app, font=('Helvetica', 12), bg=highlight_color, fg=font_color)
    close_button.grid(row=0, column=0, columnspan=2, pady=10, sticky='w')

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    run_button = tk.Button(scrollable_frame, text="Run Batch Processor", font=('Helvetica', 20, 'bold'), bg=button_color, fg=font_color, command=run_batch_processor)
    run_button.grid(row=10, column=3, columnspan=2, pady=20, sticky='n')

    update_time_date()
    update_display_listbox()

    root.mainloop()
def create_window4():
    global option_menu, selected_name, anest_names, file_listbox, time_label, root
    global hour_spinbox, minute_spinbox, helper_var, display_listbox
    
    anest_names = load_names()

    root = tk.Tk()
    root.title("Interactive App Window")
    root.attributes('-fullscreen', True)

    # New color scheme and fonts
    primary_bg_color = "#2b2d42"  # Dark Slate Blue
    secondary_bg_color = "#8d99ae"  # Cool Gray
    accent_color = "#ef233c"  # Vivid Red
    button_color = "#d90429"  # Bold Red
    listbox_bg_color = "#edf2f4"  # Light Grayish Blue
    font_color = "#edf2f4"  # Light Grayish Blue
    heading_font = ('Segoe UI', 18, 'bold')
    body_font = ('Segoe UI', 14)
    button_font = ('Segoe UI', 14, 'bold')

    # Container for the entire application
    container = tk.Frame(root, padx=20, pady=20, bg=primary_bg_color)
    container.pack(expand=True, fill='both')

    # Canvas and scrollbar for scrollable content
    canvas = tk.Canvas(container, bg=primary_bg_color)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=primary_bg_color)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Time Display
    time_label = tk.Label(scrollable_frame, font=body_font, fg=font_color, bg=primary_bg_color)
    time_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

    # Case Information Section
    case_info_frame = tk.LabelFrame(scrollable_frame, text="Case Information", font=heading_font, fg=font_color, bg=primary_bg_color, padx=10, pady=10)
    case_info_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky='nw')

    selected_name = tk.StringVar(root)
    selected_name.set(anest_names[0])

    option_menu = tk.OptionMenu(case_info_frame, selected_name, *anest_names)
    option_menu.config(width=20, font=body_font, bg=secondary_bg_color, fg=primary_bg_color)
    option_menu.grid(row=0, column=0, pady=5, sticky='w')

    add_button = tk.Button(case_info_frame, text="Add New Name", command=add_new_name, font=button_font, bg=button_color, fg=font_color)
    add_button.grid(row=0, column=1, pady=5, padx=5, sticky='w')

    time_label_desc = tk.Label(case_info_frame, text="Signature Time", font=heading_font, fg=font_color, bg=primary_bg_color)
    time_label_desc.grid(row=1, column=0, columnspan=2, pady=10, sticky='w')

    time_frame = tk.Frame(case_info_frame, bg=primary_bg_color)
    time_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky='w')

    hour_label = tk.Label(time_frame, text="Hour:", font=body_font, fg=font_color, bg=primary_bg_color)
    hour_label.pack(side=tk.LEFT)
    hour_spinbox = tk.Spinbox(time_frame, from_=0, to=23, width=2, format="%02.0f", font=body_font)
    hour_spinbox.pack(side=tk.LEFT, padx=5)

    minute_label = tk.Label(time_frame, text="Minute:", font=body_font, fg=font_color, bg=primary_bg_color)
    minute_label.pack(side=tk.LEFT)
    minute_spinbox = tk.Spinbox(time_frame, from_=0, to=59, width=2, format="%02.0f", font=body_font)
    minute_spinbox.pack(side=tk.LEFT, padx=5)

    helper_var = tk.BooleanVar()
    helper_check = tk.Checkbutton(case_info_frame, text="Helper", variable=helper_var, font=body_font, fg=font_color, bg=primary_bg_color)
    helper_check.grid(row=3, column=0, columnspan=2, pady=10, sticky='w')

    save_button = tk.Button(case_info_frame, text="Save Case", command=save_inputs, font=button_font, bg=accent_color, fg=font_color)
    save_button.grid(row=4, column=0, columnspan=2, pady=10, sticky='w')

    # Files Section
    file_frame = tk.LabelFrame(scrollable_frame, text="Files Management", font=heading_font, fg=font_color, bg=primary_bg_color, padx=10, pady=10)
    file_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='nw')

    file_label = tk.Label(file_frame, text=".seq Files Dump (up to 10 files):", font=body_font, fg=font_color, bg=primary_bg_color)
    file_label.grid(row=0, column=0, pady=10, sticky='w')

    file_listbox = tk.Listbox(file_frame, width=50, height=10, font=body_font, bg=listbox_bg_color, fg=primary_bg_color)
    file_listbox.grid(row=1, column=0, pady=5, sticky='w')

    file_button = tk.Button(file_frame, text="Add Files", command=select_files, font=button_font, bg=button_color, fg=font_color)
    file_button.grid(row=2, column=0, pady=5, sticky='w')

    clear_sequences_button = tk.Button(file_frame, text="Clear Sequences", command=clear_sequences, font=button_font, bg=button_color, fg=font_color)
    clear_sequences_button.grid(row=3, column=0, pady=5, sticky='w')

    clear_cases_button = tk.Button(file_frame, text="Clear Cases", command=clear_cases, font=button_font, bg=button_color, fg=font_color)
    clear_cases_button.grid(row=4, column=0, pady=5, sticky='w')

    # Display listbox for showing saved inputs on the right
    display_frame = tk.LabelFrame(scrollable_frame, text="Saved Cases", font=heading_font, fg=font_color, bg=primary_bg_color, padx=10, pady=10)
    display_frame.grid(row=1, column=2, rowspan=3, padx=20, pady=10, sticky='nw')

    display_listbox = tk.Listbox(display_frame, width=50, height=20, font=body_font, bg=listbox_bg_color, fg=primary_bg_color)
    display_listbox.grid(row=0, column=0, padx=20, pady=10, sticky='nw')

    delete_button = tk.Button(display_frame, text="Delete Selected Input", command=delete_selected_input, font=button_font, bg=button_color, fg=font_color)
    delete_button.grid(row=1, column=0, padx=20, pady=5, sticky='nw')

    # Run Batch Processor button
    run_button = tk.Button(scrollable_frame, text="Run Batch Processor", font=('Segoe UI', 20, 'bold'), bg=accent_color, fg=font_color, command=run_batch_processor)
    run_button.grid(row=4, column=2, padx=20, pady=20, sticky='n')

    # Close App button at the bottom
    close_button = tk.Button(scrollable_frame, text="Close App", command=close_app, font=button_font, bg=button_color, fg=font_color)
    close_button.grid(row=5, column=2, pady=10, sticky='se')

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    update_time_date()
    update_display_listbox()

    root.mainloop()

if __name__ == "__main__":
    create_window()
