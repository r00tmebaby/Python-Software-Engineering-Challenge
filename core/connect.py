from sqlalchemy.orm import sessionmaker
from models.database import *
from settings.config import DATABASE_URL
from sqlalchemy_utils import database_exists, create_database

connect = create_engine(DATABASE_URL)
if not database_exists(DATABASE_URL):
    print("Database does not exist and will be created..")
    create_database(DATABASE_URL)
Base.metadata.create_all(connect, checkfirst=True)
Session = sessionmaker(connect)
session = Session()
