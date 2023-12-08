# circular-chess

## Overview

Circular Chess is a unique chess variant played on a circular board. This project aims to implement the game rules and provide a platform for enthusiasts to play circular chess. [Here](https://www.youtube.com/watch?v=M2ZEVt-AviE) is a quick playthrough of a match of circular chess!

### Author

- [Miguel Fernandez](https://github.com/fezm)

I am the sole author and contributor to this project. [Eddie Sharick](https://www.youtube.com/@eddiesharick6649)'s "Chess Engine in Python" series was a big help though!


## Features

- **Circular Board:** Experience chess in a whole new way with a circular game board.


## Rules

In Circular Chess, the starting position is derived from orthodox chess by cutting the board in half and bending the two halves to join at the ends. The piece arrangement is as follows:

- The king and queen start on the innermost ring, with the queen on a square of the same color.
- The bishops start in the second ring from the center.
- The knights start on the third ring.
- The rooks start on the outermost ring.
- Pawns are positioned in front of the pieces.

### Piece Movements

The moves of the pieces are identical to orthodox chess:

- A queen or rook may move any distance around a ring if not obstructed.
- The "null move" of moving a piece all the way around the board and back to its original square is not permitted.
- A pawn is promoted after moving six squares from its initial position, reaching the square immediately before the opponent's starting line.

### Special Rules

- Castling and en passant captures are not permitted.
- "Snaffling" is allowed, meaning you can win the game immediately by capturing the opponent's king after they either moved into or failed to move out of check.

These rules create a unique and engaging variant of chess, offering a different strategic dimension with the circular board layout.


## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- [Python 3.9.6](https://www.python.org/downloads/release/python-396/): Circular Chess is built and tested with Python 3.9.6. You can download it from the official Python website.

- [NumPy](https://numpy.org/): NumPy is used for numerical operations in Python. Install it using:

  ```bash
  pip3 install numpy

- [Pygame](https://www.pygame.org/): Pygame is used for creating the graphical interface of Circular Chess. Install it using:

  ```bash
  pip3 install pygame


### Controls

- **Move Piece:** To move a piece, click anywhere on the space it occupies, and then click on the space where you want to move it. If the move is valid, it will be executed.

- **Undo Move:** Press the "Z" key to undo the last move.


### Usage

To play Circular Chess, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/circular-chess.git

2. Navigate to the project directory:

   ```bash
   cd circular-chess

3. Run the game:

   ```bash
    python3 main.py

4. Enjoy playing Circular Chess on the circular board!
