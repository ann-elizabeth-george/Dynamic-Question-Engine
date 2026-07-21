from sqlalchemy.orm import Session

from app.database.base import Base
from app.database.session import engine

from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.models.system_setting import SystemSetting
from app.models.district import District
from app.models.area import Area


def init_db(db: Session) -> None:
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # --------------------------------------------------
    # Seed Roles
    # --------------------------------------------------

    admin_role = db.query(Role).filter(Role.name == "Admin").first()

    if not admin_role:
        admin_role = Role(
            name="Admin",
            description="System administrator with full management access",
            is_active=True,
        )
        db.add(admin_role)
        db.flush()

    student_role = db.query(Role).filter(Role.name == "Student").first()

    if not student_role:
        student_role = Role(
            name="Student",
            description="Standard candidate/student role for taking assessments",
            is_active=True,
        )
        db.add(student_role)
        db.flush()

    # --------------------------------------------------
    # Seed Permissions
    # --------------------------------------------------

    permissions = [
        ("manage_users", "Allows managing users and roles"),
        ("manage_categories", "Allows CRUD on categories"),
        ("manage_questions", "Allows CRUD on questions and answers"),
        ("take_assessment", "Allows candidate to take assessments"),
    ]

    db_permissions = {}

    for name, desc in permissions:

        perm = db.query(Permission).filter(Permission.name == name).first()

        if not perm:
            perm = Permission(
                name=name,
                description=desc,
            )
            db.add(perm)
            db.flush()

        db_permissions[name] = perm

    # --------------------------------------------------
    # Role Permissions
    # --------------------------------------------------

    for perm in db_permissions.values():

        rp = (
            db.query(RolePermission)
            .filter(
                RolePermission.role_id == admin_role.id,
                RolePermission.permission_id == perm.id,
            )
            .first()
        )

        if not rp:
            db.add(
                RolePermission(
                    role_id=admin_role.id,
                    permission_id=perm.id,
                )
            )

    student_perm = db_permissions["take_assessment"]

    rp_student = (
        db.query(RolePermission)
        .filter(
            RolePermission.role_id == student_role.id,
            RolePermission.permission_id == student_perm.id,
        )
        .first()
    )

    if not rp_student:
        db.add(
            RolePermission(
                role_id=student_role.id,
                permission_id=student_perm.id,
            )
        )

    # --------------------------------------------------
    # System Settings
    # --------------------------------------------------

    settings_seed = [
        (
            "assessment_time_limit_mins",
            "60",
            "Global time limit for assessments in minutes",
        ),
        (
            "allow_resume",
            "true",
            "Whether candidates can resume an assessment session",
        ),
        (
            "max_attempts_per_category",
            "1",
            "Maximum number of assessment attempts per category",
        ),
    ]

    for key, value, desc in settings_seed:

        setting = (
            db.query(SystemSetting)
            .filter(SystemSetting.config_key == key)
            .first()
        )

        if not setting:
            db.add(
                SystemSetting(
                    config_key=key,
                    config_value=value,
                    description=desc,
                )
            )

    # --------------------------------------------------
    # Kerala Districts
    # --------------------------------------------------

    districts = [
        ("01", "Thiruvananthapuram"),
        ("02", "Kollam"),
        ("03", "Pathanamthitta"),
        ("04", "Alappuzha"),
        ("05", "Kottayam"),
        ("06", "Idukki"),
        ("07", "Ernakulam"),
        ("08", "Thrissur"),
        ("09", "Palakkad"),
        ("10", "Malappuram"),
        ("11", "Kozhikode"),
        ("12", "Wayanad"),
        ("13", "Kannur"),
        ("14", "Kasaragod"),
    ]

    for code, name in districts:

        district = (
            db.query(District)
            .filter(District.code == code)
            .first()
        )

        if not district:
            db.add(
                District(
                    code=code,
                    name=name,
                )
            )

    db.flush()

    # --------------------------------------------------
    # Sample Areas
    # --------------------------------------------------

    areas = [

        ("01", "Neyyattinkara", "001"),
        ("01", "Kazhakkoottam", "002"),
        ("01", "Varkala", "003"),

        ("02", "Kollam", "001"),
        ("02", "Karunagappally", "002"),
        ("02", "Punalur", "003"),

        ("03", "Adoor", "001"),
        ("03", "Thiruvalla", "002"),
        ("03", "Pandalam", "003"),

        ("04", "Cherthala", "001"),
        ("04", "Kayamkulam", "002"),
        ("04", "Haripad", "003"),

        ("05", "Pala", "001"),
        ("05", "Vaikom", "002"),
        ("05", "Ettumanoor", "003"),

        ("06", "Thodupuzha", "001"),
        ("06", "Munnar", "002"),
        ("06", "Kattappana", "003"),

        ("07", "Aluva", "001"),
        ("07", "Edappally", "002"),
        ("07", "Kalamassery", "003"),

        ("08", "Kodungallur", "001"),
        ("08", "Chalakudy", "002"),
        ("08", "Guruvayur", "003"),

        ("09", "Ottapalam", "001"),
        ("09", "Mannarkkad", "002"),
        ("09", "Chittur", "003"),

        ("10", "Manjeri", "001"),
        ("10", "Perinthalmanna", "002"),
        ("10", "Tirur", "003"),

        ("11", "Vadakara", "001"),
        ("11", "Koyilandy", "002"),
        ("11", "Ramanattukara", "003"),

        ("12", "Kalpetta", "001"),
        ("12", "Sulthan Bathery", "002"),
        ("12", "Mananthavady", "003"),

        ("13", "Thalassery", "001"),
        ("13", "Payyanur", "002"),
        ("13", "Mattannur", "003"),

        ("14", "Kanhangad", "001"),
        ("14", "Uppala", "002"),
        ("14", "Nileshwar", "003"),
    ]

    for district_code, area_name, area_code in areas:

        district = (
            db.query(District)
            .filter(District.code == district_code)
            .first()
        )

        if district:

            exists = (
                db.query(Area)
                .filter(
                    Area.district_id == district.id,
                    Area.code == area_code,
                )
                .first()
            )

            if not exists:

                db.add(
                    Area(
                        district_id=district.id,
                        name=area_name,
                        code=area_code,
                    )
                )

    db.commit()