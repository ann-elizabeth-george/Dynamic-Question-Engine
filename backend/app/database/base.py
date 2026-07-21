# Import all the models so that Base has them before being
# imported by Alembic or used in migrations

from app.database.base_class import Base  # noqa

from app.models.role import Role  # noqa
from app.models.user import User  # noqa
from app.models.user_profile import UserProfile  # noqa
from app.models.registration_counter import RegistrationCounter  # noqa

from app.models.category import Category  # noqa
from app.models.question import Question  # noqa
from app.models.answer import Answer  # noqa
from app.models.mapping import CategoryQuestionMapping  # noqa

from app.models.session import AssessmentSession  # noqa
from app.models.response import UserResponse  # noqa

from app.models.permission import Permission  # noqa
from app.models.role_permission import RolePermission  # noqa

from app.models.audit_log import AuditLog  # noqa
from app.models.event_outbox import EventOutbox  # noqa
from app.models.system_setting import SystemSetting  # noqa

# NEW
from app.models.district import District  # noqa
from app.models.area import Area