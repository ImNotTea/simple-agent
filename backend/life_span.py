from container import Container
from fastapi import FastAPI
from contextlib import asynccontextmanager
from logging import getLogger

logger = getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        """Manage application lifespan events for dependency injection"""
        logger.info("Starting application lifespan")
        # Initialize dependency injection container
        container: Container = app.state.container
        
        # Startup: Wire container to modules that use @inject decorator
        container.wire(modules=["presentation.apis.chat_api"])
        
        # Warmup database connection
        db = container.database_client()
        await db.warmup()
        
        logger.info("Application lifespan started successfully")
        yield # Application runs here
        
    except Exception as e:
        logger.error(f"Error during application lifespan: {e}")
        raise e
    finally:
        logger.info("Shutting down application and unwiring container")
        # Shutdown: Unwire container
        container.unwire()
        # Shutdown resources
        container.shutdown_resources()