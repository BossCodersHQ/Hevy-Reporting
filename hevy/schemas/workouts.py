from pydantic import BaseModel
from typing import List, Optional


class Sets(BaseModel):
    index: int
    set_type: str
    weight_kg: Optional[float]
    reps: Optional[int]
    distance_meters: Optional[float]
    duration_seconds: Optional[float]
    rpe: Optional[float]


class Exercise(BaseModel):
    index: int
    title: str
    notes: str
    exercise_template_id: str
    supersets_id: int
    sets: List[Sets]

class Workout(BaseModel):
    id: str
    title: str
    description: str
    start_time: str
    end_time: str
    updated_at: str
    created_at: str
    exercises: List[Exercise]



class PaginatedWorkouts(BaseModel):
    page:int
    page_count: int
    workouts: List[Workout]


if __name__ == "__main__":
    from pprint import pprint
    from hevy.schemas.examples import EX_PAGINATED_WORKOUTS

    pprint(PaginatedWorkouts.model_validate(EX_PAGINATED_WORKOUTS))