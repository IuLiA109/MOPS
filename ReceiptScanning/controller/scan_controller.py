from fastapi import Depends, FastAPI, Header, HTTPException, Request, File, UploadFile, APIRouter

from helpers.vision import extract_receipt_payload
from pydantic import BaseModel
from typing import List, Dict, Union, Optional
import os

router = APIRouter(prefix="/scan", tags=["scan"])


API_KEY = os.getenv("API_KEY")
async def verify_key(x_api_key: str = Header(...)):
    if API_KEY is None or x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")


class ScanResponse(BaseModel):
    produse: List[Dict[str, Union[str, float]]] = None
    total: Optional[float] = None


@router.post("", response_model=ScanResponse, dependencies=[Depends(verify_key)])
async def scan_receipt(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        with open(f"temp_{file.filename}", "wb") as f:
            f.write(contents)
            image_path = os.path.abspath(f.name)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to read uploaded file")
    finally:
        await file.close()

    if not image_path:
        os.remove(image_path)
        raise HTTPException(status_code=404, detail="Missing 'image_path'")
    try:
        payload = extract_receipt_payload(image_path)
        os.remove(image_path)
    except Exception as e:
        os.remove(image_path)
        raise HTTPException(status_code=500, detail=f"Failed to process the receipt image: {e}")
    return ScanResponse(**payload)