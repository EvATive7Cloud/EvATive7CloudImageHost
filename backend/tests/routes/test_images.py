from __future__ import annotations

from importlib import reload
from io import BytesIO

from fastapi.testclient import TestClient

import app as app_module
import config as config_module


def create_client(monkeypatch, tmp_path: str) -> TestClient:
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    reload(config_module)
    reload(app_module)
    return TestClient(app_module.create_app())


def test_get_config(monkeypatch, tmp_path):
    client = create_client(monkeypatch, tmp_path)

    response = client.get("/api/v1/config")

    assert response.status_code == 200
    assert response.json() == {
        "maxFileSize": 5 * 1024 * 1024,
        "allowedTypes": ["image/jpeg", "image/png", "image/webp"],
        "mountPath": "/imgs",
    }


def test_upload_and_get_image(monkeypatch, tmp_path):
    client = create_client(monkeypatch, tmp_path)

    response = client.post(
        "/api/v1/images",
        files={"files": ("sample.png", BytesIO(b"png-bytes"), "image/png")},
    )

    assert response.status_code == 201
    payload = response.json()
    assert "uploaded" in payload
    uploaded = payload["uploaded"][0]
    assert uploaded["filename"] == "sample.png"
    assert uploaded["status"] == 201
    assert uploaded["url"].startswith("/imgs/")

    image_response = client.get(f"/api/v1/images/{uploaded['id']}")
    assert image_response.status_code == 200
    assert image_response.content == b"png-bytes"


def test_partial_upload_failure(monkeypatch, tmp_path):
    client = create_client(monkeypatch, tmp_path)

    response = client.post(
        "/api/v1/images",
        files=[
            ("files", ("good.webp", BytesIO(b"webp"), "image/webp")),
            ("files", ("bad.gif", BytesIO(b"gif"), "image/gif")),
        ],
    )

    assert response.status_code == 207
    payload = response.json()
    assert "results" in payload
    assert payload["results"][0]["status"] == 201
    assert payload["results"][1] == {
        "filename": "bad.gif",
        "status": 415,
        "error": "UnsupportedMediaType",
        "message": "Only JPG/PNG/WebP formats are allowed.",
    }


def test_missing_image(monkeypatch, tmp_path):
    client = create_client(monkeypatch, tmp_path)

    response = client.get("/api/v1/images/not-found")

    assert response.status_code == 404
    assert response.json() == {"detail": "ImageNotFound"}
