from __future__ import annotations
from typing import Any, Protocol, TypeVar, TYPE_CHECKING

from arcade import get_window as get_arcade_window
if TYPE_CHECKING:
    from template.core.application import Window


__all__ = (
    'get_window',
    'get_arcade_window',
    'SupportsDunderLT',
    'SupportsDunderGT',
    'HasAddSubMul',
    'SupportsRichComparison',
    'clamp',
    'map_range'
)


def get_window() -> Window:
    return get_arcade_window() # type: ignore -- This is just a type casting


# Stolen from pylance
_T_contra = TypeVar("_T_contra", contravariant=True)
_T_co = TypeVar("_T_co", covariant=True)


class SupportsDunderLT(Protocol[_T_contra]):
    def __lt__(self, other: _T_contra, /) -> bool:
        ...

class SupportsDunderGT(Protocol[_T_contra]):
    def __gt__(self, other: _T_contra, /) -> bool:
        ...

class HasAddSubMul(Protocol[_T_contra, _T_co]):
    """Matches types which work with :py:func:`arcade.math.lerp`."""

    # The / matches float and similar operations to keep pyright
    # happy since built-in arithmetic makes them positional only.
    # See https://peps.python.org/pep-0570/
    def __add__(self, value: _T_contra, /) -> _T_co: ...
    def __sub__(self, value: _T_contra, /) -> _T_co: ...
    def __mul__(self, value: _T_contra, /) -> _T_co: ...


type SupportsRichComparison = SupportsDunderLT[Any] | SupportsDunderGT[Any]


TT = TypeVar("TT", bound=SupportsRichComparison)
L = TypeVar("L", bound=HasAddSubMul)


def clamp(min_val: TT, val: TT, mav_val: TT) -> TT:
    """Clamp a `val` to be no lower than `minVal`, and no higher than `maxVal`."""
    return max(min_val, min(mav_val, val))


def map_range(x: L, n1: L, m1: L, n2: L = -1, m2: L = 1) -> L:
    """Scale a value `x` that is currently somewhere between `n1` and `m1` to now be in an
    equivalent position between `n2` and `m2`."""
    # Make the range start at 0.
    old_max = m1 - n1
    old_x = x - n1
    percentage = old_x / old_max

    # Shmoove it over.
    new_max = m2 - n2
    new_pos = new_max * percentage
    ans = new_pos + n2
    return ans
