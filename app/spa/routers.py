from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from ..database import db_session
from .models import Appointment, AppointmentCreate, AppointmentStatus, MedSpa, Service

services_router = APIRouter(prefix="/services")
med_spas_router = APIRouter(prefix="/med-spas")
appointments_router = APIRouter(prefix="/appointments")


@services_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    service: Service, session: AsyncSession = Depends(db_session)
) -> Service:
    med_spa = (
        await session.exec(select(MedSpa).where(MedSpa.id == service.med_spa_id))
    ).first()
    if med_spa is None:
        raise HTTPException(
            status_code=404, detail=f"MedSpa with ID {service.med_spa_id} not found"
        )

    session.add(service)
    await session.commit()
    await session.refresh(service)
    return service


@services_router.patch("/{service_id}", response_model=Service)
async def update_service(
    service_id: int, service: Service, session: AsyncSession = Depends(db_session)
):
    db_service: Service | None = await session.get(Service, service_id)
    if db_service is None:
        raise HTTPException(
            status_code=404, detail=f"Service with ID {service_id} not found"
        )
    service_data = service.model_dump(exclude_unset=True)
    db_service.sqlmodel_update(service_data)
    session.add(db_service)
    await session.commit()
    await session.refresh(db_service)
    return db_service


@services_router.get("/{service_id}", response_model=Service)
async def get_service(service_id: int, session: AsyncSession = Depends(db_session)):
    service: Service = await session.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
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
    med_spa = await session.get(MedSpa, appointment_data.med_spa_id)
    if not med_spa:
        raise HTTPException(status_code=404, detail="MedSpa not found")

    # Fetch and validate services
    services = await session.exec(
        select(Service).where(Service.id.in_(appointment_data.service_ids))
    )
    services_list = services.all()
    if len(services_list) != len(appointment_data.service_ids):
        raise HTTPException(status_code=404, detail="One or more services not found")

    # Create the new appointment
    new_appointment = Appointment(
        med_spa_id=appointment_data.med_spa_id,
        start_time=appointment_data.start_time,
        status=AppointmentStatus.SCHEDULED,
        services=services_list,
    )

    session.add(new_appointment)
    await session.commit()
    await session.refresh(new_appointment)
    return new_appointment


@appointments_router.get("/{appointment_id}")
async def get_appointment(
    appointment_id: int, session: AsyncSession = Depends(db_session)
) -> Appointment:
    appointment = await session.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@appointments_router.patch("/{appointment_id}", response_model=Appointment)
async def update_appointment_status(
    appointment_id: int,
    status: AppointmentStatus,
    session: AsyncSession = Depends(db_session),
) -> Appointment:
    appointment = await session.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.status = status
    session.add(appointment)
    await session.commit()
    return appointment


@appointments_router.get("/")
async def list_appointments(
    status: AppointmentStatus| None = None,
    start_date: date | None = None,
    session: AsyncSession = Depends(db_session)
) -> list[Appointment]:
    query = select(Appointment)
    if status:
        query = query.where(Appointment.status == status)
    if start_date:
        query = query.where(func.date(Appointment.start_time) == start_date)

    result = await session.execute(query)
    appointments = result.scalars().all()
    return appointments
