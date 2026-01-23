import json
from pprint import pprint

import asyncio

from quart import Blueprint
from quart import flash
from quart import g
from quart import redirect
from quart import render_template
from quart import request
from quart import websocket
from quart import session
from quart import url_for

from util.db import DBDemo

bp = Blueprint("chat", __name__, url_prefix="/chat")

global connections
connections=[]

@bp.websocket("/ws")
async def ws():
    try:
        connections.append(websocket)
        while True:

            data = json.loads( await websocket.receive() )
            if data is not None:
                    print("Got a data")
            if data["event"] == "open":
                await websocket.send("Hello new connection!")
            elif data["event"] == "update all":
                for connection in connections:
                    await connection.send(json.dumps(data))
            else:
                await db_message(data["data"])
                await websocket.send(json.dumps(data))
    except asyncio.CancelledError:
        # Handle disconnection here
        print("Oh noes!")
        raise

@bp.route("/", methods=("GET", "POST"))
async def page():
        """
        Renders a simple page from a template
        """
        db = DBDemo()
        data = db.execute("SELECT timestamp, sender, message FROM chat",[])

        return await render_template("chat/page.html", data=data)

async def db_message(data):
        db = DBDemo()
        db.execute("INSERT INTO chat(sender,message) VALUES (?,?)",[data["sender"],data["message"]])

@bp.route("/send", methods=("GET", "POST"))
async def db():
        """
        Renders a simple page from a template
        """

        data = await ( request.get_json() )

        db = DBDemo()
        db.execute("INSERT INTO chat(sender,message) VALUES (?,?)",[data["sender"],data["message"]])

        resp = db.execute("SELECT timestamp, sender, message FROM chat",[])

        return await render_template("chat/page.html", data=resp)

