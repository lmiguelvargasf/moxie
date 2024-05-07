from starlette_admin.contrib.sqla import Admin, ModelView

from .database import async_engine
from .spa.models import Appointment, MedSpa, Service


class BaseModelView(ModelView):
    exclude_fields_from_create = ["created_at", "updated_at"]


admin = Admin(async_engine, title="Admin")
admin.add_view(BaseModelView(MedSpa))
admin.add_view(BaseModelView(Service))
admin.add_view(BaseModelView(Appointment))
