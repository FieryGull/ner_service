import uuid

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class SourceText(BaseModel):
    name: str
    text_data: str


class Report(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        orm_mode = True
