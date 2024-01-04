from datetime import timedelta
from fastapi import APIRouter, HTTPException, status

from backend.constants.login_constants import access_token_expiration
from backend.server.medicine import Medicine
from backend.server.patient import Patient
from backend.server.profile import add_profile, delete_profile
from backend.validations import LoginInfo, Account, MedicinePatient, Profile
from backend.server import login
from backend.utils import privilege_checks
from backend.utils.logging import Logger
import logging

from backend.validations.account import PatientProfile, AddProfilePayload, DeleteProfilePayload
from backend.validations.medicine_report import MedicineReport



class AddProfileController:
    router=APIRouter()

    @staticmethod
    @router.put("/add-profile")
    async def add_profile(payload: AddProfilePayload):
        print(f"Payload:{payload.dict()}")
        token = payload.token

        account_id = login.get_user(token)[0]

        if add_profile(account_id=account_id, profile_name=payload.profileName,
                        type="supervisor" if payload.type else "patient"):
            profiles = login.get_account_profiles_from_id(account_id)
            access_token = login.create_access_token(
                data={"AccountID": account_id, "profiles": profiles}, expires_delta=access_token_expiration
            )
            return access_token
        else:
            return -1

class DeleteProfileController:
    router = APIRouter()

    @staticmethod
    @router.delete("/delete-profile")
    async def delete_profile(payload: DeleteProfilePayload):
        print(f"Payload:{payload.dict()}")
        token = payload.token

        account_id, profiles = login.get_user(token)

        if (payload.profileId in [profile["profileId"] for profile in profiles]
                and delete_profile(profile_id=payload.profileId)):
            profiles = login.get_account_profiles_from_id(account_id)
            access_token = login.create_access_token(
                data={"AccountID": account_id, "profiles": profiles},
                expires_delta=access_token_expiration
            )
            return access_token
        else:
            return -1

