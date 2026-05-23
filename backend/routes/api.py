from fastapi import APIRouter

router = APIRouter(prefix="/api")


@router.get("/world")
def hello_world():
    return "World"
