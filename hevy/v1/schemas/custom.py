import hevy.v1.schemas.base as base
from pydantic import BaseModel
from typing import List


class PaginatedWorkouts(BaseModel):
    page: int
    page_count: int
    workouts: List[base.Workout]
