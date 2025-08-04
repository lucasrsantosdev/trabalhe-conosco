# brain_agriculture/app/routes/harvest.py

from fastapi import APIRouter

router = APIRouter(
    prefix="/harvests",
    tags=["Harvests"]
)

@router.get("/")
def list_harvests():
    return {"message": "Harvest list"}
