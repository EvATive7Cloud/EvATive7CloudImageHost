import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from config import load_app_config
from routes.images import router as imagesrouter
from routes.spa import router as sparouter
from utils.version import get_version

load_dotenv()


def create_app() -> FastAPI:
    settings = load_app_config(data_dir=None)

    app = FastAPI()
    app.state.settings = settings
    app.state.image_dir = settings.image_dir

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(imagesrouter)
    app.mount(
        settings.mount_path,
        StaticFiles(directory=settings.image_dir),
        name="imgs",
    )
    app.include_router(sparouter)
    return app


app = create_app()

if __name__ == "__main__":
    logger.debug(f"Version: {get_version() or 'unknown'}")
    settings = load_app_config(data_dir=None)

    uvicorn.run(
        app,
        host=os.environ.get("APP_HOST", "0.0.0.0"),
        port=int(os.environ.get("APP_PORT", settings.port)),
    )
