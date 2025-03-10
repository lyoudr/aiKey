from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from fastapi import Security, Depends, status, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from typing import Union, List
import jwt

from src.core.config import get_settings
from src.repositories import user_repository
from src.models.database import get_db
from src.models.user import User
from src.models.role import Role

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    user = user_repository.get_user_by_name(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to verify the token
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials  # This is the token extracted from the Authorization header

    if not token:
        raise HTTPException(
            detail="Authorization token missing",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(
                detail="Invalid token.",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        user = user_repository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                detail="User not found.",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            detail="Token has expired.", 
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    except jwt.PyJWTError:
        raise HTTPException(
            detail="Invalid token.", 
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles
    
    def __call__(
        self, 
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        role = db.query(Role).filter(Role.id == current_user.role_id).first()
        if role.name in self.allowed_roles:
            return True 
        raise HTTPException(
            detail="Insufficient permission",
            status_code=status.HTTP_403_FORBIDDEN,
        )


class BaseAuth:
    def __init__(self):
        pass

    def _check(
        self, credential: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> str:
        if credential is None:
            raise AuthException(
                error_msg="authorization need to set",
                error_detail="authorization need to set",
            )

        return credential.credentials

class ServiceAuth(BaseAuth):

    def __init__(
        self,
        audience: str = f"{settings.GCP_PROJECT_ID}"
    ):
        super().__init__()
        self.audience = audience

    def __call__(
        self,
        credential: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    ) -> bool:
        token = self._check(credential)
        try:
            id_token.verify_oauth2_token(
                token, google_requests.Request(), self.audience
            )
        except ValueError as e:
            raise HTTPException(
                detail="token verify error",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        return True