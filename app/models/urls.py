from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class URLMapping(Base):
    """
    Stores mapping between original URL
    and generated short code.
    """
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    original_url = Column(String(2048), nullable=False)
    short_code = Column(String(10), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        nullable=False)