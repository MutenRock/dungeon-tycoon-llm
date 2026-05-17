from pydantic import BaseModel


class Hero(BaseModel):
    name: str
    hero_class: str
    hp: int
    attack: int
