# Three Kingdoms Chess

This project is a graphical version of the classic Three Kingdoms Chess game, originally implemented as a text-based game in Python. The GUI version enhances the user experience by providing visual elements and interactive gameplay.

## Project Structure

```
three-kingdoms-chess-gui
├── src
│   ├── main.py        # Entry point for the GUI application
│   ├── board.py       # Manages the game state and board logic
│   ├── piece.py       # Defines the chess pieces and their properties
│   ├── game.py        # Handles overall game logic and player turns
│   ├── gui.py         # Contains GUI elements and event handling
│   ├── ability.py     # Handles basic effects of the ability in relation to the turn of the game
│   └── assets
│       └── sprites
│           └── README.md  # Information about graphical assets
├── requirements.txt   # Lists dependencies for the project
└── README.md          # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd three-kingdoms-chess-gui
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the game:
   ```
   python src/main.py
   ```

## Gameplay Rules

The game follows the classic rules of chess with a unique twist inspired by the Three Kingdoms theme. Players take turns moving their pieces on an 8x8 board, aiming to capture the opponent's king while protecting their own.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.