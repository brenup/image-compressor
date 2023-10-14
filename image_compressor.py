#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os

original_size = 0  # Initialize original_size as a global variable

def browse_image():
    initial_dir = os.path.expanduser('~') + '/Downloads'  # Set the default folder to Downloads. Change to your desired directory
    file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)
        update_image_size(file_path)

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.2f} {unit}"

def update_image_size(image_path):
    global original_size  # Use the global original_size variable
    try:
        image = Image.open(image_path)
    except Exception as e:
        result_label.config(text=f"Error: {e}")
        return

    original_size = os.path.getsize(image_path)
    original_size_label.config(text=f"Selected Image: {format_size(original_size)}")

    update_compressed_size()

def update_compressed_size():
    compression_rate = compression_var.get() / 100
    new_size = int(original_size * compression_rate)
    compressed_size_label.config(text=f"Compressed Size: {format_size(new_size)}")

    reduction = original_size - new_size
    reduction_percent = (reduction / original_size) * 100
    reduction_label.config(text=f"{format_size(reduction)} - {reduction_percent:.2f}% - reduction")

def compress_image():
    image_path = entry_path.get()
    if not image_path:
        return

    try:
        image = Image.open(image_path)
    except Exception as e:
        result_label.config(text=f"Error: {e}")
        return

    compression_rate = compression_var.get() / 100
    new_image = image.copy()
    new_image.save(image_path, quality=int(compression_rate * 95))

    update_image_size(image_path)
    result_label.config(text="Image compressed and saved!")

app = tk.Tk()
app.title("Image Compressor")

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

browse_button = tk.Button(frame, text="Browse", command=browse_image)
browse_button.pack()

entry_path = tk.Entry(frame)
entry_path.pack()

original_size_label = tk.Label(frame, text="Selected Image: N/A")
original_size_label.pack()

compressed_size_label = tk.Label(frame, text="Compressed Size: N/A")
compressed_size_label.pack()

reduction_label = tk.Label(frame, text="Reduction: N/A")
reduction_label.pack()

compression_label = tk.Label(frame, text="Select Compression Rate:")
compression_label.pack()

compression_var = tk.IntVar()
compression_var.set(100)

compression_20 = tk.Radiobutton(frame, text="20%", variable=compression_var, value=20, command=update_compressed_size)
compression_40 = tk.Radiobutton(frame, text="40%", variable=compression_var, value=40, command=update_compressed_size)
compression_60 = tk.Radiobutton(frame, text="60%", variable=compression_var, value=60, command=update_compressed_size)
compression_80 = tk.Radiobutton(frame, text="80%", variable=compression_var, value=80, command=update_compressed_size)
compression_90 = tk.Radiobutton(frame, text="90%", variable=compression_var, value=90, command=update_compressed_size)

compression_20.pack()
compression_40.pack()
compression_60.pack()
compression_80.pack()
compression_90.pack()

compress_button = tk.Button(frame, text="Compress", command=compress_image)
compress_button.pack()

result_label = tk.Label(frame, text="")
result_label.pack()

app.mainloop()
