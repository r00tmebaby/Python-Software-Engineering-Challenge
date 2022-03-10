import asyncio
import os.path
import sys
from typing import Any, Optional
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


async def csv2sql(model: Any, filepath: str, add_always: Optional[bool] = False) -> None:
    if len(session.query(model).all()) == 0:
        if os.path.isfile(filepath):
            pandas.read_csv(filepath).to_sql(
                con=connect,
                name=model.__tablename__,
                if_exists="append",
                index=False
            )
        else:
            raise FileNotFoundError(f"File {filepath} can not be found")


async def add_records():
    # Assuming that we may have a JSON config file in future
    models = {
        "Campaigns": "csv/campaigns.csv",
        "SearchItems": "csv/search_terms.csv",
        "AddGroups": "csv/adgroups.csv"
    }

    for model in models:
        await csv2sql(eval(model), models[model])
        sys.stdout.write('\r' + f"Processing {models[model]}\n")
