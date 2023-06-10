from pydantic import BaseModel
from enum import Enum

class Team(BaseModel):
    name: str
    crest: str
    country: str
    league: str
    squad_size: int

class TeamType(str, Enum):
    TRENDING = "trending"
    CLUB = "club"
    NATIONAL = "national"