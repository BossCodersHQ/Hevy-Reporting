from enum import Enum
from typing import List
from pydantic import BaseModel


class VolumeReport(BaseModel):
    body_part: str
    sets_completed: int
    threshold: int
    is_under_threshold: bool
    exercises: list


class VolumeReports(BaseModel):
    created_at: int
    suggested_exercises: list
    volume_reports: List[VolumeReport]

class BodyPart(str, Enum):
    SHOULDERS = "shoulders"
    CHEST = "chest"
    BICEPS = "biceps"
    TRICEPS = "triceps"
    LATS = "lats"
    UPPER_BACK = "upper_back"
    QUADRICEPS = "quadriceps"
    HAMSTRINGS = "hamstrings"
    GLUTES = "glutes"
    CALVES = "calves"
    FOREARMS = "forearms"
    TRAPS = "traps"
    NECK = "neck"

class Thresholds(BaseModel):
    thresholds: dict[BodyPart, int]
