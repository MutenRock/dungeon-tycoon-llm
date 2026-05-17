from pydantic import BaseModel


class Resources(BaseModel):
    wood: int = 20
    stone: int = 20
    meat: int = 10
