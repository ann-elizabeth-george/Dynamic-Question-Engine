from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True
        
class MappingCreate(BaseModel):
    category_id: int
    question_id: int
    display_order: int

class MappingResponse(BaseModel):
    id: int
    category_id: int
    question_id: int
    display_order: int
    is_active: bool

    class Config:
        from_attributes = True
