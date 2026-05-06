from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from presentation.apis.chat_api import router as chat_router
from life_span import lifespan
from container import Container
import uvicorn
from logging import getLogger

logger = getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    # Initialize dependency injection container
    logger.info("Initializing dependency injection container")
    container = Container()
    cfg_settings = container.settings()
    
    # Initialize FastAPI with lifespan management
    app = FastAPI(
        title=cfg_settings.PROJECT_NAME,
        openapi_url=f"{cfg_settings.API_V1_STR}/openapi.json",
        lifespan=lifespan
    )

    # Store container in app state for access throughout the application
    app.state.container = container
    
    # Mount individual API routes (e.g., /api/v1/health)
    logger.info("Mounting API routes")
    app.include_router(chat_router, prefix=cfg_settings.API_V1_STR)

    # Configure CORS (Security Note: In production, specify allowed origins instead of using "*")
    logger.info("Configuring CORS middleware")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # Replace with specific domains in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount individual API routes (e.g., /api/v1/health)
    app.include_router(chat_router, prefix=cfg_settings.API_V1_STR)
    return app

# Create application instance
app = create_app()
logger.info("FastAPI application created successfully")

if __name__ == "__main__":
    # Run the application using Uvicorn ASGI server
    uvicorn.run(app, host="0.0.0.0", port=8000)