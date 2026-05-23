import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from routes.api import router as apirouter
from routes.spa import router as sparouter
from utils.version import get_version

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(apirouter)
app.include_router(sparouter)

if __name__ == "__main__":
    load_dotenv()

    logger.debug(f"Version: {get_version() or 'unknown'}")

    uvicorn.run(
        app,
        host=os.environ.get("APP_HOST", "0.0.0.0"),
        port=int(os.environ.get("APP_PORT", 8000)),
    )
