import unittest
from unittest.mock import patch, mock_open
from Controller import GameManager
from Model import Player
from Model import HumanPlayer
from Model import ComputerPlayer
from Output import GameView

class TestController(unittest.TestCase):

    def setUp(self):
        self.game_manager = GameManager()

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
    @patch('builtins.input', side_effect=['3', '1'])  # First an invalid choice, then a valid one
    @patch('builtins.print')
    def test_start_new_game_invalid_num_players(self, mock_print, mock_input):
        self.game_manager.start_new_game()
        mock_print.assert_called_with("Invalid number of players. Defaulting to 1 player mode.")
        self.assertEqual(self.game_manager.num_players, 1)

if __name__ == '__main__':
    unittest.main()