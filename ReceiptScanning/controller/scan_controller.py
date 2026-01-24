from idlelib.pyparse import trans

from fastapi import Depends, FastAPI, Header, HTTPException, Request, File, UploadFile, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from helpers.auth_dependencies import get_current_user
from helpers.vision import extract_receipt_payload
from pydantic import BaseModel, Field
from typing import List, Dict, Union, Optional
import os

from models.receipts import Receipt
from schemas.receipt import ReceiptBaseModel,ProductBaseModel

router = APIRouter(prefix="/scan", tags=["scan"])


API_KEY = os.getenv("API_KEY")
async def verify_key(x_api_key: str = Header(...)):
    if API_KEY is None or x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")





@router.post("", response_model=ReceiptBaseModel,
             dependencies=[Depends(verify_key),Depends(get_current_user),])
async def scan_receipt(transaction_id: int,file: UploadFile = File(...),db: AsyncSession = Depends(get_db)):
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
        payload = extract_receipt_payload(image_path,db,transaction_id)
        os.remove(image_path)
    except Exception as e:
        os.remove(image_path)
        raise HTTPException(status_code=500, detail=f"Failed to process the receipt image: {e}")
    return payload