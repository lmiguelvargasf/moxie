from datetime import datetime
from decimal import Decimal
from enum import StrEnum, auto

from pydantic import BaseModel as PydanticBaseModel
from pydantic import EmailStr
from sqlmodel import DECIMAL, AutoString, Column, Field, Relationship, SQLModel

from ..core.models import BaseModel


class AppointmentStatus(StrEnum):
    SCHEDULED = auto()
    COMPLETED = auto()
    CANCELED = auto()


class MedSpa(BaseModel, table=True):
    """Model representing a medical spa center."""

    name: str
    address: str
    phone_number: str
    email: EmailStr = Field(sa_type=AutoString, unique=True, nullable=False)

    services: list["Service"] = Relationship(back_populates="med_spa")

    appointments: list["Appointment"] = Relationship(back_populates="med_spa")


class AppointmentServiceLink(SQLModel, table=True):
    """Join table for many-to-many relationship between Appointments and Services."""

    appointment_id: int = Field(foreign_key="appointment.id", primary_key=True)
    service_id: int = Field(foreign_key="service.id", primary_key=True)


class Service(BaseModel, table=True):
    """Model representing a service offered by a MedSpa."""

    name: str
    description: str
    price: Decimal = Field(
        default=None, sa_column=Column(DECIMAL(precision=10, scale=2), nullable=False)
    )
    duration: int  # Duration in minutes

    med_spa_id: int = Field(foreign_key="med_spa.id")
    med_spa: MedSpa = Relationship(back_populates="services")

    appointments: list["Appointment"] = Relationship(
        back_populates="services", link_model=AppointmentServiceLink
    )

class ServiceUpdate(PydanticBaseModel):

    name: str | None = None
    description: str | None = None
    price: Decimal | None = Field(
        default=None, sa_column=Column(DECIMAL(precision=10, scale=2), nullable=False)
    )
    duration: int | None = None


class Appointment(BaseModel, table=True):
    """Model representing an appointment at a MedSpa."""

    start_time: datetime
    status: AppointmentStatus
    total_duration: int
    total_price: Decimal = Field(
        default=None, sa_column=Column(DECIMAL(precision=10, scale=2), nullable=False)
    )

    med_spa_id: int = Field(foreign_key="med_spa.id")
    med_spa: MedSpa = Relationship(back_populates="appointments")

    # Relationship with services
    services: list[Service] = Relationship(
        back_populates="appointments", link_model=AppointmentServiceLink
    )


class AppointmentCreate(PydanticBaseModel):
    med_spa_id: int
    start_time: datetime
    service_ids: list[int]
