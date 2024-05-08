from datetime import datetime
from decimal import Decimal
from enum import StrEnum, auto
from typing import Self

from pydantic import BaseModel as PydanticBaseModel
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
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

    # Relationship with services and appointments
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

    # async def total_duration(self, session: AsyncSession) -> int:
    #     """Calculate total duration from all associated services."""
    #     await session.refresh(self)
    #     services = await self.services
    #     return sum(service.duration for service in services if service.duration)

    # async def total_price(self, session: AsyncSession) -> Decimal:
    #     """Calculate total price from all associated services."""
    #     await session.refresh(self)
    #     services = await self.services
    #     return sum(service.price for service in services if service.price)


class AppointmentCreate(PydanticBaseModel):
    med_spa_id: int
    start_time: datetime
    service_ids: list[int]


# class AppointmentResponse(PydanticBaseModel):
#     start_time: datetime
#     status: AppointmentStatus
#     med_spa_id: int
#     total_duration: int
#     total_price: Decimal

#     @staticmethod
#     async def from_orm(model: Appointment, session: AsyncSession) -> Self:
#         """Convert SQLModel instance to Pydantic model including computed properties."""
#         total_duration = await model.total_duration(session)
#         total_price = await model.total_price(session)
#         return AppointmentResponse(
#             start_time=model.start_time,
#             status=model.status,
#             med_spa_id=model.med_spa_id,
#             total_duration=total_duration,
#             total_price=total_price
#         )
