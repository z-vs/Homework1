import os
import tarfile
import json
import csv
import tkinter as tk
from tkinter import scrolledtext


class ShellEmulator:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.user = self.config['user']
        self.fs_archive = self.config['fs_archive']
        self.log_file = self.config['log_file']

        self.current_dir = "/"
        self.fs = self.load_filesystem()
        self.commands = {
            'ls': self.ls,
            'cd': self.cd,
            'exit': self.exit_shell,
            'uniq': self.uniq,
            'whoami': self.whoami,
            'echo': self.echo,
        }

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            return json.load(f)

    def load_filesystem(self):
        fs = {}
        with tarfile.open(self.fs_archive, 'r') as tar:
            for member in tar.getmembers():
                if member.isfile():
                    file_content = tar.extractfile(member).read().decode('utf-8')
                    fs[member.name] = file_content
        return fs

    def log_action(self, action):
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([self.user, action])

    def execute_command(self, command):
        command = command.strip().split(' ', 1)[-1]

        parts = command.split(' ', 1)
        cmd = parts[0]

        args = parts[1:] if len(parts) > 1 else []

        if cmd in self.commands:
            return self.commands[cmd](args)
        else:
            return f"Unknown command: {cmd}"

    def ls(self, args):
        dirs = set()
        for file in self.fs:
            file_parts = file.lstrip('/').split('/')
            if file.startswith(self.current_dir.lstrip('/')):
                parts_after_current_dir = file.lstrip(self.current_dir.lstrip('/')).strip('/')

                if '/' in parts_after_current_dir:
                    sub_dir = parts_after_current_dir.split('/')[0]
                    dirs.add(sub_dir)
                elif len(parts_after_current_dir) > 0:
                    dirs.add(parts_after_current_dir)

        if dirs:
            return "\n".join(sorted(dirs))
        else:
            return "No directories found."

    def cd(self, args):
        if not args:
            return "No directory specified."

        target_dir = args[0]

        if target_dir.startswith("/"):
            self.current_dir = target_dir
        else:
            if target_dir == "..":
                self.current_dir = os.path.dirname(self.current_dir.rstrip('/'))
                if self.current_dir == "":
                    self.current_dir = "/"
            else:
                new_dir = os.path.join(self.current_dir, target_dir)
                if any(file.startswith(new_dir.lstrip('/')) for file in self.fs):
                    self.current_dir = new_dir
                else:
                    return f"Directory '{target_dir}' not found."

        if self.current_dir.startswith("./"):
            self.current_dir = "/" + self.current_dir[2:]

        if self.current_dir == "":
            self.current_dir = "/"

        return f"Changed to directory {self.current_dir}"


    def exit_shell(self, args):
        self.log_action("exit")
        return "Exiting shell."

    def uniq(self, args):
        if not args:
            return "No file name provided."

        filename = args[0]
        if filename not in self.fs:
            return f"File '{filename}' not found."
        file_content = self.fs[filename]
        lines = file_content.splitlines()
        unique_lines = sorted(set(lines))
        output = "\n".join(unique_lines)
        return output

    def whoami(self, args):
        return self.user

    def echo(self, args):
        return " ".join(args)

class ShellGUI(tk.Tk):
    def __init__(self, emulator):
        super().__init__()
        self.emulator = emulator
        self.title(f"Shell Emulator - {self.emulator.user}")
        self.geometry("600x400")

        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=20, width=70)
        self.output_text.grid(row=0, column=0, padx=10, pady=10)
        self.output_text.config(state=tk.DISABLED)

        self.input_text = tk.Entry(self, width=70)
        self.input_text.grid(row=1, column=0, padx=10, pady=10)
        self.input_text.bind("<Return>", self.on_enter)

        self.display_prompt()

    def display_prompt(self):
        prompt = f"{self.emulator.user}@shell:{self.emulator.current_dir}$ "
        self.input_text.delete(0, tk.END)
        self.input_text.insert(tk.END, prompt)
        self.input_text.focus()

    def on_enter(self, event):
        command = self.input_text.get()
        if command:
            self.output_text.config(state=tk.NORMAL)
            output = self.emulator.execute_command(command)
            self.output_text.insert(tk.END, f"{command}\n{output}\n")
            self.output_text.config(state=tk.DISABLED)
            self.emulator.log_action(command)
        self.display_prompt()


def main():
    emulator = ShellEmulator("config.json")
    app = ShellGUI(emulator)
    app.mainloop()


if __name__ == "__main__":
    main()