from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from core.views import init_address_api
from services.db import Base, engine
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code: create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan, docs_url="/docs")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


init_address_api(app)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    Base.metadata.create_all(bind=engine)  # create tables if not exists
    yield
