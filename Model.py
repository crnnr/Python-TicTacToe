from collections import Counter

class GameBoard:
    BOARD_EMPTY = 0
    BOARD_PLAYER_X = "X"
    BOARD_PLAYER_O = "O"

    def __init__(self):
        self.board = [self.BOARD_EMPTY for _ in range(9)]
        self.current_turn = self.BOARD_PLAYER_O

    def current_player(self):
        if self.current_turn is not None:
            return self.current_turn
    
        counter = Counter(self.board)
        x_count = counter[self.BOARD_PLAYER_X]
        o_count = counter[self.BOARD_PLAYER_O]
        if x_count + o_count == 9:
            return None

    def set_current_player(self, player):
        if player not in [self.BOARD_PLAYER_X, self.BOARD_PLAYER_O, None]:
            raise ValueError("Invalid player symbol")
        player = self.current_player()

    def available_actions(self):
        return [(self.current_player(), i) for i, space in enumerate(self.board) if space == self.BOARD_EMPTY]

    def apply_action(self, action):
        player, index = action
        if self.board[index] == self.BOARD_EMPTY:
            self.board[index] = player

    def check_terminal_state(self):
        for i in range(3):
            if self.board[3*i] == self.board[3*i+1] == self.board[3*i+2] != self.BOARD_EMPTY:
                return self.board[3*i]
            if self.board[i] == self.board[i+3] == self.board[i+6] != self.BOARD_EMPTY:
                return self.board[i]
        if self.board[0] == self.board[4] == self.board[8] != self.BOARD_EMPTY or self.board[2] == self.board[4] == self.board[6] != self.BOARD_EMPTY:
            return self.board[4]
        return 0 if self.current_player() is None else None

class Player:
    def __init__(self, player_type):
        self.player_type = player_type

    def choose_action(self, board):
        pass

class HumanPlayer(Player):
    def choose_action(self, board, display_message, input_func):
        display_message("Type 'save' to save the current state of the game to continue later.")
        display_message("")
        display_message(f"{self.player_type}'s turn.")
        display_message("")
        while True:
            x = input_func('Enter row [1-3]: ')
            if x.lower() == 'save':
                return 'save'
            try:
                x = int(x) - 1
            except ValueError:
                display_message("Invalid input. Please enter a number between 1 and 3.")
                continue

            y = input_func('Enter column [1-3]: ')
            if y.lower() == 'save':
                return 'save'
            try:
                y = int(y) - 1
            except ValueError:
                display_message("Invalid input. Please enter a number between 1 and 3.")
                continue

            index = 3 * x + y
            if board.board[index] != GameBoard.BOARD_EMPTY:
                display_message('Space already taken. Try again.')
            else:
                return (self.player_type, index)

class ComputerPlayer(Player):
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
        elif state == GameBoard.BOARD_EMPTY:
            return 0
        else:
            return depth - 10

    def choose_action(self, board):
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
