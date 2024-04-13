import unittest
import builtins
import json
from datetime import datetime
from unittest.mock import patch, mock_open, MagicMock
import unittest.mock
from Controller import GameManager
from Model import GameBoard
from Model import Player
from Model import HumanPlayer
from Model import ComputerPlayer
from datetime import datetime
from Output import GameView
from unittest.mock import MagicMock
import re
from Model import GameBoard, ComputerPlayer  # Assumed class names


class TestController(unittest.TestCase):
    
    def setUp(self):
        self.game_manager = GameManager()
        self.game_manager.players = [MagicMock(), MagicMock()]
        self.game_manager.board = GameBoard()

    def test_start_menu_start_new_game(self):
        with patch('Output.GameView.input_prompt', side_effect=['1']), \
             patch.object(self.game_manager, 'start_new_game') as mock_start_new_game, \
             patch.object(self.game_manager, 'game_loop') as mock_game_loop:
            self.game_manager.start_menu()
            mock_start_new_game.assert_called_once()
            mock_game_loop.assert_called_once()

    @patch('Output.GameView.display_menu')
    @patch('Output.GameView.input_prompt', return_value='3')
    @patch('builtins.exit', side_effect=SystemExit)
    def test_start_menu_exit(self, mock_exit, mock_input, mock_display_menu):
        with self.assertRaises(SystemExit):
            self.game_manager.start_menu()
        mock_exit.assert_called_once_with(0)

    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    def test_create_directory_if_not_exists(self, mock_exists, mock_makedirs):
        GameManager.create_directory_if_not_exists()
        mock_makedirs.assert_called_once_with('savedGames/', exist_ok=True)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='{"board": [], "num_players": 1, "current_turn": "X"}')
    @patch('os.listdir', return_value=['save1.json'])
    @patch('json.load', return_value={"board": "board_state", "num_players": 1, "current_turn": "X"})
    def test_load_game_state_success(self, mock_json_load, mock_listdir, mock_open):
        with patch('Output.GameView.input_prompt', return_value='1'):
            self.assertTrue(self.game_manager.load_game_state())
            mock_open.assert_called_once()
            mock_json_load.assert_called_once()

    @patch("os.listdir", return_value=[])
    @patch("builtins.open", new_callable=mock_open, read_data='')
    @patch("json.load", return_value={})
    def test_load_game_state(self, mock_json_load, mock_listdir):
        with patch("Output.GameView.input_prompt", return_value="1"):
            success = self.game_manager.load_game_state()
        self.assertTrue(success)
        mock_json_load.assert_called_once()
        
    @patch("os.listdir", return_value=["test_save.json"])
    @patch("builtins.open", new_callable=mock_open, read_data='{"board": "state", "num_players": 2, "current_turn": "X"}')
    @patch("json.load", return_value={"board": "state", "num_players": 2, "current_turn": "X"})
    def test_load_game_state(self, mock_json_load, mock_file, mock_listdir):
        with patch("Output.GameView.input_prompt", return_value="1"):
            success = self.game_manager.load_game_state()
        self.assertTrue(success)
        mock_file.assert_called_once_with("savedGames/test_save.json", "r")
        mock_json_load.assert_called_once()
        
    def test_game_initialization_two_players(self):
        with patch("builtins.input", return_value="2"):
            self.game_manager.start_new_game()
            self.assertIsInstance(self.game_manager.players[0], HumanPlayer)
            self.assertIsInstance(self.game_manager.players[0], HumanPlayer)
    def test_game_initialization_single_player(self):
        with patch("builtins.input", return_value="1"):
            self.game_manager.start_new_game()
            self.assertIsInstance(self.game_manager.players[0], HumanPlayer)
            self.assertIsInstance(self.game_manager.players[1], ComputerPlayer)
    @patch('Output.GameView.input_prompt', side_effect=['secret', KeyboardInterrupt])
    def test_start_menu_secret_binary_rain_exit(self, mock_binary_rain):
        with self.assertRaises(KeyboardInterrupt):
             self.game_manager.start_menu()
             mock_binary_rain.assert_called_once()
    
    @patch('Controller.GameManager.start_menu')
    @patch('Output.GameView.input_prompt', return_value='1')
    @patch('Output.GameView.display_message')
    @patch('Model.GameBoard.print_board')
    @patch('Model.GameBoard.check_terminal_state', return_value=GameBoard.BOARD_PLAYER_X)
    def test_post_game_player_x_wins(self, mock_check_terminal_state, mock_print_board, mock_display_message, mock_input_prompt, mock_start_menu):
        self.game_manager.post_game()
        mock_check_terminal_state.assert_called_once()
        mock_print_board.assert_called_once()
        mock_display_message.assert_called()
        mock_input_prompt.assert_called_once_with("Enter your choice: ")
        mock_start_menu.assert_called_once()

    @patch('Controller.GameManager.start_menu')
    @patch('Output.GameView.input_prompt', return_value='2')
    @patch('Output.GameView.display_message')
    @patch('Model.GameBoard.print_board')
    @patch('Model.GameBoard.check_terminal_state', return_value=GameBoard.BOARD_PLAYER_O)
    def test_post_game_player_o_wins(self, mock_check_terminal_state, mock_print_board, mock_display_message, mock_input_prompt, mock_start_menu):
        with self.assertRaises(SystemExit):
            self.game_manager.post_game()
        mock_check_terminal_state.assert_called_once()
        mock_print_board.assert_called_once()
        # Verify message displayed for Player O winning and for goodbye
        mock_display_message.assert_any_call("Thank you for playing. Goodbye!")

    @patch('Controller.GameManager.post_game')
    @patch('Output.GameView.input_prompt', side_effect=['invalid', '1'])
    @patch('Output.GameView.display_message')
    @patch('Model.GameBoard.print_board')
    @patch('Model.GameBoard.check_terminal_state', return_value=None)  # Draw
    def test_post_game_draw_invalid_choice(self, mock_check_terminal_state, mock_print_board, mock_display_message, mock_input_prompt, mock_post_game):
        self.game_manager.post_game()
        # Verify post_game is called again after invalid choice
        mock_post_game.assert_called_once()

    @patch('Controller.GameManager.post_game')
    @patch('Controller.GameManager.save_game_state')
    @patch('Model.GameBoard.apply_action')
    @patch('Model.GameBoard.check_terminal_state', side_effect=[None, None, None, GameBoard.BOARD_PLAYER_X])
    def test_game_loop_save(self, mock_check_terminal_state, mock_apply_action, mock_save_game, mock_post_game):
        # Simulate player action that leads to saving the game
        self.game_manager.players[0].choose_action.side_effect = ['save']
        self.game_manager.game_loop()
        mock_apply_action.assert_not_called()
        mock_save_game.assert_called_once()
        mock_post_game.assert_not_called()
    @patch('os.listdir', side_effect=FileNotFoundError)
    def test_directory_not_found(self, mock_listdir):
        self.game_manager.board = GameManager()
        with patch('builtins.print') as mock_print:
            result = self.game_manager.board.load_game_state()
            mock_print.assert_called_with("No saved games directory found.")
            self.assertFalse(result)
    @patch('os.listdir', return_value=[])
    def test_no_saved_games(self, mock_listdir):
        self.game_manager.board = GameManager()
        with patch('builtins.print') as mock_print:
            result = self.game_manager.board.load_game_state()
            mock_print.assert_called_with("No saved games found.")
            self.assertFalse(result)
    @patch('os.listdir', return_value=['game1.save', 'game2.save'])
    @patch('Controller.GameView.input_prompt', return_value='exit')
    def test_exit_selection(self, mock_input, mock_listdir):
        self.game_manager.board = GameManager()
        with patch('builtins.print'), patch.object(self.game_manager.board, 'start_menu') as mock_start_menu:
            result = self.game_manager.board.load_game_state()
            mock_start_menu.assert_called_once()
            self.assertFalse(result)
    @patch('os.listdir', return_value=['game1.json', 'game2.json'])
    @patch('Controller.GameView.input_prompt', return_value='1')
    def test_valid_selection(self, mock_input, mock_listdir):
        self.game_manager.board = GameManager()
        # Assuming load_game_state does something with the file that we can check.
        # For now, just checking if False is not returned, indicating processing beyond input.
        with patch('builtins.print'), patch.object(self.game_manager.board, 'start_menu'):
            result = self.game_manager.board.load_game_state()
            self.assertNotEqual(result, False)
    
    @patch('builtins.input', side_effect=lambda _: '')
    @patch('datetime.datetime', autospec=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('Controller.GameManager.start_menu')
    def test_save_game_with_datetime(self, mock_start_menu, mock_open, mock_datetime, mock_input):
        # Define a specific datetime
        specific_datetime = datetime(2023, 5, 17, 3, 14, 1)  # for example
        
        # Configure the mock to return this specific datetime when now() is called
        mock_datetime.now.return_value = specific_datetime

        game_manager = GameManager()
        game_manager.save_game_state()
        
        # Assert that open is called with a filename in the correct format
        mock_open.assert_called_once()
        filename_used = mock_open.call_args[0][0]
        self.assertRegex(filename_used, r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.json')
        
        # Ensure start_menu is not called to prevent the infinite loop
        mock_start_menu.assert_called_once()
    def test_game_loop_apply_action(self):
        # Set up player action that is not 'save'
        self.game_manager.players[0].choose_action.side_effect = [(GameBoard.BOARD_PLAYER_X, 1), (GameBoard.BOARD_PLAYER_X, 2)]

        with patch('Controller.GameView.clear_screen') as mock_clear_screen:
            self.game_manager.players[0].choose_action.side_effect = [(GameBoard.BOARD_PLAYER_X, 1), (GameBoard.BOARD_PLAYER_X, 2)]
            self.game_manager.game_loop()

            # Ensure the action was applied
            self.game_manager.board.apply_action.assert_called_once_with(GameBoard.BOARD_PLAYER_X, 1, 2)
            # Ensure the board was cleared and printed twice (before and after the action)
            self.assertEqual(mock_clear_screen.call_count, 2)
            self.assertEqual(self.game_manager.board.print_board.call_count, 2)
            # Check terminal state was evaluated
            self.game_manager.board.check_terminal_state.assert_called_once()
            # Ensure post_game was called due to terminal state or full board
            self.game_manager.post_game.assert_called_once()

if __name__ == '__main__':
    unittest.main()
