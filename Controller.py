from datetime import datetime
import json
import os
from Model import GameBoard, HumanPlayer, ComputerPlayer
from Output import GameView

class GameManager:
    def __init__(self):
        self.board = GameBoard()
        self.players = []
        self.num_players = 0

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
                    GameView.display_message("Loading game failed. Returning to main menu.")
            elif choice == '3':
                GameView.display_message("Thank you for playing. Goodbye!")
                exit()
            else:
                GameView.display_message("Invalid choice. Please enter 1, 2, or 3.")

    def start_new_game(self):
        self.board = GameBoard()
        num_players = GameView.input_prompt('Enter number of players [1-2]: ')
        try:
            self.num_players = int(num_players)
        except ValueError:
            self.num_players = 1

        if self.num_players not in [1, 2]:
            GameView.display_message("Invalid number of players. Defaulting to 1 player mode.")
            self.num_players = 1

        if self.num_players == 1:
            self.players = [HumanPlayer(self.board.BOARD_PLAYER_X), ComputerPlayer(self.board.BOARD_PLAYER_O)]
        else:
            self.players = [HumanPlayer(self.board.BOARD_PLAYER_X), HumanPlayer(self.board.BOARD_PLAYER_O)]

    def game_loop(self):
        while self.board.check_terminal_state() is None and any(space == GameBoard.BOARD_EMPTY for space in self.board.board):
            for player in self.players:
                GameView.clear_screen()
                GameView.display_board(self.board)
                if self.board.check_terminal_state() is not None:
                    break
                
                if isinstance(player, HumanPlayer):
                    action = player.choose_action(self.board, GameView.display_message, GameView.input_prompt)
                elif isinstance(player, ComputerPlayer):
                    action = player.choose_action(self.board)

                if action == 'save':
                    self.save_game_state()
                    return
                elif action is not None:
                    self.board.apply_action(action)
                    if self.board.check_terminal_state() is not None:
                        break
        self.end_game()  # Handle the end of the game (displaying the winner, etc.)

    def end_game(self):
        GameView.clear_screen()
        GameView.display_board(self.board)
        
        winner = self.board.check_terminal_state()
        if winner == GameBoard.BOARD_PLAYER_X:
            GameView.display_message("Player X wins!")
        elif winner == GameBoard.BOARD_PLAYER_O:
            GameView.display_message("Player O wins!")
        else:
            GameView.display_message("It's a draw!")

    def save_game_state(self):
        
        saved_games_dir = 'savedGames/'
        self.create_directory_if_not_exists(saved_games_dir)
        save_name = GameView.input_prompt('Enter a name for your save file (leave blank for a timestamp): ')
        # Use the current timestamp as the default file name
        if not save_name.strip():
            save_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
        filename = f'savedGames/{save_name}.json'
        
        game_state = {
            'board': self.board.board,
            'current_turn': self.board.current_turn,
            'num_players': self.num_players,
        }
        
        with open(filename, 'w') as file:
            json.dump(game_state, file)
        
        GameView.display_message("Game saved successfully.")
        GameView.clear_screen()
        GameView.display_message("Game saved with filename: " + filename)
        
    def load_game_state(self):
        saved_games_dir = 'savedGames/'
        self.create_directory_if_not_exists(saved_games_dir)
        
        saved_games = [f for f in os.listdir(saved_games_dir) if f.endswith('.json')]
        if not saved_games:
            GameView.display_message("No saved games found.")
            return False

        GameView.display_message("Select a game to load:")
        for index, game in enumerate(saved_games, start=1):
            GameView.display_message(f"{index}. {game}")
        
        selected_game_index = GameView.input_prompt("Enter the number of the game you want to load: ")
        try:
            selected_game_index = int(selected_game_index) - 1
            if selected_game_index < 0 or selected_game_index >= len(saved_games):
                raise ValueError
        except ValueError:
            GameView.display_message("Invalid selection.")
            return False
        
        filename = os.path.join(saved_games_dir, saved_games[selected_game_index])

        with open(filename, 'r') as file:
            game_state = json.load(file)
    
        # Reading game state from Json 
        self.board.board = game_state['board']
        self.board.current_turn = game_state['current_turn']
        self.num_players = game_state['num_players']
        self.board.set_current_player(self.board.current_turn)

        if self.num_players == 1:
            self.players = [HumanPlayer(self.board.BOARD_PLAYER_X), ComputerPlayer(self.board.BOARD_PLAYER_O)]
        if self.num_players == 2:
            if self.board.current_turn == self.board.BOARD_PLAYER_X:
                self.players = [HumanPlayer(self.board.BOARD_PLAYER_X), ComputerPlayer(self.board.BOARD_PLAYER_O)]
            else:
                self.players = [HumanPlayer(self.board.BOARD_PLAYER_O), HumanPlayer(self.board.BOARD_PLAYER_X)]
    
        GameView.display_message("Game loaded successfully.")
        return True
        
    @staticmethod
    def create_directory_if_not_exists(self):
        path = 'savedGames/'
        directory = path if os.path.isdir(path) else os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    def end_game(self):
        exit(0)

if __name__ == '__main__':
    GameView.clear_screen()
    game_manager = GameManager()
    game_manager.start_menu()  # Display the start menu @ intial start
    game_manager.game_loop()
    
