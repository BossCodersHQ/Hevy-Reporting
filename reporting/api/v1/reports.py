import asyncio
import io
import logging
import os
from collections import Counter
from datetime import date, datetime, timedelta

from fastapi import (
    APIRouter,
    Body,
    FastAPI,
    Query,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import HTMLResponse

import reporting.conf as conf
from hevy.v1.client import HevyClientV1
from reporting.schemas import Thresholds
from reporting.services import reports

LOGGER = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/reports",
    responses={},
    tags=["reports"],
)


@router.post("/volume_report")
async def generate_volume_report(
    after_date: date = Query(...), thresholds: Thresholds = Body(...)
):
    return await reports.generate_volume_report(after_date, thresholds)
