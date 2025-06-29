from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta
from src.apps.user.serveces import UserService
from src.core.database import get_session
from src.apps.user.schemas import UserBaseSchema

SECRET_KEY = "isdohouhrgosjeignaosd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(user: dict):
    to_encode = {"sub": str(user["id"])}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth_scheme),
):
    print("Validating user...")
    try:
        print("Payload:", token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        for session in get_session():
            # db_session = session
            user_data = UserService(db_session=session).get_user_by_id(
                user_id=int(user_id)
            )
            if user_data is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return user_data.dict()
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


#
