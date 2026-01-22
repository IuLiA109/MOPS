from fastapi import APIRouter, Depends, HTTPException, Response, Request,Security,Response
from jose import jwt,JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from db.session import get_db
from helpers.security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from helpers.auth_dependencies import get_current_user
from models.users import User
from schemas.user import UserRead,UserRegister,UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])
JWT_COOKIE_NAME = "access_token"


@router.post("/register", status_code=201)
async def register(payload: UserRegister, db: AsyncSession = Depends(get_db)):
    existing_email = await db.execute(select(User).where(User.email == payload.email))
    if existing_email.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already in use.")

    existing_user = await db.execute(select(User).where(User.username == payload.username))
    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Username already taken.")

    try:
        new_user = User(
            username=payload.username,
            email=payload.email,
            password_hash=hash_password(payload.password)
        )
        db.add(new_user)
        await db.commit()
        return {"message": "Registered successfully."}
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/login")
async def login(payload: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(or_(User.email == payload.email, User.username == payload.username))
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=403, detail="Invalid account details.")

    token = create_access_token(data={"sub": str(user.id)})

    response.set_cookie(
        key=JWT_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax"
    )
    return {"message": "Authenticated successfully."}


@router.get("/me", response_model=UserRead)
async def get_me(request: Request, db: AsyncSession = Depends(get_db)):
    current_user = await get_current_user(request, db)
    return current_user

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key=JWT_COOKIE_NAME)
    return {"message": "Logged out"}