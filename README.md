A classic game of Tic Tac Toe built in Python that allows for both single-player (against a computer opponent) and two-player modes. The game features a console-based interface for easy play and includes functionalities for saving and loading game states, allowing players to pause and resume games at their convenience.

## Features

- **Single-Player Mode**: Play against a challenging computer opponent.
- **Two-Player Mode**: Play against a friend in a turn-based system.
- **Save and Load Game**: Save the current game state and load it later to resume play.
- **Dynamic Game Board Display**: The game board updates after each move, showing the current state of play.
- **Input Validation**: Ensures that player inputs are valid before making a move.

## Installation

This game is a standalone Python script that requires no additional installation of packages. Ensure you have Python 3.x installed on your system to run the game.

1. Clone the repository or download the game files to your local machine.
2. Navigate to the directory containing the game files in your terminal or command prompt.
3. Run the game using Python:

```bash
python3 Controller.py
```
## How to Play

After starting the game, you will be greeted with a main menu with the following options:

  1. **New Game**: Start a new game session.
  2. **Load a Saved Game**: Continue playing from an existing position
  3. **Quit**: Exit the game.

### Starting a New Game

- Select option `1` from the main menu to start a new game.
- You will be prompted to choose between `1` (single-player) and `2` (two-player) modes.
- In single-player mode, you will play against the computer.
- In two-player mode, you and a friend will take turns making moves.

### Making a Move

- The game board is displayed as a 3x3 grid, with rows and columns numbered from 1 to 3.
- On your turn, enter the row and column numbers where you want to place your mark (X or O).
- Alternatively, type `save` at any prompt to save the game and exit.

### Saving and Loading a Game

- During your turn, typing `save` allows you to save the current state of the game. You can enter a filename for your save or leave it blank to use a timestamp.
- To load a game, select option `2` from the main menu. You'll see a list of saved games. Enter the number corresponding to the game you wish to load.

## Game Rules

The rules are simple and follow the traditional Tic Tac Toe game:

- The game is played on a grid that's 3 squares by 3 squares.
- Player 1 is X, and Player 2 (or the computer) is O. Players take turns putting their marks in empty squares.
- The first player to get 3 of their marks in a row (up, down, across, or diagonally) is the winner.
- If all 9 squares are filled and no player has 3 marks in a row, the game is declared a draw.

## Technologies

- **Python**: The entire game is developed in Python, making use of its standard libraries for functionalities like file handling and datetime operations.

## Contribution

Contributions to the Tic Tac Toe game are welcome! Whether it's bug fixes, new features, or improvements to the documentation, feel free to fork the repository and submit a pull request.

## License

This project is open-source and available under the MIT License. See the LICENSE file for more details.


