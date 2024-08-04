from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from reporting.api.v1.routers.workouts import router as workout_router
app = FastAPI()

app.include_router(workout_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}