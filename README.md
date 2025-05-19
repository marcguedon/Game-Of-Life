# Game of Life

The Game of Life is a zero-player cellular automaton game which is Turing-complete. Devised by John Conway, it consists of a grid of cells that can be either dead or alive. The state of each cell evolves (it is born, survives or dies) at each step (generation) according to a set of simple rules based on the states of its eight neighbors.

Despite its simple rules, the Game of Life can produce complex and fascinating patterns.

## Compilation of the application

To compile the script into an only one executable file, you will need to install the PyInstaller library.
```console
python3 -m pip install pyinstaller
```

You can now start to compile the script. You may also need to use the `--exclude-module <package>` option to exclude others PyQt versions.
```console
pyinstaller --clean --onefile --windowed src/main.py
pyinstaller --clean --onefile --windowed --exclude-module PySide2 src/main.py
```

Add the line `import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5)` at the top in the `main.spec` file. Then, run the next command.
```console
pyinstaller main.spec
```

The `main` executable file has been created in the `dist/` folder. You can execute it.
```
./dist/main
```