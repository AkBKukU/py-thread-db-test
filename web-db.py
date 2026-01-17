#!/usr/bin/env python3

from web import web

import sqlite3

def start_web(self):
        app = web.create_app
        """ Run Flask in a process thread that is non-blocking """
        print("Starting Flask")
        web_thread = Process(target=app.run,
                kwargs={
                "host":self.host,
                "port":self.port,
                "debug":False,
                "use_reloader":False
                }
                )
        web_thread.start()


def db_check():

        db = sqlite3.connect("db.db")
        cur = db.cursor()

        # Initialize DB if empty
        res = cur.execute("SELECT name FROM sqlite_master")
        if res.fetchone() is None:
            # Build DB
            cur.execute("CREATE TABLE timestamps(key INTEGER PRIMARY KEY ASC, text TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)") #TODO - Add timestamp

            with db:
                # Create no-owner player
                cur.execute(f'INSERT INTO timestamps(text) VALUES(?)',("look ma, imma string"))


if __name__ == '__main__':
    db_check()
