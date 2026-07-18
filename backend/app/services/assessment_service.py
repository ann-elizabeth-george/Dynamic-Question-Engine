from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.session import AssessmentSession
from app.models.response import UserResponse
from app.models.mapping import CategoryQuestionMapping
from app.models.question import Question
from app.models.answer import Answer
from app.models.category import Category
from app.schemas.assessment import SubmitAnswerRequest
from app.services.assessment_engine import AssessmentEngine
from app.core import events

def start_session(db: Session, user_id: int, category_id: int) -> AssessmentSession:
    # Verify active category
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.is_active == True,
        Category.is_deleted == False
    ).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found or inactive"
        )
        
    # Get mapped questions to verify category is not empty
    mappings = db.query(CategoryQuestionMapping).filter(
        CategoryQuestionMapping.category_id == category_id,
        CategoryQuestionMapping.is_active == True,
        CategoryQuestionMapping.is_deleted == False
    ).order_by(CategoryQuestionMapping.display_order.asc()).all()

    if not mappings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No questions mapped to this category yet."
        )

    # Disable any existing incomplete session for this category/user to avoid overlap
    db.query(AssessmentSession).filter(
        AssessmentSession.user_id == user_id,
        AssessmentSession.category_id == category_id,
        AssessmentSession.status == "STARTED"
    ).update({"status": "ABANDONED"})

    first_question_id = mappings[0].question_id

    session = AssessmentSession(
        user_id=user_id,
        category_id=category_id,
        current_question_index=0,
        current_question_id=first_question_id,
        status="STARTED",
        start_time=datetime.utcnow(),
        progress_percentage=0.00
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    events.dispatch(events.ASSESSMENT_STARTED, {
        "session_id": session.id,
        "user_id": user_id,
        "category_id": category_id
    })

    return session

def get_current_question(db: Session, session_id: int, user_id: int) -> Question:
    session = db.query(AssessmentSession).filter(
        AssessmentSession.id == session_id,
        AssessmentSession.user_id == user_id,
        AssessmentSession.is_deleted == False
    ).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment session not found"
        )
    if session.status == "COMPLETED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment already completed"
        )

    question = db.query(Question).filter(
        Question.id == session.current_question_id,
        Question.is_deleted == False
    ).first()
    return question

def submit_answer(db: Session, user_id: int, request: SubmitAnswerRequest):
    session = db.query(AssessmentSession).filter(
        AssessmentSession.id == request.session_id,
        AssessmentSession.user_id == user_id,
        AssessmentSession.is_deleted == False
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    if session.status != "STARTED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session is not in active state"
        )

    # Validate question and answer
    answer = db.query(Answer).filter(
        Answer.id == request.answer_id,
        Answer.question_id == request.question_id,
        Answer.is_active == True,
        Answer.is_deleted == False
    ).first()
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid answer selection for this question"
        )

    # Save User Response (upsert or insert)
    # Check if response already exists for this session-question
    existing_resp = db.query(UserResponse).filter(
        UserResponse.session_id == session.id,
        UserResponse.question_id == request.question_id
    ).first()

    if existing_resp:
        existing_resp.answer_id = request.answer_id
        existing_resp.timestamp = datetime.utcnow()
    else:
        new_resp = UserResponse(
            session_id=session.id,
            user_id=user_id,
            question_id=request.question_id,
            answer_id=request.answer_id,
            timestamp=datetime.utcnow()
        )
        db.add(new_resp)

    # Load all category mapping configuration
    mappings = db.query(CategoryQuestionMapping).filter(
        CategoryQuestionMapping.category_id == session.category_id,
        CategoryQuestionMapping.is_active == True,
        CategoryQuestionMapping.is_deleted == False
    ).order_by(CategoryQuestionMapping.display_order.asc()).all()

    total_questions = len(mappings)
    
    # Calculate progress
    # Progress is current index + 1 / total
    progress = AssessmentEngine.calculate_progress(session.current_question_index + 1, total_questions)
    session.progress_percentage = progress

    # Run core engine logic to get next question details
    is_completed, next_index, next_q_id = AssessmentEngine.get_next_question_details(
        mappings, session.current_question_index
    )

    events.dispatch(events.QUESTION_ANSWERED, {
        "session_id": session.id,
        "user_id": user_id,
        "question_id": request.question_id,
        "answer_id": request.answer_id
    })

    next_question = None

    if is_completed:
        session.status = "COMPLETED"
        session.completion_time = datetime.utcnow()
        db.commit()
        db.refresh(session)
        events.dispatch(events.ASSESSMENT_COMPLETED, {
            "session_id": session.id,
            "user_id": user_id,
            "category_id": session.category_id
        })
    else:
        session.current_question_index = next_index
        session.current_question_id = next_q_id
        db.commit()
        db.refresh(session)
        
        # Load next question payload
        next_question = db.query(Question).filter(Question.id == next_q_id).first()

    return {
        "success": True,
        "is_completed": is_completed,
        "progress_percentage": float(session.progress_percentage),
        "next_question": next_question
    }

def get_user_assessment_history(db: Session, user_id: int):
    sessions = db.query(AssessmentSession).filter(
        AssessmentSession.user_id == user_id,
        AssessmentSession.is_deleted == False
    ).order_by(AssessmentSession.start_time.desc()).all()
    
    history = []
    for s in sessions:
        category = db.query(Category).filter(Category.id == s.category_id).first()
        category_name = category.name if category else "Unknown"
        
        # Fetch responses inside session
        db_responses = db.query(UserResponse).filter(UserResponse.session_id == s.id).all()
        
        responses_payload = []
        for r in db_responses:
            q = db.query(Question).filter(Question.id == r.question_id).first()
            a = db.query(Answer).filter(Answer.id == r.answer_id).first()
            
            responses_payload.append({
                "id": r.id,
                "session_id": r.session_id,
                "question_id": r.question_id,
                "question_text": q.question_text if q else "",
                "answer_id": r.answer_id,
                "answer_text": a.answer_text if a else "",
                "timestamp": r.timestamp
            })
            
        history.append({
            "session": s,
            "category_name": category_name,
            "responses": responses_payload
        })
    return history
