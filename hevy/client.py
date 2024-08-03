import requests

import aiohttp
import asyncio
from datetime import datetime
import hevy.conf as conf

class HevyClientV1:
    def __init__(self, root_url: str, api_key: str):
        self.root_url = root_url
        self.api_key = api_key

    async def _get(self, session, url: str):
        async with session.get(url) as response:
            return await response.json()
    
    async def _get_page(self, session, url: str):
        async with session.get(url) as response:
            return await response.json()

    async def list_workouts_until_date(self, target_date:datetime):
        workout_endpoint = "/v1/workouts"
        page = 1
        url = f"{self.root_url}{workout_endpoint}?page={page}"
        async with aiohttp.ClientSession() as session:
            while url:
                data = await self._get(session, workout_url)
                for item in data['items']:
                    item_date = datetime.strptime(item['date'], '%Y-%m-%d')
                    if item_date > target_date:
                        return
                    yield item
                
                url = data['next_page_url']  # Update URL to the next page if exists 



async def main():
    client = HevyClientV1(conf.get_hevy_api_root_url())
    target_date = datetime(2023, 1, 1)
    async for item in client.fetch_until_date('http://example.com/api/items', target_date):
        print(item)


if __name__ == '__main__':

    asyncio.run(main())
