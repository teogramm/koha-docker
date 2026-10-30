from dataclasses import dataclass


@dataclass
class ItemType:
    code: str
    description: str
    
Book = ItemType("B", "Book")