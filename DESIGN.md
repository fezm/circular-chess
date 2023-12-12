# Design Document: Circular Chess

## Overview

The Circular Chess project consists of three main files: `main.py`, `board.py`, and `constants.py`. Each file plays a distinct role in implementing the game's functionality.

## main.py

`main.py` serves as the entry point for the Circular Chess application. It orchestrates the game's flow, handling user input and managing the game loop. Key responsibilities include:

- Initializing the game state using the `Board` class from `board.py`.
- Rendering the game board and pieces using Pygame.
- Processing user input to execute moves and update the game state.

### Design Decisions

- Utilizes Pygame for graphical rendering and user interaction.
- Implements the game loop for continuous gameplay.
- Implements the `Board` class to manage the state of the game board.

## board.py

`board.py` encapsulates the core logic of the Circular Chess board. It defines the `Board` class, which is responsible for:

- Representing the state of the game board.
- Validating moves and updating the board accordingly.
- Handling undo functionality and maintaining a move log.

### Design Decisions

- Uses a 2D list to represent the game board, with each entry containing color and piece type information.
- Implements methods for drawing the circular game board and rendering pieces.
- Implements move-related functions, including making moves, undoing moves, and obtaining valid moves.

### Future Considerations

- Enhance the gameplay by adding support for pawn promotion, allowing players to exchange their pawns for more powerful pieces upon reaching the opposite end of the circular chessboard.
- Improve the user experience by incorporating an in-game indicator highlighting the last piece moved or the most recent move made.
- Introduce an exciting dynamic to the game by implementing timers, offering players the option to engage in timed chess matches.
- Refine the game's conclusion by incorporating a rule where capturing the king results in an immediate end to the game.

## constants.py

`constants.py` contains essential constants used throughout the project, such as colors and board dimensions. Centralizing these values enhances code readability and maintainability.

### Design Decisions

- Defines constants for colors and board dimensions.

## Code Structure

The project adopts an object-oriented approach, with distinct classes for managing the game state, handling moves, and storing constants. This design promotes modularity, readability, and ease of maintenance.

## Future Considerations

Future enhancements to the project may include:

- Improving the user interface for a more visually appealing experience.
- Implementing additional chess variants or rules.
- Implementing additional piece colors, or customizable square colors.
- Optimizing the codebase for performance improvements.

---
This document provides an overview of the design choices made in the Circular Chess project. For more detailed information, refer to the codebase in each respective file.
