#!/usr/bin/env python3
import sys
from time import sleep
import asyncio

from web.web import app_task,app_process
from util.db import DBDemo

import sqlite3


if __name__ == '__main__':
        # Load DB to init
        db = DBDemo()
        db.disconnect()

        if False:
                web_thread=app_process()
                web_thread.start()
                while web_thread.is_alive():
                        sleep(1)
        else:

                web_task=app_task()
                asyncio.run(web_task)
