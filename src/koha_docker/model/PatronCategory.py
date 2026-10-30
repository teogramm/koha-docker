from dataclasses import dataclass


@dataclass
class PatronCategory:
    code: str
    description: str
    enrollment_months: int
    
Adult = PatronCategory("AD", "Adult patron", 120)