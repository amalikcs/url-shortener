from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.database_url,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


### SessionLocal is a SQLAlchemy session factory that is configured to connect to the database specified 
# in the settings. It is used to create new database sessions for each request, 
# ensuring that each request has its own isolated session for database operations.

### get_db() is a dependency function that provides a database session to the route handlers. 
# It creates a new session using SessionLocal, yields it for use in the route, 
# and ensures that the session is closed after the request is completed, preventing any potential resource leaks.