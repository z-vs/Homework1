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
        files_in_dir = [
            file for file in self.fs if file.startswith(self.current_dir.lstrip('/'))
        ]

        if files_in_dir:
            return "\n".join([f"/{file}" for file in files_in_dir])
        else:
            return "No files found."

    def cd(self, args):
        if not args:
            return "No directory specified."

        target_dir = args[0]

        if target_dir == "..":
            self.current_dir = os.path.dirname(self.current_dir.rstrip('/'))
            if self.current_dir == "":
                self.current_dir = "/"
        else:
            if target_dir.startswith("/"):
                self.current_dir = target_dir
            else:
                new_dir = os.path.join(self.current_dir, target_dir)

                if any(file.startswith(new_dir.lstrip('/')) for file in self.fs):
                    self.current_dir = new_dir
                else:
                    return f"Directory '{target_dir}' not found."

        if self.current_dir.startswith("./"):
            self.current_dir = "/" + self.current_dir[2:]

        return f"Changed to directory {self.current_dir}"

    def exit_shell(self, args):
        self.log_action("exit")
        return "Exiting shell."

    def uniq(self, args):
        if not args:
            return "No input provided."
        input_data = args[0]
        output = "\n".join(sorted(set(input_data.split('\n'))))
        return output

    def whoami(self, args):
        return self.user

    def echo(self, args):
        return " ".join(args)