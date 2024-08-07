import asyncio
import io
import logging
import os

from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
import reporting.conf as conf
from hevy.v1.client import HevyClientV1
from collections import Counter
from datetime import datetime, timedelta

from reporting.schemas.reports import Thresholds

async def generate_volume_report(after_date: date, thresholds: Thresholds):
    client = HevyClientV1(
        root_url=conf.get_hevy_api_root_url(), api_key=conf.get_hevy_api_key()
    )

    target_date = datetime.today() - timedelta(days=7)
    target_date = target_date.date()
    body_part_counter = Counter()
    async for workout in client.list_workouts_after_date(target_date):
        for exercise in workout.exercises:
            exercise_template_id = exercise.exercise_template_id

            exercise_template = await client.get_exercise_template(
                exercise_template_id
            )
            # Get all non warm up sets and ad them to the count for a body part
            num_sets = len([s for s in exercise.sets if s.set_type != "warmup"])

            primary_body_part = exercise_template.primary_muscle_group
            body_part_counter[primary_body_part] += num_sets
            for body_part in exercise_template.secondary_muscle_groups:
                body_part_counter[body_part] += num_sets

    for body_parts in body_part_counter:
        if body_part_counter[body_parts] < DEFAULT_THRESHOLDS[body_parts]:
            print(f"Warning: {body_parts} has been trained too little!")
            print(f"Goal = {DEFAULT_THRESHOLDS[body_parts]}, Actual = {body_part_counter[body_parts]})")