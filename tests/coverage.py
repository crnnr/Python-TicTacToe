import unittest
from board import GameBoard

class TestGameBoard(unittest.TestCase):

    def test_initialization(self):
        board = GameBoard()
        self.assertEqual(board.board, [GameBoard.BOARD_EMPTY for _ in range(9)],
                         "Board should be initialized with all empty slots")

    def test_set_current_player(self):
        board = GameBoard()
        board.set_current_player(GameBoard.BOARD_PLAYER_X)
        self.assertEqual(board.current_turn, GameBoard.BOARD_PLAYER_X,
                         "Current player should be set to X")
        with self.assertRaises(ValueError):
            board.set_current_player('Z')

    def test_make_move(self):
        board = GameBoard()
        board.set_current_player(GameBoard.BOARD_PLAYER_X)
        move_success = board.make_move(0)
        self.assertTrue(move_success, "Move should be successful")
        self.assertEqual(board.board[0], GameBoard.BOARD_PLAYER_X,
                         "Board slot 0 should be marked with X")
        move_success = board.make_move(0)
        self.assertFalse(move_success, "Move should fail if slot is already taken")

if __name__ == '__main__':
    unittest.main()
