import os
import subprocess
from tkinter import ttk
from tkinter import *
from tkinter import filedialog, messagebox
import PythonDevFolderMaker


# Function to create project folders
def create_project_folders(project_name, project_dir):
    try:
        os.mkdir(os.path.join(project_dir, project_name))
        os.mkdir(os.path.join(project_dir, project_name, "src"))
        os.mkdir(os.path.join(project_dir, project_name, "data"))
        os.mkdir(os.path.join(project_dir, project_name, "data", "input"))
        os.mkdir(os.path.join(project_dir, project_name, "data", "output"))
        os.mkdir(os.path.join(project_dir, project_name, "tests"))
        os.mkdir(os.path.join(project_dir, project_name, "docs"))

        with open(os.path.join(project_dir, project_name, "src", "main.cpp"), "w") as f:
            f.write(f"// {project_name}\n\n")
            f.write("// Main C++ source file\n")

        with open(os.path.join(project_dir, project_name, "src", "utils.cpp"), "w") as f:
            f.write("// Utility functions\n")

        with open(os.path.join(project_dir, project_name, "docs", "README.md"), "w") as f:
            f.write(f"# {project_name}\n\n")
            f.write("This project uses C++.\n\n")
            f.write("## Description\n\n")
            f.write("Insert project description here.\n\n")
            f.write("## Usage\n\n")
            f.write("Insert project usage instructions here.\n\n")
            f.write("## License\n\n")
            f.write("Insert project license information here.\n")

        with open(os.path.join(project_dir, project_name, "docs", "design.md"), "w") as f:
            f.write("# Design Document\n\n")
            f.write("Insert design document here.\n")

    except OSError:
        messagebox.showerror("Error", f"Failed to create project folders for {project_name}.")
    else:
        messagebox.showinfo("Success", f"Project folders created successfully for {project_name}.")
        project_name_entry.delete(0, END)

# Function to handle button click event
def create_project():
    global language
    project_name = project_name_entry.get()
    project_dir = filedialog.askdirectory(title="Select project directory")

    if not project_name:
        messagebox.showerror("Error", "Please enter a project name.")
    elif not project_dir:
        messagebox.showerror("Error", "Please select a project directory.")
    else:
        if language == "Python":
            PythonDevFolderMaker.create_project(project_name, project_dir)  # Call create_project from PythonDevFolderMaker module
        else:
            create_project_folders(project_name, project_dir)

# Function to handle language selection
def language_selected(event):
    global language
    language = language_combobox.get()
# GUI setup
window = Tk()
window.title("Project Folder Maker")
window.geometry("400x300")
window.config(bg="#4e4e4e")

project_name_label = Label(window, text="Enter project name:", font=("Arial", 12), bg="#4e4e4e", fg="#ffffff")
project_name_label.pack(pady=10)

project_name_entry = Entry(window, width=30, font=("Arial", 12))
project_name_entry.pack()

project_dir_label = Label(window, text="Select project directory:", font=("Arial", 12), bg="#4e4e4e", fg="#ffffff")
project_dir_label.pack(pady=10)

project_dir_button = Button(window, text="Browse", font=("Arial", 12), bg="#4caf50", fg="#ffffff", activebackground="#43a047", activeforeground="#ffffff", command=create_project)
project_dir_button.pack()

language_label = Label(window, text="Select language:", font=("Arial", 12), bg="#4e4e4e", fg="#ffffff")
language_label.pack(pady=10)

language_combobox = ttk.Combobox(window, state="readonly", values=["Python", "C++"], width=28)
language_combobox.current(1)  # Set Python as the default selected option
language_combobox.bind("<<ComboboxSelected>>", language_selected)
language_combobox.pack()

create_project_button = Button(window, text="Create Project", font=("Arial", 12), bg="#4caf50", fg="#ffffff", activebackground="#43a047", activeforeground="#ffffff", command=create_project)
create_project_button.pack(pady=10)

# Initialize the language variable with the default selected option
language = language_combobox.get()

window.mainloop()