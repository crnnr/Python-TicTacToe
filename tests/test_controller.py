""" This module contains tests for the controller module. """
from datetime import datetime
from unittest.mock import patch, mock_open, MagicMock
import unittest.mock
from controller import GameManager
from board import GameBoard
from player import HumanPlayer, ComputerPlayer


class TestController(unittest.TestCase):
    """ This class contains tests for the GameManager class. """

    def setUp(self):
        """ Set up the GameManager object for unittests """
        self.game_manager = GameManager()
        self.game_manager.players = [MagicMock(), MagicMock()]
        self.game_manager.board = GameBoard()

    def test_start_menu_start_new_game(self):
        """ Test that start_menu calls start_new_game and game_loop"""
        with patch('view.GameView.input_prompt', side_effect=['1']), \
                patch.object(self.game_manager, 'start_new_game') as mock_start_new_game, \
                patch.object(self.game_manager, 'game_loop') as mock_game_loop:
            self.game_manager.start_menu()
            mock_start_new_game.assert_called_once()
            mock_game_loop.assert_called_once()

    def test_start_menu_invalid_number_player(self):
        """ Test that start_menu handles invalid number of players"""
        with patch('view.GameView.input_prompt', side_effect=['3', '1']), \
                patch('view.GameView.display_message') as mock_display_message:
            self.game_manager.start_menu()
            mock_display_message.assert_called_once_with("Invalid choice. Please enter 1 or 2.")

    def test_start_menu_load_game(self):
        """ Test that start_menu calls load_game_state and game_loop"""
        with patch('view.GameView.input_prompt', side_effect=['2']), \
                patch.object(self.game_manager, 'load_game_state') as mock_load_game_state, \
                patch.object(self.game_manager, 'game_loop') as mock_game_loop:
            self.game_manager.start_menu()
            mock_load_game_state.assert_called_once()
            mock_game_loop.assert_called_once()

    @patch('view.GameView.display_menu')
    @patch('view.GameView.input_prompt', return_value='3')
    @patch('builtins.exit', side_effect=SystemExit)
    def test_start_menu_exit(self, mock_exit):
        """ Test that start_menu exits when user selects exit option"""
        with self.assertRaises(SystemExit):
            self.game_manager.start_menu()
        with patch('view.GameView.display_message') as mock_display_message:
            mock_display_message.assert_called_once_with("Thank you for playing. Goodbye!")
        mock_exit.assert_called_once_with(0)

    def test_start_menu_invalid_choice(self):
        """ Test that start_menu handles invalid user input"""
        with patch('view.GameView.input_prompt', side_effect=['4', '3']), \
                patch('view.GameView.display_message') as mock_display_message:
            self.game_manager.start_menu()
            mock_display_message.assert_called_once_with("Invalid choice. Please enter 1, 2, or 3.")

    @patch('os.makedirs')
    def test_create_directory_if_not_exists(self, mock_makedirs):
        """ Test that create_directory_if_not_exists creates the directory """
        GameManager.create_directory_if_not_exists()
        mock_makedirs.assert_called_once_with('savedGames/', exist_ok=True)

    @patch('builtins.open', new_callable=unittest.mock.mock_open,
           read_data='{"board": [], "num_players": 1, "current_turn": "X"}')
    @patch('os.listdir', return_value=['save1.json'])
    @patch('json.load', return_value={"board": "board_state",
           "num_players": 1, "current_turn": "X"})
    def test_load_game_state_success(self, mock_json_load, mock_open):
        """ Test that load_game_state loads the game state from a file"""
        with patch('Output.GameView.input_prompt', return_value='1'):
            self.assertTrue(self.game_manager.load_game_state())
            mock_open.assert_called_once()
            mock_json_load.assert_called_once()

    @patch("os.listdir", return_value=["test_save.json"])
    @patch("builtins.open", new_callable=mock_open,
           read_data='{"board": "state", "num_players": 2, "current_turn": "X"}')
    @patch("json.load", return_value={"board": "state",
           "num_players": 2, "current_turn": "X"})
    def test_load_game_state(self, mock_json_load, mock_file):
        """ Test that load_game_state returns False when no saved games are found """
        with patch("Output.GameView.input_prompt", return_value="1"):
            success = self.game_manager.load_game_state()
        self.assertTrue(success)
        mock_file.assert_called_once_with("savedGames/test_save.json", "r")
        mock_json_load.assert_called_once()

    def test_game_initialization_two_players(self):
        """ Test that start_new_game initializes two HumanPlayer objects """
        with patch("builtins.input", return_value="2"):
            self.game_manager.start_new_game()
            self.assertIsInstance(self.game_manager.players[0], HumanPlayer)
            self.assertIsInstance(self.game_manager.players[0], HumanPlayer)

    def test_game_initialization_single_player(self):
        """ Test that start_new_game initializes one HumanPlayer and one ComputerPlayer"""
        with patch("builtins.input", return_value="1"):
            self.game_manager.start_new_game()
            self.assertIsInstance(self.game_manager.players[0], HumanPlayer)
            self.assertIsInstance(self.game_manager.players[1], ComputerPlayer)

    @patch('view.GameView.input_prompt',
           side_effect=['secret', KeyboardInterrupt])
    def test_start_menu_secret_binary_rain_exit(self, mock_binary_rain):
        """ Test that start_menu exits when user enters 'secret' """
        with self.assertRaises(KeyboardInterrupt):
            self.game_manager.start_menu()
            mock_binary_rain.assert_called_once()

    @patch('controller.GameManager.start_menu')
    @patch('view.GameView.input_prompt', return_value='1')
    @patch('view.GameView.display_message')
    @patch('view.GameView.print_board')
    @patch('board.GameBoard.check_terminal_state',
           return_value=GameBoard.BOARD_PLAYER_X)
    def test_post_game_player_x_wins(
            self,
            mock_check_terminal_state,
            mock_print_board,
            mock_display_message,
            mock_input_prompt,
            mock_start_menu):
        """ Test that post_game displays the correct message when Player X wins """
        self.game_manager.post_game()
        mock_check_terminal_state.assert_called_once()
        mock_print_board.assert_called_once()
        mock_display_message.assert_called()
        mock_input_prompt.assert_called_once_with("Enter your choice: ")
        mock_start_menu.assert_called_once()

    @patch('controller.GameManager.start_menu')
    @patch('view.GameView.input_prompt', return_value='1')
    @patch('view.GameView.display_message')
    @patch('view.GameView.print_board')
    @patch('board.GameBoard.check_terminal_state',
           return_value=GameBoard.BOARD_PLAYER_O)
    def test_post_game_player_o_wins(
            self,
            mock_check_terminal_state,
            mock_print_board,
            mock_display_message,
            mock_input_prompt,
            mock_start_menu):
        """ Test that post_game displays the correct message when Player O wins """
        self.game_manager.post_game()
        mock_check_terminal_state.assert_called_once()
        mock_print_board.assert_called_once()
        mock_display_message.assert_called()
        mock_input_prompt.assert_called_once_with("Enter your choice: ")
        mock_start_menu.assert_called_once()

    @patch('view.GameView.input_prompt', return_value='2')
    @patch('view.GameView.display_message')
    @patch('view.GameView.print_board')
    @patch('board.GameBoard.check_terminal_state',
           return_value=GameBoard.BOARD_PLAYER_O)
    def test_post_game_exit(
            self,
            mock_check_terminal_state,
            mock_print_board,
            mock_display_message,
            mock_input_prompt):
        """ Test that post_game displays the correct message when Player O wins """
        with self.assertRaises(SystemExit):
            self.game_manager.post_game()
        mock_check_terminal_state.assert_called_once()
        mock_print_board.assert_called_once()
        mock_input_prompt.assert_called_once_with("Enter your choice: ")
        # Verify message displayed for Exiting the game
        mock_display_message.assert_any_call("Thank you for playing. Goodbye!")

    @patch('controller.GameManager.post_game')
    def test_post_game_draw(self):
        """ Test that post_game displays the correct message when the game is a draw """
        with patch('view.GameView.input_prompt', return_value='3') as mock_input_prompt:
            self.game_manager.post_game()
            mock_input_prompt.assert_called_once_with("Enter your choice: ")


    def test_post_game_draw_invalid_choice(self):
        """ Test that post_game displays the correct message when invalid choice is entered"""
        with patch('view.GameView.display_message') as mock_display_message:
            self.game_manager.post_game()
            mock_display_message.assert_called_with('Invalid choice. Please enter 1, 2, or 3.')


    @patch('controller.GameManager.post_game')
    @patch('controller.GameManager.save_game_state')
    @patch('board.GameBoard.apply_action')
    @patch('board.GameBoard.check_terminal_state',
           side_effect=[None, None, None, GameBoard.BOARD_PLAYER_X])
    @patch('view.GameView.choose_move', return_value=(GameBoard.BOARD_PLAYER_X, 'save'))
    def test_game_loop_save_game(self, mock_choose_action, mock_check_terminal_state):
        """ Test that game_loop saves the game state when the player chooses to save """
        self.game_manager.game_loop()
        mock_choose_action.assert_called_once()
        mock_check_terminal_state.assert_called_once()
        self.game_manager.save_game_state.assert_called_once()

    def test_game_loop_apply_action(self):
        """ Test that game_loop applies the player's action and checks the terminal state """
        # Set up player action that is not 'save'
        self.game_manager.players[0].choose_action.side_effect = [
            (GameBoard.BOARD_PLAYER_X, 1), (GameBoard.BOARD_PLAYER_X, 2)]

        with patch('view.GameView.clear_screen') as mock_clear_screen:
            self.game_manager.players[0].choose_action.side_effect = [
                (GameBoard.BOARD_PLAYER_X, 1), (GameBoard.BOARD_PLAYER_X, 2)]
            self.game_manager.game_loop()

            # Ensure the action was applied
            self.game_manager.board.apply_action.assert_called_once_with(
                GameBoard.BOARD_PLAYER_X, 1, 2)
            # Ensure the board was cleared and printed twice (before and after
            # the action)
            self.assertEqual(mock_clear_screen.call_count, 2)
            self.assertEqual(self.game_manager.board.print_board.call_count, 2)
            # Check terminal state was evaluated
            self.game_manager.board.check_terminal_state.assert_called_once()
            # Ensure post_game was called due to terminal state or full board
            self.game_manager.post_game.assert_called_once()


    @patch('view.GameView.display_message')
    def test_directory_not_found(self, mock_display_message):
        """ Test that load_game_state handles a FileNotFoundError"""
        self.game_manager.board = GameManager()
        result = self.game_manager.board.load_game_state()
        mock_display_message.assert_called_with("No saved games found.")
        self.assertFalse(result)

    def test_save_game_with_savename(self):
        """ Test that save_game_state with a specific filename"""
        self.game_manager.board = GameManager()
        with patch('builtins.open', new_callable=mock_open) as mock_open:
            # Save the game state with a specific filename without .json extension
            self.game_manager.board.save_game_state("test_save")
            # Assert that open is called with the correct filename and .json extension is appended
            mock_open.assert_called_once_with("savedGames/test_save.json", "w")

    @patch('builtins.input', side_effect=lambda _: '')
    @patch('datetime.datetime', autospec=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('controller.GameManager.start_menu')
    def test_save_game_with_datetime(
            self, mock_start_menu, mock_open, mock_datetime):
        """ Test that save_game_state with default filename format"""
        # Define a specific datetime
        specific_datetime = datetime(2023, 5, 17, 3, 14, 1)  # for example

        # Configure the mock to return this specific datetime when now() is
        # called
        mock_datetime.now.return_value = specific_datetime

        game_manager = GameManager()
        game_manager.save_game_state()

        # Assert that open is called with a filename in the correct format
        mock_open.assert_called_once()
        filename_used = mock_open.call_args[0][0]
        self.assertRegex(
            filename_used,
            r'\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}\.json')

        # Ensure start_menu is not called to prevent the infinite loop
        mock_start_menu.assert_called_once()

    @patch('os.listdir', return_value=['game1.json', 'game2.json'])
    @patch('controller.GameView.input_prompt', return_value='1')
    def test_valid_selection(self):
        """ Test that load_game_state handles valid selection"""
        self.game_manager.board = GameManager()
        # Assuming load_game_state does something with the file that we can check.
        # For now, just checking if False is not returned, indicating
        # processing beyond input.
        with patch('builtins.print'), patch.object(self.game_manager.board, 'start_menu'):
            result = self.game_manager.board.load_game_state()
            self.assertNotEqual(result, False)

    @patch('os.listdir', return_value=['game1.json', 'game2.json'])
    @patch('controller.GameView.display_message')
    def test_list_saved_games(self, mock_display_message):
        """ Test that load_game_state lists saved games"""
        self.game_manager.board = GameManager()
        with patch('builtins.print'), patch.object(self.game_manager.board, 'start_menu'):
            self.game_manager.board.load_game_state()
            mock_display_message.assert_called()

    @patch('os.listdir', return_value=['game1.json', 'game2.json'])
    @patch('controller.GameView.input_prompt', return_value='exit')
    def test_exit_selection_save_game(self, mock_input_prompt, mock_listdir):
        """ Test that load_game_state handles exit selection"""
        self.game_manager.board = GameManager()
        with patch('builtins.print'), patch.object(self.game_manager.board, 'start_menu'):
            result = self.game_manager.board.load_game_state()
            self.assertFalse(result)

    @patch('os.listdir')
    @patch('json.load')
    @patch('controller.GameView')
    @patch('controller.GameBoard')
    @patch('controller.HumanPlayer')
    @patch('controller.ComputerPlayer')
    def test_load_game_state(self,
                            mock_computer_player,
                            mock_human_player,
                            mock_game_board,
                            mock_game_view,
                            mock_json_load,
                            mock_os_listdir):
        """ Test that load_game_state loads the game state from a file """
        # Mock the behavior of os.listdir
        mock_os_listdir.return_value = ['game1', 'game2']
        # Mock the behavior of json.load
        mock_json_load.return_value = {
            'board': 'mock_board',
            'num_players': 2,
            'current_turn': 'X'
        }
        # Mock the behavior of GameView.input_prompt
        mock_game_view.input_prompt.return_value = '1'
        self.game_manager.board = GameManager()
        result = self.game_manager.board.load_game_state()
        self.assertTrue(result)

        # Assert that the correct methods were called with the correct arguments
        mock_os_listdir.assert_called_once_with('savedGames')
        mock_game_view.input_prompt.assert_called_once_with("Enter the number of the game you want to load('exit' to return to main menu): ")
        mock_json_load.assert_called_once()
        mock_game_board.assert_called_once()
        mock_human_player.assert_called()
        mock_computer_player.assert_not_called()

    @patch('os.listdir')
    @patch('controller.GameView')
    def test_load_game_state_no_saved_games(self, mock_game_view, mock_os_listdir):
        """ Test that load_game_state returns False when no saved games are availabl """
        # Mock the behavior of os.listdir
        mock_os_listdir.return_value = []
        self.game_manager.board = GameManager()
        result = self.game_manager.board.load_game_state()
        self.assertFalse(result)
        # Assert that the correct methods were called with the correct arguments
        mock_os_listdir.assert_called_once_with('savedGames')
        mock_game_view.display_message.assert_called_once_with("No saved games found.")

    @patch('os.listdir', side_effect=FileNotFoundError)
    @patch('controller.GameView')
    def test_load_game_state_no_saved_games_directory(self, mock_game_view, mock_os_listdir):
        """ Test that load_game_state returns False when no saved games directory is found """
        self.game_manager.board = GameManager()
        result = self.game_manager.board.load_game_state()
        self.assertFalse(result)
        # Assert that "No saved games directory found." is displayed
        mock_os_listdir.assert_called_once_with('savedGames')
        mock_game_view.display_message.assert_called_once_with("No saved games directory found.")

    @patch('os.listdir', return_value=['game1.json', 'game2.json'])
    @patch('view.GameView.input_prompt', return_value='3')
    @patch('view.GameView.display_message')
    def test_invalid_selection_save_game(self, mock_input_prompt,
                                         mock_listdir,
                                         mock_display_message):
        """ Test that load_game_state handles invalid selection"""
        self.game_manager.board = GameManager()
        result = self.game_manager.board.load_game_state()
        self.assertFalse(result)
        #Assert that "Invalid selection." is displayed
        mock_input_prompt.assert_called_once()
        mock_listdir.assert_called_once()
        mock_display_message.assert_called_with("Invalid selection.")

if __name__ == '__main__':
    unittest.main()
