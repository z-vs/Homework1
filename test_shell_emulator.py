from shell_emulator import ShellEmulator
import unittest
from io import StringIO
from unittest.mock import patch

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        self.emulator = ShellEmulator("config.json")

    @patch('sys.stdout', new_callable=StringIO)
    def test_ls_directories(self, mock_stdout):
        self.emulator.current_dir = '/'
        output = self.emulator.ls([])
        self.assertIn('etc', output)
        self.assertIn('home', output)
        self.assertIn('tmp', output)
        self.assertIn('example.txt', output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_ls_home_directory(self, mock_stdout):
        self.emulator.current_dir = '/home'
        output = self.emulator.ls([])
        self.assertIn('testuser', output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_ls_testuser_directory(self, mock_stdout):
        self.emulator.current_dir = '/home/testuser'
        output = self.emulator.ls([])
        self.assertIn('file1.txt', output)
        self.assertIn('file2.txt', output)

    def test_cd_to_home(self):
        self.emulator.current_dir = '/'
        output = self.emulator.cd(['home'])
        self.assertEqual(self.emulator.current_dir, '/home')
        self.assertEqual(output, "Changed to directory /home")

    def test_cd_to_nonexistent_directory(self):
        self.emulator.current_dir = '/'
        output = self.emulator.cd(['nonexistent'])
        self.assertEqual(output, "Directory 'nonexistent' not found.")

    @patch('sys.stdout', new_callable=StringIO)
    def test_uniq_example_file(self, mock_stdout):
        self.emulator.fs = {
            '/example.txt': "line1\nline2\nline1\nline3\nline2"
        }
        output = self.emulator.uniq(['/example.txt'])
        self.assertEqual(output, "line1\nline2\nline3")

    def test_uniq_file_not_found(self):
        output = self.emulator.uniq(['/nonexistent.txt'])
        self.assertEqual(output, "File '/nonexistent.txt' not found.")

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

    def test_exit(self):
        self.emulator.current_dir = "/"
        result = self.emulator.exit_shell([])
        expected = "Exiting shell."
        self.assertEqual(result, expected)

    def test_exit_logs(self):
        self.emulator.exit_shell([])
        with open(self.emulator.log_file, 'r') as log:
            log_content = log.readlines()
        self.assertTrue("exit" in log_content[-1], f"Expected 'exit' to be in the last log entry, but got {log_content[-1]}")

if __name__ == '__main__':
    unittest.main()
