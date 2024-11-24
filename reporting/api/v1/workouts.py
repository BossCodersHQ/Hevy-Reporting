import asyncio
import io
import logging
import os
from collections import Counter
from datetime import date, datetime, timedelta

from fastapi import (
    APIRouter,
    Body,
    Depends,
    FastAPI,
    Query,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import HTMLResponse

import reporting.conf as conf
from hevy.v1.client import HevyClientV1
from reporting.depedencies import get_hevy_client_v1
from reporting.schemas import Thresholds
from reporting.services import reports

LOGGER = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/workouts",
    responses={},
    tags=["workouts"],
)


@router.get("/")
async def list_workouts(
    after_date: date = Query(..., example="2024-11-24", description="List workouts after this date"),
    hevy_client: HevyClientV1 = Depends(get_hevy_client_v1),
):
    """List workouts after a given date"""
    workouts_list = []
    async for workout in hevy_client.list_workouts_after_date(after_date):
        workouts_list.append(workout)
    return workouts_list
