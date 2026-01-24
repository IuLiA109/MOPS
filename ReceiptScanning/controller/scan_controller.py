from datetime import datetime

from fastapi import Depends, Header, HTTPException, File, UploadFile, APIRouter, Form
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from helpers.auth_dependencies import get_current_user
from helpers.vision import extract_receipt_payload
from typing import Optional
import os

from models.users import User
from schemas.receipt import ReceiptBaseModel
from schemas.transaction import TransactionRead
from service.transaction_service import TransactionService
from repository.account_repository import AccountRepository
router = APIRouter(prefix="/scan", tags=["scan"])


API_KEY = os.getenv("API_KEY")
async def verify_key(x_api_key: str = Header(...)):
    if API_KEY is None or x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")





@router.post(
    "",
    response_model=ReceiptBaseModel,
    dependencies=[Depends(verify_key), Depends(get_current_user)],
)
async def scan_receipt(file: UploadFile = File(...)):
    image_path: str | None = None
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process the receipt image: {e}")
    finally:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
    return payload


@router.post(
    "/transaction",
    response_model=TransactionRead,
    dependencies=[Depends(verify_key)],
)
async def scan_and_create_transaction(
    account_id: int = Form(...),
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    merchant_name: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = AccountRepository(db)
    image_path: str | None = None
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
        raise HTTPException(status_code=404, detail="Missing 'image_path'")

    service = TransactionService(db)
    account = await repo.get_by_id(account_id=account_id,user_id=current_user.id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    try:
        receipt_payload = extract_receipt_payload(image_path)
        transaction = await service.create_with_receipt(
            user_id=current_user.id,
            account_id=account_id,
            receipt_payload=receipt_payload,
            transaction_type="expense",
            description=description,
            currency = account.currency,
            transaction_date=datetime.now(),
            merchant_name=merchant_name,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process the receipt image: {e}")
    finally:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)

    return await service.build_transaction_read(transaction)