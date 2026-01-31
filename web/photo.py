

# Template creates one button for each configured camera, and created web endpoint to activate it
# User connects websocket
# User clicks photo button [GET]
# All clients recieve updated photo list over websocket
# client renders photos



import json, os, sys
from pprint import pprint

from datetime import datetime
import asyncio
import signal
import uuid
import glob
import shutil

from quart import Blueprint
from quart import flash
from quart import g
from quart import redirect
from quart import render_template
from quart import request
from quart import websocket
from quart import session
from quart import url_for
from quart import current_app

from util.db import DBDemo
from util.uvc_photo import get_photo

# For copying function metadata through decorators
from functools import wraps

bp = Blueprint("photo", __name__, url_prefix="/photo", static_folder='static', static_url_path='/static')

#####   ------------- User defnined line --------------

def take_photo():
    out_path = "web/static/photos"
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    uvc_id = int(os.path.basename(request.base_url).replace("camera",""))
    # check if id valid
    if "cameras" in current_app.config['config']:
        for camera in current_app.config['config']["cameras"]:
            if uvc_id == camera["uvc_id"]:
                get_photo(
                    output=f"{out_path}/{str(datetime.now().isoformat()).replace(":","-")}.jpg",
                    uvc_id=camera["uvc_id"],
                    options=camera["options"],
                    uvc_options=camera["uvc_options"]
                    )
                return "cheese"

    return "404 camera not found"



# cameras: [
#   {
#     "uvc_id": 0,
#     "photo":[5104, 3828],
#     "crop":[1500,1500],
#     "options":{"sharpness":0}
#   }
# ]



class DBPhoto(DBDemo):

    # Table: ActionQueue
    # timestamp | action | name | controller_id
    #-----------------------------------------
    # now       | move   | mypix| cd robot

    def actionAdd(self, action, name, controller_id):
        db = DBPhoto(schema = "web/photo.sql")
        db.modify("INSERT INTO action_queue(action,name,controller_id) VALUES (?,?,?)",[action, name, controller_id])

    def actionCheck(self,controller_id):
        db = DBPhoto(schema = "web/photo.sql")
        return db.to_dict(db.read("SELECT key, action, name FROM action_queue WHERE controller_id = ?",[controller_id]))

    def actionDelete(self,key):
        db = DBPhoto(schema = "web/photo.sql")
        return db.modify("DELETE FROM action_queue WHERE key = ?",[key])




def dynamicRoutes(app,dbp):
    if "cameras" in app.config['config']:
        for camera in app.config['config']["cameras"]:
            dbp.add_url_rule(f'/camera{camera["uvc_id"]}',f'/camera{camera["uvc_id"]}', take_photo)
    return dbp


@bp.route("/", methods=("GET", "POST"))
async def page():
        """
        Renders a simple page from a template
        """

        out_path = "web/static/photos"
        db = DBPhoto(schema = "web/photo.sql")
        for action in db.actionCheck(0):
            match action["action"]:
                case "move":
                    folder = f'{out_path}/{str(datetime.now().isoformat()).replace(":","-")}_{action["name"]}'
                    if not os.path.exists(folder):
                        os.makedirs(folder)
                    photos = glob.glob(f"{out_path}/*.jpg")
                    for photo in photos:
                        shutil.move(photo, folder)
                    # Something that moves photos
                    print("I totally moved the photos, yep")
                    db.actionDelete(action["key"])


        if not os.path.exists(out_path):
            os.makedirs(out_path)
        photos = glob.glob(f"{out_path}/*.jpg")
        photos = [p.replace("web/","") for p in photos]

        data = { "photos":photos, "cameras":current_app.config['config']["cameras"]}

        return await render_template("photo/page.html", data=data)


@bp.route("/move", methods=["POST"])
async def moveAction():
    """
    Renders a simple page from a template
    """

    data =( await  request.form )

    pprint(data["words-go-here"])

    db = DBPhoto(schema = "web/photo.sql")
    db.actionAdd("move", data["words-go-here"], 0)
    return "yep"

