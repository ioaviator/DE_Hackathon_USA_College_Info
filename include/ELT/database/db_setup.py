from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from .utils import db_password, db_username

host='postgress-schools.postgres.database.azure.com'
db_name='top_1000_schools'

def get_db():
    url = f"postgresql://{db_username}:{db_password}@{host}/{db_name}?sslmode=require"
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, echo=False)
    return engine


db_engine = get_db()