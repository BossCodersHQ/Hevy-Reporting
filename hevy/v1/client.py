import requests

import aiohttp
import asyncio
from datetime import datetime, date, timedelta
import reporting.conf as conf
from hevy.v1.schemas.custom import PaginatedWorkouts, PaginatedExerciseTemplates
from hevy.v1.schemas.base import Workout, ExerciseTemplate
from typing import AsyncGenerator, Generator
from collections import Counter
from async_lru import alru_cache
from time import time
from datetime import timedelta

WORKOUT_PREFIX = "/v1/workouts"
EXERCISE_TEMPLATE_PREFIX = "/v1/exercise_templates"


class HevyClientV1:
    def __init__(self, root_url: str, api_key: str):
        self.root_url = root_url
        self.api_key = api_key
        self.headers = headers = {"api-key": self.api_key}

    async def _get(self, session, url: str) -> dict:
        async with session.get(url, headers=self.headers) as response:
            return await response.json()

    async def _get_page(self, session, url: str, page: int = 1) -> dict:
        url = f"{url}?page={page}"
        return await self._get(session, url)

    async def list_workouts_after_date(
        self, target_date: date
    ) -> AsyncGenerator[Workout, None]:
        # TODO: Change this to use the /v1/workouts/events endpoint
        page = 1
        workouts_prefix = WORKOUT_PREFIX
        workouts_endpoint = f"{self.root_url}{workouts_prefix}"
        async with aiohttp.ClientSession() as session:
            while True:

                start_w_time = time()
                data = await self._get_page(
                    session=session, url=workouts_endpoint, page=page
                )
                print(f"Time taken to get page: {time() - start_w_time}")

                paginated_workout = PaginatedWorkouts.model_validate(data)

                for workout in paginated_workout.workouts:
                    start_time = workout.start_time.date()
                    if start_time < target_date:
                        return

                    yield workout

                # Update URL to next page
                page += 1

    async def list_exercise_templates(
        self, page: int = 1
    ) -> AsyncGenerator[ExerciseTemplate, None]:
        exercise_template_prefix = EXERCISE_TEMPLATE_PREFIX
        exercise_template_endpoint = f"{self.root_url}{exercise_template_prefix}"
        page = 1
        last_page = None
        async with aiohttp.ClientSession() as session:
            while True:
                if last_page and page > last_page:
                    return
                data = await self._get_page(
                    session=session, url=exercise_template_endpoint, page=page
                )
                exercise_templates = PaginatedExerciseTemplates.model_validate(data)
                if not last_page:
                    last_page = exercise_templates.page_count
                for exercise_template in exercise_templates.exercise_templates:
                    yield exercise_template
                page += 1

    @alru_cache(maxsize=128)
    async def get_exercise_template(self, id: str) -> ExerciseTemplate:
        exercise_template_prefix = EXERCISE_TEMPLATE_PREFIX
        exercise_template_endpoint = f"{self.root_url}{exercise_template_prefix}/{id}"
        async with aiohttp.ClientSession() as session:
            data = await self._get(session=session, url=exercise_template_endpoint)
            exercise_template = ExerciseTemplate.model_validate(data)
            return exercise_template
