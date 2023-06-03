from pydantic import BaseModel

class Team(BaseModel):
    name: str
    crest: str
    country: str
    league: str
    squad_size: int