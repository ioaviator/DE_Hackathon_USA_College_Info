from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists


def get_db():
    url = f"postgresql://{'adminadmin'}:{'12345678He'}@{'postgres-schools.postgres.database.azure.com'}/{'top_1000_schools'}?sslmode=require"
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, echo=False)
    return engine


db_engine = get_db()

Session = sessionmaker(bind=db_engine)
session = Session()
