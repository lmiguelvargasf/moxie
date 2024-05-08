from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..database import db_session
from .models import Service

services_router = APIRouter(prefix="/services")
med_spas_router = APIRouter(prefix="/med-spas")


@services_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    service: Service, session: AsyncSession = Depends(db_session)
) -> Service:
    session.add(service)
    await session.commit()
    await session.refresh(service)
    return service


@services_router.patch("/{service_id}", response_model=Service)
async def update_service(
    service_id: int, service: Service, session: AsyncSession = Depends(db_session)
):
    db_service: Service = await session.get(Service, service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
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
        await session.exec(
            select(Service).where(Service.med_spa_id == med_spa_id)
        )
    ).all()
    return services
