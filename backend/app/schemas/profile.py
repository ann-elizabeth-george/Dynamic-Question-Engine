from pydantic import BaseModel
from typing import Optional

class ProfileCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    district_code: str
    area_code: str
    category_code: str

class ProfileResponse(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    phone: str
    district_code: str
    area_code: str
    category_code: str
    running_number: int
    registration_number: str

    class Config:
        from_attributes = True
