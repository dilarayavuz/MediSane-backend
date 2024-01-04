from datetime import timedelta

from fastapi import APIRouter, HTTPException, status

from backend.constants.login_constants import access_token_expiration
from backend.validations import LoginInfo, Account
from backend.server import login
from backend.utils.logging import Logger
import logging


class LoginController:
    router = APIRouter()

    @staticmethod
    @router.post("/login")
    async def login(payload: LoginInfo):
        print(f"Payload:{payload.dict()}")
        auth_passed = login.check_user(payload)

        if not auth_passed:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        print(f"Authentication passed?: {auth_passed}")

        profiles = login.get_account_profiles(payload.username)
        print("profiles")
        print(profiles)
        if len(profiles) == 0:
            accountID = login.get_account_id(payload.username)[0]['account_id']
        else:
            accountID = profiles[0]['accountId']
        access_token = login.create_access_token(
            data={"AccountID": accountID, "profiles": profiles}, expires_delta=access_token_expiration
        )
        return {"account_id": accountID, "access_token": access_token, "token_type": "bearer"}

    @staticmethod
    @router.post("/profiles")
    async def profiles(payload: Account):  # Bartu
        print(f"Payload in profiles:{payload}")

        accountID, profiles = login.get_user(payload.token)

        print(f"Profiles of account in profiles: {profiles}")
        for profile in profiles:
            del profile['accountId']

        return profiles
