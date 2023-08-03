import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import webbrowser

def resize_image(image_path, width, height):
    image = Image.open(image_path)
    resized_image = image.resize((width, height), Image.ANTIALIAS)
    return ImageTk.PhotoImage(resized_image)

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        populate_treeview(folder_path)

def populate_treeview(folder_path):
    global tree_path
    tree_path = folder_path  # Update the current folder path
    tree.delete(*tree.get_children())

    if folder_path == 'This PC':  # If This PC is selected, list all drives
        drives = ['C:\\', 'D:\\', 'E:\\', 'F:\\', 'G:\\']  # Add more drive letters as needed
        for drive in drives:
            tree.insert("", "end", text=" " + drive, image=folder_icon_resized)
    else:
        items = os.listdir(folder_path)
        folders = [os.path.join(folder_path, item) for item in items if os.path.isdir(os.path.join(folder_path, item))]
        files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]

        for folder in folders:
            folder_name = os.path.basename(folder)
            tree.insert("", "end", text=" " + folder_name, image=folder_icon_resized)

        for file in files:
            file_name = os.path.basename(file)
            tree.insert("", "end", text=" " + file_name, image=file_icon_resized)

    # Update the path_label with the current folder path
    path_var.set(tree_path.replace('\\', ' \\ '))

def on_tree_double_click(event):
    item_id = tree.selection()[0]
    item_text = tree.item(item_id, "text")
    folder_path = os.path.join(tree_path, item_text.strip())  # Remove leading space from item_text
    if os.path.isdir(folder_path):
        populate_treeview(folder_path)
    else:
        open_file(folder_path)

def open_file(file_path):
    try:
        # Check if the file is a text file or other type of file
        _, extension = os.path.splitext(file_path)
        if extension == '.txt':
            with open(file_path, 'r') as file:
                content = file.read()

            # Create a new window to display file content
            file_window = tk.Toplevel(root)
            file_window.title(f"File Content: {os.path.basename(file_path)}")

            # Create a Text widget to display the file content
            text_widget = tk.Text(file_window, wrap="word", font=("Arial", 12))
            text_widget.pack(fill="both", expand=True)

            # Insert the file content into the Text widget
            text_widget.insert("1.0", content)

            # Disable text editing in the Text widget (read-only)
            text_widget.config(state="disabled")
        else:
            # Open other types of files using the default program
            webbrowser.open(file_path)

    except Exception as e:
        messagebox.showerror("Error", f"Unable to open file: {e}")

def go_up_directory(event):
    if (tree_path in ['C:\\', 'D:\\', 'E:\\', 'F:\\', 'G:\\']):
        populate_treeview('This PC')
        return
    parent_directory = os.path.dirname(tree_path)
    if parent_directory:
        populate_treeview(parent_directory)

# Initialize the main window
root = tk.Tk()
root.title("SS Explorer")
root.geometry(f"600x400+500+200")
root.bind('<BackSpace>', go_up_directory)

# Load the icons for files and folders (replace "folder_icon.png" and "file_icon.png" with your image files)
folder_icon_resized = resize_image(r"GUI\15_fileExplorer\assets\folder-regular.png", 15, 15)  # Adjust the width and height as needed
file_icon_resized = resize_image(r"GUI\15_fileExplorer\assets\file-regular.png", 12, 15)  # Adjust the width and height as needed

# Create a Frame to hold the heading and path label
heading_frame = tk.Frame(root)
heading_frame.pack(fill="x", padx=10, pady=5)

# Create the TreeView widget
tree = ttk.Treeview(root)
tree.bind("<Double-1>", on_tree_double_click)
tree.bind("<Return>", on_tree_double_click)
tree.pack(fill="both", expand=True)

# Create a toolbar
# toolbar_frame = tk.Frame(root)
# toolbar_frame.pack(padx=10, pady=5, fill="x")

# browse_button = tk.Button(toolbar_frame, text="Browse", command=browse_folder)
# browse_button.pack(side="left", padx=5)

# Add the "Up" button to navigate up a directory
# up_button = tk.Button(toolbar_frame, text="<-", command=go_up_directory)
# up_button.pack(side="left", padx=5)

# Create a menubar
menubar = tk.Menu(root)
root.config(menu=menubar)

# File menu
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=lambda: populate_treeview('This PC'))  # Show drives on "Open"
file_menu.add_command(label="Exit", command=root.quit)

# Edit menu (Add more options as needed)
edit_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Cut")
edit_menu.add_command(label="Paste")
edit_menu.add_command(label="Delete")

# Help menu (Add more options as needed)
help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About")

# StringVar to hold the current path for the label
path_var = tk.StringVar()

# Label to show current path
path_label = tk.Label(heading_frame, textvariable=path_var, font=("Arial", 10))
path_label.pack(side="left")

# Initial path for the file explorer (start with 'This PC' to list drives)
tree_path = 'This PC'
populate_treeview(tree_path)

root.mainloop() 