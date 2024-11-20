import unittest
from shell_emulator import ShellEmulator


class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        self.emulator = ShellEmulator("config.json")

    def test_ls(self):
        result = self.emulator.ls([])
        self.assertIn("/home/testuser/file1.txt", result)
        self.assertIn("/home/testuser/file2.txt", result)
        self.assertNotIn("No files found.", result)

    def test_cd(self):
        result = self.emulator.cd(["home/testuser"])
        self.assertEqual(self.emulator.current_dir, "/home/testuser")

        result = self.emulator.cd([".."])
        self.assertEqual(self.emulator.current_dir, "/home")

        result = self.emulator.cd(["folder"])
        self.assertEqual(result, "Directory 'folder' not found.")

    def test_uniq(self):
        result = self.emulator.uniq(["apple\napple\nbanana\nbanana"])
        self.assertEqual(result, "apple\nbanana")

    def test_whoami(self):
        result = self.emulator.whoami([])
        self.assertEqual(result, "username")

    def test_echo(self):
        result = self.emulator.echo(["Hello", "world!"])
        self.assertEqual(result, "Hello world!")

if __name__ == '__main__':
    unittest.main()