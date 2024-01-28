from typing import Callable, Dict, TypeVar

T = TypeVar("T")

Control = Callable[..., Dict[str, str]]
Generation = Callable[..., str]
Analysis = Callable[..., str]
Function = Callable[..., str]
