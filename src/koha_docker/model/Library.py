from dataclasses import dataclass


@dataclass
class Library:
    code: str
    name: str

Springfield = Library("SPR", "Springfield")
Marytown = Library("MRT", "Marytown")