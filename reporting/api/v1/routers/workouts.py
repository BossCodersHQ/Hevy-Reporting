import asyncio
import io
import logging
import os

from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
import reporting.conf as conf
from hevy.v1.client import HevyClientV1
from collections import Counter
from datetime import datetime,timedelta

LOGGER = logging.getLogger(__name__)
ROUTER_PREFIX = "/api/v1/workouts"

router = APIRouter(
    prefix=ROUTER_PREFIX,
    responses={},
)


@router.get("/")
async def get(request: Request):
    client = HevyClientV1(
        root_url=conf.get_hevy_api_root_url(), api_key=conf.get_hevy_api_key()
    )

    exercise_templates = {}
    thresholds = {}
    target_date = datetime.today() - timedelta(days=7)
    target_date = target_date.date()
    body_part_counter = Counter()
    async for workout in client.list_workouts_after_date(target_date):
        for exercise in workout.exercises:
            exercise_template_id = exercise.exercise_template_id

            if exercise_template_id not in exercise_templates:
                exercise_template = await client.get_exercise_template(
                    exercise_template_id
                )
                exercise_templates[exercise_template_id] = exercise_template
            else:
                exercise_template = exercise_templates[exercise_template_id]

            # Get all non warm up sets and ad them to the count for a body part
            num_sets = len([s for s in exercise.sets if s.set_type != "warmup"])

            primary_body_part = exercise_template.primary_muscle_group
            body_part_counter[primary_body_part] += num_sets
            for body_part in exercise_template.secondary_muscle_groups:
                body_part_counter[
                    body_part
                ] += (
                    num_sets
                )

    print(body_part_counter)