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

    # def print_board(self):
    #     symbols = {self.BOARD_PLAYER_X: 'X', self.BOARD_PLAYER_O: 'O', self.BOARD_EMPTY: ' '}
    #     print('\n+---+---+---+')
    #     for i in range(0, 9, 3):
    #         row = []
    #         for j in range(3):
    #             # Fallback for unexpected values
    #             row.append(symbols.get(self.board[i+j], '?'))
    #         print('| ' + ' | '.join(row) + ' |')
    #         print('+---+---+---+')

class Player:
    def __init__(self, player_type):
        self.player_type = player_type

    def choose_action(self, board):
        pass

class HumanPlayer(Player):
    def __init__(self, player_type):
        super().__init__(player_type)

    def choose_action(self, board):
        print ("To save the game, type 'save' at any time. \n")
        print(f"{self.player_type}'s turn.")
        while True:
            x = input('Enter row [1-3]: ')
            if x.lower() == 'save':
                return 'save'
            if not x.isdigit() or not 1 <= int(x) <= 3:
                print("Invalid input. Please enter a number between 1 and 3.")
                continue

            y = input('Enter column [1-3]: ')
            if y.lower() == 'save':
                return 'save'
            if not y.isdigit() or not 1 <= int(y) <= 3:
                print("Invalid input. Please enter a number between 1 and 3.")
                continue

            x, y = int(x) - 1, int(y) - 1
            index = 3 * x + y
            if board.board[index] != GameBoard.BOARD_EMPTY:
                print('Space already taken. Try again.')
            else:
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
                board.board[action[1]] = GameBoard.BOARD_EMPTY  # Undo the move
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for action in board.available_actions():
                board.apply_action(action)
                score = self.minimax(board, depth + 1, True)
                board.board[action[1]] = GameBoard.BOARD_EMPTY  # Undo the move
                best_score = min(score, best_score)
            return best_score

    def evaluate_terminal_state(self, state, depth):
        if state == self.player_type:
            return 10 - depth
        elif state == GameBoard.BOARD_EMPTY:  # It's a draw
            return 0
        else:  # The opponent wins
            return depth - 10

    def choose_action(self, board):
        best_score = float('-inf')
        best_action = None
        for action in board.available_actions():
            board.apply_action(action)
            score = self.minimax(board, 0, False)
            board.board[action[1]] = GameBoard.BOARD_EMPTY  # Undo the move
            if score > best_score:
                best_score = score
                best_action = action
        return best_action