import requests

import aiohttp
import asyncio
from datetime import datetime, date
import hevy.conf as conf
from hevy.v1.schemas.custom import PaginatedWorkouts
from hevy.v1.schemas.base import Workout, ExerciseTemplate
from typing import AsyncGenerator, Generator
from collections import Counter

WORKOUT_PREFIX = "/v1/workouts"
EXERCISE_TEMPLATE_PREFIX = "/v1/exercise_templates"

class HevyClientV1:
    def __init__(self, root_url: str, api_key: str):
        self.root_url = root_url
        self.api_key = api_key
        self.headers = headers = {
            "api-key": self.api_key
        }

    async def _get(self, session, url: str) -> dict:
        async with session.get(url, headers=self.headers) as response:
            return await response.json()
    
    async def _get_page(self, session, url: str, page: int = 1) -> dict:
        url = f"{url}?page={page}"
        return await self._get(session, url)

    async def list_workouts_after_date(self, target_date: date) -> AsyncGenerator[Workout, None]:
        page = 1
        workouts_prefix = WORKOUT_PREFIX
        workouts_endpoint = f"{self.root_url}{workouts_prefix}"
        async with aiohttp.ClientSession() as session:
            while True:
                data = await self._get_page(
                    session=session, url=workouts_endpoint, page=page
                )
                paginated_workout = PaginatedWorkouts.model_validate(data)

                for workout in paginated_workout.workouts:
                    start_time = workout.start_time.date()
                    if start_time < target_date:
                        return

                    yield workout

                # Update URL to next page
                page += 1

    async def get_exercise_type(self, id:str) -> ExerciseTemplate:
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

    target_date = date(2024, 7, 29)
    body_part_counter = Counter()
    async for workout in client.list_workouts_after_date(target_date):
        for exercise in workout.exercises:
            exercise_template_id = exercise.exercise_template_id
            exercise_template = await client.get_exercise_type(exercise_template_id)


            primary_body_part = exercise_template.primary_muscle_group
            body_part_counter[primary_body_part] += 1

            for body_part in exercise_template.secondary_muscle_groups:
                body_part_counter[body_part] += 1 # weight volume on secondary muscle group arbitrarily less

    
    print(body_part_counter)




if __name__ == "__main__":
    from hevy.conf import initialise_app

    initialise_app()
    asyncio.run(main())
