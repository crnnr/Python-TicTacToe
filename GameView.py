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
    def choose_move(board, player):
        print ("To save the game, type 'save' at any time. \n")
        print(f"{player.player_type}'s turn.")
        while True:
            row = input('Enter row [1-3]: ')
            if row.lower() == 'save':
               return 'save'
            if not row.isdigit() or not 1 <= int(row) <= 3:
                print("Invalid input. Please enter a number between 1 and 3.")
                continue

            column = input('Enter column [1-3]: ')
            if column.lower() == 'save':
                return 'save'
            if not column.isdigit() or not 1 <= int(column) <= 3:
                print("Invalid input. Please enter a number between 1 and 3.")
                continue
            index = (int(row) - 1) * 3 + (int(column) - 1)
            if board.board[index] != board.BOARD_EMPTY:
                print('Space already taken. Try again.')
            else:
                break
        return row, column
            
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