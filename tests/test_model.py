import unittest
from Model import GameBoard
from Model import Player
from Model import HumanPlayer
from Model import ComputerPlayer
from unittest.mock import patch
from unittest.mock import MagicMock

class TestGameBoard(unittest.TestCase):

    def setUp(self):
        self.board = GameBoard()
        self.player = HumanPlayer(GameBoard.BOARD_PLAYER_X)
    def test_game_over_conditions(self):
        # Test a specific win condition
        self.board.board = [None, None, None,
                            'X', 'X', 'X',  # Assume 'X' wins here
                            None, None, None]

    def test_player_setting(self):
        self.board.set_current_player(GameBoard.BOARD_PLAYER_X)
        self.assertEqual(self.board.current_turn, GameBoard.BOARD_PLAYER_X)
        with self.assertRaises(ValueError):
            self.board.set_current_player("Invalid")

    def test_win_conditions(self):
        # Test for a horizontal win
        for i in range(3):
            self.board.board = [GameBoard.BOARD_EMPTY] * 9
            self.board.board[i*3:(i+1)*3] = [GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_PLAYER_X]
        # Additional tests for vertical, diagonal wins and tie should be added

    def test_set_current_player_valid(self):
        self.board.set_current_player(GameBoard.BOARD_PLAYER_X)
        self.assertEqual(self.board.current_turn, GameBoard.BOARD_PLAYER_X)

    def test_set_current_player_invalid(self):
        with self.assertRaises(ValueError):
            self.board.set_current_player("A")

    def test_current_player_no_moves(self):
        self.board.board = [GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_PLAYER_X,
                            GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_PLAYER_O,
                            GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_PLAYER_O]
        self.assertIsNone(self.board.current_player())

    def test_current_player_X_turn(self):
        self.board.board = [GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_EMPTY,
                            GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_EMPTY,
                            GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY]
        self.assertEqual(self.board.current_player(), GameBoard.BOARD_PLAYER_X)

    def test_current_player_O_turn(self):
        self.board.board = [GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY,
                            GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_EMPTY,
                            GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY]
        self.assertEqual(self.board.current_player(), GameBoard.BOARD_PLAYER_O)

    def test_available_actions(self):
        self.board.board = [GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_EMPTY,
                            GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_EMPTY,
                            GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY]
        expected_actions = [(GameBoard.BOARD_PLAYER_X, 2), (GameBoard.BOARD_PLAYER_X, 5), (GameBoard.BOARD_PLAYER_X, 6), (GameBoard.BOARD_PLAYER_X, 7), (GameBoard.BOARD_PLAYER_X, 8)]
        self.assertEqual(self.board.available_actions(), expected_actions)

    def test_apply_action(self):
        action = (GameBoard.BOARD_PLAYER_X, 4)
        self.board.apply_action(action)
        self.assertEqual(self.board.board, [GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY,
                                            GameBoard.BOARD_EMPTY, GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_EMPTY,
                                            GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY])

    def test_check_terminal_state_X_wins(self):
        self.board.board = [GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_EMPTY,
                            GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_EMPTY,
                            GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY, GameBoard.BOARD_PLAYER_X]
        self.assertEqual(self.board.check_terminal_state(), GameBoard.BOARD_PLAYER_X)

    def test_check_terminal_state_O_wins(self):
        self.board.board = [GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_EMPTY,
                            GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_EMPTY,
                            GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_EMPTY, GameBoard.BOARD_PLAYER_X]
        self.assertEqual(self.board.check_terminal_state(), GameBoard.BOARD_PLAYER_O)

    def test_check_terminal_state_draw(self):
        self.board.board = [GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_PLAYER_X,
                            GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_PLAYER_O,
                            GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_PLAYER_O]
        self.assertEqual(self.board.check_terminal_state(), 0)

    def test_check_terminal_state_incomplete(self):
        self.board.board = [GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_EMPTY,
                            GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_EMPTY,
                            GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY]
        self.assertIsNone(self.board.check_terminal_state())

    @patch('builtins.input', side_effect=['save'])
    def test_save_option(self, mocked_input):
        action = self.player.choose_action(self.board)
        self.assertEqual(action, 'save')

    @patch('builtins.input', side_effect=['4', '2', '1'])  # Invalid row, then valid
    def test_invalid_row_input(self, mocked_input):
        with patch('builtins.print') as mocked_print:
            self.player.choose_action(self.board)
            mocked_print.assert_called_with("Invalid input. Please enter a number between 1 and 3.")

    def test_evaluate_terminal_state_win(self):
        self.player = ComputerPlayer(GameBoard.BOARD_PLAYER_X)
        self.board.board = ['X', 'X', 'X', None, None, None, None, None, None]  # Assuming 'X' wins
        score = self.player.evaluate_terminal_state('X', 0)
        self.assertEqual(score, 10)

    def test_choose_action_selects_optimal_move(self):
        self.player = ComputerPlayer("X")
        self.board = GameBoard()
        self.board.board = ['X', 'X', None,
                            'O', 'O', None,
                            None, None, None]                           
        available_actions = [(0, 2), (1, 2), (2, 0), (2, 1), (2, 2)]
        self.board.available_actions = MagicMock(return_value=available_actions)
        scores = {2: 10, 5: 0, 6: 0, 7: 0, 8: 0}
        self.player.minimax = MagicMock(side_effect=lambda board, depth, is_maximizing: scores[board.board.index(None)])
        expected_action = (0, 2)
        chosen_action = self.player.choose_action(self.board)
        self.assertEqual(chosen_action, expected_action)
        
    def test_initial_game_state(self):
        self.assertEqual(self.board._calculate_current_player(), self.board.BOARD_PLAYER_X)

    def test_uneven_play_x_more(self):
        self.board.board = ["X", "O", "X", GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY]
        self.assertEqual(self.board._calculate_current_player(), self.board.BOARD_PLAYER_O)

    def test_uneven_play_o_more(self):
        self.board.board = ["O", "X", "O", "X", "O", GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY]
        self.assertEqual(self.board._calculate_current_player(), self.board.BOARD_PLAYER_X)
    
    def test_full_board(self):
        self.board.board = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
        self.assertIsNone(self.board._calculate_current_player())

    def test_equal_number_of_x_and_o(self):
        self.board.board = ["X", "O", "X", "O", GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY]
        self.assertEqual(self.board._calculate_current_player(), self.board.BOARD_PLAYER_X)
    def test_terminal_state_evaluation(self):
        self.player = ComputerPlayer("X")
        self.board = GameBoard()
        # Mock check_terminal_state to simulate a terminal state
        self.board.check_terminal_state = MagicMock(return_value="X")
        # Mock evaluate_terminal_state to return a specific score
        self.player.evaluate_terminal_state = MagicMock(return_value=10)

        score = self.player.minimax(self.board, 0, True)
        self.assertEqual(score, 10)
        self.player.evaluate_terminal_state.assert_called_once_with("X", 0)

    def test_maximizing_player_win_scenario(self):
        board = GameBoard()
        self.board.board = ["X", "X", GameBoard.BOARD_EMPTY, "O", "O", GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY, GameBoard.BOARD_EMPTY]
        agent = ComputerPlayer("X")
        
        expected_score = 0 
        score = agent.minimax(board, 0, True)
        self.assertEqual(score, expected_score, "Test successful")
        
if __name__ == '__main__':
    unittest.main()
