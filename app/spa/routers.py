from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import db_session
from .models import Service

services_router = APIRouter(
    prefix="/services",
    tags=["users"],
)


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
