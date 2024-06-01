import unittest
from unittest.mock import patch
from view import GameView
from board import GameBoard

class TestOutput(unittest.TestCase):

    @patch('builtins.print')
    def test_display_start_screen(self, mock_print):
        GameView.display_start_screen()
        mock_print.assert_called()

    @patch('builtins.print')
    def test_display_menu(self, mock_print):
        GameView.display_menu()
        mock_print.assert_called()

    @patch('builtins.print')
    def test_display_message(self, mock_print):
        GameView.display_message("Test message")
        mock_print.assert_called_with("Test message")

    @patch('os.system')
    def test_clear_screen(self, mock_system):
        GameView.clear_screen()
        mock_system.assert_called_once()

    @patch('builtins.input', return_value='test')
    def test_input_prompt(self, mock_input):
        response = GameView.input_prompt("Enter: ")
        mock_input.assert_called_once_with("Enter: ")
        self.assertEqual(response, 'test')

if __name__ == '__main__':
    unittest.main()
