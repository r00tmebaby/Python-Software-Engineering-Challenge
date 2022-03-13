import asyncio
import os
import subprocess
import threading
import unittest

from cffi.setuptools_ext import execfile

from core.connect import session, add_records
from models.database import *
from core import connect
import requests
from subprocess import call

from settings import config


class TestDB(unittest.TestCase):
    __TABLES = ["Campaigns", "SearchItems", "AddGroups"]

    def test_delete(self):
        with session as ses:
            for each_table in self.__TABLES:
                ses.query(eval(each_table)).delete()
                ses.commit()
                camp = ses.query(eval(each_table)).all()
        self.assertEqual(len(camp), 0, f"{each_table} table must have 0 records")

    # def test_create(self):
    #    asyncio.run(add_records())
    #    with session as ses:
    #        for each_table in self.__TABLES:
    #            camp = ses.query(eval(each_table)).all()
    #    self.assertGreater(len(camp), 0x186A0, f"{each_table} table must have at least 100k records")


class TestWebServer(unittest.TestCase):
    __IS_ONLINE: bool = False

    def test_web_server(self):
        self.is_online = os.system(f"ping -c 1 {config.HOST}:{config.PORT}") == 0  # is the server currently online
        self.assertFalse(self.is_online)


if __name__ == '__main__':
    thread = threading.Thread(target=unittest.main, daemon=True)
    thread.start()
    thread.join()
