class GameView:
    @staticmethod
    def display_start_screen():
        print("""
  _______ _   _______      _______         
 |__   __(_) |__   __|    |__   __|        
    | |   _  ___| | __ _  ___| | ___   ___ 
    | |  | |/ __| |/ _` |/ __| |/ _ \\ / _ \\
    | |  | | (__| | (_| | (__| | (_) |  __/
    |_|  |_|\___|_|\__,_|\___|_|\___/ \___|
          by Christof & Manuel                                  
""")

    @staticmethod
    def display_menu():
        print("""
Welcome to Tic Tac Toe
1) New game
2) Load a saved game
3) Quit
""")

    @staticmethod
    def display_message(message):
        print(message)

    @staticmethod
    def clear_screen():
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def input_prompt(prompt):
        return input(prompt)

    @staticmethod
    def print_board(board):
        symbols = {board.BOARD_PLAYER_X: 'X', board.BOARD_PLAYER_O: 'O', board.BOARD_EMPTY: ' '}
        print('\n+---+---+---+')
        for i in range(0, 9, 3):
            row = []
            for j in range(3):
                # Fallback for unexpected values
                row.append(symbols.get(board.board[i+j], '?'))
            print('| ' + ' | '.join(row) + ' |')
            print('+---+---+---+')