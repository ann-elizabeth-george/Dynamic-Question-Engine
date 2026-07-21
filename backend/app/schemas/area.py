from pydantic import BaseModel


class AreaResponse(BaseModel):
    id: int
    district_id: int
    name: str
    code: str

    class Config:
        from_attributes = True