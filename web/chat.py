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

bp = Blueprint("chat", __name__, url_prefix="/chat", static_folder='static', static_url_path='/static')

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
        elif data["event"] == "sub":
            print(f"Sub [{data["data"]["channel"]}] connected to [{self.uuid}]")
            await wsc.websocket_unsubscribe_all(self.uuid)
            await wsc.websocket_subscribe(data["data"]["channel"],self.uuid)

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
        data = db.read("SELECT timestamp, sender, message, channel FROM chat",[])

        db.disconnect()
        return await render_template("chat/page.html", data=data)

async def db_message(data):
        db = DBDemo()
        db.modify("INSERT INTO chat(sender,message) VALUES (?,?)",[data["sender"],data["message"]])

@bp.route("/api.json", methods=("GET", "POST"))
async def api_json():

    channel=request.args.get('channel').strip()
    if channel is None:
        channel = ""

    db = DBDemo()
    #pprint(channel)
    if channel == "" or channel is None:

        return db.to_dict(db.read("SELECT timestamp, sender, message, channel FROM chat",[]))
    else:
        return db.to_dict(db.read("SELECT timestamp, sender, message, channel FROM chat WHERE channel = ?",[channel]))


@bp.route("/send", methods=("GET", "POST"))
async def db():
    """
    Renders a simple page from a template
    """

    data = await ( request.get_json() )
    data["channel"] = data["channel"].strip()

    db = DBDemo()
    pprint(data["channel"])
    if data["channel"] == "" or data["channel"] is None:
        db.modify("INSERT INTO chat(sender,message) VALUES (?,?)",[data["sender"],data["message"]])

        resp = db.read("SELECT timestamp, sender, message FROM chat",[])
        await wsc.websocket_broadcast({
            "sender":data["sender"],
            "message":data["message"]
        })
    else:
        db.modify("INSERT INTO chat(sender,message,channel) VALUES (?,?,?)",[data["sender"],data["message"],data["channel"]])

        resp = db.read("SELECT timestamp, sender, message, channel FROM chat WHERE channel = ?",[data["channel"]])
        await wsc.call_sub(data["channel"],{
            "sender":data["sender"],
            "message":data["message"],
            "channel":data["channel"]
        })

    db.disconnect()

    return await render_template("chat/page.html", data=resp)

