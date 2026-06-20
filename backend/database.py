from sqlalchemy  import  create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from config import get_settings

settings = get_settings ()

engine =  create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)

SessionLocal =  sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base =  declarative_base()

def get_deb():
    db =  SessionLocal()
    try:
        yield db
    finally:
        db.close()
