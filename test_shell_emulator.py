import unittest
from shell_emulator import ShellEmulator


class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        self.emulator = ShellEmulator("config.json")

    def test_ls_files(self):
        result = self.emulator.ls([])
        self.assertIn("/home/testuser/file1.txt", result)
        self.assertIn("/home/testuser/file2.txt", result)

    def test_ls_no_files(self):
        self.emulator.current_dir = "/empty_dir"
        result = self.emulator.ls([])
        self.assertEqual(result, "No files found.")

    def test_cd_change_to_absolute(self):
        result = self.emulator.cd(["/home/testuser"])
        self.assertEqual(self.emulator.current_dir, "/home/testuser")
        self.assertIn("Changed to directory", result)

    def test_cd_directory_not_found(self):
        result = self.emulator.cd(["/non_existent_dir"])
        self.assertEqual(result, "Directory '/non_existent_dir' not found.")

    def test_exit(self):
        result = self.emulator.exit_shell([])
        self.assertEqual(result, "Exiting shell.")

    def test_exit_logs_action(self):
        self.emulator.exit_shell([])
        with open(self.emulator.log_file, 'r') as f:
            lines = f.readlines()
            self.assertIn("exit", lines[-1])

    def test_uniq(self):
        input_data = "apple\nbanana\napple\norange"
        result = self.emulator.uniq([input_data])
        self.assertEqual(result, "apple\nbanana\norange")

    def test_uniq_no_input(self):
        result = self.emulator.uniq([])
        self.assertEqual(result, "No input provided.")

    def test_whoami(self):
        result = self.emulator.whoami([])
        self.assertEqual(result, self.emulator.user)

    def test_whoami_config_user(self):
        self.assertEqual(self.emulator.user, "testuser")  # Предполагаем, что в конфиге задано имя 'testuser'

    def test_echo_single(self):
        result = self.emulator.echo(["Hello"])
        self.assertEqual(result, "Hello")

    def test_echo_multiple(self):
        result = self.emulator.echo(["Hello", "world!"])
        self.assertEqual(result, "Hello world!")


if __name__ == '__main__':
    unittest.main()