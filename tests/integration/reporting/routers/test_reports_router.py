import pytest
import asyncio
from hevy.v1.client import HevyClientV1
from reporting import conf
from datetime import datetime, timedelta
from reporting.schemas import BodyPart, Thresholds
from reporting.services import reports as reports_svc

@pytest.mark.asyncio
async def test_generate_volume_report():
    # Given
    after_date = datetime.today().date() - timedelta(days=7)
    thresholds = Thresholds(
        thresholds={
            BodyPart.SHOULDERS: 10,
            BodyPart.BICEPS: 10,
            BodyPart.QUADRICEPS: 10,
        }
    )
    # When
    await reports_svc.generate_volume_report(after_date, thresholds)
