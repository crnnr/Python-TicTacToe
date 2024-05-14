"""Takes care of the game board and its state."""

"""
    Import Counter for calculating the current players.
"""
from collections import Counter


class GameBoard:
    """Board handeling class."""
    BOARD_EMPTY = 0
    BOARD_PLAYER_X = "X"
    BOARD_PLAYER_O = "O"

    def __init__(self):
        """
        Initialize the game board with empty spaces.
        """
        self.board = [self.BOARD_EMPTY for _ in range(9)]

    def set_current_player(self, player):
        """
        Set the current player.

        Args:
            player: The symbol of the player to set as the current player.
        """
        # Ensure only valid player symbols are accepted
        if player not in [self.BOARD_PLAYER_X, self.BOARD_PLAYER_O, None]:
            raise ValueError("Invalid player symbol")
        self.current_turn = player

    def current_player(self):
        """
        Determine the current player based on the state of the board.

        Returns:
            The symbol of the current player.
        """
        counter = Counter(self.board)
        x_count = counter[self.BOARD_PLAYER_X]
        o_count = counter[self.BOARD_PLAYER_O]
        if x_count + o_count == 9:
            return None
        return self.BOARD_PLAYER_O if x_count > o_count \
            else self.BOARD_PLAYER_X

    def _calculate_current_player(self):
        """
        Calculate the current player based on the state of the board.

        Returns:
            The symbol of the current player.
        """
        # Existing logic to calculate the current player
        counter = Counter(self.board)
        x_count = counter[self.BOARD_PLAYER_X]
        o_count = counter[self.BOARD_PLAYER_O]
        if x_count + o_count == 9:
            return None
        return self.BOARD_PLAYER_O if x_count > o_count \
                                   else self.BOARD_PLAYER_X

    def available_actions(self):
        """
        Determine the available actions for the current player.

        Returns:
            A list of tuples with player symbols.
        """
        player = self.current_player()
        return [(player, i) for i,
                space in enumerate(self.board) if space == self.BOARD_EMPTY]

    def apply_action(self, action):
        """
        Apply an action to the game board.

        Args:
            action: A tuple containing the current player's symbol 
            and the index of the space on the board to mark.
        """
        player, index = action
        new_board = self.board.copy()
        new_board[index] = player
        self.board = new_board

    def check_terminal_state(self):
        """
        Check if the game is in a terminal state.

        Returns:
            The symbol of the winning player, if there is one. 
            If the game is a draw, returns 0. If the game is not over, returns None.
        """
        for i in range(3):
            if self.board[3*i] == self.board[3*i + 1] == \
                self.board[3*i + 2] != self.BOARD_EMPTY:
                return self.board[3*i]
            if self.board[i] == self.board[i + 3] == \
                self.board[i + 6] != self.BOARD_EMPTY:
                return self.board[i]

        if self.board[0] == self.board[4] \
        == self.board[8] != self.BOARD_EMPTY \
        or self.board[2] == self.board[4] \
        == self.board[6] != self.BOARD_EMPTY:
            return self.board[4]

        return 0 if self.current_player() is None else None
