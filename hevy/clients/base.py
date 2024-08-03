import requests

import aiohttp
import asyncio
from datetime import datetime

async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.json()

async def fetch_until_date(url, target_date):
    async with aiohttp.ClientSession() as session:
        while url:
            data = await fetch_page(session, url)
            for item in data['items']:
                item_date = datetime.strptime(item['date'], '%Y-%m-%d')
                if item_date > target_date:
                    return
                yield item
            url = data['next_page_url']  # Update URL to the next page if exists

# Usage example:
target_date = datetime(2023, 1, 1)
async def main():
    async for item in fetch_until_date('http://example.com/api/items', target_date):
        print(item)

if __name__ == '__main__':
    asyncio.run(main())


class HevyClient:
    def __init__(self, root_url: str):
        self.root_url = root_url

    async def _get(self, url: str):
        return requests.get(f"{self.root_url}/{url}")
    
    async def _fetch_until_date()