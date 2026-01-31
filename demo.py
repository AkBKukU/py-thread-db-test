#!/usr/bin/env python3

# Python System
import argparse
import sys, os, json
from time import sleep
import asyncio
import sqlite3

# Project
from web.web import app_task,app_process
from util.db import DBDemo



if __name__ == '__main__':

        # Setup CLI arguments
        parser = argparse.ArgumentParser(
                        prog="Async Web Demo",
                        description='async test for interacting between different parts of the python code.',
                        epilog='')
        parser.add_argument('-c', '--config', help="JSON config file", default=None)
        args = parser.parse_args()

        # If file exists, load it
        config_data=None
        if args.config is not None and os.path.exists(args.config):
            print("Reading from config")
            with open(args.config, newline='') as jsonfile:
                config_data=json.load(jsonfile)


        # Load DB to init
        db = DBDemo()
        db.disconnect()

        if False:
                web_thread=app_process(config_data=config_data)
                web_thread.start()
                while web_thread.is_alive():
                        sleep(1)
        else:

                web_task=app_task(config_data=config_data)
                asyncio.run(web_task)
