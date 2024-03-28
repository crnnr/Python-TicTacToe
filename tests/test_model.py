import unittest
from Model import GameBoard

class TestGameBoard(unittest.TestCase):

    def setUp(self):
        self.board = GameBoard()

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
        
if __name__ == '__main__':
    unittest.main()
