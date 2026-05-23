from __future__ import annotations

import mimetypes
from pathlib import Path
from time import time
from uuid import uuid4

import aiofiles
from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse

router = APIRouter(tags=["images"])


@router.post("/api/v1/images")
async def upload_images(
    request: Request,
    files: list[UploadFile] = File(...),
):
    settings = request.app.state.settings
    image_dir: Path = request.app.state.image_dir

    results: list[dict[str, object]] = []
    all_success = True

    for file in files:
        file_result: dict[str, object] = {"filename": file.filename}

        if file.content_type not in settings.allowed_types:
            file_result.update(
                {
                    "status": 415,
                    "error": "UnsupportedMediaType",
                    "message": "Only JPG/PNG/WebP formats are allowed.",
                }
            )
            all_success = False
            results.append(file_result)
            continue

        contents = await file.read()

        if len(contents) > settings.max_file_size:
            file_result.update(
                {
                    "status": 413,
                    "error": "PayloadTooLarge",
                    "message": f"File size exceeds {settings.max_file_size // 1024 // 1024}MB.",
                }
            )
            all_success = False
            results.append(file_result)
            continue

        suffix = Path(file.filename or "").suffix
        file_id = str(uuid4())
        file_path = image_dir / f"{file_id}{suffix}"
        while file_path.exists():
            file_id = str(uuid4())
            file_path = image_dir / f"{file_id}{suffix}"

        async with aiofiles.open(file_path, "wb") as output:
            await output.write(contents)

        file_result.update(
            {
                "status": 201,
                "id": file_id,
                "url": f"{settings.mount_path}/{file_id}{suffix}",
                "size": len(contents),
                "content_type": file.content_type,
                "uploaded_at": time(),
            }
        )
        results.append(file_result)

    if all_success:
        return JSONResponse(status_code=201, content={"uploaded": results})

    return JSONResponse(status_code=207, content={"results": results})


@router.get("/api/v1/images/{image_id}")
async def get_image(request: Request, image_id: str):
    image_dir: Path = request.app.state.image_dir
    for file_path in image_dir.iterdir():
        if file_path.stem == image_id:
            return FileResponse(
                file_path,
                media_type=mimetypes.guess_type(file_path.name)[0],
            )

    raise HTTPException(status_code=404, detail="ImageNotFound")


@router.get("/api/v1/config")
async def get_config(request: Request):
    settings = request.app.state.settings
    return JSONResponse(
        status_code=200,
        content={
            "maxFileSize": settings.max_file_size,
            "allowedTypes": settings.allowed_types,
            "mountPath": settings.mount_path,
        },
    )
