from GameBoard import GameBoard


class Player:
    def __init__(self, player_type):
        self.player_type = player_type

    def make_move(self, board):
        pass


class HumanPlayer(Player):
    def __init__(self, player_type):
        super().__init__(player_type)

    def make_move(self, board, row, column):
        x, y = int(row) - 1, int(column) - 1
        index = 3 * x + y
        return (self.player_type, index)


class ComputerPlayer(Player):
    def __init__(self, player_type):
        super().__init__(player_type)

    def minimax(self, board, depth, is_maximizing):
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
        if state == self.player_type:
            return 10 - depth
        elif state == GameBoard.BOARD_EMPTY:  # It's a draw
            return 0
        else:  # The opponent wins
            return depth - 10

    def make_move(self, board):
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
