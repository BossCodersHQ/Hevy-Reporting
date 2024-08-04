import requests

import aiohttp
import asyncio
from datetime import datetime, date, timedelta
import hevy.conf as conf
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


async def main():
    client = HevyClientV1(
        root_url=conf.get_hevy_api_root_url(), api_key=conf.get_hevy_api_key()
    )

    exercise_templates = {}

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
            # Do the same for the secondary muscle groups
            for body_part in exercise_template.secondary_muscle_groups:
                body_part_counter[
                    body_part
                ] += (
                    num_sets  # weight volume on secondary muscle group arbitrarily less
                )

    print(body_part_counter)


if __name__ == "__main__":
    from hevy.conf import initialise_app

    initialise_app()
    asyncio.run(main())
