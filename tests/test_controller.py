""" This module contains tests for the controller module. """
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock
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

    @patch('view.GameView.input_prompt', return_value='3')
    @patch('view.GameView.display_message')
    def test_start_game_invalid_number_player(self, mock_display_message, mock_input_prompt):
        """ Test that start_menu handles invalid number of players"""
        self.game_manager.start_new_game()
        mock_input_prompt.assert_called_with('Enter number of players [1-2]: ')
        mock_display_message.assert_called_with("Invalid number of players. \
                                     Defaulting to 1 player mode.")

    def test_start_menu_load_game(self):
        """ Test that start_menu calls load_game_state and game_loop"""
        with patch('view.GameView.input_prompt', side_effect=['2']), \
                patch.object(self.game_manager, 'load_game_state') as mock_load_game_state, \
                patch.object(self.game_manager, 'game_loop') as mock_game_loop:
            self.game_manager.start_menu()
            mock_load_game_state.assert_called_once()
            mock_game_loop.assert_called_once()

    @patch('view.GameView.display_message')
    @patch('view.GameView.input_prompt', side_effect=['3'])
    def test_start_menu_exit(self, mock_input_prompt, mock_display_message):
        """ Test that start_menu exits when user selects exit option"""
        with self.assertRaises(SystemExit):
            self.game_manager.start_menu()
        mock_display_message.assert_called_once_with("Thank you for playing. Goodbye!")
        mock_input_prompt.assert_called_once_with("Enter your choice [1-3]: ")

    def test_start_menu_invalid_choice(self):
        """ Test that start_menu handles invalid user input"""
        with patch('view.GameView.input_prompt', side_effect=['4', '3']), \
                patch('view.GameView.display_message') as mock_display_message, \
                    self.assertRaises(SystemExit):
            self.game_manager.start_menu()
            mock_display_message.assert_called_with("Invalid choice. Please enter 1, 2, or 3.")

    @patch('pathlib.Path.mkdir')
    def test_create_directory_if_not_exists(self, mock_makedirs):
        """ Test that create_directory_if_not_exists creates the directory """
        GameManager.create_directory_if_not_exists()
        mock_makedirs.assert_called_once_with(parents=True, exist_ok=True)

    @patch('builtins.open', new_callable=unittest.mock.mock_open,
           read_data='{"board": [], "num_players": 1, "current_turn": "X"}')
    @patch('os.listdir', return_value=['save1.json'])
    @patch('json.load', return_value={"board": "board_state",
           "num_players": 1, "current_turn": "X"})
    def test_load_game_state_success(self, mock_json_load, mock_os_listdir, mock_open):
        """ Test that load_game_state loads the game state from a file"""
        with patch('view.GameView.input_prompt', return_value='1'):
            self.assertTrue(self.game_manager.load_game_state())
            mock_open.assert_called_once()
            mock_json_load.assert_called_once()
            mock_os_listdir.assert_called_once()

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

    # def test_binary_rain(self):
    #     """ Test the binary_rain method
    #     Test this method by raising a KeyboardInterrupt exception (Ctrl+C)"""
    #     self.game_manager.binary_rain()

    @patch('controller.GameManager.game_loop')
    @patch('controller.GameManager.start_new_game')
    @patch('view.GameView.display_message')
    @patch('controller.GameManager.binary_rain', side_effect=KeyboardInterrupt)
    def test_start_menu_secret_binary_rain_exit(self, mock_binary_rain,
                                                 mock_display_message,
                                                 mock_start_new_game,
                                                 mock_game_loop):
        """ Test that start_menu exits when user enters 'secret'
         and then exits binary rain with KeyboardInterrupt.
         after that the choice is 1 which starts the game."""
        with patch('view.GameView.input_prompt', side_effect=['secret', '1']):
            self.game_manager.start_menu()

        mock_binary_rain.assert_called_once()
        mock_display_message.assert_called_once_with("\nExiting binary rain...\n")
        mock_start_new_game.assert_called_once()
        mock_game_loop.assert_called_once()


    @patch('controller.GameManager.start_menu')
    @patch('view.GameView.display_message')
    @patch('view.GameView.print_board')
    @patch('board.GameBoard.check_terminal_state',
           return_value=GameBoard.BOARD_PLAYER_X)
    def test_post_game_player_x_wins(
            self,
            mock_check_terminal_state,
            mock_print_board,
            mock_display_message,
            mock_start_menu):
        """ Test that post_game displays the correct message when Player X wins """
        with patch('view.GameView.input_prompt', return_value='1') as mock_input_prompt:
            self.game_manager.post_game()
        mock_check_terminal_state.assert_called_once()
        mock_print_board.assert_called_once()
        mock_display_message.assert_called()
        mock_input_prompt.assert_called_once_with("Enter your choice: ")
        mock_start_menu.assert_called_once()

    @patch('controller.GameManager.start_menu')
    @patch('view.GameView.display_message')
    @patch('view.GameView.print_board')
    @patch('board.GameBoard.check_terminal_state',
           return_value=GameBoard.BOARD_PLAYER_O)
    def test_post_game_player_o_wins(
            self,
            mock_check_terminal_state,
            mock_print_board,
            mock_display_message,
            mock_start_menu):
        """ Test that post_game displays the correct message when Player O wins """
        with patch('view.GameView.input_prompt', return_value='1') as mock_input_prompt:
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

    @patch('controller.GameManager.start_menu')
    @patch('view.GameView.display_message')
    def test_post_game_draw(self, mock_display_message, mock_start_menu):
        """ Test that post_game displays the correct message when the game is a draw """
        with patch('view.GameView.input_prompt', return_value='1') as mock_input_prompt:
            self.game_manager.post_game()
            calls =  [unittest.mock.call("It's a draw."),
                 unittest.mock.call("\n1. Return to Main Menu\n2. Exit")]

            mock_display_message.call_args_list == calls
            mock_input_prompt.assert_called_once_with("Enter your choice: ")
            mock_start_menu.assert_called_once()

    @patch('controller.GameManager.start_menu')
    @patch('view.GameView.input_prompt', return_value='3')
    def test_post_game_draw_invalid_choice(self, mock_input_prompt, mock_start_menu):
        """ Test that post_game displays the correct message when invalid choice is entered"""
        with patch('view.GameView.display_message') as mock_display_message:
            self.game_manager.post_game()
            mock_input_prompt.assert_called_once_with("Enter your choice: ")

            calls = [unittest.mock.call("It's a draw."),
                        unittest.mock.call("\n1. Return to Main Menu\n2. Exit"),
                        unittest.mock.call("Invalid choice. Returning to main menu.")]
            mock_display_message.call_args_list == calls
            mock_start_menu.assert_called_once()


    @patch('board.GameBoard.check_terminal_state',
           side_effect=[None, GameBoard.BOARD_PLAYER_X])
    @patch('view.GameView.choose_move', return_value='save')
    def test_game_loop_save_game(self, mock_choose_move,
                                 mock_check_terminal_state):
        """ Test that game_loop saves the game state when the player chooses to save """
        self.game_manager.players[0] = HumanPlayer(GameBoard.BOARD_PLAYER_X)

        with patch('controller.GameManager.save_game_state') as mock_save_game_state:
            self.game_manager.game_loop()
        mock_choose_move.assert_called_once()
        mock_check_terminal_state.assert_called_once()
        mock_save_game_state.assert_called_once()

    @patch('view.GameView.print_board')
    @patch('controller.GameManager.post_game')
    @patch('board.GameBoard.check_terminal_state',
           side_effect=[None, GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_PLAYER_O])
    @patch('view.GameView.choose_move', return_value=(1, 2))
    def test_game_loop_apply_action(self, mock_choose_move,
                                    mock_check_terminal_state,
                                    mock_post_game,
                                    mock_print_board):
        """ Test that game_loop applies the player's action and checks the terminal state """

        self.game_manager.players[0] = HumanPlayer(GameBoard.BOARD_PLAYER_X)

        with patch('view.GameView.clear_screen') as mock_clear_screen:
            self.game_manager.game_loop()
        mock_choose_move.assert_called_once()
        self.assertEqual(mock_clear_screen.call_count, 2)
        self.assertEqual(mock_print_board.call_count, 2)
        # Check terminal state was evaluated
        mock_check_terminal_state.assert_called()
        # Ensure post_game was called due to terminal state or full board
        mock_post_game.assert_called_once()


    @patch('controller.GameManager.start_menu')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_game_with_savename(self, mock_open, mock_start_menu):
        """ Test that save_game_state with a specific filename"""
        with patch('view.GameView.input_prompt', return_value="test_save") as mock_input_prompt:
            self.game_manager.save_game_state()
            mock_input_prompt.assert_called_once_with("Enter a name for your save"
                          "(leave blank to use the current datetime): ")
            mock_open.assert_called_once_with(Path("savedGames", "test_save.json"),
                                              "w", encoding="utf-8")
            mock_start_menu.assert_called_once()

    @patch('datetime.datetime', autospec=True)
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('controller.GameManager.start_menu')
    def test_save_game_with_datetime(
            self, mock_start_menu, mock_open, mock_datetime):
        """ Test that save_game_state with default filename format"""
        # Define a specific datetime
        specific_datetime = datetime(2023, 5, 17, 3, 14, 1)  # for example

        # Configure the mock to return this specific datetime when now() is
        # called
        mock_datetime.now.return_value = specific_datetime

        with patch('view.GameView.input_prompt', return_value=None):
            self.game_manager.save_game_state()

        # Assert that open is called with a filename in the correct format
        mock_open.assert_called_once()
        filename_used = mock_open.call_args[0][0]
        self.assertRegex(
            filename_used.name,
            r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.json')

        mock_start_menu.assert_called_once()


    @patch('os.listdir', return_value=['game1.json', 'game2.json'])
    @patch('controller.GameView.input_prompt', return_value='exit')
    def test_exit_selection_save_game(self, mock_input_prompt, mock_listdir):
        """ Test that load_game_state handles exit selection"""
        with patch('view.GameView.display_message'), patch.object(self.game_manager, 'start_menu'):
            result = self.game_manager.load_game_state()
            self.assertFalse(result)
        mock_input_prompt.assert_called_once_with(
            "Enter the number of the game you want to load('exit' to return to main menu): ")
        mock_listdir.assert_called_once()

    @patch('json.load')
    @patch('controller.GameBoard')
    @patch('controller.HumanPlayer')
    @patch('controller.ComputerPlayer')
    def test_load_game_state_pvp(self,
                            mock_computer_player,
                            mock_human_player,
                            mock_game_board,
                            mock_json_load):
        """ Test that load_game_state loads the game state from a file """

        # Mock the behavior of json.load
        mock_json_load.return_value = {
            "board": [0, 0, 0, 0, "X", 0, 0, 0, "O"],
            "num_players": 2,
            "current_turn": "X"
        }
        # Mock that BOARD_PLAYER_X is "X"
        mock_game_board.BOARD_PLAYER_X= "X"

        with patch('builtins.open', new_callable=unittest.mock.mock_open), \
                patch('view.GameView.input_prompt', return_value="1") as mock_input_prompt, \
                    patch('os.listdir', return_value=['game1.json', 'game2.json']) as mock_listdir:
            result = self.game_manager.load_game_state()
            self.assertTrue(result)

        # Assert that the correct methods were called with the correct arguments
        mock_listdir.assert_called_once_with('savedGames')
        mock_input_prompt.assert_called_once_with(
            "Enter the number of the game you want to load('exit' to return to main menu): ")
        mock_json_load.assert_called_once()
        mock_game_board.assert_called()
        mock_human_player.assert_called()
        mock_computer_player.assert_not_called()

    @patch('json.load')
    @patch('controller.GameBoard')
    @patch('controller.HumanPlayer', return_value="X")
    @patch('controller.ComputerPlayer', return_value="O")
    def test_load_game_state_pve(self,
                            mock_computer_player,
                            mock_human_player,
                            mock_game_board,
                            mock_json_load):
        """ Test that load_game_state loads the game state from a file """

        # Mock the behavior of json.load
        mock_json_load.return_value = {
            "board": [0, 0, 0, 0, "X", 0, 0, 0, "O"],
            "num_players": 1,
            "current_turn": "X"
        }

        # Mock that BOARD_PLAYER_X is "X"
        mock_game_board.BOARD_PLAYER_X= "X"

        with patch('builtins.open', new_callable=unittest.mock.mock_open), \
                patch('view.GameView.input_prompt', return_value="1") as mock_input_prompt, \
                    patch('os.listdir', return_value=['game1.json', 'game2.json']) as mock_listdir:
            result = self.game_manager.load_game_state()
            self.assertTrue(result)

        # Assert that the correct methods were called with the correct arguments
        mock_listdir.assert_called_once_with('savedGames')
        mock_input_prompt.assert_called_once_with(
            "Enter the number of the game you want to load('exit' to return to main menu): ")
        mock_json_load.assert_called_once()
        mock_game_board.assert_called()
        mock_human_player.assert_called_once()
        mock_computer_player.assert_called_once()

    @patch('os.listdir')
    @patch('controller.GameView')
    def test_load_game_state_no_saved_games(self, mock_game_view, mock_os_listdir):
        """ Test that load_game_state returns False when no saved games are availabl """
        # Mock the behavior of os.listdir
        mock_os_listdir.return_value = []
        result = self.game_manager.load_game_state()
        self.assertFalse(result)
        # Assert that the correct methods were called with the correct arguments
        mock_os_listdir.assert_called_once_with('savedGames')
        mock_game_view.display_message.assert_called_once_with("No saved games found.")

    @patch('view.GameView.display_message')
    def test_load_game_state_no_saved_game(self, mock_display_message):
        """ Test that load_game_state handles a FileNotFoundError"""
        with patch('view.GameView.input_prompt', return_value="invalid_file"), \
                patch('os.listdir', return_value=None):
                result = self.game_manager.load_game_state()
        mock_display_message.assert_called_with("No saved games found.")
        self.assertFalse(result)
    
    @patch('os.listdir', side_effect=FileNotFoundError)
    @patch('controller.GameView')
    def test_load_game_state_no_saved_games_directory(self, mock_game_view, mock_os_listdir):
        """ Test that load_game_state returns False when no saved games directory is found """
        result = self.game_manager.load_game_state()
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
        result = self.game_manager.load_game_state()
        self.assertFalse(result)

        # display_message is used more than one time
        calls =  [unittest.mock.call("Please select a game to load"),
                 unittest.mock.call("1. game1.json"),
                 unittest.mock.call("2. game2.json"),
                 unittest.mock.call("Invalid selection.")]

        mock_input_prompt.assert_called()
        mock_listdir.assert_called_once()
        mock_display_message.call_args_list == calls
        
if __name__ == '__main__':
    unittest.main()
