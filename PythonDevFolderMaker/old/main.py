import re 
import sys 
import os
import subprocess
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def increment_project():
    project_dir = filedialog.askdirectory(title="Select project directory")
    if not project_dir:
        messagebox.showerror("Error", "Please select a project directory.")
        return

    folder_name = os.path.basename(project_dir)
    
    custom_folder_name = custom_folder_entry.get().strip()
    if custom_folder_name:
        custom_folder_name = f"_{custom_folder_name}_"
        folder_name += custom_folder_name

    if not re.search(r"\d+\.\d+$", folder_name):
        folder_name = folder_name + ".1"
    else:
        major, minor = folder_name.rsplit(".", maxsplit=1)
        minor = str(int(minor) + 1)  # Increment the minor version as an integer
        folder_name = f"{major}.{minor}"

    project_name = project_name_entry.get()
    if project_name:
        project_name_parts = project_name.split("_")
        if len(project_name_parts) > 1 and project_name_parts[-1].startswith("v"):
            project_name_parts[-1] = f"v{folder_name}"
        else:
            project_name_parts.append(f"v{folder_name}")
        project_name = "_".join(project_name_parts)
    else:
        project_name = folder_name

    project_name_entry.delete(0, END)
    project_name_entry.insert(0, project_name)

    env_name_entry.delete(0, END)
    custom_folder_entry.delete(0, END)

    project_dir_label.config(text="Selected project directory:", fg="#ffffff")
    project_dir_label_value.config(text=project_dir, fg="#ffffff")
    create_project_button.config(command=create_project)

    custom_folder_entry.delete(0, END)

# Function to create project folders and auxiliary file
def create_project_folders(project_name, project_dir, env_name, custom_folder_name=None):
    try:
        if custom_folder_name:
            project_name += f" {custom_folder_name}"

        os.mkdir(os.path.join(project_dir, project_name))
        os.mkdir(os.path.join(project_dir, project_name, "src"))
        os.mkdir(os.path.join(project_dir, project_name, "data"))
        os.mkdir(os.path.join(project_dir, project_name, "data", "input"))
        os.mkdir(os.path.join(project_dir, project_name, "data", "output"))
        os.mkdir(os.path.join(project_dir, project_name, "tests"))
        os.mkdir(os.path.join(project_dir, project_name, "docs"))

        with open(os.path.join(project_dir, project_name, "src", "main.py"), "w") as f:
            f.write(f"# {project_name}\n\n")
            f.write("# Main Python script file\n")

        with open(os.path.join(project_dir, project_name, "src", "utils.py"), "w") as f:
            f.write("# Utility functions\n")

        with open(os.path.join(project_dir, project_name, "docs", "README.md"), "w") as f:
            f.write(f"# {project_name}\n\n")
            f.write(f"This project uses Python version {sys.version}\n\n")
            f.write("## Description\n\n")
            f.write("Insert project description here.\n\n")
            f.write("## Usage\n\n")
            f.write("Insert project usage instructions here.\n\n")
            f.write("## License\n\n")
            f.write("Insert project license information here.\n")

        with open(os.path.join(project_dir, project_name, "docs", "design.md"), "w") as f:
            f.write("# Design Document\n\n")
            f.write("Insert design document here.\n")

        with open(os.path.join(project_dir, project_name, "auxiliarylibs_install.py"), "w") as f:
            f.write("# This file is generated automatically by the project folder maker script.\n")
            f.write("# Use this file to install the required auxiliary libraries for this project.\n")
            f.write("# Add the library name and version number to the 'REQUIRED_LIBRARIES' list.\n\n")
            f.write("import subprocess\n\n")
            f.write(f"ENV_NAME = '{env_name}'\n\n")
            f.write("REQUIRED_LIBRARIES = [\n")
            f.write("    # Add library name and version number here, e.g.:\n")
            f.write("    # f'{ENV_NAME}-numpy==1.21.0',\n")
            f.write("    # f'{ENV_NAME}-pandas==1.3.0',\n")
            f.write("]\n\n")
            f.write("for library in REQUIRED_LIBRARIES:\n")
            f.write("    subprocess.call(['pip', 'install', library])\n")

    except OSError:
        messagebox.showerror("Error", f"Failed to create project folders for {project_name}.")
    else:
        messagebox.showinfo("Success", f"Project folders created successfully for {project_name}.")
        subprocess.Popen(['notepad.exe', os.path.join(project_dir, project_name, "auxiliarylibs_install.py")])
        project_name_entry.delete(0, END)
        env_name_entry.delete(0, END)



# Function to handle button click event
def create_project():
    project_name = project_name_entry.get()
    project_dir = filedialog.askdirectory(title="Select project directory")
    env_name = env_name_entry.get()
    custom_folder_name = custom_folder_entry.get()
    create_another = True # Initialize create_another variable here

    if not project_name:
        messagebox.showerror("Error", "Please enter a project name.")
    elif not project_dir:
        messagebox.showerror("Error", "Please select a project directory.")
    else:
        if env_name:
            create_virtual_environment(project_dir, env_name)

        create_project_folders(project_name, project_dir, env_name, custom_folder_name)

        if env_name:
            activate_virtual_environment(project_dir, env_name)

        if create_another:
            project_name_entry.delete(0, END)
            env_name_entry.delete(0, END)
            custom_folder_entry.delete(0, END) # Reset the custom folder field

        else:
            window.destroy()


def create_another_project():
    create_another = messagebox.askyesno("Create Another Project", "Do you want to create another project?")
    if create_another:
        project_name_entry.delete(0, END)
        env_name_entry.delete(0, END)
        custom_folder_entry.delete(0, END) # Reset the custom folder field
    else:
        window.destroy()


def create_virtual_environment(project_dir, env_name):
    venv_path = os.path.join(project_dir, env_name)
    if not os.path.exists(venv_path):
        subprocess.run(["python", "-m", "venv", venv_path])
        messagebox.showinfo("Success", f"Virtual environment created: {env_name}")
    else:
        messagebox.showinfo("Info", f"Virtual environment already exists: {env_name}")


def activate_virtual_environment(project_dir, env_name):
    try:
        activate_script = "Scripts/activate" if os.name == "nt" else "bin/activate"
        subprocess.check_call([os.path.join(project_dir, env_name, activate_script)])
        messagebox.showinfo("Success", f"Virtual environment activated: {env_name}")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", f"Failed to activate virtual environment: {env_name}")


# GUI setup
window = Tk()
window.title("Python Project Folder Maker")
window.geometry("500x600")
window.resizable(width=False, height=False)

# Create a canvas
canvas = Canvas(window, width=500, height=600, bg="#4e4e4e")
canvas.pack(fill=BOTH, expand=YES)

# Place the widgets on the canvas
project_name_label = Label(window, text="Enter project name:", font=("Arial", 12), bg="#4e4e4e", fg="#ffffff", borderwidth=0)
project_name_entry = Entry(window, width=30, font=("Arial", 12))
canvas.create_window(250, 50, window=project_name_label)
canvas.create_window(250, 80, window=project_name_entry)

project_dir_label = Label(window, text="Select project directory:", font=("Arial", 12), bg="#4e4e4e", fg="#ffffff")
project_dir_label_value = Label(window, text="", font=("Arial", 12), bg="#4e4e4e", fg="#ffffff")
project_dir_button = Button(window, text="Browse", font=("Arial", 12), bg="#2c2c2c", fg="#ffffff", activebackground="#404040", activeforeground="#ffffff", command=create_project)
canvas.create_window(250, 130, window=project_dir_label)
canvas.create_window(250, 160, window=project_dir_label_value)
canvas.create_window(250, 190, window=project_dir_button)

increment_project_button = Button(window, text="Increment Project", font=("Arial", 12), bg="#2c2c2c", fg="#ffffff", activebackground="#404040", activeforeground="#ffffff", command=increment_project)
create_project_button = Button(window, text="Create Project", font=("Arial", 12), bg="#2c2c2c", fg="#ffffff", activebackground="#404040", activeforeground="#ffffff", command=create_project)
env_name_label = Label(window, text="Enter environment name (optional):", font=("Arial", 12), bg="#4e4e4e", fg="#ffffff")
env_name_entry = Entry(window, width=30, font=("Arial", 12))
commands_label = Label(window, text="Common Python commands:", font=("Arial", 12), bg="#4e4e4e", fg="#ffffff")
commands_text = Text(window, width=40, height=6, font=("Arial", 12))
canvas.create_window(250, 240, window=increment_project_button)
canvas.create_window(250, 280, window=create_project_button)
canvas.create_window(250, 320, window=env_name_label)
canvas.create_window(250, 360, window=env_name_entry)
canvas.create_window(250, 410, window=commands_label)
canvas.create_window(250, 490, window=commands_text)

commands_text.insert(END, "print()\ninput()\nopen()\nrange()\nlen()\nsum()\nlist()\ndict()\nset()\ntuple()\nint()\nfloat()\nstr()\nbool()\nif...else\nfor...in\nwhile\ntry...except\nraise\nassert\nimport\nfrom...import\nas\ndef\nreturn\nlambda\n\n")

window.mainloop()



