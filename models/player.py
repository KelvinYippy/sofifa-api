from pydantic import BaseModel

class Player(BaseModel):
    name: str
    age: int
    overall: int
    potential: int
    positions: list[str]