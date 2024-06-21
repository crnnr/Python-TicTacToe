""" Test the GameBoard class """
import unittest
from board import GameBoard

class TestGameBoard(unittest.TestCase):
    """ Test the GameBoard class """

    def test_initialization(self):
        """ Test that the board is initialized correctly"""
        board = GameBoard()
        self.assertEqual(board.board, [GameBoard.BOARD_EMPTY for _ in range(9)],
                         "Board should be initialized with all empty slots")

    def test_set_current_player(self):
        """ Test that the current player is correctly set """
        board = GameBoard()
        board.set_current_player(GameBoard.BOARD_PLAYER_X)
        self.assertEqual(board.current_turn, GameBoard.BOARD_PLAYER_X,
                         "Current player should be set to X")
        with self.assertRaises(ValueError):
            board.set_current_player('Z')

    def test_current_player(self):
        """ Test that the current player is correctly returned """
        board = GameBoard()
        board.board = [GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_PLAYER_O,
                       GameBoard.BOARD_EMPTY, GameBoard.BOARD_PLAYER_X,
                       GameBoard.BOARD_PLAYER_O, GameBoard.BOARD_EMPTY,
                       GameBoard.BOARD_PLAYER_X, GameBoard.BOARD_PLAYER_O,
                       GameBoard.BOARD_PLAYER_X]
        self.assertEqual(board.current_player(), GameBoard.BOARD_PLAYER_O,
                         "Current player should be O")
    #make_move() is part of the Player class, why here?
    # def test_make_move(self):
    #     board = GameBoard()
    #     board.set_current_player(GameBoard.BOARD_PLAYER_X)
    #     move_success = board.make_move(0)
    #     self.assertTrue(move_success, "Move should be successful")
    #     self.assertEqual(board.board[0], GameBoard.BOARD_PLAYER_X,
    #                      "Board slot 0 should be marked with X")
    #     move_success = board.make_move(0)
    #     self.assertFalse(move_success, "Move should fail if slot is already taken")

if __name__ == '__main__':
    unittest.main()
