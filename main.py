from controller import GameManager
from view import GameView

if __name__ == '__main__':
    GameView.clear_screen()
    game_manager = GameManager()
    game_manager.start_menu()  # Display the start menu @ intial start
    game_manager.game_loop()
