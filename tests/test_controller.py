import unittest
import json
from unittest.mock import patch, mock_open, MagicMock
from Controller import GameManager
from Model import GameBoard
from Model import Player
from Model import HumanPlayer
from Model import ComputerPlayer
from datetime import datetime
from Output import GameView
from unittest.mock import MagicMock
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
    
    
if __name__ == '__main__':
    unittest.main()
