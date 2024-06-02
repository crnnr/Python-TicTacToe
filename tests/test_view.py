""" Test the output functions of the GameView class """
import unittest
from unittest.mock import patch
from view import GameView

class TestOutput(unittest.TestCase):
    """ Test the output functions of the GameView class """

    @patch('builtins.print')
    def test_display_start_screen(self, mock_print):
        """ Test the display_start_screen method"""
        GameView.display_start_screen()
        mock_print.assert_called()

    @patch('builtins.print')
    def test_display_menu(self, mock_print):
        """ Test the display_menu method """
        GameView.display_menu()
        mock_print.assert_called()

    @patch('builtins.print')
    def test_display_message(self, mock_print):
        """ Test the display_message method """
        GameView.display_message("Test message")
        mock_print.assert_called_with("Test message")

    @patch('os.system')
    def test_clear_screen(self, mock_system):
        """ Test the clear_screen method """
        GameView.clear_screen()
        mock_system.assert_called_once()

    @patch('builtins.input', return_value='test')
    def test_input_prompt(self, mock_input):
        """ Test the input_prompt method """
        response = GameView.input_prompt("Enter: ")
        mock_input.assert_called_once_with("Enter: ")
        self.assertEqual(response, 'test')

    @patch('builtins.input', return_value='1')
    def test_choose_action(self, mock_input):
        """ Test the choose_action method """
        mock_input.side_effect = ['1']
        response = GameView.choose_action()
        self.assertEqual(response, '1')
        mock_input.assert_called()

    @patch('builtins.print')
    def print_board(self, mock_print):
        """ Test the print_board method """
        board = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X']
        GameView.print_board(board)
        mock_print.assert_called()

if __name__ == '__main__':
    unittest.main()
    