from pydantic import BaseModel
from typing import List


class Account(BaseModel):
    account_id: int
    token: str


class PatientProfile(BaseModel):
    patient_id: int
    token: str


class Profile(BaseModel):
    profileId: int
    profileName: str
    accountId : int
    type: str

class AddProfilePayload(BaseModel):
    profileName: str
    type: bool

    token: str

class DeleteProfilePayload(BaseModel):
    profileId: int

    token: str