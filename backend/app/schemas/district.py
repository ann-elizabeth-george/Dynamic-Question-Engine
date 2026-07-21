from pydantic import BaseModel


class DistrictBase(BaseModel):
    name: str
    code: str


class DistrictCreate(DistrictBase):
    pass


class DistrictResponse(DistrictBase):
    id: int

    class Config:
        from_attributes = True