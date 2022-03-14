import asyncio
import json
import os
import unittest
from http.client import HTTPException
from multiprocessing import Process

import pytest
import requests
import uvicorn
from fastapi.encoders import jsonable_encoder
from core.connect import session, add_records
from core.exception_handler import http_exception_handler
from endpoints import users, search, auth, default
from main import custom_openapi
from models.database import *
from settings import config
from fastapi import FastAPI

app = FastAPI()

app.openapi = custom_openapi
# Exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)

# Add the routers (endpoints)
app.include_router(default.router)  # Not visible -> Redirects to the API documentation

app.include_router(auth.router)
app.include_router(search.router)
app.include_router(users.router)

# Config
_HOST = "127.0.0.1"
_PORT = 8090
__IS_ONLINE: bool = os.system(f"ping -c 1 {config.HOST}:{config.PORT}") == 0

_URL = f"http://{_HOST}:{_PORT}/"


def run_server():
    uvicorn.run(app, host=_HOST, port=_PORT)


@pytest.fixture
def server():
    proc = Process(target=run_server, daemon=True)
    proc.start()
    yield
    proc.kill()  # Cleanup after test


class TestDB(unittest.TestCase):
   __TABLES = ["Campaigns", "SearchItems", "AddGroups"]

   def test_delete(self):
       # Delete all tables and check if deleted
       with session as ses:
           for each_table in self.__TABLES:
               ses.query(eval(each_table)).delete()
               ses.commit()
               camp = ses.query(eval(each_table)).all()
       self.assertEqual(len(camp), 0, f"{each_table} table must have 0 records")

   def test_create(self):
       # Create all tables and check if existing
       asyncio.run(add_records())
       with session as ses:
           for each_table in self.__TABLES:
               camp = ses.query(eval(each_table)).all()
       self.assertGreater(len(camp), 0x186A0, f"{each_table} table must have at least 100k records")


def test_offline_server():
    # Confirm the webserver is offline
    assert not __IS_ONLINE


def test_online_server(server):
    # Try the webserver is offline
    assert requests.get(_URL).status_code == 200


def test_session(server):
    # Unauthorized - User is not logged yet
    assert requests.delete(_URL + "session").status_code == 401

    # Bad Request - User does not exist, but we do not specify which field is wrong.
    assert requests.post(_URL + "session", data={
        "username": "asdasdasd",
        "password": "122345"
    }).status_code == 400


def test_register(server):
    header = {
        'content-type': 'application/json', 'Accept-Charset': 'UTF-8'
    }
    dummy_user = json.dumps({
            "name": "r00tme",
            "surname": "r00tme1",
            "summary": "user",
            "email": "r00tme@abv.bg",
            "password": "R00tme123#"
        })

    # Bad Request - Header application/json is not specified
    assert requests.post(_URL + "user", json=dummy_user).status_code == 400

    #TODO
    # Register new user, List users
    # Login, Logout
    # Search items



def test_search(server):
    # Search should not be accessible from unauthorised users
    assert requests.get(_URL + "search").status_code == 401


if __name__ == '__main__':
    unittest.main()
