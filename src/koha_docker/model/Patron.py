from dataclasses import dataclass

from koha_docker.model.Credentials import Credentials

@dataclass
class Patron:
    first_name: str
    surname: str
    card_number: str
    login: Credentials
    
Administrator = Patron("John", "Smith", "1", Credentials("jsmith", "StrongPW126"))