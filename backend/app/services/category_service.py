from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.mapping import CategoryQuestionMapping
from app.schemas.category import CategoryCreate, MappingCreate

def get_active_categories(db: Session):
    return db.query(Category).filter(Category.is_active == True, Category.is_deleted == False).all()

def create_category(db: Session, category_in: CategoryCreate) -> Category:
    db_cat = Category(
        name=category_in.name,
        description=category_in.description,
        is_active=category_in.is_active
    )
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def create_mapping(db: Session, mapping_in: MappingCreate) -> CategoryQuestionMapping:
    # Disable duplicate mappings if any exist
    db.query(CategoryQuestionMapping).filter(
        CategoryQuestionMapping.category_id == mapping_in.category_id,
        CategoryQuestionMapping.question_id == mapping_in.question_id
    ).update({"is_deleted": True})
    
    db_map = CategoryQuestionMapping(
        category_id=mapping_in.category_id,
        question_id=mapping_in.question_id,
        display_order=mapping_in.display_order
    )
    db.add(db_map)
    db.commit()
    db.refresh(db_map)
    return db_map
