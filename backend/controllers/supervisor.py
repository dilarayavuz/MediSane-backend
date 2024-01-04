from fastapi import APIRouter, HTTPException, status

from backend.server import login
from backend.server.supervisor import Supervisor
from backend.validations.supervisor_payload import SupervisorPayload
from backend.utils import privilege_checks

class GetPatientsController:
    router = APIRouter()

    @staticmethod
    @router.post("/get-patients")
    async def schedule_medicine(payload: SupervisorPayload):
        print(f"Payload:{payload.dict()}")
        token = payload.token

        profiles = login.get_user(token)[1]
        if privilege_checks.supervisor_check(supervisor_id=payload.supervisor_id,
                                             profiles=profiles):
            supervisor = Supervisor(profile_id=payload.supervisor_id)
            patients = supervisor.get_patients()

        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthenticated Access",
            )

        return patients
