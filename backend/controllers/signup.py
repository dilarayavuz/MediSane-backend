from datetime import timedelta

from fastapi import APIRouter, HTTPException, status

from backend.constants.login_constants import access_token_expiration
from backend.validations import LoginInfo, Account
from backend.server import login, signup



class SignupController:
    router = APIRouter()

    @staticmethod
    @router.put("/signup")
    async def login(payload: LoginInfo):
        print(f"Payload:{payload.dict()}")
        return signup.signup(username=payload.username, password=payload.password)