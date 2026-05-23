import sys
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

if hasattr(sys, "_MEIPASS"):
    static_path = Path(sys._MEIPASS, "static")
else:
    static_path = Path("static")


router = APIRouter(tags=["spa"], include_in_schema=False)


def serve_file(path: Path):
    if path.name == "index.html":
        return FileResponse(path, headers={"Cache-Control": "no-store"})
    return FileResponse(path)


@router.get("/")
def serve_index():
    return serve_file(static_path / "index.html")


@router.get("/{full_path:path}")
def serve_spa(full_path: str):
    path = static_path / full_path
    if path.is_file():
        return serve_file(path)

    return serve_file(static_path / "index.html")
