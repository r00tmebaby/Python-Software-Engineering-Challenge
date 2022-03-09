import os.path
from typing import Any

from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from models.database import *
from settings.config import DATABASE_URL
from sqlalchemy_utils import database_exists, create_database
import pandas

connect = create_engine(DATABASE_URL)

if not database_exists(DATABASE_URL):
    print("Database does not exist and will be created..")
    create_database(DATABASE_URL)

Base.metadata.create_all(connect, checkfirst=True)
Session = sessionmaker(connect)
session = Session()


def create_data(model: Any, filepath: str) -> None:
    if os.path.isfile(filepath):
        pandas.read_csv(filepath).to_sql(
            con=connect,
            name=model.__tablename__,
            if_exists="append",
            index=False
        )
    else:
        raise FileNotFoundError(f"File {filepath} can not be found")


create_data(Campaigns, "csv/campaigns.csv")
create_data(AddGroups, "csv/adgroups.csv")
create_data(SearchItems, "csv/search_terms.csv")
