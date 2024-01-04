from fastapi import APIRouter, HTTPException, status

from backend.server.medicine import Medicine
from backend.server.patient import Patient
from backend.validations import LoginInfo, Account, MedicinePatient, Profile
from backend.server import login
from backend.utils import privilege_checks
from backend.utils.logging import Logger
import logging

from backend.validations.account import PatientProfile
from backend.validations.medicine_report import MedicineReport


class ScheduleMedicineController:
    router = APIRouter()

    @staticmethod
    @router.put("/schedule-medicine")
    async def schedule_medicine(payload: MedicinePatient):
        print(f"Payload:{payload.dict()}")
        patient = Patient(profile_id = payload.patient_id)  # could change to profile_id
        token = payload.token

        profiles = login.get_user(token)[1]

        if privilege_checks.patients_check(patient.profile_id, profiles):
            medicine = Medicine(medicine_name=payload.medicine_name,
                                frequency=payload.frequency,
                                start_dates=payload.start_dates,
                                dose_amount=payload.dose_amount if payload.dose_amount else None,
                                usage_description=payload.usage_description,
                                has_notif=payload.has_notif,
                                remaining_amount=payload.remaining_amount,
                                end_date=payload.end_date
                                )
            medicine_added, date_added = patient.add_medicine(medicine)

            return {
                "medicine_added": medicine_added,
                "date_added": date_added
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthenticated Access",
            )


class AllMedicinesController:
    router = APIRouter()

    @staticmethod
    @router.post("/get-all-medicines")
    async def get_all_medicine(payload: PatientProfile):
        print(f"Payload:{payload.dict()}")

        token = payload.token

        profiles = login.get_user(token)[1]
        patient = Patient(profile_id=payload.patient_id)

        if privilege_checks.patients_check(patient.profile_id, profiles):
            all_medicines, clashes = patient.get_all_medicines()
            print(f"Medicines of the patient {payload.patient_id}: {all_medicines}")
            print(f"Clashes: {clashes}")
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthenticated Access",
            )

        return {
            "medicines": all_medicines,
            "clashes": clashes
        }

class AddMedicineReportController:
    router = APIRouter()

    @staticmethod
    @router.put("/add-medicine-report")
    async def add_medicine_report(payload: MedicineReport):
        token = payload.token

        profiles = login.get_user(token)[1]
        patient = Patient(profile_id=payload.patient_id)
        is_update = payload.is_update
        payload.hour_of_dose = payload.hour_of_dose.split('.')[0]

        payload = {k:v for k,v in payload if k != "token" and k != "is_update"}

        if (privilege_checks.patients_check(patient.profile_id, profiles)
                or privilege_checks.patients_check(patient.profile_id, profiles)):
            res = patient.add_medicine_report(payload, is_update=is_update)
            print(f"Add Medicine report result: {res}")
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthenticated Access",
            )

        return res

class GetMedicineReportController:
    router = APIRouter()
    @staticmethod
    @router.post("/get-medicine-report")
    async def get_medicine_report(payload: PatientProfile):
        token = payload.token

        profiles = login.get_user(token)[1]
        patient = Patient(profile_id=payload.patient_id)



        if (privilege_checks.patients_check(patient.profile_id, profiles)
                or privilege_checks.patients_check(patient.profile_id, profiles)):
            res = patient.get_medicine_report()
            print(f"Get Medicine Result: {res}")
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthenticated Access",
            )

        return res

