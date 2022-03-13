import asyncio
import os
import unittest
from http.client import HTTPException
from multiprocessing import Process

import pytest
import requests
import uvicorn

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


def webserver():
    uvicorn.run(app, host=_HOST, port=_PORT)


@pytest.fixture
def server():
    proc = Process(target=webserver, daemon=True)
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
    # Running the webserver and confirm
    assert __IS_ONLINE


if __name__ == '__main__':
    unittest.main()
