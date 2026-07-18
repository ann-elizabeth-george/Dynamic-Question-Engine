from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.question import Question
from app.models.answer import Answer
from app.models.mapping import CategoryQuestionMapping
from app.schemas.question import QuestionCreate

def create_question(db: Session, question_in: QuestionCreate) -> Question:
    # Check duplicate code
    existing_q = db.query(Question).filter(Question.code == question_in.code).first()
    if existing_q:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Question with code '{question_in.code}' already exists"
        )
        
    db_q = Question(
        code=question_in.code,
        question_text=question_in.question_text,
        question_type=question_in.question_type,
        status=question_in.status
    )
    db.add(db_q)
    db.commit()
    db.refresh(db_q)
    
    # Predefined answers
    for idx, ans in enumerate(question_in.answers):
        db_ans = Answer(
            question_id=db_q.id,
            answer_text=ans.answer_text,
            display_order=ans.display_order,
            is_active=ans.is_active
        )
        db.add(db_ans)
    db.commit()
    db.refresh(db_q)
    return db_q

def get_questions_by_category(db: Session, category_id: int):
    # Query join CategoryQuestionMapping -> Question -> Answer
    mappings = db.query(CategoryQuestionMapping).filter(
        CategoryQuestionMapping.category_id == category_id,
        CategoryQuestionMapping.is_active == True,
        CategoryQuestionMapping.is_deleted == False
    ).order_by(CategoryQuestionMapping.display_order.asc()).all()
    
    questions = []
    for m in mappings:
        q = db.query(Question).filter(
            Question.id == m.question_id,
            Question.is_deleted == False,
            Question.status == "ACTIVE"
        ).first()
        if q:
            questions.append(q)
    return questions
