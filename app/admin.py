from starlette_admin.contrib.sqla import Admin, ModelView

from .database import async_engine
from .models import Appointment, MedSpa, Service


class BaseAdmin(ModelView):
    exclude_fields_from_create = ["created_at", "updated_at"]


admin = Admin(async_engine, title="Admin")
admin.add_view(BaseAdmin(MedSpa))
admin.add_view(BaseAdmin(Service))
admin.add_view(BaseAdmin(Appointment))
