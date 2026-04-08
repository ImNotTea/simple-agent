from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from config.settings import get_settings

Base = declarative_base(metadata=MetaData(schema=get_settings().DB_SCHEMA))
