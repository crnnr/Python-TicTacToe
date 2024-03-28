from datetime import datetime
import json
import os
from Model import GameBoard, HumanPlayer, ComputerPlayer
from Output import GameView

class GameManager:

    def __init__(self):
        self.board = GameBoard()  # Ensure board is always initialized
        self.players = []

    def start_screen(self):
        GameView.display_start_screen()

    def start_menu(self):
        self.start_screen()
        while True:
            GameView.display_menu()
            choice = GameView.input_prompt("Enter your choice [1-3]: ")
            if choice == '1':
                self.start_new_game()
                self.game_loop()
                break
            elif choice == '2':
                if self.load_game_state():
                    self.game_loop()
                else:
                    GameView.display_message("Loading game failed.")
                    self.load_game_state()
            elif choice == '3':
                GameView.display_message("Thank you for playing. Goodbye!")
                exit(0)
            elif choice.lower() == 'secret':  # Check for the "secret" input
                # Execute the binary rain function
                try:
                    self.binary_rain()  # You might want to adjust rows, columns, and speed parameters based on your console size and desired effect
                except KeyboardInterrupt:
                # Handle the interruption gracefully and return to the menu
                    print("\nExiting binary rain...\n")
                # Optionally, clear the screen or reset any game state if necessary
            else:
                GameView.display_message("Invalid choice. Please enter 1, 2, or 3.")

    def game_loop(self):
        while self.board.check_terminal_state() is None and any(space == GameBoard.BOARD_EMPTY for space in self.board.board):
            for player in self.players:
                GameView.clear_screen()  # Clear screen at the beginning of each turn
                self.board.print_board()  # Print the board at the start of each turn
                if self.board.check_terminal_state() is not None:
                    break
                action = player.choose_action(self.board)
                if action == 'save':
                    self.save_game_state()
                    return
                elif action is not None:
                    self.board.apply_action(action)
                    GameView.clear_screen()
                    self.board.print_board()  # Display the board immediately after an action
                    if self.board.check_terminal_state() is not None:
                        break
                else:  # This else block is for handling unexpected cases, can be removed if not needed
                    print("An unexpected error occurred. Please try again.")
        self.post_game()

    def post_game(self):
        # Check for the winner after the loop ends
        winner = self.board.check_terminal_state()
        GameView.clear_screen()
        self.board.print_board()
        if winner == GameBoard.BOARD_PLAYER_X:
            print("Player X wins!")
        elif winner == GameBoard.BOARD_PLAYER_O:
            print("Player O wins!")
        else:
            print("It's a draw!") 
        GameView.display_message("\n1. Return to Main Menu\n2. Exit")
        choice = GameView.input_prompt("Enter your choice: ")
        if choice == '1':
            GameView.clear_screen()
            self.start_menu()
        elif choice == '2':
            GameView.display_message("Thank you for playing. Goodbye!")
            exit(0)
        else:
            GameView.display_message("Invalid choice. Please enter '1' or '2'.")
            self.post_game()  # Recursively prompt for a valid choice

    def start_new_game(self):
        self.board = GameBoard()
        num_players = input('Enter number of players [1-2]: ')
        try:
            self.num_players = int(num_players)
        except ValueError:
            self.num_players = 1

        if num_players not in [1, 2]:
            print("Invalid number of players. Defaulting to 1 player mode.")
            self.num_players = 1

        if self.num_players == 1:
            self.players = [HumanPlayer(self.board.BOARD_PLAYER_X), ComputerPlayer(self.board.BOARD_PLAYER_O)]
        else:
            self.players = [HumanPlayer(self.board.BOARD_PLAYER_X), HumanPlayer(self.board.BOARD_PLAYER_O)]
    
    @staticmethod
    def binary_rain(rows=1080, columns=1920, speed=0.01):
        import random
        import time
        while True:
            # Generate a frame of binary rain
            frame = [[' ' for _ in range(columns)] for _ in range(rows)]
            for col in range(columns):
                if random.choice([True, False]):  # Randomly decide if a column will have rain
                    start_row = random.randint(0, rows - 1)
                    for row in range(start_row, rows):
                        frame[row][col] = str(random.randint(0, 1))
            # Print the frame
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen command for Windows and Unix
            for row in frame:
                print(''.join(row))  # Corrected to print the contents of each row
            time.sleep(speed)  # Control the speed of "rain"

    def save_game_state(self):
      save_name = input("Enter a name for your save (leave blank to use the current datetime): ").strip()
      if not save_name:
        save_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      filename = f'savedGames/{save_name}.json'
      self.create_directory_if_not_exists()  # Ensure the directory exists
      game_state = {
          'board': self.board,
          'num_players': self.num_players,
          'current_turn': self.board.current_player()
      }
      with open(filename, 'w') as file:
          json.dump(game_state, file)
      print(f"Game saved successfully as '{filename}'")
      GameView.clear_screen()
      self.start_menu()  # Return to the main menu after saving game

    def load_game_state(self):
        saved_games_dir = 'savedGames'
        try:
            saved_files = os.listdir(saved_games_dir)
            if not saved_files:
                print("No saved games found.")
                return False
        except FileNotFoundError:
            print("No saved games directory found.")
            return False

        print("Please select a game to load:")
        for i, file in enumerate(saved_files, 1):
            print(f"{i}. {file}")
        choice = GameView.input_prompt("Enter the number of the game you want to load ('exit' to return to main menu): ")
        if choice.lower() == 'exit':
            GameView.clear_screen()
            self.start_menu()
            return False  # Return to main menu
        try:
            selected_file = saved_files[int(choice) - 1]
        except (ValueError, IndexError):
            print("Invalid selection.")
            return False

        with open(f'{saved_games_dir}/{selected_file}', 'r') as file:
            state = json.load(file)
        
        self.board = GameBoard()
        self.board.board = state['board']
        self.num_players = state['num_players']
        current_turn = state['current_turn']

        if self.num_players == 1:
            if current_turn == GameBoard.BOARD_PLAYER_X:
                self.players = [HumanPlayer(GameBoard.BOARD_PLAYER_X), ComputerPlayer(GameBoard.BOARD_PLAYER_O)]
        if self.num_players == 2:
            if current_turn == GameBoard.BOARD_PLAYER_X:
                self.players = [HumanPlayer(self.board.BOARD_PLAYER_X), ComputerPlayer(self.board.BOARD_PLAYER_O)]
            else:
                self.players = [HumanPlayer(self.board.BOARD_PLAYER_O), HumanPlayer(self.board.BOARD_PLAYER_X)]
        
        if current_turn:
            self.board.set_current_player(current_turn)

        print("Game loaded successfully.")
        return True  # Indicate success
    
    @staticmethod
    def create_directory_if_not_exists(directory='savedGames/'):  # Made the path a default argument
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)


if __name__ == '__main__':
    GameView.clear_screen()
    game_manager = GameManager()
    game_manager.start_menu()  # Display the start menu @ intial start
    game_manager.game_loop()
    
