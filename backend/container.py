# Define dependecie injection container for managing application components and dependencies
from dependency_injector import containers, providers
from application.use_case.chat_use_case import ChatUseCase
from application.interface.llm_client import LLMClient
from application.interface.unit_of_work import UnitOfWork
from infrastructure.persistence.uow import UOW
from infrastructure.persistence.database.db import PostgresDatabase
from config.settings import Settings, get_settings
from infrastructure.llm.groq_llm_client import GroqLLMClient
from config.settings import LLMSettings, DBSettings

class Container(containers.DeclarativeContainer):
    """Dependency Injection Container for managing application components and dependencies"""
    
    # Provide settings as a singleton to ensure consistent configuration across the application
    settings: providers.Singleton[Settings] = providers.Singleton(get_settings)
    
    # Provide db setting
    db_settings: providers.Singleton[DBSettings] = providers.Singleton(settings.provided.get_db_settings.call())
    
    # Provide llm settings as a factory to create new instances when needed, using settings for configuration
    llm_settings: providers.Singleton[LLMSettings] = providers.Singleton(settings.provided.get_llm_settings.call())
    
    # Provide llm_client as a factory to create new instances when needed, using settings for configuration
    llm_client: providers.Factory[LLMClient] = providers.Factory(GroqLLMClient, llm_settings=llm_settings)
    
    # Provide database as a factory to create new instances when needed, using settings for configuration
    database_client: providers.Factory[PostgresDatabase] = providers.Factory(PostgresDatabase, settings=db_settings)
    
    # Provide unit of work for all repositories, using the database client to manage sessions
    unit_of_work: providers.Factory[UnitOfWork] = providers.Factory(UOW, db=database_client)
    
    # Provide chat use case as a factory to create new instances when needed, injecting the llm_client dependency
    chat_use_case: providers.Factory[ChatUseCase] = providers.Factory(ChatUseCase, llm_client=llm_client, unit_of_work=unit_of_work)