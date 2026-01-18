#!/usr/bin/env python3
import sys
from time import sleep
from multiprocessing import Process

from web import web
from util.db import DBDemo

import sqlite3

def process_web():
        app = web.create_app()
        """ Run Flask in a process thread that is non-blocking """
        print("Starting Flask")
        return Process(
                target=app.run,
                kwargs={
                "host":"0.0.0.0",
                "port":"5000",
                "debug":False,
                "use_reloader":False
                }
        )




if __name__ == '__main__':
        # Load DB to init
        db = DBDemo()
        db.disconnect()

        web_thread = process_web()
        web_thread.start()
        while web_thread.is_alive():
                sleep(1)
