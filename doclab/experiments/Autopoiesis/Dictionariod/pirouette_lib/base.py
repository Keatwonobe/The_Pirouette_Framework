# Auto-generated base interfaces for pirouette_lib
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Protocol, TypedDict

class Context(TypedDict, total=False):
    data: Any
    params: Dict[str, Any]

@dataclass
class Measurement:
    name: str
    description: str
    compute: Callable[[Context], Any]

@dataclass
class Constraint:
    name: str
    description: str
    check: Callable[[Context], bool]

@dataclass
class Mapping:
    name: str
    description: str
    confidence: float
    transform: Optional[Callable[[Any], Any]] = None

class Term(Protocol):
    canonical_id: str
    symbol: str

    def measure(self, ctx: Context) -> List[Measurement]: ...
    def constraints(self) -> List[Constraint]: ...
    def mappings(self) -> List[Mapping]: ...
    def example(self) -> str: ...
