"""Minimal ASP data containers used to serialize facts for clingo."""

from itertools import chain
from typing import Iterable, Iterator, Tuple


class Atom:
    """Represent an ASP atom with a predicate and arguments."""

    def __init__(self, predicate: str, args: Iterable[object] = ()) -> None:
        self.predicate = predicate
        self.arguments: Tuple[object, ...] = tuple(args)

    def args(self) -> Tuple[object, ...]:
        return self.arguments

    def nb_args(self) -> int:
        return len(self.arguments)

    def arg(self, index: int) -> object:
        return self.arguments[index]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Atom):
            return NotImplemented
        return (
            self.predicate == other.predicate
            and self.arguments == other.arguments
        )

    def __hash__(self) -> int:
        return hash((self.predicate, self.arguments))

    def __str__(self) -> str:
        if self.arguments:
            return '{}({})'.format(
                self.predicate,
                ','.join(map(str, self.arguments)),
            )
        return self.predicate

    def __repr__(self) -> str:
        return str(self)

    def __iter__(self) -> Iterator[object]:
        return iter((self.predicate, self.arguments))


Term = Atom


class TermSet:
    """Set-like collection of ASP atoms."""

    def __init__(self, terms: Iterable[Atom] = ()) -> None:
        self._terms = frozenset(terms)

    def __iter__(self) -> Iterator[Atom]:
        return iter(self._terms)

    def __len__(self) -> int:
        return len(self._terms)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TermSet):
            return self._terms == other._terms
        try:
            return set(self._terms) == other
        except TypeError:
            return False

    def add(self, atom: Atom) -> None:
        self._terms |= frozenset({atom})

    def union(self, *others: 'TermSet') -> 'TermSet':
        return TermSet(chain(self._terms, *(other._terms for other in others)))

    def __str__(self) -> str:
        return '.'.join(map(str, self)) + ('.' if self._terms else '')

    def __repr__(self) -> str:
        return str(self)
