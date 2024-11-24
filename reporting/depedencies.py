from fastapi import Depends
from hevy.v1.client import HevyClientV1
from fastapi import FastAPI

def get_hevy_client_v1() -> HevyClientV1:
    """Get a HevyClientV1 instance"""
    return HevyClientV1()
