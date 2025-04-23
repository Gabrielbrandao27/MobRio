from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    bus_line: str
    bus_stop: str
    open_time: str
    close_time: str

    @field_validator("open_time", "close_time")
    def validate_time_format(cls, value):
        try:
            from datetime import datetime
            datetime.strptime(value, "%H:%M:%S")
        except ValueError:
            raise ValueError("Time must be in HH:MM:SS format")
        return value

class UserLogin(BaseModel):
    email: EmailStr
    password: str