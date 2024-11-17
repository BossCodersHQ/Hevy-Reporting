import pytest
import asyncio
from hevy.v1.client import HevyClientV1
from reporting import conf
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_list_workouts_after_date():
    # Given
    client = HevyClientV1(
        root_url=conf.get_hevy_api_root_url(), api_key=conf.get_hevy_api_key()
    )
    target_date = datetime.today().date() - timedelta(days=30)

    # When
    async for workout in client.list_workouts_after_date(target_date):
        # Then
        assert workout is not None
        print(workout.model_dump_json())
        break



@pytest.mark.asyncio
async def test_get_exercise_template():
    # Given
    client = HevyClientV1(
        root_url=conf.get_hevy_api_root_url(), api_key=conf.get_hevy_api_key()
    )

    # When
    excercise = await client.get_exercise_template("AC1BB830")

    # Then
    assert excercise is not None
    assert excercise.title == "Running"
