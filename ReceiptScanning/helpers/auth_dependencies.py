from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from models.users import User
from helpers.security import SECRET_KEY, ALGORITHM

JWT_COOKIE_NAME = "access_token"

# get current authenticated user
async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> User:
    token = request.cookies.get(JWT_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid token")

    user: User|None = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User no longer exists")

    return user

async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return current_user