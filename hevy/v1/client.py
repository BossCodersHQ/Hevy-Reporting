import requests

import aiohttp
import asyncio
from datetime import datetime, date
import hevy.conf as conf
from hevy.v1.schemas.custom import PaginatedWorkouts


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

    async def fetch_workouts_until_date(self, target_date: date):
        page = 1
        workouts_prefix = "/v1/workouts"
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


async def main():
    client = HevyClientV1(
        root_url=conf.get_hevy_api_root_url(), api_key=conf.get_hevy_api_key()
    )
    target_date = date(2024, 7, 29)

    counter = 0
    async for item in client.fetch_workouts_until_date(target_date):
        
        print(counter)
        counter+=1


if __name__ == "__main__":
    from hevy.conf import initialise_app

    initialise_app()
    asyncio.run(main())
