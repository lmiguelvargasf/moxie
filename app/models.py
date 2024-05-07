# Enum for Appointment status
from datetime import datetime
from decimal import Decimal
from enum import StrEnum, auto

from pydantic import EmailStr
from sqlmodel import DECIMAL, AutoString, Column, Field, Relationship, SQLModel

from .core.models import BaseModel


class AppointmentStatus(StrEnum):
    SCHEDULE = auto()
    completed = auto()
    canceled = auto()


class MedSpa(BaseModel, table=True):
    """Model representing a medical spa center."""

    name: str
    address: str
    phone_number: str
    email: EmailStr = Field(sa_type=AutoString, unique=True, nullable=False)

    #     # Relationship with services and appointments
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

    # Relationship to appointments through a secondary table
    appointments: list["Appointment"] = Relationship(
        back_populates="services", link_model=AppointmentServiceLink
    )


class Appointment(BaseModel, table=True):
    """Model representing an appointment at a MedSpa."""

    start_time: datetime
    # total_duration: int | None # Auto-calculated
    # total_price: float | None # Auto-calculated
    status: AppointmentStatus

    med_spa_id: int = Field(foreign_key="med_spa.id")
    med_spa: MedSpa = Relationship(back_populates="appointments")

    # Relationship with services
    services: list[Service] = Relationship(
        back_populates="appointments", link_model=AppointmentServiceLink
    )
