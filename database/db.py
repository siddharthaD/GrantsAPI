from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import app_settings
from .models import Base

# Using In-memory engine
engine = create_engine(app_settings.PGSQL_URL, echo=True, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
def get_session():
    with SessionLocal() as session:
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
