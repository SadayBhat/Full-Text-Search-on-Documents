from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.dialects.postgresql import TSVECTOR
from app.database.rds import Base
from app.core.constants.app_constant import AppConstants

class SearchIndex(Base):
    __tablename__ = AppConstants.TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, nullable=False)
    file_hash = Column(String, nullable=False)
    file_path = Column(String, nullable=True)
    search_vector = Column(TSVECTOR, nullable=False)

# GIN index for fast full-text search
Index(AppConstants.INDEX_COLUMN_NAME, SearchIndex.search_vector, postgresql_using=AppConstants.INDEX)
