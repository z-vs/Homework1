import os
import tarfile
import json
import unittest
from shell_emulator import ShellEmulator

class TestShellEmulator(unittest.TestCase):

    def setUp(self):
        self.config_data = {
            "user": "username",
            "fs_archive": "C:\\Users\\zvs11\\config1p.tar",
            "log_file": "C:\\Users\\zvs11\\log.csv"
        }

        with open("test_config.json", 'w') as f:
            json.dump(self.config_data, f)

        with tarfile.open("C:\\Users\\zvs11\\config1p.tar", "w") as tar:
            dummy_file = tarfile.TarInfo(name="dummy_file.txt")
            dummy_file.size = 0
            tar.addfile(dummy_file)

        self.emulator = ShellEmulator("test_config.json")

    def tearDown(self):
        os.remove("test_config.json")

    def test_ls(self):
        self.emulator.current_dir = "/"
        result = self.emulator.ls([])
        expected = "dummy_file.txt"
        self.assertEqual(result, expected)

    def test_ls_no_files(self):
        self.emulator.current_dir = "/nonexistent"
        result = self.emulator.ls([])
        expected = "No directories found."
        self.assertEqual(result, expected)

    def test_cd_valid_directory(self):
        self.emulator.current_dir = "/"
        result = self.emulator.cd(["dummy_file.txt"])
        expected = "Changed to directory /dummy_file.txt"
        self.assertEqual(result, expected)

    def test_cd_invalid_directory(self):
        self.emulator.current_dir = "/"
        result = self.emulator.cd(["nonexistent_dir"])
        expected = "Directory 'nonexistent_dir' not found."
        self.assertEqual(result, expected)

    def test_exit(self):
        self.emulator.current_dir = "/"
        result = self.emulator.exit_shell([])
        expected = "Exiting shell."
        self.assertEqual(result, expected)

    def test_exit_logs(self):
        self.emulator.exit_shell([])
        with open(self.config_data['log_file'], 'r') as log:
            log_content = log.readlines()
        self.assertTrue("exit" in log_content[-1])

    def test_uniq(self):
        result = self.emulator.uniq(["line1\nline2\nline1"])
        expected = "line1\nline2"
        self.assertEqual(result, expected)

    def test_uniq_empty_input(self):
        result = self.emulator.uniq([""])
        expected = ""
        self.assertEqual(result, expected)

    def test_whoami(self):
        result = self.emulator.whoami([])
        expected = "username"
        self.assertEqual(result, expected)

    def test_whoami_empty(self):
        result = self.emulator.whoami([])
        expected = "username"
        self.assertEqual(result, expected)

    def test_echo(self):
        result = self.emulator.echo(["Hello", "world!"])
        expected = "Hello world!"
        self.assertEqual(result, expected)

    def test_echo_empty(self):
        result = self.emulator.echo([])
        expected = ""
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
