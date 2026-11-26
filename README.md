# camel_case_splitter_lib

Splits PascalCase and camelCase identifiers into lowercase word tokens for readability or indexing.

```python
from camel_case_splitter_lib import split

split("HTTPServer")
# ['http', 'server']

split("camelCase2D")
# ['camel', 'case', '2', 'd']
```

The public API is exactly two functions:

- `split_identifier(identifier: str) -> list[str]`
- `split(text: str) -> list[str]` (an alias for `split_identifier`)

Both return a list of lowercase strings.  Both raise `TypeError` when given a
non-string argument.

## Why this exists

Indexing systems and search tools often need to turn an identifier such as
`XMLHttpRequest` into the words a human would read: `xml`, `http`, `request`.
Doing that with a regular expression forces a choice between two ambiguous
cases: acronyms (`HTTPServer`) and digits (`parse2D`).  This library picks one
interpretation and states it plainly:

- A run of uppercase letters followed by a lowercase letter splits before the
  last uppercase letter, so `HTTPServer` becomes `http` and `server`.
- Digits are always their own tokens, so `parse2D` becomes `parse`, `2`, and
  `d`.
- Underscores, hyphens, and whitespace are hard separators and are dropped.
- Every returned token is lowercased.

That means `split("HTTP")` returns `['http']`, not `['h', 't', 't', 'p']`.
If you need a different treatment of acronyms or digits, this library is not
for you; the trade-off is deliberate and documented so that callers can rely on
it.

## The awkward edge

Non-ASCII letters are treated as ordinary characters and do not create case
boundaries.  `split("caféBar")` returns `['cafébar']`, not `['café', 'bar']`.
This keeps the splitter deterministic and independent of locale; if you need
Unicode case folding, pre-normalise your input.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

