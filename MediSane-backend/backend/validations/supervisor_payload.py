from pydantic import BaseModel


class SupervisorPayload(BaseModel):
    supervisor_id: int
    token: str
