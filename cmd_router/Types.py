from dataclasses import dataclass
from typing import Callable 

@dataclass
class Command:
    name:str
    func:Callable
    description:str
        
@dataclass
class Event:
    name:str
    func:Callable