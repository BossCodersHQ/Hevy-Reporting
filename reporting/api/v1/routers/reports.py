import asyncio
import io
import logging
import os

from fastapi import APIRouter, Body, FastAPI, Query, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
import reporting.conf as conf
from hevy.v1.client import HevyClientV1
from collections import Counter
from datetime import datetime, timedelta, date
from reporting.services.reports import generate_volume_report
from reporting.schemas.reports import Thresholds
LOGGER = logging.getLogger(__name__)
ROUTER_PREFIX = "/api/v1/workouts"

router = APIRouter(
    prefix=ROUTER_PREFIX,
    responses={},
)

DEFAULT_THRESHOLDS = {
    "shoulders": 10,
    "biceps": 10,
    "quadriceps": 10,
    "triceps": 10,
    "lats": 10,
    "upper_back": 10,
    "chest": 10,
    "hamstrings": 10,
    "glutes": 10,
    "calves": 10,
    "forearms": 10,
    "traps": 10,
    "neck": 10,
}


@router.get("/volume_report")
async def generate_volume_report(
    after_date: date = Query(...),
    thresholds: Thresholds = Body(...) = defaul
):
    return await generate_volume_report(after_date, thresholds)
    
    