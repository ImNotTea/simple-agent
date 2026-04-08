import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine
from config.settings import DBSettings
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class Database(ABC):
    """Abstract base class for database management to define the interface for database operations"""
    
    @abstractmethod
    async def get_session(self) -> AsyncSession:
        """Return a new async session for database operations"""
        pass
    
    @abstractmethod
    async def shutdown(self) -> None:
        """Dispose the engine and close all connections"""
        pass

class PostgresDatabase(Database):
    """Manages the async PostgreSQL engine lifecycle and provides session factories.

    Use as an async context manager at application startup/shutdown:

        async with PostgresDatabase(settings) as db:
            ...

    Use ``get_session()`` to obtain a new ``AsyncSession`` for each unit of work.
    """

    def __init__(self, settings: DBSettings) -> None:
        self.settings = settings

        self._engine: AsyncEngine = create_async_engine(
            url=(
                f"postgresql+asyncpg://{settings.user}:{settings.password.get_secret_value()}"
                f"@{settings.host}:{settings.port}/{settings.database}"
            ),
            pool_size=settings.pool_size,
            max_overflow=settings.max_overflow,
            pool_recycle=settings.pool_recycle,
            connect_args={"server_settings": {"search_path": settings.db_schema}},
            echo=False,
        )

        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

        logger.info("Async PostgreSQL engine created with connection pooling")

    async def warmup(self) -> None:
        """Verify the database connection is reachable."""
        try:
            async with self._engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info("Successfully connected to PostgreSQL database")
        except Exception as exc:
            logger.error("Error connecting to PostgreSQL database: %s", exc)
            raise


    async def get_session(self) -> AsyncSession:
        """Return a new async session. The caller is responsible for lifecycle management."""
        return self._session_factory()

    async def shutdown(self) -> None:
        """Dispose the engine and close all connections."""
        logger.info("Shutting down PostgreSQL database and disposing engine")
        try:
            await self._engine.dispose()
            logger.info("PostgreSQL engine disposed and all connections closed")
        except Exception as exc:
            logger.error("Error disposing PostgreSQL engine: %s", exc)
            raise
