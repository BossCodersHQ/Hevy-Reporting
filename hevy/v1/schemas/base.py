"""This file was created originally using chatgpt to parse responses on the Hevy API Swagger page"""

from pydantic import BaseModel
from typing import Optional, List, Union
from datetime import datetime


class PostRoutinesRequestSet(BaseModel):
    type: str  # example: "normal"
    weight_kg: Optional[float] = None  # example: 100
    reps: Optional[int] = None  # example: 10
    distance_meters: Optional[int] = None  # example: None
    duration_seconds: Optional[int] = None  # example: None


class PostRoutinesRequestExercise(BaseModel):
    exercise_template_id: str  # example: "D04AC939"
    superset_id: Optional[int] = None  # example: None
    rest_seconds: Optional[int] = None  # example: 90
    notes: Optional[str] = None  # example: "Stay slow and controlled."
    sets: List[PostRoutinesRequestSet]


class PostRoutinesRequestBody(BaseModel):
    title: str  # example: "April Leg Day 🔥"
    notes: Optional[str] = (
        None  # example: "Focus on form over weight. Remember to stretch."
    )
    exercises: List[PostRoutinesRequestExercise]


class ExerciseTemplate(BaseModel): 
    id: str  # example: "b459cba5-cd6d-463c-abd6-54f8eafcadcb"
    title: str  # example: "Bench Press (Barbell)"
    type: str  # example: "weight_reps"
    primary_muscle_group: str  # example: "weight_reps"
    secondary_muscle_groups: List[str]
    is_custom: bool  # example: False


class RoutineExerciseSet(BaseModel):
    index: int  # example: 0
    set_type: str  # example: "normal"
    weight_kg: Optional[float] = None  # example: 100
    reps: Optional[int] = None  # example: 10
    distance_meters: Optional[int] = None  # example: None
    duration_seconds: Optional[int] = None  # example: None
    rpe: Optional[float] = None  # example: 9.5


class RoutineExercise(BaseModel):
    index: int  # example: 0
    title: str  # example: "Bench Press (Barbell)"
    notes: Optional[str] = None  # example: "Focus on form. Go down to 90 degrees."
    exercise_template_id: str  # example: "05293BCA"
    supersets_id: Optional[int] = None  # example: 0
    sets: List[RoutineExerciseSet]


class Routine(BaseModel):
    id: str  # example: "b459cba5-cd6d-463c-abd6-54f8eafcadcb"
    title: str  # example: "Upper Body 💪"
    updated_at: datetime  # example: "2021-09-14T12:00:00Z"
    created_at: datetime  # example: "2021-09-14T12:00:00Z"
    exercises: List[RoutineExercise]


class WorkoutExerciseSet(BaseModel):
    index: int  # example: 0
    set_type: str  # example: "normal"
    weight_kg: Optional[float] = None  # example: 100
    reps: Optional[int] = None  # example: 10
    distance_meters: Optional[int] = None  # example: None
    duration_seconds: Optional[int] = None  # example: None
    rpe: Optional[float] = None  # example: 9.5


class WorkoutExercise(BaseModel):
    index: int  # example: 0
    title: str  # example: "Bench Press (Barbell)"
    notes: Optional[str] = (
        None  # example: "Paid closer attention to form today. Felt great!"
    )
    exercise_template_id: str  # example: "05293BCA"
    supersets_id: Optional[int] = None  # example: 0
    sets: List[WorkoutExerciseSet]


class Workout(BaseModel):
    id: str  # example: "b459cba5-cd6d-463c-abd6-54f8eafcadcb"
    title: str  # example: "Morning Workout 💪"
    description: Optional[str] = None  # example: "Pushed myself to the limit today!"
    start_time: datetime  # example: "2021-09-14T12:00:00Z"
    end_time: datetime  # example: "2021-09-14T12:00:00Z"
    updated_at: datetime  # example: "2021-09-14T12:00:00Z"
    created_at: datetime  # example: "2021-09-14T12:00:00Z"
    exercises: List[WorkoutExercise]


class UpdatedWorkout(BaseModel):
    type: str  # example: "updated"
    workout: Workout


class DeletedWorkout(BaseModel):
    type: str  # example: "deleted"
    id: str  # example: "efe6801c-4aee-4959-bcdd-fca3f272821b"
    deleted_at: Optional[datetime] = None  # example: "2021-09-13T12:00:00Z"


class PaginatedWorkoutEvents(BaseModel):
    page: int  # example: 1
    page_count: int  # example: 5
    events: List[Union[UpdatedWorkout, DeletedWorkout]]
