"""Split PascalCase and camelCase identifiers into lowercase word tokens.

This module intentionally implements a single, documented interpretation of
how to break identifiers.  The rules are:

* An underscore, hyphen, or whitespace is a hard separator.  The separator
  itself is dropped and the surrounding text is split as if it were two
  identifiers.
* A run of uppercase letters followed by a lowercase letter is split before
  the last uppercase letter, so ``HTTPServer`` becomes ``http`` and ``server``.
* A lowercase letter or digit followed by an uppercase letter is split between
  them, so ``camelCase`` becomes ``camel`` and ``case``.
* Runs of digits are kept as a single token, so ``parse2D`` becomes ``parse``,
  ``2``, and ``d``.
* Leading, trailing, and repeated separators produce no empty tokens.

Every returned token is lowercased.  The function never raises for string
input; it only raises :class:`TypeError` when given a non-string.
"""

from __future__ import annotations

from typing import List

__all__ = ["split", "split_identifier"]


def _is_upper(ch: str) -> bool:
    return "A" <= ch <= "Z"


def _is_lower(ch: str) -> bool:
    return "a" <= ch <= "z"


def _is_digit(ch: str) -> bool:
    return "0" <= ch <= "9"


def _is_separator(ch: str) -> bool:
    # Only ASCII separators are recognised.  Unicode whitespace and other
    # punctuation would make the token boundaries locale-dependent, which is
    # not useful for identifier indexing.
    return ch in "_- \t\n\r\f\v"


def _split_word(word: str) -> List[str]:
    """Split a single separator-free chunk into lowercase tokens."""
    if not word:
        return []

    # First, split on digit/non-digit boundaries.  Digits are their own
    # tokens because mixing them with letters makes indexing less useful.
    pieces: List[str] = []
    current = ""
    current_is_digit = _is_digit(word[0])
    for ch in word:
        ch_is_digit = _is_digit(ch)
        if ch_is_digit != current_is_digit:
            if current:
                pieces.append(current)
            current = ch
            current_is_digit = ch_is_digit
        else:
            current += ch
    if current:
        pieces.append(current)

    tokens: List[str] = []
    for piece in pieces:
        if piece[0].isdigit():
            tokens.append(piece)
            continue
        tokens.extend(_split_alpha(piece))
    return tokens


def _split_alpha(piece: str) -> List[str]:
    """Split an alphabetic piece on case boundaries."""
    tokens: List[str] = []
    start = 0
    n = len(piece)
    for i in range(1, n):
        prev = piece[i - 1]
        curr = piece[i]
        nxt = piece[i + 1] if i + 1 < n else ""

        boundary = False
        # lower -> upper: camelCase boundary.
        if _is_lower(prev) and _is_upper(curr):
            boundary = True
        # upper -> upper -> lower: acronym boundary, split before the last
        # uppercase letter so HTTPServer becomes HTTP + Server.
        elif _is_upper(prev) and _is_upper(curr) and nxt and _is_lower(nxt):
            boundary = True

        if boundary:
            tokens.append(piece[start:i])
            start = i
    tokens.append(piece[start:])
    return tokens


def split_identifier(identifier: str) -> List[str]:
    """Split *identifier* into lowercase word tokens.

    The input is treated as a single identifier.  Separators still apply, so
    ``foo_bar`` yields ``["foo", "bar"]``.

    Raises
    ------
    TypeError
        If *identifier* is not a :class:`str`.
    """
    if not isinstance(identifier, str):
        raise TypeError("identifier must be a str, got %r" % (type(identifier).__name__,))

    tokens: List[str] = []
    chunk = ""
    for ch in identifier:
        if _is_separator(ch):
            if chunk:
                tokens.extend(_split_word(chunk))
                chunk = ""
        else:
            chunk += ch
    if chunk:
        tokens.extend(_split_word(chunk))
    return [t.lower() for t in tokens]


def split(text: str) -> List[str]:
    """Split *text* into lowercase word tokens.

    This is an alias for :func:`split_identifier`, kept because the shorter
    name reads better when the input is already known to be an identifier.

    Raises
    ------
    TypeError
        If *text* is not a :class:`str`.
    """
    return split_identifier(text)
