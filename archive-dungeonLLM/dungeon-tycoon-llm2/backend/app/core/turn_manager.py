from enum import Enum


class TurnPhase(str, Enum):
    NIGHT = "night"
    DAY = "day"
    RESOLUTION = "resolution"
