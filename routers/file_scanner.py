from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/")
async def scan_file(file: UploadFile = File(...)):
    return {"filename": file.filename, "status": "pending scan"}
