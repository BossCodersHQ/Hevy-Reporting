import asyncio
import io
import logging
import os

from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
import reporting.conf as conf
from hevy.v1.client import HevyClientV1
from collections import Counter
from datetime import datetime, timedelta, date

from reporting.schemas import Thresholds

DEFAULT_THRESHOLDS = {
    "shoulders": 10,
    "biceps": 10,
    "quadriceps": 10,
    "triceps": 10,
    "lats": 10,
    "upper_back": 10,
    "chest": 10,
    "hamstrings": 10,
    "glutes": 10,
    "calves": 10,
    "forearms": 10,
    "traps": 10,
    "neck": 10,
}


async def generate_volume_report(target_date: date, thresholds: Thresholds) -> None:
    """Generate a volume report based on the workouts after a given date"""
    client = HevyClientV1(
        root_url=conf.get_hevy_api_root_url(), api_key=conf.get_hevy_api_key()
    )

    body_part_counter = await get_body_part_counters(
        client=client, target_date=target_date
    )

    for body_part in body_part_counter:
        if body_part_counter[body_part] < thresholds.thresholds.get(body_part, 0):
            print(f"Warning: {body_part} has been trained too little!")
            print(
                f"Goal = {DEFAULT_THRESHOLDS[body_part]}, Actual = {body_part_counter[body_part]})"
            )


async def get_body_part_counters(client: HevyClientV1, target_date: date):
    """Get the number of sets for each body part after a given date"""
    body_part_counter = Counter()
    async for workout in client.list_workouts_after_date(target_date):
        print(f"Processing workout: {workout.id}, {workout.start_time}")
        for exercise in workout.exercises:
            exercise_template_id = exercise.exercise_template_id

            exercise_template = await client.get_exercise_template(exercise_template_id)
            # Get all non warm up sets and ad them to the count for a body part
            num_sets = len([s for s in exercise.sets if s.set_type != "warmup"])

            primary_body_part = exercise_template.primary_muscle_group
            body_part_counter[primary_body_part] += num_sets
            for body_part in exercise_template.secondary_muscle_groups:
                body_part_counter[body_part] += num_sets
