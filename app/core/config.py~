from typing import Optional

from pydantic import BaseSettings, EmailStr
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.constans import ConfigConstants


class Settings(BaseSettings):
    app_title: str = ConfigConstants.APP_TITLE
    app_description: str = ConfigConstants.APP_DESCRIPTION
    app_version: str = ConfigConstants.APP_VERSION
    database_url: str = ConfigConstants.DATABASE_URL
    auth_backend_name: str = ConfigConstants.AUTH_BACKEND_NAME
    secret: str = ConfigConstants.SECRET
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()

engine = create_async_engine(settings.database_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
