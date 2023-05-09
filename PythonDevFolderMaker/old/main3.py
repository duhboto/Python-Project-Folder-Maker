import os
import re
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

class ProjectFolderMaker:
    def __init__(self, master):
        self.master = master
        master.title("Python Project Folder Maker")

        # Labels
        self.label_project_name = tk.Label(master, text="Enter project name:")
        self.label_project_name.grid(row=0, column=0, sticky="w")

        self.label_project_dir = tk.Label(master, text="Select project directory:")
        self.label_project_dir.grid(row=1, column=0, sticky="w")

        self.label_env_name = tk.Label(master, text="Enter environment name (optional):")
        self.label_env_name.grid(row=2, column=0, sticky="w")

        self.label_custom_text = tk.Label(master, text="Enter custom text to append to project (optional):")
        self.label_custom_text.grid(row=3, column=0, sticky="w")

        self.label_commands = tk.Label(master, text="Common Python commands:")
        self.label_commands.grid(row=4, column=0, sticky="w")

        # Entry fields
        self.entry_project_name = tk.Entry(master)
        self.entry_project_name.grid(row=0, column=1)

        self.entry_project_dir = tk.Entry(master)
        self.entry_project_dir.grid(row=1, column=1)

        self.entry_env_name = tk.Entry(master)
        self.entry_env_name.grid(row=2, column=1)

        self.entry_custom_text = tk.Entry(master)
        self.entry_custom_text.grid(row=3, column=1)

        self.text_commands = tk.Text(master, height=6, width=40)
        self.text_commands.grid(row=4, column=1)

        # Buttons
        self.button_browse = tk.Button(master, text="Browse", command=self.browse_project_dir)
        self.button_browse.grid(row=1, column=2)

        self.button_increment = tk.Button(master, text="Increment Project", command=self.increment_project)
        self.button_increment.grid(row=0, column=2)

        self.button_create = tk.Button(master, text="Create Project", command=self.create_project)
        self.button_create.grid(row=5, column=1)

    def browse_project_dir(self):
        directory = filedialog.askdirectory()
        self.entry_project_dir.delete(0, tk.END)
        self.entry_project_dir.insert(0, directory)

    def increment_project(self):
        project_name = self.entry_project_name.get()
        regex_pattern = r"(.*)\.(\d+)$"
        match = re.match(regex_pattern, project_name)
        if match:
            project_name, version = match.groups()
            new_version = int(version) + 1
            self.entry_project_name.delete(0, tk.END)
            self.entry_project_name.insert(0, f"{project_name}.{new_version}")
        else:
            self.entry_project_name.insert(tk.END, ".1")

    def create_project(self):
        project_name = self.entry_project_name.get()
        project_dir = self.entry_project_dir.get()
        env_name = self.entry_env_name.get()
        custom_text = self.entry_custom_text.get()
        commands = self.text_commands.get("1.0", "end-1c").split("\n")

        # Check if project directory exists
        if not os.path.exists(project_dir):
            messagebox.showerror("Error", "Project directory does not exist.")
            return

        # Create project directory
        project_path = os.path.join(project_dir, f"{project_name}{custom_text}")
        try:
            os.mkdir(project_path)
        except FileExistsError:
            messagebox.showerror("Error", "Project directory already exists.")
            return

        # Create subdirectories
        subdirectories = ["src", "data/input", "data/output", "tests", "docs"]
        for subdirectory in subdirectories:
            os.mkdir(os.path.join(project_path, subdirectory))

        # Create virtual environment
        if env_name:
            env_path = os.path.join(project_path, env_name)
            subprocess.run(["python", "-m", "venv", env_path], check=True)

        # Create files
        main_py = os.path.join(project_path, "src/main.py")
        with open(main_py, "w") as f:
            f.write("# Main script")

        utils_py = os.path.join(project_path, "src/utils.py")
        with open(utils_py, "w") as f:
            f.write("# Utility functions")

        readme_md = os.path.join(project_path, "docs/README.md")
        with open(readme_md, "w") as f:
            f.write(f"# {project_name}\n\nThis is a Python project named {project_name}.")

        design_md = os.path.join(project_path, "docs/design.md")
        with open(design_md, "w") as f:
            f.write("# Design document")

        auxiliarylibs_install_py = os.path.join(project_path, "auxiliarylibs_install.py")
        with open(auxiliarylibs_install_py, "w") as f:
            f.write("# Install auxiliary libraries")

        # Run commands
        os.chdir(project_path)
        for command in commands:
            subprocess.run(command.split(), check=True)

        # Show success message
        messagebox.showinfo("Success", "Project folder structure and auxiliary files created successfully.")
if __name__ == '__main__':
    root = tk.Tk()
    app = ProjectFolderMaker(root)
    root.mainloop()
