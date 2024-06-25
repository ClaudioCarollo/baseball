from dataclasses import dataclass

@dataclass
class Team:
    code: str
    name: str

    def __hash__(self):
        return hash(self.code)
