from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from ..database import db_session
from .models import (
    Appointment,
    AppointmentCreate,
    AppointmentStatus,
    MedSpa,
    Service,
    ServiceCreate,
    ServiceUpdate,
)

services_router = APIRouter(prefix="/services")
med_spas_router = APIRouter(prefix="/med-spas")
appointments_router = APIRouter(prefix="/appointments")


@services_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_service(
    service_create: ServiceCreate, session: AsyncSession = Depends(db_session)
) -> Service:
    med_spa: MedSpa | None = await session.get(MedSpa, service_create.med_spa_id)
    if med_spa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MedSpa with ID {service_create.med_spa_id} not found.",
        )

    service = Service.model_validate(service_create)
    session.add(service)
    await session.commit()
    await session.refresh(service)
    return service


@services_router.patch("/{service_id}")
async def update_service(
    service_id: int, service_update: ServiceUpdate, session: AsyncSession = Depends(db_session)
) -> Service:
    service: Service | None = await session.get(Service, service_id)
    if service is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service with ID {service_id} not found.",
        )
    service_update_data = service_update.model_dump(exclude_unset=True)
    service.sqlmodel_update(service_update_data)
    session.add(service)
    await session.commit()
    await session.refresh(service)
    return service


@services_router.get("/{service_id}")
async def read_service(
    service_id: int, session: AsyncSession = Depends(db_session)
) -> Service:
    service: Service | None = await session.get(Service, service_id)
    if service is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service with ID {service_id} not found.",
        )
    return service


@med_spas_router.get("/{med_spa_id}/services")
async def read_services_for_medspa(
    med_spa_id: int, session: AsyncSession = Depends(db_session)
) -> list[Service]:
    services = (
        await session.exec(select(Service).where(Service.med_spa_id == med_spa_id))
    ).all()
    return services


@appointments_router.post(
    "/", response_model=Appointment, status_code=status.HTTP_201_CREATED
)
async def create_appointment(
    appointment_data: AppointmentCreate, session: AsyncSession = Depends(db_session)
) -> Appointment:
    med_spa_id = appointment_data.med_spa_id
    med_spa: MedSpa | None = await session.get(MedSpa, med_spa_id)
    if med_spa is None:
        raise HTTPException(
            status_code=404, detail=f"MedSpa with ID {med_spa_id} not found."
        )

    service_ids = appointment_data.service_ids
    services: list[Service] = (
        await session.exec(select(Service).where(Service.id.in_(service_ids)))
    ).all()
    if len(services) != len(appointment_data.service_ids):
        raise HTTPException(status_code=404, detail="One or more services not found")

    appointment = Appointment(
        med_spa_id=appointment_data.med_spa_id,
        start_time=appointment_data.start_time,
        status=AppointmentStatus.SCHEDULED,
        total_duration=sum(service.duration for service in services),
        total_price=sum(service.price for service in services),
        services=services,
    )

    session.add(appointment)
    await session.commit()
    await session.refresh(appointment)
    return appointment


@appointments_router.get("/{appointment_id}")
async def read_appointment(
    appointment_id: int, session: AsyncSession = Depends(db_session)
) -> Appointment:
    appointment: Appointment | None = await session.get(Appointment, appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=404, detail=f"Appointment with ID {appointment_id} not found."
        )
    return appointment


@appointments_router.patch("/{appointment_id}")
async def update_appointment_status(
    appointment_id: int,
    status: AppointmentStatus,
    session: AsyncSession = Depends(db_session),
) -> Appointment:
    appointment: Appointment | None = await session.get(Appointment, appointment_id)
    if appointment is None:
        raise HTTPException(
            status_code=404, detail=f"Appointment with ID {appointment_id} not found."
        )

    appointment.status = status
    session.add(appointment)
    await session.commit()
    return appointment


@appointments_router.get("/")
async def list_appointments(
    status: AppointmentStatus | None = None,
    start_date: date | None = None,
    session: AsyncSession = Depends(db_session),
) -> list[Appointment]:
    query = select(Appointment)
    if status:
        query = query.where(Appointment.status == status)
    if start_date:
        query = query.where(func.date(Appointment.start_time) == start_date)

    result = await session.execute(query)
    appointments = result.scalars().all()
    return appointments
