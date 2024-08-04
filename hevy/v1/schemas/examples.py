import json
from pathlib import Path
from hevy.schemas.legit import 
EXAMPLES_BASE_FOLDER = "./examples"


def get_paginated_workouts() -> dict:
    """Load an example paginated workouts"""
    with open(Path(__file__).parent / EXAMPLES_BASE_FOLDER /"paginated_workout.json") as f:
        return json.load(f)
    
  

if __name__ == "__main__":
    paginated_workouts = get_paginated_workouts()
    pw = PaginatedWorkouts.model_validate(paginated_workouts)
    print(pw)
    