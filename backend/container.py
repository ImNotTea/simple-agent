# Define dependecie injection container for managing application components and dependencies
from dependency_injector import containers, providers
from backend.application.use_cases.chat_use_case import ChatUseCase
from application.interfaces.llm_client import LLMClient
from config.settings import Settings, get_settings
from infrastructure.llms.groq_llm_client import GroqLLMClient
from config.settings import LLMSettings

class Container(containers.DeclarativeContainer):
    """Dependency Injection Container for managing application components and dependencies"""
    
    # Provide settings as a singleton to ensure consistent configuration across the application
    settings: providers.Singleton[Settings] = providers.Singleton(get_settings)
    
    # Provide llm settings as a factory to create new instances when needed, using settings for configuration
    llm_settings: providers.Singleton[LLMSettings] = providers.Singleton(settings.provided().get_llm_settings)
    
    # Provide llm_client as a factory to create new instances when needed, using settings for configuration
    llm_client: providers.Factory[LLMClient] = providers.Factory(GroqLLMClient, llm_settings=llm_settings)
    
    # Provide chat use case as a factory to create new instances when needed, injecting the llm_client dependency
    chat_use_case: providers.Factory[ChatUseCase] = providers.Factory(ChatUseCase, llm_client=llm_client)