# backend/routers/profiles.py
from fastapi import APIRouter

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.get("/")
def list_profiles():
    return {"message": "Profiles route active"}
