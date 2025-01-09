import threading
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def run_pipeline(input_file, progress_bar):

    # Start the progress bar
    progress_bar.start()

    # Escape spaces if they exist
    input_file_fixed = str(input_file).replace(" ","\ ")

    # Run command
    command = f"seqkit split -i --by-id-prefix \"\"  {input_file_fixed}"
    
    try:
        subprocess.run(["bash", "-c", command], check=True)
        progress_bar.stop()
        messagebox.showinfo("Success", f"Output files created at {input_file}.split")

    except subprocess.CalledProcessError as e:
        progress_bar.stop()
        print(f"Error: {e}")
        
def start_thread():
    input_file = input_file_var.get()

    if not input_file:
        messagebox.showwarning("Input Error", "Please select an input FASTA file.")
        return
    
    # Start command in a new thread
    thread = threading.Thread(target=run_pipeline, args=(input_file, progress_bar))
    thread.start()

def select_file():
    file_path = filedialog.askopenfilename()
    input_file_var.set(file_path)

# Set up tkinter app
app = tk.Tk()
app.title("Multi FASTA Splitter")

# Input file selection
input_file_var = tk.StringVar()
tk.Label(app, text="Input FASTA File:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
tk.Entry(app, textvariable=input_file_var, width=40).grid(row=0, column=1, padx=10, pady=10)
tk.Button(app, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=10)

# Progress Bar (indeterminate)
progress_bar = ttk.Progressbar(app, mode="indeterminate", length=200)
progress_bar.grid(row=1, column=0, columnspan=3, padx=10, pady=20)

# Start button
tk.Button(app, text="Run program", command=start_thread).grid(row=2, column=1, padx=10, pady=20)

app.mainloop()
