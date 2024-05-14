""" Handles actions for  HumanPlayer and ComputerPlayer classes """
from board import GameBoard


class Player:
    def __init__(self, player_type):
        """
        Check if the game is in a terminal state.

        Returns:
            The symbol of the winning player, if there is one.
            If the game is a draw, returns 0.
            If the game is not over, returns None.
        """
        self.player_type = player_type

    def make_move(self, board):
        """
        Make a move on the game board. 
        This method should be overridden by subclasses.

        Args:
            board: The current state of the game board.
        """
        pass


class HumanPlayer(Player):
    def __init__(self, player_type):
        """
        Initialize a human player with a specified type.

        Args:
            player_type: The type of the player (e.g., "X" or "O").
        """
        super().__init__(player_type)

    def make_move(self, board, row, column):
        """
        Make a move on the game board at the specified row and column.

        Args:
        board: The current state of the game board.
        row: The row of the board where the player wants to make a move.
        column: The column of the board where the player wants to make a move

        Returns:
        A tuple containing the player's type and
        the index of the board where the move was made.
        """
        x, y = int(row) - 1, int(column) - 1
        index = 3 * x + y
        return (self.player_type, index)


class ComputerPlayer(Player):
    def __init__(self, player_type):
        """
        Initialize a computer player with a specified type.

        Args:
            player_type: The type of the player (e.g., "X" or "O").
        """
        super().__init__(player_type)

    def minimax(self, board, depth, is_maximizing):
        """
        Implement the minimax algorithm to determine the best move.

        Args:
            board: The current state of the game board.
            depth: The current depth of the game tree.
            is_maximizing: boolean indicating if the 
            current player is maximizing or minimizing.

        Returns:
            The best score that can be achieved with the current game state.
        """
        terminal_state = board.check_terminal_state()
        if terminal_state is not None:
            return self.evaluate_terminal_state(terminal_state, depth)

        if is_maximizing:
            best_score = float('-inf')
            for action in board.available_actions():
                board.apply_action(action)
                score = self.minimax(board, depth + 1, False)
                board.board[action[1]] = GameBoard.BOARD_EMPTY
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for action in board.available_actions():
                board.apply_action(action)
                score = self.minimax(board, depth + 1, True)
                board.board[action[1]] = GameBoard.BOARD_EMPTY
                best_score = min(score, best_score)
            return best_score

    def evaluate_terminal_state(self, state, depth):
        """
        Evaluate the score of a terminal game state.

        Args:
        state: The terminal state of the game.
        depth: The depth of the game tree when the terminal state was reached

        Returns:
            The score of the terminal state.
        """
        if state == self.player_type:
            return 10 - depth
        elif state == GameBoard.BOARD_EMPTY:  # It's a draw
            return 0
        else:  # The opponent wins
            return depth - 10

    def make_move(self, board):
        """
        Make the best move on the game board using the minimax algorithm.

        Args:
            board: The current state of the game board.

        Returns:
            The best action that can be taken on the current game board.
        """
        best_score = float('-inf')
        best_action = None
        for action in board.available_actions():
            board.apply_action(action)
            score = self.minimax(board, 0, False)
            board.board[action[1]] = GameBoard.BOARD_EMPTY
            if score > best_score:
                best_score = score
                best_action = action
        return best_action
