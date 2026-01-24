import json
from pprint import pprint

import asyncio
import signal
import uuid

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

# For copying function metadata through decorators
from functools import wraps

bp = Blueprint("chat", __name__, url_prefix="/chat")

#####   ------------- User defnined line --------------

from .websocket_interface import WebSocketClients, WebSocketHandler

wsc = WebSocketClients()

class CustomWebsocket(WebSocketHandler):

    async def receive(self,data):
        if data is not None:
                print("Got a data")
                pprint(data)
        if data["event"] == "open":
            #await self.ws.send("Hello new connection!")
            print("new")
        elif data["event"] == "broadcast":
            await wsc.websocket_broadcast({
            "sender":data["data"]["sender"],
            "message":data["data"]["message"]
        })
        else:
            await db_message(data["data"])
            await self.ws.send(json.dumps(data))

@bp.websocket("/ws")
@wsc.websocket_register(CustomWebsocket)
async def ws(wsh):
    await wsc.websocket_connect(wsh)
    return



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
        await wsc.websocket_broadcast({
            "sender":data["sender"],
            "message":data["message"]
        })

        return await render_template("chat/page.html", data=resp)

