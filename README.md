*This project has been created as part of the 42 curriculum by <mvoskany>, <edmvarda>.*

# A-Maze-ing

## Description

A-Maze-ing is a Python project that generates and displays random mazes from a configuration file.

The project implements a maze generator using **Prim's algorithm**. The generated maze can be either:

* **Perfect**, meaning there is exactly one path between any two reachable cells and no loops.
* **Non-perfect**, designed as a playable Pac-Man-like board with multiple routes and few dead ends.

The maze uses a hexadecimal wall representation internally and in the output file. Each cell contains four possible walls: North, East, South and West.

The project also includes:

* A terminal-based visual representation.
* Entry and exit markers.
* A shortest-path solver.
* Show/hide solution functionality.
* Multiple wall colours.
* Maze regeneration.
* The special "42" pattern.
* Reproducible maze generation using a seed.
* Configuration validation and error handling.
* A reusable `MazeGenerator` class that can be used independently in another project.

## Requirements

* Python 3.10 or later
* Pydantic
* Flake8
* Mypy

## Instructions

### Installation

Install the required dependencies with:

```bash
pip install pydantic flake8 mypy
```

It is recommended to use a virtual environment.

### Running the project

Run the program with:

```bash
python3 a_maze_ing.py config.txt
```

For example:

```bash
python3 a_maze_ing.py config.txt
```

The program reads the configuration, generates the maze, calculates the shortest path and displays the maze in the terminal.

The generated solution is also written to the file specified by `OUTPUT_FILE`.

### Controls

When the maze is displayed:

```text
R - Regenerate the maze
P - Show / hide the shortest path
C - Change wall colour
Q - Quit
```

Press `R` to generate a new maze. If a seed was specified in the configuration, regeneration uses a new random seed so that a different maze is produced.

## Configuration File

The configuration file contains one `KEY=VALUE` pair per line.

Lines beginning with `#` are treated as comments and ignored.

### Required keys

```text
WIDTH=10
HEIGHT=10
ENTRY=2,2
EXIT=3,8
OUTPUT_FILE=maze.txt
PERFECT=True
```

### Optional keys

```text
SEED=42
```

### Configuration parameters

| Key           | Description                                  | Example                |
| ------------- | -------------------------------------------- | ---------------------- |
| `WIDTH`       | Width of the maze in cells                   | `WIDTH=20`             |
| `HEIGHT`      | Height of the maze in cells                  | `HEIGHT=15`            |
| `ENTRY`       | Entry coordinates                            | `ENTRY=0,0`            |
| `EXIT`        | Exit coordinates                             | `EXIT=19,14`           |
| `OUTPUT_FILE` | File where the maze and solution are written | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | Enables perfect maze generation              | `PERFECT=True`         |
| `SEED`        | Seed used for reproducible generation        | `SEED=42`              |

Coordinates are written as:

```text
ENTRY=x,y
EXIT=x,y
```

The configuration validator checks that the coordinates are inside the maze, that entry and exit are different, and that neither is located inside the "42" pattern.

### Example configuration

```text
# A-Maze-ing configuration

WIDTH=20
HEIGHT=15
ENTRY=1,1
EXIT=18,13
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

## Maze Representation

Each maze cell is represented by one hexadecimal digit.

The four lowest bits represent the four walls:

```text
Bit 0: North
Bit 1: East
Bit 2: South
Bit 3: West
```

A bit set to `1` means that the wall is closed.

A bit set to `0` means that the wall is open.

For example:

```text
0011 = 3
```

means that the North and East walls are closed while the South and West walls are open.

The maze is stored row by row, with one line per maze row.

After the maze, the output file contains:

1. The entry coordinates.
2. The exit coordinates.
3. The shortest path represented using `N`, `E`, `S` and `W`.

## Maze Generation Algorithm

### Prim's Algorithm

The maze generator uses a randomized version of **Prim's algorithm**.

The algorithm starts from a randomly selected cell and keeps a collection of neighbouring unvisited cells called the frontier.

The general process is:

1. Initialize every cell with all four walls closed.
2. Mark the special "42" cells as unavailable for maze generation.
3. Select a random starting cell.
4. Mark it as visited.
5. Add its unvisited neighbours to the frontier.
6. Randomly select a cell from the frontier.
7. Find one of its already visited neighbours.
8. Remove the wall between the two cells.
9. Mark the selected cell as visited.
10. Add its unvisited neighbours to the frontier.
11. Continue until there are no more frontier cells.

This produces a connected maze without loops when operating in perfect-maze mode.

### Why Prim's Algorithm?

Prim's algorithm was chosen because it is well suited to random maze generation and is relatively straightforward to implement and understand.

It also naturally produces a spanning tree when each new cell is connected to exactly one previously visited cell. This makes it particularly useful for generating perfect mazes.

Another advantage is that the algorithm uses randomness while still guaranteeing connectivity of the generated maze, provided that the generation is performed correctly.

For non-perfect mazes, additional walls can be removed after generation to create loops and reduce dead ends.

## Perfect and Non-Perfect Modes

### Perfect Maze

When:

```text
PERFECT=True
```

the maze is generated as a perfect maze.

A perfect maze is a maze with no loops, meaning there is exactly one path between any two cells.

### Non-Perfect Maze

When:

```text
PERFECT=False
```

additional walls can be removed to create alternative routes.

This allows the maze to behave more like a Pac-Man-style board, where the player can have multiple possible routes instead of being forced through one unique path.

The generator also attempts to reduce dead ends.

## The "42" Pattern

The maze contains a special "42" pattern in the centre when the maze is large enough.

The pattern is made from fully closed cells and is excluded from the normal maze-generation process.

The pattern requires a minimum maze size of:

```text
WIDTH >= 9
HEIGHT >= 7
```

If the maze is too small, the pattern cannot be placed and an error message is displayed.

## Shortest Path

After generating a maze, the program calculates a shortest valid path between the configured entry and exit.

The path finder uses a **bidirectional Breadth-First Search (BFS)**.

BFS explores the maze level by level, making it suitable for finding a shortest path when every movement has the same cost.

The resulting path is converted into a sequence of:

```text
N
E
S
W
```

and written to the output file.

The shortest path can also be displayed visually in the terminal.

## Visual Representation

The maze is displayed using ASCII/Unicode characters.

The display shows:

* Maze walls
* Entry (`S`)
* Exit (`E`)
* Shortest path
* The "42" pattern
* Coloured walls

The wall colour can be changed interactively while the program is running.

## Project Structure

A typical project structure is:

```text
.
├── a_maze_ing.py
├── mazegen.py
├── utils.py
├── parse_validate.py
├── validator.py
├── my_exceptions.py
├── config.txt
├── maze.txt
├── Makefile
├── README.md
├── LICENSE.md
├── .gitignore
└── mazegen-*.whl
```

The exact package/build files may vary depending on the final packaging structure.

## Reusable Code

The main reusable component is the `MazeGenerator` class.

It is implemented independently from the terminal interface and can therefore be imported into another Python project.

A basic example is:

```python
from mazegen import MazeGenerator

config = {
    "WIDTH": 20,
    "HEIGHT": 15,
    "PERFECT": True,
    "SEED": 42
}

generator = MazeGenerator(config)
maze = generator.generate()

print(maze)
```

The generated maze is returned as a two-dimensional list of integers.

Each integer represents the walls of one cell using the hexadecimal/bit representation described above.

The reusable generator can be configured with different maze sizes and seeds.

For example:

```python
config = {
    "WIDTH": 30,
    "HEIGHT": 20,
    "PERFECT": False,
    "SEED": 12345
}

generator = MazeGenerator(config)
maze = generator.generate()
```

The maze-generation logic is separated from the display and configuration parsing so that it can be reused by a future project.

## Packaging

The reusable maze generator is provided as a Python package named:

```text
mazegen-*
```

The package can be built using the standard Python packaging tools.

For example:

```bash
python3 -m build
```

This produces a package such as:

```text
mazegen-1.0.0-py3-none-any.whl
```

The generated package can then be installed with:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

## Error Handling

The program handles common errors such as:

* Missing configuration files.
* Invalid configuration syntax.
* Duplicate configuration keys.
* Unknown configuration keys.
* Missing required configuration keys.
* Invalid integer values.
* Invalid coordinates.
* Entry and exit being identical.
* Entry or exit being inside the "42" pattern.
* Maze dimensions that are invalid.
* Other unexpected runtime errors.

Clear error messages are displayed instead of allowing the program to fail silently.

## Testing and Code Quality

The project follows Python 3.10+ type-hinting requirements.

The code uses:

* Type hints.
* Docstrings.
* `flake8` for style checking.
* `mypy` for static type checking.

The required lint command is:

```bash
flake8 .
mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
```

If a Makefile is provided, these checks can also be run using:

```bash
make lint
```

## Makefile

The Makefile provides commands for common project operations.

Expected commands include:

```bash
make install
make run
make debug
make clean
make lint
```

`make install` installs dependencies.

`make run` executes the project.

`make debug` runs the project using Python's debugger.

`make clean` removes temporary Python files and caches.

`make lint` runs Flake8 and Mypy.

## Team and Project Management

### Team Members

* `<mvoskany>` — Maze generation and algorithm (Prim's algorithm)
* `<edmvarda>` — Configuration parsing and validation
* `<mvoskany>, <edmvarda>` — Shorest path finding (Bidirectional BFS) and Visualisation

### Planning

The project was divided into several main stages:

1. Understand the subject requirements.
2. Design the maze representation.
3. Implement the maze generation algorithm.
4. Implement configuration parsing and validation.
5. Implement shortest-path calculation.
6. Implement the terminal visualisation.
7. Implement interactive controls.
8. Implement reusable package support.
9. Test the generated mazes.
10. Run linting and fix code-quality issues.
11. Prepare the README and final submission.

During development, the implementation was adjusted as problems were discovered through testing and peer review.

### What Worked Well

* Separating maze generation from visualisation made the code easier to modify.
* Using a wall bitmask provides a compact representation of the maze.
* Using a seed makes maze generation reproducible.
* Bidirectional BFS provides an efficient way to find the shortest path.
* Interactive controls make it easy to test different generated mazes.

### What Could Be Improved

* More automated tests could be added for unusual maze dimensions and configurations.
* The non-perfect generation could be further improved to consistently minimise dead ends.
* The visualisation could be extended with a graphical interface.
* More maze-generation algorithms could be supported in the future.

## Tools Used

The project was developed using:

* Python
* Git and GitHub
* VS Code
* Pydantic
* Flake8
* Mypy
* Python's built-in debugger
* Terminal/CLI tools

## AI Usage

AI tools were used as an assistance and learning resource during development.

They were used for:

* Explaining maze-generation algorithms such as Prim's algorithm.
* Discussing data structures and maze representations.
* Reviewing code for possible bugs and improvements.
* Helping identify type-checking and linting issues.
* Discussing configuration parsing and validation.
* Improving the terminal visualisation.
* Helping understand project requirements and organise the README.
* Suggesting tests and edge cases.

AI-generated suggestions were reviewed, tested and adapted before being used. The final code was checked manually and with tools such as Flake8 and Mypy.

The goal was to use AI to assist with repetitive or difficult tasks while maintaining an understanding of the implemented code.

## Resources

The following resources were used to understand the concepts involved in the project:

* Prim's algorithm and minimum spanning trees.
* Breadth-First Search and shortest-path algorithms.
* Python documentation for lists, sets, tuples, file handling and the `random` module.
* Python type hints and the `typing` module.
* Pydantic documentation for data validation.
* Flake8 documentation for Python code style.
* Mypy documentation for static type checking.
* Python packaging documentation for creating reusable packages.
* The official A-Maze-ing project subject and the provided maze analysis script.

## License

This project includes a `LICENSE.md` file specifying the license under which the reusable maze generator may be reused and distributed.

The license is intended to allow the maze generator to be incorporated into future projects.
