""" Controller module for gamelogic """
from datetime import datetime
import random
import json
import os
import sys
from pathlib import Path
from board import GameBoard
from player import HumanPlayer, ComputerPlayer
from view import GameView


class GameManager:
    """ Brain of the operation"""

    def __init__(self):
        """
        Initialize the game manager with a new game board and one player.
        """
        self.board = GameBoard()
        self.num_players = 1
        self.players = [HumanPlayer(GameBoard.BOARD_PLAYER_X),
                        ComputerPlayer(GameBoard.BOARD_PLAYER_O)]

    def start_screen(self):
        """
        Display the start screen of the game.
        """
        GameView.display_start_screen()

    def start_menu(self):
        """
        Display the start menu and handle user input for game options.
        """
        self.start_screen()
        while True:
            GameView.display_menu()
            choice = GameView.input_prompt("Enter your choice [1-3]: ")
            if choice == '1':
                self.start_new_game()
                self.game_loop()
                break
            if choice == '2':
                if self.load_game_state():
                    self.game_loop()
                    break
                else:
                    GameView.display_message("Loading game failed.")
                    self.load_game_state()
            elif choice == '3':
                GameView.display_message("Thank you for playing. Goodbye!")
                sys.exit(0)
            elif choice.lower() == 'secret':
                try:
                    self.binary_rain()
                except KeyboardInterrupt:
                    GameView.display_message("\nExiting binary rain...\n")
            else:
                GameView.display_message("Invalid choice. Please enter"
                                         "1, 2, or 3.")

    def game_loop(self):
        """
        Main game loop, handles player turns and game state updates.
        """
        while self.board.check_terminal_state() is None \
        and any(space == GameBoard.BOARD_EMPTY for space in self.board.board):
            for player in self.players:
                GameView.clear_screen()  # Clear screen for each turn
                GameView.print_board(self.board)
                if isinstance(player, HumanPlayer):
                    move = GameView.choose_move(self.board, player)
                    if move == 'save':
                        self.save_game_state()
                        return
                    #  Unpack the tuple
                    row, column = move
                    action = player.make_move(self.board, row, column)
                else:
                    # Pass the board argument to the make_move() method
                    action = player.make_move(self.board)
                self.board.apply_action(action)
                GameView.clear_screen()
                GameView.print_board(self.board)
                if self.board.check_terminal_state() is not None:
                    break
        self.post_game()

    def post_game(self):
        """
        Handle post-game actions, 
        such as displaying the winner and offering replay options.
        """
        # Check for the winner after the loop ends
        winner = self.board.check_terminal_state()
        GameView.clear_screen()
        GameView.print_board(self.board)
        if winner == GameBoard.BOARD_PLAYER_X:
            GameView.display_message("Player X wins!")
        elif winner == GameBoard.BOARD_PLAYER_O:
            GameView.display_message("Player O wins!")
        else:
            GameView.display_message("It's a draw!")
        GameView.display_message("\n1. Return to Main Menu\n2. Exit")
        choice = GameView.input_prompt("Enter your choice: ")
        if choice == '1':
            GameView.clear_screen()
            self.start_menu()
        elif choice == '2':
            GameView.display_message("Thank you for playing. Goodbye!")
            sys.exit(0)

    def start_new_game(self):
        """
        Start a new game, 
        asking the number of players
        initializies the game board and players.
        """
        self.board = GameBoard()
        num_players = GameView.input_prompt('Enter number of players [1-2]: ')
        self.num_players = int(num_players)

        if self.num_players not in [1, 2]:
            GameView.display_message("Invalid number of players. \
                                     Defaulting to 1 player mode.")

        if self.num_players == 1:
            self.players = [HumanPlayer(GameBoard.BOARD_PLAYER_X),
                            ComputerPlayer(GameBoard.BOARD_PLAYER_O)]
        elif self.num_players == 2:
            self.players = [HumanPlayer(GameBoard.BOARD_PLAYER_X),
                            HumanPlayer(GameBoard.BOARD_PLAYER_O)]

    @staticmethod
    def binary_rain(rows=1080, columns=1920):
        """
        Display a binary rain animation. Can be interrupted with a keyboard interrupt.
        """
        while True:
            # Generate a frame of binary rain
            frame = [[' ' for _ in range(columns)] for _ in range(rows)]
            for col in range(columns):
                if random.choice([True, False]):
                    start_row = random.randint(0, rows - 1)
                    for row in range(start_row, rows):
                        frame[row][col] = str(random.randint(0, 1))

    def save_game_state(self):
        """
        Save the current game state to a file.
        """
        save_name = GameView.input_prompt("Enter a name for your save"
                          "(leave blank to use the current datetime): ")
        if not save_name:
            # Ensure filename valid filename, regardless of OS
            save_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".json"
        else:
            if not save_name.endswith('.json'):
                save_name += ".json"
        # OS independent filepath
        filename = Path("savedGames", save_name)
        self.create_directory_if_not_exists()
        game_state = {
            'board': self.board.board,
            'num_players': self.num_players,
            'current_turn': self.board.current_player()
        }
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(game_state, file)
            GameView.display_message(f"Game saved as '{filename}'")
        except IOError as e:
            GameView.display_message(f"Failed to save the game: {str(e)}")
        GameView.clear_screen()
        self.start_menu()  # Return to the main menu after saving the game

    def load_game_state(self):
        """
        Load a game state from a file.
        """
        saved_games_dir = 'savedGames'
        try:
            saved_files = os.listdir(saved_games_dir)
            if not saved_files:
                GameView.display_message("No saved games found.")
                return False
        except FileNotFoundError:
            GameView.display_message("No saved games directory found.")
            return False

        GameView.display_message("Please select a game to load:")
        for i, file in enumerate(saved_files, 1):
            GameView.display_message(f"{i}. {file}")
        choice = GameView.input_prompt("Enter the number of the game you "
                                       "want to load"
                                       "('exit' to return to main menu): ")
        if choice.lower() == 'exit':
            GameView.clear_screen()
            self.start_menu()
            return False
        try:
            selected_file = saved_files[int(choice) - 1]
        except (ValueError, IndexError):
            GameView.display_message("Invalid selection.")
            return False

        with open(f'{saved_games_dir}/{selected_file}', 'r', encoding='utf-8') as file:
            state = json.load(file)

        self.board = GameBoard()
        self.board.board = state['board']
        self.num_players = state['num_players']
        current_turn = state['current_turn']

        if self.num_players == 1:
            if current_turn == GameBoard.BOARD_PLAYER_X:
                self.players = [HumanPlayer(GameBoard.BOARD_PLAYER_X),
                                ComputerPlayer(GameBoard.BOARD_PLAYER_O)]
        if self.num_players == 2:
            if current_turn == GameBoard.BOARD_PLAYER_X:
                self.players = [HumanPlayer(self.board.BOARD_PLAYER_X),
                                HumanPlayer(self.board.BOARD_PLAYER_O)]
            else:
                self.players = [HumanPlayer(self.board.BOARD_PLAYER_O),
                                HumanPlayer(self.board.BOARD_PLAYER_X)]
        if current_turn:
            self.board.set_current_player(current_turn)

        GameView.display_message("Game loaded successfully.")
        return True  # Indicate success

    @staticmethod
    def create_directory_if_not_exists():
        """
        Create the directory for saved games if it does not exist.
        """
        Path("savedGames").mkdir(parents=True, exist_ok=True)
