"""Unit tests for the game board and player classes."""
import unittest
from unittest.mock import MagicMock
from board import GameBoard
from player import HumanPlayer
from player import ComputerPlayer


class TestGameBoard(unittest.TestCase):
    """Unit tests for the GameBoard class."""
    def setUp(self):
        """Set up the test environment."""
        self.board = GameBoard()
        self.player = HumanPlayer(GameBoard.BOARD_PLAYER_X)

    def test_game_over_conditions(self):
        """Test the game over conditions."""
        # Test a specific win condition
        self.board.board = [None, None, None,
                            'X', 'X', 'X',  # Assume 'X' wins here
                            None, None, None]

    def test_player_setting(self):
        """Test the player setting method."""
        self.board.set_current_player(GameBoard.BOARD_PLAYER_X)
        self.assertEqual(self.board.current_turn, GameBoard.BOARD_PLAYER_X)
        with self.assertRaises(ValueError):
            self.board.set_current_player("Invalid")

    def test_win_conditions(self):
        """Test the win conditions."""
        # Test for a horizontal win
        for i in range(3):
            self.board.board = [GameBoard.BOARD_EMPTY] * 9
            self.board.board[i * 3:(i + 1) * 3] = [GameBoard.BOARD_PLAYER_X,
                                                   GameBoard.BOARD_PLAYER_X,
                                                   GameBoard.BOARD_PLAYER_X]
        # Additional tests for vertical, diagonal wins and tie should be added

    def test_set_current_player_valid(self):
        """Test setting the current player."""
        self.board.set_current_player(GameBoard.BOARD_PLAYER_X)
        self.assertEqual(self.board.current_turn, GameBoard.BOARD_PLAYER_X)

    def test_set_current_player_invalid(self):
        """Test setting the current player with an invalid value."""
        with self.assertRaises(ValueError):
            self.board.set_current_player("A")

    def test_current_player_no_moves(self):
        """Test the current player with no moves."""
        self.board.board = [
            GameBoard.BOARD_PLAYER_X,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_PLAYER_X,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_PLAYER_X,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_PLAYER_X,
            GameBoard.BOARD_PLAYER_O]
        self.assertIsNone(self.board.current_player())

    def test_current_player_x_turn(self):
        """Test the current player when it is X's turn."""
        self.board.board = [
            GameBoard.BOARD_PLAYER_X,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_PLAYER_X,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY]
        self.assertEqual(self.board.current_player(), GameBoard.BOARD_PLAYER_X)

    def test_current_player_o_turn(self):
        """Test the current player when it is O's turn."""
        self.board.board = [
            GameBoard.BOARD_PLAYER_X,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_PLAYER_X,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY]
        self.assertEqual(self.board.current_player(), GameBoard.BOARD_PLAYER_O)

    def test_available_actions(self):
        """Test the available actions method."""
        self.board.board = [
            GameBoard.BOARD_PLAYER_X,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_PLAYER_X,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY]
        expected_actions = [
            (GameBoard.BOARD_PLAYER_X,
             2),
            (GameBoard.BOARD_PLAYER_X,
             5),
            (GameBoard.BOARD_PLAYER_X,
             6),
            (GameBoard.BOARD_PLAYER_X,
             7),
            (GameBoard.BOARD_PLAYER_X,
             8)]
        self.assertEqual(self.board.available_actions(), expected_actions)

    def test_apply_action(self):
        """Test the apply action method."""
        action = (GameBoard.BOARD_PLAYER_X, 4)
        self.board.apply_action(action)
        self.assertEqual(self.board.board,
                         [GameBoard.BOARD_EMPTY,
                          GameBoard.BOARD_EMPTY,
                          GameBoard.BOARD_EMPTY,
                          GameBoard.BOARD_EMPTY,
                          GameBoard.BOARD_PLAYER_X,
                          GameBoard.BOARD_EMPTY,
                          GameBoard.BOARD_EMPTY,
                          GameBoard.BOARD_EMPTY,
                          GameBoard.BOARD_EMPTY])

    def test_check_terminal_state_x_wins(self):
        """Test the check terminal state method when X wins."""
        self.board.board = [
            GameBoard.BOARD_PLAYER_X,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_PLAYER_X,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_PLAYER_X]
        self.assertEqual(
            self.board.check_terminal_state(),
            GameBoard.BOARD_PLAYER_X)

    def test_check_terminal_state_o_wins(self):
        """Test the check terminal state method when O wins."""
        self.board.board = [
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_PLAYER_X,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_PLAYER_X]
        self.assertEqual(
            self.board.check_terminal_state(),
            GameBoard.BOARD_PLAYER_O)

    def test_check_terminal_state_draw(self):
        """Test the check terminal state method when the game is a draw."""
        self.board.board = [
            GameBoard.BOARD_PLAYER_X,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_PLAYER_X,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_PLAYER_X,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_PLAYER_X,
            GameBoard.BOARD_PLAYER_O]
        self.assertEqual(self.board.check_terminal_state(), 0)

    def test_check_terminal_state_incomplete(self):
        """Test the check terminal state method when the game is incomplete."""
        self.board.board = [
            GameBoard.BOARD_PLAYER_X,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_PLAYER_O,
            GameBoard.BOARD_PLAYER_X,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY]
        self.assertIsNone(self.board.check_terminal_state())


    def test_evaluate_terminal_state_win(self):
        """Test the evaluate terminal state method when a player wins."""
        self.player = ComputerPlayer(GameBoard.BOARD_PLAYER_X)
        self.board.board = ['X', 'X', 'X', None, None,
                            None, None, None, None]  # Assuming 'X' wins
        score = self.player.evaluate_terminal_state('X', 0)
        self.assertEqual(score, 10)

    def test_make_move_selects_optimal_move(self):
        """Test the make_move method when selecting the optimal move."""
        self.player = ComputerPlayer("X")
        self.board = GameBoard()
        self.board.board = ['X', 'X', None,
                            'O', 'O', None,
                            None, None, None]
        available_actions = [(0, 2), (1, 2), (2, 0), (2, 1), (2, 2)]
        self.board.available_actions = MagicMock(
            return_value=available_actions)
        scores = {2: 10, 5: 0, 6: 0, 7: 0, 8: 0}
        self.player.minimax = MagicMock(
            side_effect=lambda board, depth, is_maximizing: scores[board.board.index(None)])
        expected_action = (0, 2)
        chosen_action = self.player.make_move(self.board)
        self.assertEqual(chosen_action, expected_action)

    def test_initial_game_state(self):
        """Test the initial game state."""
        self.assertEqual(
            self.board._calculate_current_player(),
            self.board.BOARD_PLAYER_X)

    def test_uneven_play_x_more(self):
        """Test the current player when X has more moves."""
        self.board.board = [
            "X",
            "O",
            "X",
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY]
        self.assertEqual(
            self.board._calculate_current_player(),
            self.board.BOARD_PLAYER_O)

    def test_uneven_play_o_more(self):
        """Test the current player when O has more moves."""
        self.board.board = [
            "O",
            "X",
            "O",
            "X",
            "O",
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY]
        self.assertEqual(
            self.board._calculate_current_player(),
            self.board.BOARD_PLAYER_X)

    def test_full_board(self):
        """Test the current player when the board is full."""
        self.board.board = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
        self.assertIsNone(self.board._calculate_current_player())

    def test_equal_number_of_x_and_o(self):
        """Test the current player when there is an equal number of X and O."""
        self.board.board = [
            "X",
            "O",
            "X",
            "O",
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY]
        self.assertEqual(
            self.board._calculate_current_player(),
            self.board.BOARD_PLAYER_X)

    def test_terminal_state_evaluation(self):
        """Test the terminal state evaluation."""
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
        """Test the maximizing player win scenario."""
        board = GameBoard()
        self.board.board = [
            "X",
            "X",
            GameBoard.BOARD_EMPTY,
            "O",
            "O",
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY,
            GameBoard.BOARD_EMPTY]
        agent = ComputerPlayer("X")

        expected_score = 0
        score = agent.minimax(board, 0, True)
        self.assertEqual(score, expected_score, "Test successful")


if __name__ == '__main__':
    unittest.main()
