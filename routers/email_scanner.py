from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def scan_email(email_content: str):
    return {"analysis": "pending scan"}
