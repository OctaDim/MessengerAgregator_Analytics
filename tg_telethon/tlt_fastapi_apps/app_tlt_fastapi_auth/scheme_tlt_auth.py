from pydantic import BaseModel


class TelethonAuthData(BaseModel):
    username: str
    password: str
