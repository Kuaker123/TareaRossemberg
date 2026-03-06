import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import subprocess

# It's better to import the script to be tested
import AITool_Phishing

class TestAIToolPhishing(unittest.TestCase):

    @patch('AITool_Phishing.subprocess.run')
    def test_run_command_success(self, mock_run):
        """Test that run_command returns True on successful command execution."""
        mock_run.return_value = MagicMock(returncode=0)
        result = AITool_Phishing.run_command("echo 'success'")
        self.assertTrue(result)

    @patch('AITool_Phishing.subprocess.run')
    def test_run_command_failure(self, mock_run):
        """Test that run_command returns False on failed command execution."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "cmd", stderr=b"error")
        result = AITool_Phishing.run_command("invalid_command")
        self.assertFalse(result)

    @patch('builtins.input', return_value='/tmp')
    @patch('pathlib.Path.is_dir', return_value=True)
    def test_get_install_path_valid(self, mock_is_dir, mock_input):
        """Test get_install_path with a valid directory."""
        path = AITool_Phishing.get_install_path()
        self.assertEqual(path, Path('/tmp'))

    @patch('builtins.input', side_effect=['invalid_path', '/tmp'])
    @patch('pathlib.Path.is_dir', side_effect=[False, True])
    @patch('builtins.print')
    def test_get_install_path_invalid_then_valid(self, mock_print, mock_is_dir, mock_input):
        """Test get_install_path with an invalid path followed by a valid one."""
        path = AITool_Phishing.get_install_path()
        self.assertEqual(path, Path('/tmp'))
        mock_print.assert_called_with(f"{AITool_Phishing.RED}La ruta especificada no es un directorio válido. Inténtelo de nuevo.{AITool_Phishing.END}")

    @patch('AITool_Phishing.run_command', return_value=True)
    @patch('pathlib.Path.exists', return_value=False)
    def test_install_tool_clone_and_install(self, mock_exists, mock_run_command):
        """Test install_tool clones and installs a new tool."""
        success, path = AITool_Phishing.install_tool("Zphisher (Modern & Stable)", Path("/fake/dir"))
        self.assertTrue(success)
        self.assertEqual(path, Path("/fake/dir/Zphisher (Modern & Stable)"))
        mock_run_command.assert_any_call("git clone https://github.com/htr-tech/zphisher.git /fake/dir/Zphisher (Modern & Stable)")
        mock_run_command.assert_any_call("chmod +x zphisher.sh", cwd=Path("/fake/dir/Zphisher (Modern & Stable)"))


    @patch('AITool_Phishing.run_command', return_value=True)
    @patch('pathlib.Path.exists', return_value=True)
    def test_install_tool_skip_clone(self, mock_exists, mock_run_command):
        """Test install_tool skips cloning if the directory exists."""
        success, path = AITool_Phishing.install_tool("Zphisher (Modern & Stable)", Path("/fake/dir"))
        self.assertTrue(success)
        # git clone should not be called
        self.assertNotIn('git clone', [call[0][0] for call in mock_run_command.call_args_list])


    @patch('AITool_Phishing.run_command', return_value=False)
    @patch('pathlib.Path.exists', return_value=False)
    def test_install_tool_clone_fails(self, mock_exists, mock_run_command):
        """Test install_tool handles git clone failure."""
        success, path = AITool_Phishing.install_tool("Zphisher (Modern & Stable)", Path("/fake/dir"))
        self.assertFalse(success)
        self.assertIsNone(path)

    @patch('builtins.input', return_value='y')
    @patch('AITool_Phishing.run_command', return_value=True)
    def test_execute_tool_yes(self, mock_run_command, mock_input):
        """Test execute_tool runs the tool when the user says yes."""
        AITool_Phishing.execute_tool("Zphisher (Modern & Stable)", Path("/fake/dir/Zphisher (Modern & Stable)"))
        mock_run_command.assert_called_with("./zphisher.sh", cwd=Path("/fake/dir/Zphisher (Modern & Stable)"))

    @patch('builtins.input', return_value='n')
    @patch('AITool_Phishing.run_command')
    def test_execute_tool_no(self, mock_run_command, mock_input):
        """Test execute_tool does not run the tool when the user says no."""
        AITool_Phishing.execute_tool("Zphisher (Modern & Stable)", Path("/fake/dir/Zphisher (Modern & Stable)"))
        mock_run_command.assert_not_called()

    @patch('shutil.which', return_value='/usr/bin/git')
    def test_check_dependencies_git_exists(self, mock_which):
        """Test check_dependencies when git is installed."""
        try:
            AITool_Phishing.check_dependencies()
        except SystemExit:
            self.fail("check_dependencies() exited unexpectedly.")

    @patch('shutil.which', return_value=None)
    @patch('builtins.print')
    def test_check_dependencies_git_missing(self, mock_print, mock_which):
        """Test check_dependencies when git is not installed."""
        with self.assertRaises(SystemExit) as cm:
            AITool_Phishing.check_dependencies()
        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_called_with(f"{AITool_Phishing.RED}Error: Git no está instalado. Por favor, instálelo para continuar.{AITool_Phishing.END}")


if __name__ == '__main__':
    unittest.main()
