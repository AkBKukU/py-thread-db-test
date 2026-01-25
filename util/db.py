import sqlite3
import signal

class DBDemo:
        def __init__(self, db_file="db.db", auto_connect=True,schema = "schema.sql"):

                if auto_connect:
                        self.connect(db_file)

                        # Initialize DB if empty
                        res = self.cur.execute("SELECT name FROM sqlite_master")
                        if res.fetchall() == []:
                                print("Initializing database...")
                                self.db_init(schema)
                        else:
                                print(f"Reloading [{db_file}]...")

        def connect(self,db_file="db.db"):

                self.db = sqlite3.connect(db_file)
                self.db.row_factory = sqlite3.Row
                self.cur = self.db.cursor()


        def disconnect(self,db_file="db.db"):

                self.db.commit()
                self.db.close()

        def to_dict(self,rows):
                return [{k: row[k] for k in row.keys()} for row in rows]

        def db_init(self,schema = "schema.sql"):

                with open(schema, "r") as f:
                        print(f"Loading schema [{schema}]...")
                        self.cur.executescript(f.read())

                self.db.commit()

        def read(self, query, parameters):
                print(f"Reading: [{query}]...")
                return self.cur.execute(query,parameters).fetchall()

        def modify(self, query, parameters):
                print(f"Modify: [{query}]...")
                self.cur.execute(query,parameters)
                self.db.commit()

