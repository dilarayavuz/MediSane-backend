from pydantic import BaseModel
from typing import List


class LoginInfo(BaseModel):
    username: str
    password: str
