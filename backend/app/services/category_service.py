from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.category import Category
from app.models.mapping import CategoryQuestionMapping
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    MappingCreate,
)


def get_active_categories(db: Session):
    return (
        db.query(Category)
        .filter(
            Category.is_active == True,
            Category.is_deleted == False
        )
        .all()
    )


def create_category(db: Session, category_in: CategoryCreate) -> Category:

    existing = (
        db.query(Category)
        .filter(
            Category.name == category_in.name,
            Category.is_deleted == False
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists"
        )

    db_cat = Category(
        name=category_in.name,
        description=category_in.description,
        is_active=category_in.is_active,
    )

    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)

    return db_cat


def update_category(
    db: Session,
    category_id: int,
    category_in: CategoryUpdate,
):

    category = (
        db.query(Category)
        .filter(
            Category.id == category_id,
            Category.is_deleted == False
        )
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    update_data = category_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)

    return category


def delete_category(
    db: Session,
    category_id: int,
):

    category = (
        db.query(Category)
        .filter(
            Category.id == category_id,
            Category.is_deleted == False
        )
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    category.is_active = False
    category.is_deleted = True

    db.commit()

    return {
        "message": "Category deleted successfully"
    }


def create_mapping(
    db: Session,
    mapping_in: MappingCreate,
) -> CategoryQuestionMapping:

    db.query(CategoryQuestionMapping).filter(
        CategoryQuestionMapping.category_id == mapping_in.category_id,
        CategoryQuestionMapping.question_id == mapping_in.question_id,
    ).update(
        {"is_deleted": True}
    )

    db_map = CategoryQuestionMapping(
        category_id=mapping_in.category_id,
        question_id=mapping_in.question_id,
        display_order=mapping_in.display_order,
    )

    db.add(db_map)
    db.commit()
    db.refresh(db_map)

    return db_map