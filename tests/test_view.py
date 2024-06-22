""" Test the output functions of the GameView class """
import unittest
from unittest.mock import patch, Mock
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

    @patch('builtins.print')
    def test_print_board(self, mock_print):
        """ Test the print_board method """
        # Create a mock board object with the required attributes
        mock_board = Mock()
        mock_board.BOARD_PLAYER_X = 'X'
        mock_board.BOARD_PLAYER_O = 'O'
        mock_board.BOARD_EMPTY = ' '
        # Define the board layout
        mock_board.board = [
            mock_board.BOARD_PLAYER_X, mock_board.BOARD_PLAYER_O, mock_board.BOARD_PLAYER_X,
            mock_board.BOARD_PLAYER_O, mock_board.BOARD_PLAYER_X, mock_board.BOARD_PLAYER_O,
            mock_board.BOARD_PLAYER_X, mock_board.BOARD_PLAYER_O, mock_board.BOARD_PLAYER_X
        ]

        # Call the print_board method with the board layout
        GameView.print_board(mock_board)

        # Check that print was called (at least once)
        mock_print.assert_called()

    @patch('builtins.input', side_effect=['save'])
    @patch('builtins.print')
    def test_choose_move_save(self, mock_print, mock_input):
        """ Test the choose_move method when the user chooses to save """
        mock_board = Mock()
        mock_board.board = [' '] * 9
        mock_board.BOARD_EMPTY = ' '
        mock_player = Mock()
        mock_player.player_type = 'X'

        result = GameView.choose_move(mock_board, mock_player)
        mock_print.assert_any_call("To save the game, type 'save' at any time. \n")
        mock_print.assert_any_call("X's turn.")
        mock_input.assert_any_call('Enter row [1-3]: ')
        self.assertEqual(result, 'save')

    @patch('builtins.input', side_effect=['1', '1'])
    @patch('builtins.print')
    def test_choose_move_valid(self, mock_print, mock_input):
        """ Test the choose_move method with a valid move """
        mock_board = Mock()
        mock_board.board = [' '] * 9
        mock_board.BOARD_EMPTY = ' '
        mock_player = Mock()
        mock_player.player_type = 'X'

        result = GameView.choose_move(mock_board, mock_player)
        mock_print.assert_any_call("To save the game, type 'save' at any time. \n")
        mock_print.assert_any_call("X's turn.")
        mock_input.assert_any_call('Enter row [1-3]: ')
        mock_input.assert_any_call('Enter column [1-3]: ')
        self.assertEqual(result, ('1', '1'))

    @patch('builtins.input', side_effect=['1', '1', '2', '2'])
    @patch('builtins.print')
    def test_choose_move_taken_space(self, mock_print, mock_input):
        """ Test the choose_move method when the chosen space is already taken """
        mock_board = Mock()
        mock_board.board = ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        mock_board.BOARD_EMPTY = ' '
        mock_player = Mock()
        mock_player.player_type = 'X'

        result = GameView.choose_move(mock_board, mock_player)
        mock_print.assert_any_call("To save the game, type 'save' at any time. \n")
        mock_print.assert_any_call("X's turn.")
        mock_print.assert_any_call("Space already taken. Try again.")
        mock_input.assert_any_call('Enter row [1-3]: ')
        mock_input.assert_any_call('Enter column [1-3]: ')
        self.assertEqual(result, ('2', '2'))

    @patch('builtins.input', side_effect=['4', 'save'])
    @patch('builtins.print')
    def test_choose_move_invalid_row_high(self, mock_print, mock_input):
        """ Test the choose_move method with an invalid row input (too high) """
        mock_board = Mock()
        mock_board.board = [' '] * 9
        mock_board.BOARD_EMPTY = ' '
        mock_player = Mock()
        mock_player.player_type = 'X'
        result = GameView.choose_move(mock_board, mock_player)
        mock_print.assert_any_call("To save the game, type 'save' at any time. \n")
        mock_print.assert_any_call("X's turn.")
        mock_print.assert_any_call("Invalid input. Please enter a number between 1 to 3.")
        mock_input.assert_any_call('Enter row [1-3]: ')
        self.assertEqual(result, 'save')

    @patch('builtins.input', side_effect=['0', 'save'])
    @patch('builtins.print')
    def test_choose_move_invalid_row_low(self, mock_print, mock_input):
        """ Test the choose_move method with an invalid row input (too low) """
        mock_board = Mock()
        mock_board.board = [' '] * 9
        mock_board.BOARD_EMPTY = ' '
        mock_player = Mock()
        mock_player.player_type = 'X'
        result = GameView.choose_move(mock_board, mock_player)
        mock_print.assert_any_call("To save the game, type 'save' at any time. \n")
        mock_print.assert_any_call("X's turn.")
        mock_print.assert_any_call("Invalid input. Please enter a number between 1 to 3.")
        mock_input.assert_any_call('Enter row [1-3]: ')
        self.assertEqual(result, 'save')

    @patch('builtins.input', side_effect=['1', '4', 'save'])
    @patch('builtins.print')
    def test_choose_move_invalid_column_high(self, mock_print, mock_input):
        """ Test the choose_move method with an invalid column input (too high) """
        mock_board = Mock()
        mock_board.board = [' '] * 9
        mock_board.BOARD_EMPTY = ' '
        mock_player = Mock()
        mock_player.player_type = 'X'
        result = GameView.choose_move(mock_board, mock_player)
        mock_print.assert_any_call("To save the game, type 'save' at any time. \n")
        mock_print.assert_any_call("X's turn.")
        mock_print.assert_any_call("Invalid input. Please enter a number between 1 to 3.")
        mock_input.assert_any_call('Enter column [1-3]: ')
        self.assertEqual(result, 'save')

    @patch('builtins.input', side_effect=['1', '0', 'save'])
    @patch('builtins.print')
    def test_choose_move_invalid_column_low(self, mock_print, mock_input):
        """ Test the choose_move method with an invalid column input (too low) """
        mock_board = Mock()
        mock_board.board = [' '] * 9
        mock_board.BOARD_EMPTY = ' '
        mock_player = Mock()
        mock_player.player_type = 'X'
        result = GameView.choose_move(mock_board, mock_player)
        mock_print.assert_any_call("To save the game, type 'save' at any time. \n")
        mock_print.assert_any_call("X's turn.")
        mock_print.assert_any_call("Invalid input. Please enter a number between 1 to 3.")
        mock_input.assert_any_call('Enter column [1-3]: ')
        self.assertEqual(result, 'save')

    @patch('builtins.input', side_effect=['1', 'a', 'save'])
    @patch('builtins.print')
    def test_choose_move_invalid_row_non_digit(self, mock_print, mock_input):
        """ Test the choose_move method with a non-digit row input """
        mock_board = Mock()
        mock_board.board = [' '] * 9
        mock_board.BOARD_EMPTY = ' '
        mock_board.is_valid_move.return_value = True
        mock_player = Mock()
        mock_player.player_type = 'X'
        result = GameView.choose_move(mock_board, mock_player)
        mock_print.assert_any_call("To save the game, type 'save' at any time. \n")
        mock_print.assert_any_call("X's turn.")
        mock_print.assert_any_call("Invalid input. Please enter a number between 1 to 3.")
        mock_input.assert_any_call('Enter column [1-3]: ')
        self.assertEqual(result, 'save')

if __name__ == '__main__':
    unittest.main()
