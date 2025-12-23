from fastapi import Depends, FastAPI, Header, HTTPException, Request,File,UploadFile
from fastapi.responses import RedirectResponse
from helpers.return_results import return_results
from pydantic import BaseModel

from typing import List, Dict, Union, Optional
import os

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    #await init_db()
    #de adaugat cand trecem la baza de date
    pass

class ScanResponse(BaseModel):
    produse: List[Dict[str, Union[str, float]]] = None
    total: Optional[float] = None


@app.post("/scan", response_model=ScanResponse)
async def scan_receipt(file: UploadFile = File(...)):
    data={}
    try:
        contents = await file.read()
        with open(f"temp_{file.filename}", "wb") as f:
            f.write(contents)
            data = {"image_path": os.path.abspath(f.name)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to read uploaded file")
    finally:
        await file.close()
    

    if 'image_path' not in data:
        raise HTTPException(status_code=400, detail="Missing 'image_path'")
    
    image_path = data['image_path']
    
    rezultate = return_results(image_path)
    
    if rezultate is None:
        raise HTTPException(status_code=500, detail="Failed to process the receipt image")
    
    response_data = ScanResponse(
        produse=rezultate.get('produse'),
        total=rezultate.get('total')
    )
    
    
    return response_data