from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from reporting.api.v1.reports import router as reports_router
from reporting.api.v1.workouts import router as workouts_router
from contextlib import asynccontextmanager
from reporting.conf import initialise_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    initialise_app()

    yield  # The application is running at this point

    # Shutdown actions & cleanup tasks


app = FastAPI(lifespan=lifespan)

app.include_router(reports_router)
app.include_router(workouts_router)

# Add tags to the app


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
