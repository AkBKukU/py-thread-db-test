#!/usr/bin/env python3
import sys
from time import sleep
import asyncio

from web.web import WebServer
from util.db import DBDemo

import sqlite3


if __name__ == '__main__':
        # Load DB to init
        db = DBDemo()
        db.disconnect()

        web_server = WebServer()

        if False:
                web_thread=web_server.create_process()
                web_thread.start()
                while web_thread.is_alive():
                        sleep(1)
        else:

                web_task=web_server.create_task()
                asyncio.run(web_task)
