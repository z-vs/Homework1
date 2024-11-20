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


if __name__ == '__main__':
    unittest.main()