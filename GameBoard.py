import pickle
from collections import Counter


class GameBoard:
    BOARD_EMPTY = 0
    BOARD_PLAYER_X = "X"
    BOARD_PLAYER_O = "O"

    def __init__(self):
        self.board = [self.BOARD_EMPTY for _ in range(9)]

    def set_current_player(self, player):
        # Ensure only valid player symbols are accepted
        if player not in [self.BOARD_PLAYER_X, self.BOARD_PLAYER_O, None]:
            raise ValueError("Invalid player symbol")
        self.current_turn = player

    def current_player(self):
        counter = Counter(self.board)
        x_count = counter[self.BOARD_PLAYER_X]
        o_count = counter[self.BOARD_PLAYER_O]
        if x_count + o_count == 9:
            return None
        return self.BOARD_PLAYER_O if x_count > o_count else self.BOARD_PLAYER_X
    
    def _calculate_current_player(self):
        # Existing logic to calculate the current player
        counter = Counter(self.board)
        x_count = counter[self.BOARD_PLAYER_X]
        o_count = counter[self.BOARD_PLAYER_O]
        if x_count + o_count == 9:
            return None
        return self.BOARD_PLAYER_O if x_count > o_count else self.BOARD_PLAYER_X

    def available_actions(self):
        player = self.current_player()
        return [(player, i) for i, space in enumerate(self.board) if space == self.BOARD_EMPTY]

    def apply_action(self, action):
        player, index = action
        new_board = self.board.copy()
        new_board[index] = player
        self.board = new_board

    def check_terminal_state(self):
        for i in range(3):
            if self.board[3*i] == self.board[3*i + 1] == self.board[3*i + 2] != self.BOARD_EMPTY:
                return self.board[3*i]
            if self.board[i] == self.board[i + 3] == self.board[i + 6] != self.BOARD_EMPTY:
                return self.board[i]

        if self.board[0] == self.board[4] == self.board[8] != self.BOARD_EMPTY or self.board[2] == self.board[4] == self.board[6] != self.BOARD_EMPTY:
            return self.board[4]

        return 0 if self.current_player() is None else None
