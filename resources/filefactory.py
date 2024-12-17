from typing import IO as _IO
from collections.abc import Callable
from pathlib import Path
from contextlib import contextmanager
import importlib.resources as pkg

try:
    from importlib.resources import Anchor
except ImportError:
    from importlib.resources import Package as Anchor

__all__ = (
    "make_file_opener",
    "make_string_opener",
    "make_binary_opener",
    "make_path_finder"
)

type IO = _IO[bytes] | _IO[str]


def make_file_opener(
        anchor: Anchor,
        file_extension: str | None = None,
        _mode: str = "r",
        _buffering: int = -1,
        _encoding: str | None = None,
        _errors: str | None = None,
        _newline: str | None = None,
        _closefd: bool = True,
        _opener: Callable[[str, int], int] | None = None
        ) -> Callable[[str, tuple[str, ...], str, int, str | None, str | None, str | None, bool, Callable[[str, int], int] | None], IO]:
    """
    Create a reusable function for opening files of a particular type at a particular location
    Can also set new defaults for the `open` function used internally.

    See `open` for other arguments

    :param anchor: The location to open at, as a module from `import <x>`.
    :param file_extension: The file extension expected to open. can be `.<extension>` or  `<extension>` or `None`.
        If None is provided then the extension must included in the file name when calling the returned function
    :return: A function which creates a context manager around an opened file
    """

    # Add the dot to the extension. We expect people to not add one, but its easier to add then remove
    if file_extension is not None and not file_extension.startswith('.'):
        data_extension = '.'+file_extension
    root = pkg.files(anchor)

    @contextmanager
    def _open_file(
        name: str,
        sub_directories: tuple[str, ...] = (),
        mode: str = _mode,
        buffering: int = _buffering,
        encoding: str | None = _encoding,
        errors: str | None = _errors,
        newline: str | None = _newline,
        closefd: bool = _closefd,
        opener: Callable[[str, int], int] | None = _opener
        ) -> IO:
            """
            Open a file with a predetermined location.
            Also has the arguments for `open` available. Custom defaults can be provided
            at the same time as the type and location

            See `open` for other arguments

            Args:
                name: The name of the file to open. If no file extension was provided on
                    creation it must be included in the name.
                sub_directory: Any sub directories from the root WITHOUT seperators ('<subdir1>', '<subdir2>')
            Returns:
                A context manger for opening files.
            """
            file_name = f'{name}{data_extension}' if data_extension is not None else f'{name}'
            path = root.joinpath(*sub_directories).joinpath(file_name)
            return path.open(mode, buffering, encoding, errors, newline, closefd, opener)

    return _open_file


def make_path_finder(anchor: Anchor, file_extension: str | None = None) -> Callable[[str, tuple[str, ...]], Path]:
    """
    Create a reusable function for finding paths.

    :param anchor: The location to start at, as a module from `import <x>`.
    :param file_extension: The file extension expected to find. can be `.<extension>` or  `<extension>` or `None`.
        If None is provided then the extension must included in the file name when calling the returned function
    """

    if file_extension is not None and not file_extension.startswith('.'):
        file_extension = '.' + file_extension
    root = pkg.files(anchor)

    def _find_path(name: str, sub_directories: tuple[str, ...] = ()) -> Path:
        """
        Find the absolute path to the file with specified name and file extension.
        Uses the file extension provided at creation. If None was used then name
        must include the file extension

        Args:
            name: The name of the file to open. If no file extension was provided on
                creation it must be included in the name.
            sub_directory: Any sub directories from the root WITHOUT seperators ('<subdir1>', '<subdir2>')

        Returns:
            A pathlib Path object with the absolute path to the specified file
        """
        file_name = f'{name}{file_extension}' if file_extension is not None else name
        path = root.joinpath(*sub_directories).joinpath(file_name)
        with pkg.as_file(path) as p:
            return p

    return _find_path


def make_string_opener(anchor: Anchor, file_extension: str='txt', _encoding: float = 'utf-8') -> Callable[[str, tuple[str, ...], str], str]:
    """
    Create a reusable function for retrieving the text from files of a particular type.

    Args:
        anchor: The location to open at, as a module from `import <x>`.
        file_extension: The file extension expected to open. can be `.<extension>` or just `<extension>`. Defaults to 'txt'
        _encoding: The default text encoding to use. Defaults to 'utf-8'.

    Returns:
        The reusable read string function
    """
    if not file_extension.startswith('.'):
         file_extension = '.' + file_extension
    root = pkg.files(anchor)

    def _read_string(name: str, sub_directories: tuple[str, ...] = (), encoding: str = _encoding) -> str:
        """
        Read the entire contents of the provided file and return it as a single sting.
        Uses the file extension provided at creation.

        Args:
            name: The name of the file WITHOUT the file extension
            sub_directories: Any sub directories from the root WITHOUT seperators ('<subdir1>', '<subdir2>')
            encoding: The text encoding to use. Defaults to the provided encoding at creation.

        Returns:
            The entire file as a single string.
        """
        file_name = f'{name}{file_extension}'
        path = root.joinpath(*sub_directories).joinpath(file_name)
        return path.read_text(encoding)

    return _read_string

def make_binary_opener(anchor: Anchor, file_extension: str) -> Callable[[str, tuple[str, ...]], bytes]:
    """
    Create a reusable function for retrieving the binary from files of a particular type.

    Args:
        anchor: The location to open at, as a module from `import <x>`.
        file_extension: The file extension expected to open. can be `.<extension>` or just `<extension>`

    Returns:
        The reusable read bytes function
    """
    if not file_extension.startswith('.'):
         file_extension = '.' + file_extension
    root = pkg.files(anchor)

    def _read_bytes(name: str, sub_directories: tuple[str, ...] = ()) -> bytes:
        """
        Read the entire contents of the provided file and return it as bytes.
        Uses the file extension provided at creation.

        Args:
            name: The name of the file WITHOUT the file extension
            sub_directories: Any sub directories from the root WITHOUT seperators ('<subdir1>', '<subdir2>')

        Returns:
            The entire file as bytes
        """
        file_name = f'{name}{file_extension}'
        path = root.joinpath(*sub_directories).joinpath(file_name)
        return path.read_binary()

    return _read_bytes
