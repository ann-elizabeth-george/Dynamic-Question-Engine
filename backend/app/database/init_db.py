from sqlalchemy.orm import Session
from app.database.base import Base
from app.database.session import engine
from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.models.system_setting import SystemSetting

def init_db(db: Session) -> None:
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Check if roles exist, if not, create them
    admin_role = db.query(Role).filter(Role.name == "Admin").first()
    if not admin_role:
        admin_role = Role(
            name="Admin",
            description="System administrator with full management access",
            is_active=True
        )
        db.add(admin_role)
        db.flush()
        
    student_role = db.query(Role).filter(Role.name == "Student").first()
    if not student_role:
        student_role = Role(
            name="Student",
            description="Standard candidate/student role for taking assessments",
            is_active=True
        )
        db.add(student_role)
        db.flush()
        
    # Seed permissions
    permissions = [
        ("manage_users", "Allows managing users and roles"),
        ("manage_categories", "Allows CRUD on categories"),
        ("manage_questions", "Allows CRUD on questions and answers"),
        ("take_assessment", "Allows candidate to take assessments")
    ]
    db_permissions = {}
    for name, desc in permissions:
        perm = db.query(Permission).filter(Permission.name == name).first()
        if not perm:
            perm = Permission(name=name, description=desc)
            db.add(perm)
            db.flush()
        db_permissions[name] = perm

    # Seed Role Permissions (Admin gets all, Student gets take_assessment)
    for perm_name, perm_obj in db_permissions.items():
        rp = db.query(RolePermission).filter(
            RolePermission.role_id == admin_role.id,
            RolePermission.permission_id == perm_obj.id
        ).first()
        if not rp:
            rp = RolePermission(role_id=admin_role.id, permission_id=perm_obj.id)
            db.add(rp)

    student_perm = db_permissions["take_assessment"]
    rp_student = db.query(RolePermission).filter(
        RolePermission.role_id == student_role.id,
        RolePermission.permission_id == student_perm.id
    ).first()
    if not rp_student:
        rp_student = RolePermission(role_id=student_role.id, permission_id=student_perm.id)
        db.add(rp_student)

    # Seed System Settings
    settings_seed = [
        ("assessment_time_limit_mins", "60", "Global time limit for assessments in minutes"),
        ("allow_resume", "true", "Whether candidates can resume an assessment session"),
        ("max_attempts_per_category", "1", "Maximum number of assessment attempts per category")
    ]
    for key, val, desc in settings_seed:
        setting = db.query(SystemSetting).filter(SystemSetting.config_key == key).first()
        if not setting:
            setting = SystemSetting(config_key=key, config_value=val, description=desc)
            db.add(setting)

    db.commit()
