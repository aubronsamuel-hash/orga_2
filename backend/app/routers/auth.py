from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginIn(BaseModel):
    username: str | None = None


class LoginOut(BaseModel):
    userId: str


@router.post("/login", response_model=LoginOut)
def login_dev(payload: LoginIn) -> LoginOut:
    uid = (payload.username or "dev-user").strip() or "dev-user"
    return LoginOut(userId=uid)
