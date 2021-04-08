
from dataclasses import dataclass

@dataclass
class Candidate:
    '''
    A candidate competing in the elections.
    '''
    name: str
    twitter: str
