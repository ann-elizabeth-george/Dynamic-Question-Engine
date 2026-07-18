from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.models.role import Role
from app.models.user_profile import UserProfile
from app.models.registration_counter import RegistrationCounter
from app.schemas.user import UserCreate
from app.schemas.profile import ProfileCreate
from app.core import security
from app.core import events

def get_role_by_name(db: Session, name: str) -> Role:
    return db.query(Role).filter(Role.name == name).first()

def register_user(db: Session, user_in: UserCreate) -> User:
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user_in.email) | (User.username == user_in.username)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Get standard Student role
    student_role = get_role_by_name(db, "Student")
    if not student_role:
        # Fallback if roles not seeded yet
        student_role = Role(name="Student", description="Student Role")
        db.add(student_role)
        db.commit()
        db.refresh(student_role)

    hashed_pw = security.get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hashed_pw,
        role_id=student_role.id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Publish registration event
    events.dispatch(events.USER_REGISTERED, {"user_id": db_user.id, "username": db_user.username})
    
    return db_user

def authenticate_user(db: Session, username_or_email: str, password: str) -> User:
    user = db.query(User).filter(
        (User.email == username_or_email) | (User.username == username_or_email)
    ).first()
    if not user or not security.verify_password(password, user.password_hash):
        return None
    return user

def create_user_profile(db: Session, user_id: int, profile_in: ProfileCreate) -> UserProfile:
    # Check if user already has a profile
    existing_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists for this user"
        )
        
    # Transactional increment of the counter
    # Use select for update to lock the row for thread safety
    counter = db.query(RegistrationCounter).filter(
        RegistrationCounter.district_code == profile_in.district_code,
        RegistrationCounter.area_code == profile_in.area_code,
        RegistrationCounter.category_code == profile_in.category_code
    ).with_for_update().first()

    if not counter:
        counter = RegistrationCounter(
            district_code=profile_in.district_code,
            area_code=profile_in.area_code,
            category_code=profile_in.category_code,
            current_number=1
        )
        db.add(counter)
    else:
        counter.current_number += 1

    # Format running number as 3-digit zero-padded string (e.g. 001, 002)
    running_str = f"{counter.current_number:03d}"
    reg_number = f"{profile_in.district_code}-{profile_in.area_code}-{profile_in.category_code}-{running_str}"

    profile = UserProfile(
        user_id=user_id,
        first_name=profile_in.first_name,
        last_name=profile_in.last_name,
        phone=profile_in.phone,
        district_code=profile_in.district_code,
        area_code=profile_in.area_code,
        category_code=profile_in.category_code,
        running_number=counter.current_number,
        registration_number=reg_number
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

    # Publish profile completed event
    events.dispatch(events.PROFILE_COMPLETED, {
        "user_id": user_id,
        "registration_number": reg_number,
        "first_name": profile.first_name,
        "last_name": profile.last_name
    })

    return profile
