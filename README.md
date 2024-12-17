A Simple Template for Python Arcade Projects

## Includes:
- A `core` submodule for game features
- A `lib` submodule for utility features
- A `views` submodule for views
- A `resources` module for game resources
- `filefactory` functions for creating safe file-finding functions
- Simple Nuitka config, which should work on Linux, Windows, and macOS
- A `Window` and `View` subclass for easy overriding
- A `root` view so there is already a safe launchable window
- The arcade logo for a better executable logo
- prefilled `.gitignore` with common files in python + game dev
- a prefilled `pyproject.toml`
- includes a type cast `get_window` method for the custom window class
- includes a well-typed `clamp` and `map_range` function

## How to Use
Download the included zip file with this release.
Find and replace all references to `template` with your game's name.
This includes: `pyproject.toml`, `template/main.py`, `template/__main__.py`,
`template/views/root.py`, `template/views/TEMPLATE.py`, `template/lib/utils.py`,
`template/libs/application.py`.
Then, create your virtual environment and install the required modules using `pip install -I .[dev]`
